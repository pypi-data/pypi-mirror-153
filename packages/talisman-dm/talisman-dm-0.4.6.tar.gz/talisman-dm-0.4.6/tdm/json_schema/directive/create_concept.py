from typing import Optional, Tuple

from typing_extensions import Literal

from tdm.abstract.datamodel.directive import DirectiveType
from tdm.datamodel import CreateConceptDirective
from tdm.json_schema.directive.abstract import AbstractDirectiveModel


class CreateConceptDirectiveModel(AbstractDirectiveModel):
    id: str
    name: str
    concept_type: str
    notes: Optional[str]
    markers: Optional[Tuple[str, ...]]
    access_level: Optional[str]

    directive_type: Literal[DirectiveType.CREATE_CONCEPT] = DirectiveType.CREATE_CONCEPT

    @classmethod
    def build(cls, directive: CreateConceptDirective) -> 'CreateConceptDirectiveModel':
        return cls.construct(
            id=directive.id,
            name=directive.name,
            concept_type=directive.concept_type,
            notes=directive.notes,
            markers=directive.markers,
            access_level=directive.access_level
        )

    def to_directive(self) -> CreateConceptDirective:
        return CreateConceptDirective(
            name=self.name,
            concept_type=self.concept_type,
            notes=self.notes,
            markers=self.markers,
            access_level=self.access_level,
            id_=self.id
        )

    def __hash__(self):
        return hash((self.directive_type, self.concept_type, self.id))
