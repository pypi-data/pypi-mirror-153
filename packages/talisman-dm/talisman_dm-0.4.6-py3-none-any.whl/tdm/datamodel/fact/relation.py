from copy import deepcopy
from typing import Iterable, Optional, Tuple

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanSpan, FactMetadata, FactStatus, FactType
from tdm.abstract.datamodel.fact import AbstractLinkValue
from tdm.datamodel.fact.concept import ConceptFact


class RelationLinkValue(AbstractLinkValue[ConceptFact, ConceptFact]):
    @classmethod
    def validate_slots(cls, source: ConceptFact, target: ConceptFact):
        if source.fact_type is not FactType.CONCEPT:
            raise ValueError(f"inconsistent relation link source type: {source.fact_type}")
        if target.fact_type is not FactType.CONCEPT:
            raise ValueError(f"inconsistent relation link target type: {target.fact_type}")


class RelationFact(AbstractFact[RelationLinkValue]):
    def __init__(self, id_: Optional[str], status: FactStatus, type_id: str, value: RelationLinkValue,
                 mention: Iterable[AbstractTalismanSpan] = None, metadata: Optional[FactMetadata] = None):
        if not isinstance(value, RelationLinkValue):
            raise ValueError(f"illegal value type for relation fact: {type(value)}")
        metadata = deepcopy(metadata)  # guarantee immutability
        super().__init__(id_, FactType.RELATION, status, type_id, value, mention, metadata)

    def with_changes(self: 'RelationFact', *, status: FactStatus = None, type_id: str = None, value: RelationLinkValue = None,
                     mention: Tuple[AbstractTalismanSpan, ...] = None,
                     metadata: FactMetadata = None) -> 'RelationFact':

        return RelationFact(
            self._id,
            status if status is not None else self._status,
            type_id if type_id is not None else self._type_id,
            value if value is not None else self._value,
            mention if mention is not None else self._mention,
            metadata if metadata is not None else self._metadata
        )
