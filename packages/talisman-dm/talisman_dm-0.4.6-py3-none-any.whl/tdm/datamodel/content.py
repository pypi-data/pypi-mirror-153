from copy import deepcopy
from typing import Any, Callable, Dict, Iterable, Optional, Tuple, TypeVar

from intervaltree import IntervalTree

from tdm.abstract.datamodel import AbstractSpan, AbstractTalismanSpan, AbstractTreeDocumentContent, NodeType
from .span import NullableSpan, TalismanSpan
from .tree import TreeNode

_TreeDocumentContent = TypeVar('_TreeDocumentContent', bound='TreeDocumentContent')


class TreeDocumentContent(TreeNode, AbstractTreeDocumentContent):
    __slots__ = (
        '_node_type', '_text', '_markup', '_original_text', '_hidden',
        '_text_references', '_concat_text_len', '_id2span', '_spans_tree'
    )

    DOCUMENT_SEPARATOR = '\n'  # Must be one whitespace character as methods implementations use this condition

    def __init__(self: _TreeDocumentContent, node_id: str, node_type: NodeType, text: str,
                 nodes: Optional[Iterable[_TreeDocumentContent]] = None,
                 markup: Optional[Dict[str, Any]] = None,
                 original_text: Optional[str] = None,
                 hidden: bool = False,
                 parent_func: Optional[Callable[[_TreeDocumentContent], _TreeDocumentContent]] = None):
        TreeNode.__init__(self, node_id, nodes, parent_func)

        self._node_type = node_type
        self._text = text
        self._markup = deepcopy(markup) if markup is not None else {}
        self._original_text = original_text
        self._hidden = hidden

        self._texts_references = [self._text]  # store references instead of concatted string to reduce memory usage
        self._id2span: Dict[str, NullableSpan] = {self._id: NullableSpan(0, len(self._text))}
        pointer = len(self._text) + len(TreeDocumentContent.DOCUMENT_SEPARATOR)
        for node in self._nodes:
            self._texts_references.extend(node._texts_references)
            self._id2span.update({node_id: span.shift(pointer) for node_id, span in node._id2span.items()})
            pointer += node._concat_text_len + len(TreeDocumentContent.DOCUMENT_SEPARATOR)
        self._concat_text_len = pointer - len(TreeDocumentContent.DOCUMENT_SEPARATOR)

        self._spans_tree = IntervalTree.from_tuples((s.start_idx, s.end_idx, n_id) for n_id, s in self._id2span.items() if s.length != 0)

    @property
    def type(self) -> NodeType:
        return self._node_type

    @property
    def text(self) -> str:
        return TreeDocumentContent.DOCUMENT_SEPARATOR.join(self._texts_references)

    def text_for(self, span: AbstractSpan) -> str:
        if not isinstance(span, AbstractTalismanSpan):
            span = self.talisman_span(span)
        if span.node_id == self._id:
            if span.end_idx > len(self._text):
                raise ValueError(f"Tree node {self._id} doesn't contain provided span: {span}")
            return self._text[span.start_idx:span.end_idx]
        if span.node_id not in self._id2node:
            raise ValueError(f"Tree node {self._id} doesn't contain provided span: {span}")
        return self._id2node[span.node_id].text_for(span)

    @property
    def node_text(self) -> str:
        return self._text

    @property
    def original_node_text(self) -> str:
        return self._original_text if self._original_text is not None else self._text

    def with_node_text(self, text: str) -> _TreeDocumentContent:
        return self._with_changes(text=text)

    @property
    def markup(self) -> Dict[str, Any]:
        return deepcopy(self._markup)

    @property
    def is_hidden(self) -> bool:
        return self._hidden

    def hide(self: _TreeDocumentContent) -> _TreeDocumentContent:
        return self._with_changes(hidden=True, nodes=map(lambda node: node.hide(), self._nodes))

    def show(self: _TreeDocumentContent) -> _TreeDocumentContent:
        return self._with_changes(hidden=False, nodes=map(lambda node: node.show(), self._nodes))

    def talisman_spans(self, span: AbstractSpan) -> Tuple[AbstractTalismanSpan, ...]:
        if isinstance(span, AbstractTalismanSpan):
            if span.node_id == self._id:
                self._validate_talisman_span(span)
                return (span, )
            return self._id2node[span.node_id].talisman_spans(span)
        self._validate_span(span)
        overlapped_node_ids = self._spans_tree.overlap(span.start_idx, span.end_idx)
        result = []
        for _, _, node_id in overlapped_node_ids:
            node_span: NullableSpan = self._id2span[node_id]
            span_start = max(span.start_idx, node_span.start_idx) - node_span.start_idx
            span_end = min(span.end_idx, node_span.end_idx) - node_span.start_idx
            result.append(TalismanSpan(node_id, span_start, span_end))
        return tuple(result)

    def span(self, talisman_span: AbstractTalismanSpan) -> NullableSpan:
        self._validate_talisman_span(talisman_span)
        shift = self._id2span[talisman_span.node_id].start_idx
        return NullableSpan(talisman_span.start_idx + shift, talisman_span.end_idx + shift)

    def equal_structure(self: _TreeDocumentContent, other: _TreeDocumentContent) -> bool:
        if not isinstance(other, TreeDocumentContent):
            return False
        return self._node_type is other._node_type and self._text == other._text and super().equal_structure(other)

    def _validate_talisman_span(self, span: AbstractTalismanSpan) -> None:
        if span.node_id not in self._id2node:
            raise ValueError(f"provided span {span} is not contained in doc")
        if span.end_idx > len(self._id2node[span.node_id]._text):
            raise ValueError(f"Document {span.node_id} doesn't contain provided span: {span}")

    def _validate_span(self, span: AbstractSpan):
        if span.end_idx > self._concat_text_len:
            raise ValueError(f"Document {self._id} doesn't contain provided span: {span}")

    def _get_updated_constructor_params(self, **kwargs) -> dict:
        result = super()._get_updated_constructor_params(**kwargs)

        for param in ['node_type', 'original_text']:
            if param in kwargs:
                raise ValueError(f"Can't change {param} for node {self._id}")
        result['node_type'] = self._node_type

        if 'text' in kwargs:
            result['original_text'] = self._original_text if self._original_text is not None else self._text
            result['text'] = kwargs['text']
        else:
            result['original_text'] = self._original_text
            result['text'] = self._text

        result['markup'] = kwargs.get('markup', self._markup)
        result['hidden'] = kwargs.get('hidden', self._hidden)

        return result

    def __eq__(self, other):
        if not isinstance(other, TreeDocumentContent):
            return NotImplemented
        return TreeNode.__eq__(self, other) and self._node_type == other._node_type and self._text == other._text and \
            self._markup == other._markup and self._original_text == other._original_text and self._hidden == other._hidden
