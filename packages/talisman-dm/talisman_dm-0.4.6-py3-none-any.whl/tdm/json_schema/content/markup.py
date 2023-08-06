from typing import Iterable, Optional

from pydantic import BaseModel

from tdm.datamodel import TreeDocumentContent


class NodeMarkup(BaseModel):
    class Config:
        extra = 'allow'  # any other extra fields will be kept

    def to_doc(self, node_id: str, text: str, nodes: Optional[Iterable[TreeDocumentContent]], **kwargs) -> TreeDocumentContent:
        return TreeDocumentContent(
            node_id=node_id,
            text=text,
            nodes=nodes,
            markup=self.dict(),
            **kwargs
        )

    @classmethod
    def build(cls, doc: TreeDocumentContent) -> 'NodeMarkup':
        return cls.construct(**doc.markup)
