import pyarrow as pa

import sarus_data_spec.typing as st


def convert_record_batch(
    record_batch: pa.RecordBatch, _type: st.Type
) -> pa.Array:

    if (
        _type.protobuf().WhichOneof('type')  # type:ignore
        not in ['struct', 'union']
        == 1
    ):
        return record_batch.column(0)
    if _type.protobuf().HasField('struct'):
        names = list(_type.children().keys())
    elif _type.protobuf().HasField('union'):
        names = list(_type.children().keys())
        names.append('field_selected')
    else:
        raise TypeError('got {type} but many columns in the batch array')
    return pa.StructArray.from_arrays(record_batch.columns, names=names)
