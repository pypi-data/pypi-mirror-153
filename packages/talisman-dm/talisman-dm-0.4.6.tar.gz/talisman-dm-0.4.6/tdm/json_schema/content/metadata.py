from typing import Optional

from pydantic import BaseModel

from tdm.abstract.datamodel import NodeType
from tdm.datamodel import TreeDocumentContent


class NodeMetadata(BaseModel):
    node_type: NodeType
    original_text: Optional[str]
    hidden: bool = False

    class Config:
        extra = 'allow'  # any other extra fields will be kept

    def parse(self) -> dict:
        return self.dict()

    @classmethod
    def build(cls, node: TreeDocumentContent) -> 'NodeMetadata':
        return cls.construct(
            node_type=node.type,
            original_text=node.original_node_text if node.original_node_text != node.node_text else None,
            hidden=node.is_hidden
        )
