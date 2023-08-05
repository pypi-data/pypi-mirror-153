from __future__ import annotations

from typing import AsyncIterator, Iterator
import asyncio
import logging
import os
import typing

import pandas as pd
import pyarrow as pa

from sarus_data_spec.arrow.array import convert_record_batch
from sarus_data_spec.manager.base import Base
from sarus_data_spec.storage.typing import Storage
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

try:
    import tensorflow as tf

    from sarus_data_spec.manager.ops.tensorflow.features import (
        deserialize,
        flatten,
        nest,
        serialize,
        to_internal_signature,
    )
    from sarus_data_spec.manager.ops.tensorflow.tensorflow_visitor import (
        convert_tensorflow,
    )
except ModuleNotFoundError:
    pass  # error message printed from typing.py

from .utils import iter_over_async

logger = logging.getLogger(__name__)

BATCH_SIZE = 10000


class BaseAsyncManager(Base):
    """Asynchronous Manager Base implementation.

    Make synchronous methods rely on asynchronous ones for consistency.
    """

    def __init__(self, storage: Storage, protobuf: sp.Manager):
        super().__init__(
            storage=storage,
            protobuf=protobuf,
        )

    async def async_value(self, scalar: st.Scalar) -> st.DataSpecValue:
        raise NotImplementedError("async_value")

    def value(self, scalar: st.Scalar) -> st.DataSpecValue:
        return asyncio.run(self.async_value(scalar=scalar))

    async def async_to_arrow(
        self, dataset: st.Dataset, batch_size: int
    ) -> AsyncIterator[pa.RecordBatch]:
        raise NotImplementedError("async_to_arrow")

    def to_arrow(
        self, dataset: st.Dataset, batch_size: int
    ) -> Iterator[pa.RecordBatch]:
        batches_async_iterator = asyncio.run(
            self.async_to_arrow(dataset=dataset, batch_size=batch_size)
        )
        return iter_over_async(batches_async_iterator)

    async def async_to_pandas(self, dataset: st.Dataset) -> pd.DataFrame:
        batches_async_it = await self.async_to_arrow(
            dataset=dataset, batch_size=BATCH_SIZE
        )
        arrow_batches = [batch async for batch in batches_async_it]
        return pa.Table.from_batches(arrow_batches).to_pandas()

    def to_pandas(self, dataset: st.Dataset) -> pd.DataFrame:
        return asyncio.run(self.async_to_pandas(dataset=dataset))

    def to_tensorflow(self, dataset: st.Dataset) -> tf.data.Dataset:
        return asyncio.run(self.async_to_tensorflow(dataset=dataset))

    async def async_to_tensorflow(
        self, dataset: st.Dataset
    ) -> tf.data.Dataset:

        root_dir = os.path.join(self.parquet_dir, "tfrecords", dataset.uuid())
        schema_type = dataset.schema().type()
        signature = to_internal_signature(schema_type)

        if not os.path.exists(root_dir):
            # the dataset is cached first
            os.makedirs(root_dir)

            flattener = flatten(signature)
            serializer = serialize(signature)
            i = 0
            batches_async_it = await self.async_to_arrow(
                dataset=dataset, batch_size=BATCH_SIZE
            )
            async for batch in batches_async_it:
                filename = os.path.join(root_dir, f"batch_{i}.tfrecord")
                i += 1
                await write_tf_batch(
                    filename, batch, schema_type, flattener, serializer
                )

        # reading from cache
        glob = os.path.join(root_dir, "*.tfrecord")
        filenames = tf.data.Dataset.list_files(glob, shuffle=False)
        deserializer = deserialize(signature)
        nester = nest(signature)
        return tf.data.TFRecordDataset(filenames).map(deserializer).map(nester)


#
async def write_tf_batch(
    filename: str,
    batch: pa.RecordBatch,
    schema_type: st.Type,
    flattener: typing.Callable,
    serializer: typing.Callable,
) -> None:
    with tf.io.TFRecordWriter(filename) as writer:
        batch = convert_tensorflow(
            convert_record_batch(record_batch=batch, _type=schema_type),
            schema_type,
        )
        batch = tf.data.Dataset.from_tensor_slices(batch).map(flattener)
        for row in batch:
            as_bytes = serializer(row)
            writer.write(as_bytes)
