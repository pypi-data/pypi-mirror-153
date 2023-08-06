from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict, Generic, Iterable, Iterator, Optional, Tuple, Type, TypeVar

from .content import AbstractTreeDocumentContent
from .directive import AbstractDirective
from .fact import AbstractFact

DocumentMetadata = Dict[str, Any]
_AbstractTalismanDocument = TypeVar('_AbstractTalismanDocument', bound='AbstractTalismanDocument')
_AbstractTreeDocumentContent = TypeVar('_AbstractTreeDocumentContent', bound=AbstractTreeDocumentContent)
_Fact = TypeVar('_Fact', bound=AbstractFact)
_Directive = TypeVar('_Directive', bound=AbstractDirective)


class AbstractTalismanDocument(Generic[_AbstractTreeDocumentContent], metaclass=ABCMeta):
    __slots__ = ()

    @property
    @abstractmethod
    def doc_id(self) -> str:
        pass

    @property
    @abstractmethod
    def content(self) -> _AbstractTreeDocumentContent:
        pass

    @abstractmethod
    def with_content(self: _AbstractTalismanDocument, content: _AbstractTreeDocumentContent) -> _AbstractTalismanDocument:
        pass

    @property
    @abstractmethod
    def metadata(self) -> Optional[DocumentMetadata]:
        pass

    @abstractmethod
    def with_metadata(self: _AbstractTalismanDocument, metadata: DocumentMetadata) -> _AbstractTalismanDocument:
        pass

    @property
    @abstractmethod
    def facts(self) -> Tuple[AbstractFact, ...]:
        pass

    @abstractmethod
    def filter_facts(self, type_: Type[_Fact], filter_: Callable[[_Fact], bool] = lambda _: True) -> Iterator[_Fact]:
        pass

    @abstractmethod
    def with_facts(self: _AbstractTalismanDocument, facts: Iterable[AbstractFact]) -> _AbstractTalismanDocument:
        pass

    @abstractmethod
    def without_facts(self: _AbstractTalismanDocument) -> _AbstractTalismanDocument:
        pass

    @property
    @abstractmethod
    def directives(self) -> Tuple[AbstractDirective, ...]:
        pass

    @abstractmethod
    def with_directives(self: _AbstractTalismanDocument, directives: Iterable[AbstractDirective]) -> _AbstractTalismanDocument:
        pass

    @abstractmethod
    def without_directives(self: _AbstractTalismanDocument) -> _AbstractTalismanDocument:
        pass

    @abstractmethod
    def filter_directives(self, type_: Type[_Directive], filter_: Callable[[_Directive], bool] = lambda _: True) -> Iterator[_Directive]:
        pass
