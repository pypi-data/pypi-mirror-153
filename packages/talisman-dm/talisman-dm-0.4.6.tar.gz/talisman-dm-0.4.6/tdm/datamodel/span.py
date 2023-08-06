from abc import ABCMeta
from functools import total_ordering
from typing import Tuple

from tdm.abstract.datamodel import AbstractSpan, AbstractTalismanSpan


class DefaultSpan(AbstractSpan, metaclass=ABCMeta):
    __slots__ = ('_start_idx', '_end_idx')

    def __init__(self, start_idx: int, end_idx: int, *, nullable=False):
        self._start_idx = start_idx
        self._end_idx = end_idx

        if not (0 <= self._start_idx <= self._end_idx):
            raise Exception("Incorrect span range")
        if not nullable and self._start_idx == self._end_idx:
            raise Exception("Incorrect span range")

    @property
    def start_idx(self) -> int:
        return self._start_idx

    @property
    def end_idx(self) -> int:
        return self._end_idx

    @property
    def length(self) -> int:
        return self._end_idx - self._start_idx


class NullableSpan(DefaultSpan):
    __slots__ = ()

    def __init__(self, start: int, end: int):
        super().__init__(start, end, nullable=True)

    def shift(self, shift: int) -> 'NullableSpan':
        return NullableSpan(self._start_idx + shift, self._end_idx + shift)

    def _as_tuple(self) -> Tuple[int, int]:
        return self.start_idx, self.end_idx

    def __eq__(self, other):
        if not isinstance(other, NullableSpan):
            return NotImplemented
        return other._as_tuple() == self._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())

    def __repr__(self):
        return repr(self._as_tuple())

    def __lt__(self, other):
        if not isinstance(other, NullableSpan):
            return NotImplemented
        return self._as_tuple() < other._as_tuple()


def _compare_ids(func):
    def decorate(self: AbstractTalismanSpan, obj: AbstractSpan):
        if not isinstance(obj, AbstractTalismanSpan) or self.node_id != obj.node_id:
            return False
        return func(self, obj)
    return decorate


@total_ordering
class TalismanSpan(DefaultSpan, AbstractTalismanSpan):
    __slots__ = ('_id', )

    def __init__(self, id_: str, start_idx: int, end_idx: int):
        super().__init__(start_idx, end_idx, nullable=True)
        self._id = id_

    @property
    def node_id(self):
        return self._id

    def _as_tuple(self) -> Tuple[str, int, int]:
        return self._id, self.start_idx, self.end_idx

    def shift(self, shift: int) -> 'TalismanSpan':
        return TalismanSpan(self._id, self._start_idx + shift, self._end_idx + shift)

    coincides = _compare_ids(DefaultSpan.coincides)
    intersects = _compare_ids(DefaultSpan.intersects)
    contains = _compare_ids(DefaultSpan.contains)

    def distance(self, obj: 'AbstractSpan') -> int:
        if not isinstance(obj, AbstractTalismanSpan) or obj.node_id != self.node_id:
            raise ValueError(f'Spans {self} and {obj} are on the different nodes!')
        return super().distance(obj)

    def __eq__(self, other):
        if not isinstance(other, TalismanSpan):
            return NotImplemented
        return other._as_tuple() == self._as_tuple()

    def __lt__(self, other):
        if not isinstance(other, TalismanSpan):
            return NotImplemented
        if self.node_id != other.node_id:
            raise ValueError(f'Spans {self} and {other} are on the different nodes!')
        return self._as_tuple() < other._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())

    def __repr__(self):
        return repr(self._as_tuple())
