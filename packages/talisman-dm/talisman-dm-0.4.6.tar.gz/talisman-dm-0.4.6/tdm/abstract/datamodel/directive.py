from abc import ABCMeta
from enum import Enum


class DirectiveType(str, Enum):
    CREATE_CONCEPT = 'create_concept'


class AbstractDirective(metaclass=ABCMeta):
    __slots__ = ('_directive_type',)

    def __init__(self, directive_type: DirectiveType):
        self._directive_type = directive_type

    @property
    def directive_type(self) -> DirectiveType:
        return self._directive_type
