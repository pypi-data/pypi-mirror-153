from abc import ABCMeta, abstractmethod
from typing import TypeVar


_AbstractSpan = TypeVar('_AbstractSpan', bound='AbstractSpan')


class AbstractSpan(metaclass=ABCMeta):
    __slots__ = ()

    @property
    @abstractmethod
    def start_idx(self) -> int:
        pass

    @property
    @abstractmethod
    def end_idx(self) -> int:
        pass

    @property
    @abstractmethod
    def length(self) -> int:
        pass

    @abstractmethod
    def shift(self: _AbstractSpan, shift: int) -> _AbstractSpan:
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __lt__(self, other):
        pass

    def coincides(self, obj: 'AbstractSpan') -> bool:
        if not isinstance(obj, AbstractSpan):
            raise TypeError(f"expected {AbstractSpan}, got {type(obj)}")
        return self.start_idx == obj.start_idx and self.end_idx == obj.end_idx

    def intersects(self, obj: 'AbstractSpan') -> bool:
        return self._distance(obj) < 0

    def distance(self, obj: 'AbstractSpan') -> int:
        return max(0, self._distance(obj))

    def _distance(self, obj: 'AbstractSpan') -> int:
        if not isinstance(obj, AbstractSpan):
            raise TypeError(f"expected {AbstractSpan}, got {type(obj)}")
        return max(self.start_idx, obj.start_idx) - min(self.end_idx, obj.end_idx)

    def contains(self, obj: 'AbstractSpan') -> bool:
        if not isinstance(obj, AbstractSpan):
            raise TypeError(f"expected {AbstractSpan}, got {type(obj)}")
        return self.start_idx <= obj.start_idx and self.end_idx >= obj.end_idx


class AbstractTalismanSpan(AbstractSpan, metaclass=ABCMeta):

    @property
    @abstractmethod
    def node_id(self):
        pass
