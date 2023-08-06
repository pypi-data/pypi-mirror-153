from __future__ import annotations

from datetime import datetime
from typing import Callable, List, Mapping, Optional, Type, cast

from sarus_data_spec.base import Base, Referring
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.typing import Manager
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class Status(Referring[sp.Status]):
    """A python class to describe status"""

    def __init__(self, protobuf: sp.Status) -> None:
        self._referred = {
            protobuf.dataspec,
            protobuf.manager,
        }  # This has to be defined before it is initialized
        super().__init__(protobuf)

    def prototype(self) -> Type[sp.Status]:
        """Return the type of the underlying protobuf."""
        return sp.Status

    def datetime(self) -> datetime:
        return datetime.fromisoformat(self.protobuf().datetime)

    def update(
        self,
        task_stages: Optional[Mapping[str, st.Stage]] = None,
        properties: Optional[Mapping[str, str]] = None,
    ) -> Status:
        # We copy the content of the current status
        proto = self.protobuf()
        # We update its timestamp and properties
        proto.datetime = datetime.now().isoformat()
        if properties is not None:
            proto.properties.update(properties)
            # Protobuf implementation of the merge
            # does not work as expected on maps...
        if task_stages is not None:
            for task in task_stages:
                stage = task_stages[task].protobuf()
                if task in proto.task_stages and proto.task_stages[
                    task
                ].WhichOneof('stage') == task_stages[
                    task
                ].protobuf().WhichOneof(
                    'stage'
                ):
                    proto.task_stages[task].properties.update(stage.properties)
                else:
                    proto.task_stages[task].CopyFrom(stage)
        # And create a new data spec object
        return Status(proto)

    def task(self, task: str) -> Stage:  # tODO: optional ?
        return Stage(self.protobuf().task_stages[task])

    def pending(
        self,
    ) -> bool:
        """this is true if all tasks have status at least pending
        (i.e. pending, processing or ready) and at least one is pending"""
        has_one = False
        all_better = True
        task_stages = self.protobuf().task_stages
        if task_stages is not None:
            for task in task_stages:
                has_one = has_one or task_stages[task].HasField('pending')
                all_better = all_better and not (
                    task_stages[task].HasField('error')
                )
        return has_one and all_better

    def processing(
        self,
    ) -> bool:
        """this is true if all tasks have status at least processing
        (i.e. processing or ready) and at least one is processing"""
        has_one = False
        all_better = True
        task_stages = self.protobuf().task_stages
        if task_stages is not None:
            for task in task_stages:
                has_one = has_one or task_stages[task].HasField('processing')
                all_better = all_better and not (
                    task_stages[task].HasField('error')
                    or task_stages[task].HasField('pending')
                )
        return has_one and all_better

    def ready(
        self,
    ) -> bool:  # TODO this should be true if all tasks have status ready
        """this is true if all tasks have status ready"""
        all_ready = True
        task_stages = self.protobuf().task_stages
        if task_stages is not None:
            for task in task_stages:
                all_ready = all_ready and task_stages[task].HasField('ready')
        return all_ready

    def error(
        self,
    ) -> bool:  # TODO this should be true if any task have status error
        """this is true if any tasks have status error"""
        has_error = False
        task_stages = self.protobuf().task_stages
        if task_stages is not None:
            for task in task_stages:
                has_error = has_error or task_stages[task].HasField('error')
        return has_error

    def dataset(self) -> Dataset:
        dataspec = self.dataspec()
        assert isinstance(dataspec, Dataset)
        return dataspec

    def dataspec(self) -> st.DataSpec:  # TODO check this works
        return cast(
            st.DataSpec, self.storage().referrable(self._protobuf.dataspec)
        )

    def owner(
        self,
    ) -> Manager:
        # TODO: Maybe find a better name, but this was shadowing
        # the actual manager of this object.  # noqa: E501
        return cast(Manager, self.storage().referrable(self._protobuf.manager))


