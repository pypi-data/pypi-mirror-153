from abc import abstractmethod
from typing import Any, Callable, Dict, Optional, Tuple

from pydantic import BaseModel

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanSpan, AbstractTreeDocumentContent, FactMetadata, \
    FactStatus, FactType
from tdm.abstract.datamodel.fact import AbstractLinkValue
from tdm.datamodel import TalismanSpan


class SpanModel(BaseModel):
    node_id: str
    value: str
    start: int
    end: int

    def to_span(self) -> TalismanSpan:
        return TalismanSpan(start_idx=self.start, end_idx=self.end, id_=self.node_id)

    @classmethod
    def build(cls, span: AbstractTalismanSpan, doc: AbstractTreeDocumentContent) -> 'SpanModel':
        return cls.construct(node_id=span.node_id, value=doc.text_for(span), start=span.start_idx, end=span.end_idx)


class PropertyLinkValueModel(BaseModel):
    property_id: Optional[str]
    from_fact: str
    to_fact: str

    @classmethod
    def build(cls, value: AbstractLinkValue) -> 'PropertyLinkValueModel':
        return cls.construct(property_id=value.property_id, from_fact=value.from_fact.id, to_fact=value.to_fact.id)


class AbstractFactModel(BaseModel):
    id: str
    fact_type: FactType
    status: FactStatus
    type_id: str
    value: Any
    mention: Optional[Tuple[SpanModel, ...]]
    metadata: Optional[FactMetadata]

    def to_fact_factory(self) -> Tuple[FactType, Callable[[Dict[str, AbstractFact]], AbstractFact]]:
        def create_fact(mapping: Dict[str, AbstractFact]) -> AbstractFact:
            mention = tuple(span_model.to_span() for span_model in self.mention) if self.mention is not None else None
            return self.fact_factory(self.id, self.status, self.type_id, self.to_value(mapping), mention, self.metadata)

        return self.fact_type, create_fact

    @abstractmethod
    def to_value(self, mapping: Dict[str, AbstractFact]) -> Any:
        pass

    @property
    @abstractmethod
    def fact_factory(self) -> Callable[[str, FactStatus, str, Any, Tuple[AbstractTalismanSpan, ...],
                                       FactMetadata], AbstractFact]:
        pass

    @classmethod
    @abstractmethod
    def build_value(cls, value: Any) -> Any:
        pass

    def __hash__(self) -> int:
        return hash((self.id, self.fact_type, self.status, self.type_id))
