from collections import defaultdict
from typing import Dict, Optional, Tuple, Union

from pydantic import BaseModel

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanDocument, FactType
from tdm.datamodel import TalismanDocument
from .content import TreeDocumentContentModel
from .directive import CreateConceptDirectiveModel
from .directive.factory import build_directive_model
from .fact import ConceptFactModel, PropertyFactModel, RelationFactModel, ValueFactModel, build_fact_model
from .metadata import DocumentMetadataModel

FactModel = Union[ConceptFactModel, ValueFactModel, PropertyFactModel, RelationFactModel]
DirectiveModel = Union[CreateConceptDirectiveModel]


class TalismanDocumentModel(BaseModel):
    id: str
    content: TreeDocumentContentModel
    metadata: Optional[DocumentMetadataModel]
    facts: Optional[Tuple[FactModel, ...]]  # pydantic fails to serialize FrozenSet[FactModel]
    directives: Optional[Tuple[DirectiveModel, ...]]

    def to_doc(self) -> TalismanDocument:
        type2fact_factory = defaultdict(list)
        for t, ff in map(lambda model: model.to_fact_factory(), (self.facts or tuple())):
            type2fact_factory[t].append(ff)

        def build_facts(fact_type: FactType, ids_mapping: Dict[str, AbstractFact]) -> Dict[str, AbstractFact]:
            return {fact.id: fact for fact in map(lambda factory: factory(ids_mapping), type2fact_factory.get(fact_type, []))}
        ids2facts = {}
        for ft in [FactType.CONCEPT, FactType.VALUE, FactType.RELATION, FactType.PROPERTY]:
            ids2facts.update(build_facts(ft, ids2facts))

        return TalismanDocument(
            doc_id=self.id, content=self.content.to_content(),
            metadata=self.metadata.to_metadata() if self.metadata is not None else None,
            facts=tuple(ids2facts.values()),
            directives=tuple(directive.to_directive() for directive in self.directives) if self.directives else None
        )

    @classmethod
    def build(cls, doc: AbstractTalismanDocument) -> 'TalismanDocumentModel':
        content_type = cls.__fields__['content'].type_
        return cls.construct(
            id=doc.doc_id,
            content=content_type.build(doc.content),
            metadata=DocumentMetadataModel(**doc.metadata) if doc.metadata is not None else None,
            facts=tuple(build_fact_model(fact, doc.content) for fact in doc.facts) if doc.facts is not None else None,
            directives=tuple(build_directive_model(directive) for directive in doc.directives) if doc.directives else None
        )