# Builders
def status(
    dataspec: st.DataSpec,
    task_stages: Optional[Mapping[str, st.Stage]] = None,
    properties: Optional[Mapping[str, str]] = None,
    manager: Optional[Manager] = None,
) -> st.Status:
    """A builder to ease the construction of a status
    - dataspec: is the dataspec, the status is added to
    - manager: is which manager, if None,
        the default manager of the dataspec is used
    """
    # Use the right manager
    manager = dataspec.manager() if manager is None else manager
    # If a status already exists for the dataspec
    # and manager simply create an updated verion of it
    last = last_status(dataspec)
    if last is None:
        return Status(
            sp.Status(
                dataspec=dataspec.uuid(),
                manager=manager.uuid(),
                datetime=datetime.now().isoformat(),
                task_stages=None
                if task_stages is None
                else {
                    task: task_stages[task].protobuf() for task in task_stages
                },
                properties=properties,
            )
        )
    else:
        return last.update(task_stages=task_stages, properties=properties)


def last_status(
    dataspec: st.DataSpec,
    manager: Optional[Manager] = None,
) -> Optional[st.Status]:
    """Return a DataSpec's last status by sorted datetime."""
    manager = dataspec.manager() if manager is None else manager
    return cast(
        Optional[st.Status],
        manager.storage().last_referring(
            (dataspec, manager), sp.type_name(sp.Status)
        ),
    )


def last_statuses(
    dataspec: st.DataSpec,
) -> List[st.Status]:
    """Return a list composed by the last status of every
    DataSpec's manager."""
    managers = dataspec.storage().type_name(sp.type_name(sp.Manager))
    statuses = []
    for manager in managers:
        stt = last_status(
            dataspec,
            cast(
                Optional[Manager],
                manager,
            ),
        )
        if stt is not None:
            statuses.append(stt)
    return statuses


class Stage(Base[sp.Status.Stage]):
    """A simple wrapper type to simplify protobuf usage"""

    def accept(self, visitor: st.StageVisitor) -> None:
        dispatch: Callable[[], None] = {
            'pending': visitor.pending,
            'processing': visitor.processing,
            'ready': visitor.ready,
            'error': visitor.error,
        }[cast(str, self.protobuf().WhichOneof('stage'))]
        dispatch()

    def stage(self) -> str:
        print(self.protobuf())
        return cast(str, self.protobuf().WhichOneof('stage'))


# Builders for stages
def pending_stage(properties: Optional[Mapping[str, str]] = None) -> Stage:
    return Stage(
        sp.Status.Stage(
            pending=sp.Status.Stage.Pending(), properties=properties
        )
    )


def processing_stage(properties: Optional[Mapping[str, str]] = None) -> Stage:
    return Stage(
        sp.Status.Stage(
            processing=sp.Status.Stage.Processing(), properties=properties
        )
    )


def ready_stage(properties: Optional[Mapping[str, str]] = None) -> Stage:
    return Stage(
        sp.Status.Stage(ready=sp.Status.Stage.Ready(), properties=properties)
    )


def error_stage(properties: Optional[Mapping[str, str]] = None) -> Stage:
    return Stage(
        sp.Status.Stage(error=sp.Status.Stage.Error(), properties=properties)
    )


# Builders for statuses


def properties(
    dataspec: st.DataSpec,
    properties: Optional[Mapping[str, str]],
    manager: Optional[Manager] = None,
) -> st.Status:
    return status(
        dataspec,
        task_stages=None,
        properties=properties,
        manager=manager,
    )


def pending(
    dataspec: st.DataSpec,
    task: str,
    properties: Optional[Mapping[str, str]] = None,
    manager: Optional[Manager] = None,
) -> st.Status:
    return status(
        dataspec,
        task_stages={task: pending_stage(properties=properties)},
        properties=None,
        manager=manager,
    )


def processing(
    dataspec: st.DataSpec,
    task: str,
    properties: Optional[Mapping[str, str]] = None,
    manager: Optional[Manager] = None,
) -> st.Status:
    return status(
        dataspec,
        task_stages={task: processing_stage(properties=properties)},
        properties=None,
        manager=manager,
    )


def ready(
    dataspec: st.DataSpec,
    task: str,
    properties: Optional[Mapping[str, str]] = None,
    manager: Optional[Manager] = None,
) -> st.Status:
    return status(
        dataspec,
        task_stages={task: ready_stage(properties=properties)},
        properties=None,
        manager=manager,
    )


def error(
    dataspec: st.DataSpec,
    task: str,
    properties: Optional[Mapping[str, str]] = None,
    manager: Optional[Manager] = None,
) -> st.Status:
    return status(
        dataspec,
        task_stages={task: error_stage(properties=properties)},
        properties=None,
        manager=manager,
    )
