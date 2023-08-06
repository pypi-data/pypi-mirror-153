from copy import deepcopy
from typing import Iterable, Optional, Tuple, Union

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanSpan, FactMetadata, FactStatus, FactType
from tdm.abstract.datamodel.fact import AbstractLinkValue
from tdm.datamodel.fact.concept import ConceptFact
from tdm.datamodel.fact.relation import RelationFact
from tdm.datamodel.fact.value import ValueFact


class PropertyLinkValue(AbstractLinkValue[Union[ConceptFact, RelationFact], ValueFact]):
    @classmethod
    def validate_slots(cls, source: Union[ConceptFact, RelationFact], target: ValueFact):
        if source.fact_type is not FactType.CONCEPT and source.fact_type is not FactType.RELATION:
            raise ValueError(f"inconsistent property link source type: {source.fact_type}")
        if target.fact_type is not FactType.VALUE:
            raise ValueError(f"inconsistent property link target type: {target.fact_type}")


class PropertyFact(AbstractFact[PropertyLinkValue]):
    def __init__(self, id_: Optional[str], status: FactStatus, type_id: str, value: PropertyLinkValue,
                 mention: Iterable[AbstractTalismanSpan] = None, metadata: Optional[FactMetadata] = None):
        if not isinstance(value, PropertyLinkValue):
            raise ValueError(f"illegal value type for property fact: {type(value)}")
        metadata = deepcopy(metadata)  # guarantee immutability
        super().__init__(id_, FactType.PROPERTY, status, type_id, value, mention, metadata)

    def with_changes(self: 'PropertyFact', *, status: FactStatus = None, type_id: str = None,
                     value: PropertyLinkValue = None,
                     mention: Tuple[AbstractTalismanSpan, ...] = None,
                     metadata: FactMetadata = None) -> 'PropertyFact':
        return PropertyFact(
            self._id,
            status if status is not None else self._status,
            type_id if type_id is not None else self._type_id,
            value if value is not None else self._value,
            mention if mention is not None else self._mention,
            metadata if metadata is not None else self._metadata
        )
