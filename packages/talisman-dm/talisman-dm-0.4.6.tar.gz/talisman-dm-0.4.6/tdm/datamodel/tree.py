from itertools import chain
from typing import Callable, Iterable, Optional, Tuple, TypeVar

from tdm.abstract.datamodel.tree import AbstractTree

_TreeNode = TypeVar('_TreeNode', bound='TreeNode')


class TreeNode(AbstractTree):
    __slots__ = ('_id', '_nodes', '_id2node', '_parent_func')

    def __init__(self: _TreeNode, node_id: str, nodes: Optional[Iterable[_TreeNode]] = None,
                 parent_func: Optional[Callable[[_TreeNode], _TreeNode]] = None):
        self._id = node_id
        self._nodes = tuple(nodes) if nodes is not None else ()

        self._id2node = {id_: child for node in self._nodes for id_, child in node._id2node.items()}
        if self._id in self._id2node or len(self._id2node) != sum((len(node._id2node) for node in self._nodes)):
            raise ValueError("Provided documents have node id collisions")
        self._id2node[self._id] = self

        self._parent_func = parent_func

    @property
    def id(self) -> str:
        return self._id

    @property
    def parent(self: _TreeNode) -> Optional[_TreeNode]:
        return self._parent_func(self) if self._parent_func is not None else None

    @property
    def nodes(self: _TreeNode) -> Tuple[_TreeNode, ...]:
        return tuple(node._with_changes(parent_func=self._parent_func_factory(i)) for i, node in enumerate(self._nodes))

    def node(self: _TreeNode, node_id: str) -> _TreeNode:
        if node_id == self._id:
            return self
        for i, node in enumerate(self._nodes):
            if node_id in node._id2node:
                return node._with_changes(parent_func=self._parent_func_factory(i)).node(node_id)
        raise ValueError(f"Node {self._id} contains no {node_id} node")

    def pruned(self: _TreeNode) -> _TreeNode:
        return self._with_changes(nodes=None)

    def with_nodes(self: _TreeNode, nodes: Iterable[_TreeNode]) -> _TreeNode:
        return self._with_changes(nodes=nodes)

    def as_root(self: _TreeNode) -> _TreeNode:
        return self._with_changes(parent_func=None)

    def equal_structure(self: _TreeNode, other: _TreeNode) -> bool:
        if not isinstance(other, TreeNode):
            return False
        return self._id == other._id and len(self._nodes) == len(other._nodes) and \
            all(s_node.equal_structure(o_node) for s_node, o_node in zip(self._nodes, other._nodes))

    def _get_updated_constructor_params(self, **kwargs) -> dict:
        if 'node_id' in kwargs:
            raise ValueError(f"Can't change node id for node {self._id}")
        return {
            'node_id': self._id,
            'nodes': kwargs.get('nodes', self._nodes),
            'parent_func': kwargs.get('parent_func', self._parent_func)
        }

    def _parent_func_factory(self: _TreeNode, index: int) -> Callable[[_TreeNode], _TreeNode]:
        def parent(node: _TreeNode) -> _TreeNode:
            return self._with_changes(nodes=chain(self._nodes[:index], [node], self._nodes[index + 1:]))
        return parent

    def __hash__(self):
        return hash((self._id, len(self._nodes)))  # check only nodes count not to perform recursively

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return NotImplemented
        return self._id == other._id and self._nodes == other._nodes
