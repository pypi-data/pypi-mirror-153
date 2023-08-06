from abc import ABCMeta, abstractmethod
from typing import Iterable, Optional, Tuple, TypeVar

_AbstractTree = TypeVar('_AbstractTree', bound='AbstractTree')


class AbstractTree(metaclass=ABCMeta):
    __slots__ = ()

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    def root(self: _AbstractTree) -> _AbstractTree:
        parent = self.parent
        if parent is None:
            return self
        return parent.root

    @property
    @abstractmethod
    def parent(self: _AbstractTree) -> Optional[_AbstractTree]:
        pass

    @property
    @abstractmethod
    def nodes(self: _AbstractTree) -> Tuple[_AbstractTree, ...]:
        pass

    @abstractmethod
    def node(self: _AbstractTree, node_id: str) -> _AbstractTree:
        pass

    @abstractmethod
    def pruned(self: _AbstractTree) -> _AbstractTree:
        pass

    @abstractmethod
    def with_nodes(self: _AbstractTree, nodes: Iterable[_AbstractTree]) -> _AbstractTree:
        pass

    @abstractmethod
    def as_root(self: _AbstractTree) -> _AbstractTree:
        pass

    @abstractmethod
    def equal_structure(self: _AbstractTree, other: _AbstractTree) -> bool:
        pass

    @abstractmethod
    def _get_updated_constructor_params(self, **kwargs) -> dict:
        pass

    def _with_changes(self: _AbstractTree, **kwargs) -> _AbstractTree:
        return type(self)(**self._get_updated_constructor_params(**kwargs))
