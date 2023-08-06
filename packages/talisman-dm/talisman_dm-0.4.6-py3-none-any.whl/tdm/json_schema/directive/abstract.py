from abc import abstractmethod
from typing import Type, TypeVar

from pydantic import BaseModel

from tdm.abstract.datamodel.directive import AbstractDirective, DirectiveType


_AbstractDirectiveModel = TypeVar('_AbstractDirectiveModel', bound='AbstractDirectiveModel')


class AbstractDirectiveModel(BaseModel):
    directive_type: DirectiveType

    @classmethod
    @abstractmethod
    def build(cls: Type[_AbstractDirectiveModel], directive: AbstractDirective) -> _AbstractDirectiveModel:
        pass

    @abstractmethod
    def to_directive(self) -> AbstractDirective:
        pass
