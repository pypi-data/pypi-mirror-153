import uuid
from typing import Iterable, Optional, Tuple

from tdm.abstract.datamodel import AbstractDirective
from tdm.abstract.datamodel.directive import DirectiveType


class CreateConceptDirective(AbstractDirective):
    __slots__ = ('_name', '_concept_type', '_notes', '_markers', '_access_level', '_id')

    def __init__(self, name: str, concept_type: str, notes: Optional[str] = None, markers: Optional[Iterable[str]] = None,
                 access_level: Optional[str] = None, id_: Optional[str] = None):
        super().__init__(DirectiveType.CREATE_CONCEPT)
        self._id = id_ or self.generate_id()
        self._name = name
        self._concept_type = concept_type
        self._notes = notes
        self._markers = tuple(markers) if markers else None
        self._access_level = access_level

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def concept_type(self) -> str:
        return self._concept_type

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @property
    def markers(self) -> Optional[Tuple[str]]:
        return self._markers

    @property
    def access_level(self):
        return self._access_level

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())

    def __eq__(self, other):
        if not isinstance(other, AbstractDirective):
            return NotImplemented
        return isinstance(other, CreateConceptDirective) and other._id == self._id and other._name == self._name and \
            other._concept_type == self._concept_type and other._notes == self._notes and other._markers == self._markers and \
            other._access_level == self._access_level

    def __hash__(self):
        return hash((self._directive_type, self.concept_type, self._id))
