from typing import Any, Callable, Dict, Tuple

from typing_extensions import Literal

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanSpan, FactMetadata, FactStatus, FactType
from tdm.datamodel.fact import ConceptFact
from tdm.json_schema.fact.common import AbstractFactModel


class ConceptFactModel(AbstractFactModel):
    fact_type: Literal[FactType.CONCEPT] = FactType.CONCEPT

    def to_value(self, mapping: Dict[str, AbstractFact]) -> Any:
        return self.value

    @property
    def fact_factory(self) -> Callable[[str, FactStatus, str, Any, Tuple[AbstractTalismanSpan, ...], FactMetadata],
                                       ConceptFact]:
        return ConceptFact

    @classmethod
    def build_value(cls, value: Any) -> Any:
        return value
