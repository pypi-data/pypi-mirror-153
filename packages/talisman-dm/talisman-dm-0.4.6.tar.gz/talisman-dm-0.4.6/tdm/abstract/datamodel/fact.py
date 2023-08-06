import uuid
from abc import ABCMeta, abstractmethod
from enum import Enum
from functools import total_ordering
from typing import Any, Dict, Generic, Iterable, Optional, Tuple, TypeVar, Union

from tdm.abstract.datamodel.span import AbstractTalismanSpan


@total_ordering
class FactStatus(str, Enum):

    def __new__(cls, name: str, priority: int):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj.priority = priority
        return obj

    APPROVED = ("approved", 0)
    DECLINED = ("declined", 1)
    AUTO = ("auto", 2)
    HIDDEN = ("hidden", 3)
    NEW = ("new", 4)

    def __lt__(self, other: 'FactStatus'):
        if not isinstance(other, FactStatus):
            return NotImplemented
        return self.priority < other.priority


class FactType(str, Enum):
    PROPERTY = "property"
    RELATION = "relation"
    CONCEPT = "concept"
    VALUE = "value"


FactMetadata = Dict[str, Any]

_FactValue = TypeVar('_FactValue')
_AbstractFact = TypeVar('_AbstractFact', bound='AbstractFact')


class AbstractFact(Generic[_FactValue], metaclass=ABCMeta):
    __slots__ = ('_id', '_mention', '_fact_type', '_status', '_type_id', '_value', '_metadata')

    def __init__(self, id_: Optional[str], fact_type: FactType, status: FactStatus, type_id: str,
                 value: Optional[Union[_FactValue, Tuple[_FactValue, ...]]] = None,
                 mention: Iterable[AbstractTalismanSpan] = None, metadata: Optional[FactMetadata] = None):
        self._id = id_ or self.generate_id()
        self._mention = tuple(mention) if mention is not None else None
        self._fact_type = fact_type
        self._status = status
        self._type_id = type_id
        self._value = value  # subclasses must guarantee value immutability
        self._metadata = metadata  # subclasses must guarantee metadata immutability

    @property
    def id(self) -> str:
        return self._id

    @property
    def mention(self) -> Optional[Tuple[AbstractTalismanSpan, ...]]:
        return self._mention

    @property
    def fact_type(self) -> FactType:
        return self._fact_type

    @property
    def status(self) -> FactStatus:
        return self._status

    @property
    def type_id(self) -> str:
        return self._type_id

    @property
    def value(self) -> Union[_FactValue, Tuple[_FactValue, ...]]:
        return self._value  # subclasses must guarantee value immutability

    @property
    def has_value(self) -> bool:
        return bool(self._value)

    @property
    def metadata(self) -> FactMetadata:
        return self._metadata  # subclasses must guarantee metadata immutability

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())

    def __eq__(self, other):
        if not isinstance(other, AbstractFact):
            return NotImplemented
        return self._id == other._id and self._mention == other._mention and self._fact_type == other._fact_type \
            and self._status == other._status and self._type_id == other._type_id and self._value == other._value

    def __hash__(self):
        return hash((self._id, self._mention, self._fact_type, self._status, self._type_id))

    @abstractmethod
    def with_changes(self: _AbstractFact, *, status: FactStatus = None, type_id: str = None,
                     value: Union[_FactValue, Tuple[_FactValue, ...]] = None,
                     mention: Tuple[AbstractTalismanSpan, ...] = None,
                     metadata: FactMetadata = None) -> _AbstractFact:
        pass

    def __repr__(self):
        return f"Fact({self._id}, {self._fact_type}, {self._status}, {self._type_id}, {self._value}, " \
               f"{self._metadata}, {self._mention})"


_SourceFactType = TypeVar('_SourceFactType', bound=AbstractFact)
_TargetFactType = TypeVar('_TargetFactType', bound=AbstractFact)


class AbstractLinkValue(Generic[_SourceFactType, _TargetFactType], metaclass=ABCMeta):
    def __init__(self, property_id: Optional[str], from_fact: _SourceFactType, to_fact: _TargetFactType):
        self.validate_slots(from_fact, to_fact)
        self._property_id = property_id
        self._from_fact = from_fact
        self._to_fact = to_fact

    @property
    def property_id(self) -> Optional[str]:
        return self._property_id

    @property
    def from_fact(self) -> _SourceFactType:
        return self._from_fact

    @property
    def to_fact(self) -> _TargetFactType:
        return self._to_fact

    def update_value(self, id2fact: Dict[str, AbstractFact]):
        return type(self)(self._property_id, id2fact[self._from_fact.id], id2fact[self._to_fact.id])

    @classmethod
    @abstractmethod
    def validate_slots(cls, source: _SourceFactType, target: _TargetFactType):
        pass

    def __eq__(self, other):
        if not isinstance(other, AbstractLinkValue):
            return NotImplemented
        return self._property_id == other._property_id and self._from_fact == other._from_fact and self._to_fact == self._to_fact

    def __hash__(self):
        return hash((self._property_id, self._from_fact, self._to_fact))

    def __repr__(self):
        return f"PropertyLinkValue({self._property_id}, {self.from_fact.id}, {self.to_fact.id})"
