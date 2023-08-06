from typing import Any, Callable, Dict, Tuple

from typing_extensions import Literal

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanSpan, FactMetadata, FactStatus, FactType
from tdm.datamodel.fact import ValueFact
from tdm.json_schema.fact.common import AbstractFactModel


class ValueFactModel(AbstractFactModel):
    fact_type: Literal[FactType.VALUE] = FactType.VALUE

    def to_value(self, mapping: Dict[str, AbstractFact]) -> Any:
        return self.value

    @property
    def fact_factory(self) -> Callable[[str, FactStatus, str, Any, Tuple[AbstractTalismanSpan, ...], FactMetadata],
                                       AbstractFact]:
        return ValueFact

    @classmethod
    def build_value(cls, value: Any) -> Any:
        return value
