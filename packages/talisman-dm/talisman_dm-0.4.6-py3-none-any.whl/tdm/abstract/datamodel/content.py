from abc import ABCMeta, abstractmethod
from enum import Enum
from operator import attrgetter
from typing import Any, Dict, Tuple, TypeVar

from .span import AbstractSpan, AbstractTalismanSpan
from .tree import AbstractTree


class NodeType(Enum):
    HEADER = "header"
    TEXT = "text"
    LIST = "list"
    JSON = "json"
    KEY = "key"
    TABLE = "table"
    TABLE_ROW = "row"
    IMAGE = "image"


_AbstractDocumentContent = TypeVar('_AbstractDocumentContent', bound='AbstractDocumentContent')


class AbstractDocumentContent(metaclass=ABCMeta):
    __slots__ = ()

    @property
    @abstractmethod
    def type(self) -> NodeType:
        pass

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @abstractmethod
    def text_for(self, span: AbstractSpan) -> str:
        pass

    @property
    @abstractmethod
    def node_text(self) -> str:
        pass

    @abstractmethod
    def with_node_text(self: _AbstractDocumentContent, text: str) -> _AbstractDocumentContent:
        pass

    @property
    @abstractmethod
    def original_node_text(self) -> str:
        pass

    @property
    @abstractmethod
    def markup(self) -> Dict[str, Any]:
        pass

    @property
    @abstractmethod
    def is_hidden(self) -> bool:
        pass

    @abstractmethod
    def hide(self: _AbstractDocumentContent) -> _AbstractDocumentContent:
        pass

    @abstractmethod
    def show(self: _AbstractDocumentContent) -> _AbstractDocumentContent:
        pass


_AbstractTreeDocumentContent = TypeVar('_AbstractTreeDocumentContent', bound='AbstractTreeDocumentContent')


class AbstractTreeDocumentContent(AbstractTree, AbstractDocumentContent, metaclass=ABCMeta):

    @abstractmethod
    def talisman_spans(self, span: AbstractSpan) -> Tuple[AbstractTalismanSpan, ...]:
        pass

    def talisman_span(self, span: AbstractSpan) -> AbstractTalismanSpan:
        spans = self.talisman_spans(span)
        if len(spans) != 1:
            raise ValueError(f"{span} spreads over several nodes {tuple(map(attrgetter('node_id'), spans))}")
        return spans[0]

    @abstractmethod
    def span(self, talisman_span: AbstractTalismanSpan) -> AbstractSpan:
        pass
