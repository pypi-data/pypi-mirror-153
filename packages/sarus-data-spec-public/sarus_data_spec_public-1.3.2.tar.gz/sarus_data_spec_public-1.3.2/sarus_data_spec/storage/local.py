from collections import defaultdict
from itertools import chain, combinations
from typing import (
    Collection,
    DefaultDict,
    Final,
    FrozenSet,
    List,
    MutableMapping,
    Optional,
    Set,
    Union,
    cast,
)

from sarus_data_spec.protobuf.typing import (
    ProtobufWithUUID,
    ProtobufWithUUIDAndDatetime,
)
from sarus_data_spec.typing import Referrable, Referring

SEP: Final[str] = ','


def referrable_collection_string(
    values: Collection[Referrable[ProtobufWithUUID]],
) -> str:
    return SEP.join(sorted(value.uuid() for value in values))


def referrable_collection_set(
    values: Collection[Referrable[ProtobufWithUUID]],
) -> FrozenSet[str]:
    return frozenset(value.uuid() for value in values)


class Storage:
    """Simple local Storage."""

    def __init__(self) -> None:
        # A Store to save (timestamp, type_name, data, relating data)
        self._referrables: MutableMapping[
            str, Referrable[ProtobufWithUUID]
        ] = dict()
        self._referring: DefaultDict[str, Set[str]] = defaultdict(set)

    def store(self, value: Referrable[ProtobufWithUUID]) -> None:
        # Checks the value for consistency
        assert value._frozen()
        self._referrables[value.uuid()] = value

        if isinstance(value, Referring):
            value = cast(Referring[ProtobufWithUUID], value)
            referred_combinations = chain.from_iterable(
                combinations(value.referred(), r) for r in range(1, 3)
            )
            for combination in referred_combinations:
                self._referring[referrable_collection_string(combination)].add(
                    value.uuid()
                )

    def referrable(self, uuid: str) -> Optional[Referrable[ProtobufWithUUID]]:
        return self._referrables.get(uuid, None)

    def referring(
        self,
        referred: Union[
            Referrable[ProtobufWithUUID],
            Collection[Referrable[ProtobufWithUUID]],
        ],
        type_name: Optional[str] = None,
    ) -> Collection[Referring[ProtobufWithUUID]]:
        if isinstance(referred, Referrable):
            referring_uuids = self._referring[referred.uuid()]
        else:
            referring_uuids = self._referring[
                referrable_collection_string(referred)
            ]
        referrings = [self.referrable(uuid) for uuid in referring_uuids]
        if type_name is not None:
            referrings = [
                item
                for item in referrings
                if (item is not None) and (item.type_name() == type_name)
            ]
        return referrings  # type:ignore

    def last_referring(
        self,
        referred: Union[
            Referrable[ProtobufWithUUID],
            Collection[Referrable[ProtobufWithUUID]],
        ],
        type_name: str,
    ) -> Optional[Referring[ProtobufWithUUIDAndDatetime]]:
        """Last value referring to one referred.
        This implementation is not very efficient"""
        referrings = cast(
            Collection[Referring[ProtobufWithUUIDAndDatetime]],
            self.referring(referred, type_name),
        )
        if len(referrings) > 0:
            return max(referrings, key=lambda r: r.protobuf().datetime)
        else:
            return None

    def type_name(
        self, type_name: str
    ) -> Collection[Referrable[ProtobufWithUUID]]:
        return {
            ref
            for ref in self._referrables.values()
            if ref.type_name() == type_name
        }

    def all_referrings(self, uuid: str) -> List[str]:
        """Returns a list all items referring to a Referrable recursively."""
        target = self.referrable(uuid)

        to_delete, to_check = set(), {target}
        while len(to_check) > 0:
            node = to_check.pop()
            if not node:
                continue
            to_delete.add(node)
            deps = node.referring()
            if not deps:
                continue
            for dep in deps:
                if dep not in to_delete:
                    to_check.add(dep)

        return [msg.uuid() for msg in to_delete]

    def delete(self, uuid: str) -> None:
        """Delete a Referrable and all elements referring to it to let the
        storage in a consistent state."""
        uuids_to_delete = set(self.all_referrings(uuid))

        self._referrables = {
            k: v
            for k, v in self._referrables.items()
            if k not in uuids_to_delete
        }

        self._referring = defaultdict(
            set,
            {
                k: v - uuids_to_delete
                for k, v in self._referring.items()
                if k not in uuids_to_delete
            },
        )
