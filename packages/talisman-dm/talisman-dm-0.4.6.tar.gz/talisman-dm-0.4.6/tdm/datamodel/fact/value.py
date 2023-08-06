from copy import deepcopy
from typing import Any, Dict, Iterable, Optional, Tuple, Union

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanSpan, FactMetadata, FactStatus, FactType

ValueType = Dict[str, Any]  # TODO: maybe we should restrict Any typing


class ValueFact(AbstractFact[ValueType]):
    def __init__(self, id_: Optional[str], status: FactStatus, type_id: str,
                 value: Optional[Union[ValueType, Tuple[ValueType, ...]]] = None,
                 mention: Iterable[AbstractTalismanSpan] = None,
                 metadata: Optional[FactMetadata] = None):
        value = deepcopy(value)  # guarantee immutability
        metadata = deepcopy(metadata)  # guarantee immutability
        super().__init__(id_, FactType.VALUE, status, type_id, value, mention, metadata)

    @property
    def value(self) -> Union[ValueType, Tuple[ValueType, ...]]:
        return deepcopy(self._value)  # guarantee immutability

    def with_changes(self: 'ValueFact', *, status: FactStatus = None, type_id: str = None,
                     value: Union[ValueType, Tuple[ValueType, ...]] = None,
                     mention: Tuple[AbstractTalismanSpan, ...] = None,
                     metadata: FactMetadata = None) -> 'ValueFact':
        return ValueFact(
            self._id,
            status if status is not None else self._status,
            type_id if type_id is not None else self._type_id,
            value if value is not None else self._value,
            mention if mention is not None else self._mention,
            metadata if metadata is not None else self._metadata
        )
