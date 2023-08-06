import logging
from copy import deepcopy
from typing import Iterable, Optional, Tuple, Union

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanSpan, FactMetadata, FactStatus, FactType

ConceptValueType = str  # TODO: describe concept type

logger = logging.getLogger(__name__)


class ConceptFact(AbstractFact[ConceptValueType]):
    def __init__(self, id_: Optional[str], status: FactStatus, type_id: str,
                 value: Union[ConceptValueType, Tuple[ConceptValueType, ...]] = tuple(),
                 mention: Optional[Iterable[AbstractTalismanSpan]] = None,
                 metadata: Optional[FactMetadata] = None):
        metadata = deepcopy(metadata)  # guarantee immutability
        if value is None:
            value = tuple()
            logger.warning("value must not be None, value=tuple()")
        super().__init__(id_, FactType.CONCEPT, status, type_id, value, mention, metadata)

    def with_changes(self: 'ConceptFact', *, status: FactStatus = None, type_id: str = None,
                     value: Union[str, Tuple[str, ...]] = None,
                     mention: Tuple[AbstractTalismanSpan, ...] = None,
                     metadata: FactMetadata = None) -> 'ConceptFact':
        return ConceptFact(
            self._id,
            status if status is not None else self._status,
            type_id if type_id is not None else self._type_id,
            value if value is not None else self._value,
            mention if mention is not None else self._mention,
            metadata if metadata is not None else self._metadata
        )
