from collections import defaultdict
from copy import deepcopy
from itertools import chain
from typing import Callable, Dict, FrozenSet, Generic, Iterable, Iterator, List, Optional, Type, TypeVar, Union

from tdm.abstract.datamodel import AbstractDirective, AbstractFact, AbstractTalismanDocument, AbstractTreeDocumentContent, FactType
from tdm.abstract.datamodel.document import DocumentMetadata
from tdm.datamodel.fact import ConceptFact, PropertyFact, RelationFact, ValueFact
from .fact import PropertyLinkValue

_TalismanDocument = TypeVar('_TalismanDocument', bound='TalismanDocument')
_Content = TypeVar('_Content', bound=AbstractTreeDocumentContent)
_Fact = TypeVar('_Fact', bound=AbstractFact)
_Directive = TypeVar('_Directive', bound=AbstractDirective)


class TalismanDocument(AbstractTalismanDocument[_Content], Generic[_Content]):
    __slots__ = (
        '_doc_id', '_content', '_metadata', '_facts', '_directives'
    )

    def __init__(self, doc_id: str, content: _Content, metadata: DocumentMetadata = None,
                 facts: Optional[Iterable[AbstractFact]] = None, directives: Optional[Iterable[AbstractDirective]] = None):

        self._doc_id = doc_id
        self._content = content
        self._metadata = deepcopy(metadata)  # TODO: rewrite when DocumentMetadata has been changed
        self._facts = frozenset(facts) if facts else frozenset()
        self._validate_facts(self._facts)
        self._directives = frozenset(directives) if directives else frozenset()

    @staticmethod
    def _validate_facts(facts: Iterable[AbstractFact]) -> None:
        id2fact = {}
        for fact in facts:
            if fact.id in id2fact:
                raise ValueError(f"duplicate fact id: {id2fact[fact.id]} and {fact}")
            id2fact[fact.id] = fact
        for fact in filter(lambda f: f.fact_type is FactType.RELATION or f.fact_type is FactType.PROPERTY, facts):
            value: PropertyLinkValue = fact.value
            if value.from_fact.id not in id2fact:
                raise ValueError(f"link fact {fact} source is not in facts")
            if id2fact[value.from_fact.id] != value.from_fact:
                raise ValueError(f"link fact {fact} source refers to another fact. "
                                 f"Document contains {id2fact[value.from_fact.id]}, link fact refers to {value.from_fact}")
            if value.to_fact.id not in id2fact:
                raise ValueError(f"link fact {fact} target is not in facts")
            if id2fact[value.to_fact.id] != value.to_fact:
                raise ValueError(f"link fact {fact} target refers to another fact. "
                                 f"Document contains {id2fact[value.to_fact.id]}, link fact refers to {value.to_fact}")

    @property
    def doc_id(self) -> str:
        return self._doc_id

    @property
    def content(self) -> _Content:
        return self._content

    def with_content(self: _TalismanDocument, content: _Content) -> _TalismanDocument:
        return type(self)(doc_id=self._doc_id, content=content, metadata=self._metadata, facts=self._facts, directives=self._directives)

    @property
    def metadata(self) -> Optional[DocumentMetadata]:
        return deepcopy(self._metadata)  # TODO: rewrite when DocumentMetadata has been changed

    def with_metadata(self: _TalismanDocument, metadata: DocumentMetadata) -> _TalismanDocument:
        return type(self)(doc_id=self._doc_id, content=self._content, metadata=metadata, facts=self._facts, directives=self._directives)

    @property
    def facts(self) -> FrozenSet[AbstractFact]:
        return self._facts

    def filter_facts(self, type_: Type[_Fact], filter_: Callable[[_Fact], bool] = lambda _: True) -> Iterator[_Fact]:
        for fact in self._facts:
            if isinstance(fact, type_) and filter_(fact):
                yield fact

    @staticmethod
    def _normalize_facts(facts: Iterable[AbstractFact]) -> FrozenSet[AbstractFact]:
        id2fact: Dict[str, AbstractFact] = {fact.id: fact for fact in facts}  # keep last fact in input sequence
        for fact in filter(lambda f: f.fact_type is FactType.RELATION, id2fact.values()):
            id2fact[fact.id] = fact.with_changes(value=fact.value.update_value(id2fact))
        for fact in filter(lambda f: f.fact_type is FactType.PROPERTY, id2fact.values()):
            id2fact[fact.id] = fact.with_changes(value=fact.value.update_value(id2fact))
        return frozenset(id2fact.values())

    def with_facts(self: _TalismanDocument, facts: Iterable[AbstractFact]) -> _TalismanDocument:
        # Update facts with same id (keep last fact in input sequence)
        unique_facts: Dict[str, AbstractFact] = {fact.id: fact for fact in chain(self._facts, facts)}

        # Collect groups of facts by type, type_id and mention
        span2facts = defaultdict(list)
        for fact in unique_facts.values():
            span2facts[(fact.fact_type, fact.type_id, fact.mention)].append(fact)

        def choose_best_fact(group: List[AbstractFact]) -> AbstractFact:
            if len(group) == 1:
                return group[0]
            sorted_facts = sorted(group, key=lambda fact: fact.status)  # sort by status
            best_facts = tuple(filter(lambda f: f.status is sorted_facts[0].status, sorted_facts))
            if any(f.value != best_facts[0].value for f in best_facts):
                raise ValueError(f"adding duplicate facts with different values are not permitted: {best_facts}")
            # choose last fact with best status
            return best_facts[0]

        # Choose best fact in each group
        id2fact = {}
        for (_, _, mention), facts in span2facts.items():
            if mention is None:  # facts without mentions should not be grouped
                for fact in facts:
                    id2fact[fact.id] = fact
                continue
            best_fact = choose_best_fact(facts)
            for fact in facts:  # map all group items to best fact
                id2fact[fact.id] = best_fact

        def update_link_values(fact_type: FactType):
            span2facts = defaultdict(list)  # group relations with respect to type_id, mention and value
            for fact in filter(lambda f: f.fact_type is fact_type, id2fact.values()):
                fact = fact.with_changes(value=fact.value.update_value(id2fact))
                span2facts[(fact.type_id, fact.mention, fact.value)].append(fact)
            # Filter out link duplicate facts
            for group in span2facts.values():
                best_fact = choose_best_fact(group)
                for fact in group:
                    id2fact[fact.id] = best_fact

        # Update relation fact values to refer to correct facts
        update_link_values(FactType.RELATION)
        # Update property fact values to refer to correct facts
        update_link_values(FactType.PROPERTY)

        return type(self)(doc_id=self._doc_id, content=self._content, metadata=self._metadata, facts=set(id2fact.values()),
                          directives=self._directives)

    def without_facts(self: _TalismanDocument) -> _TalismanDocument:
        return type(self)(doc_id=self._doc_id, content=self._content, metadata=self._metadata, facts=None, directives=self._directives)

    @property
    def directives(self) -> FrozenSet[AbstractDirective]:
        return self._directives

    def filter_directives(self, type_: Type[_Directive], filter_: Callable[[_Directive], bool] = lambda _: True) -> Iterator[_Directive]:
        for directive in self._directives:
            if isinstance(directive, type_) and filter_(directive):
                yield directive

    def with_directives(self: _TalismanDocument, directives: Iterable[AbstractDirective]) -> _TalismanDocument:
        return type(self)(doc_id=self._doc_id, content=self._content, metadata=self._metadata, facts=self._facts,
                          directives=tuple(directives))

    def without_directives(self: _TalismanDocument) -> _TalismanDocument:
        return type(self)(doc_id=self._doc_id, content=self._content, metadata=self._metadata, facts=self._facts, directives=None)

    def __eq__(self, other: 'TalismanDocument'):
        if not isinstance(other, TalismanDocument):
            return NotImplemented
        return self._doc_id == other._doc_id and self._content == other._content and other._facts == self._facts \
            and other._metadata == self._metadata and other._directives == self._directives

    def __hash__(self):
        return hash((self._doc_id, self._content, self._metadata, self._facts, self._directives))

    def get_concept_related_concept(self, fact: ConceptFact, link_type_id: Optional[str] = None,
                                    filter_: Callable[[_Fact], bool] = lambda _: True) -> Iterator[ConceptFact]:

        for fact_ in self.filter_facts(RelationFact):
            if link_type_id is not None and fact_.type_id != link_type_id:
                continue
            related_fact = None
            if fact_.value.from_fact == fact:
                related_fact = fact_.value.to_fact

            elif fact_.value.to_fact == fact:
                related_fact = fact_.value.from_fact

            if filter_(related_fact):
                yield related_fact

    def get_value_associated_via_property(self, fact: Union[ConceptFact, RelationFact], property_type_id: Optional[str] = None,
                                          filter_: Callable[[_Fact], bool] = lambda _: True) -> Iterator[ValueFact]:
        for fact_ in self.filter_facts(PropertyFact):
            if property_type_id is not None and fact_.type_id != property_type_id:
                continue
            if fact_.value.from_fact == fact and filter_(fact_.value.to_fact):
                yield fact_.value.to_fact
