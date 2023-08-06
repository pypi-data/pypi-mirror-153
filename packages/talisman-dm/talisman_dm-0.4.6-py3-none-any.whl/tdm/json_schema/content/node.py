from typing import Optional, Tuple

from tdm.abstract.json_schema import AbstractContentModel
from tdm.datamodel import TreeDocumentContent
from tdm.json_schema.content.markup import NodeMarkup
from tdm.json_schema.content.metadata import NodeMetadata


class TreeDocumentContentModel(AbstractContentModel):
    id: str
    metadata: NodeMetadata
    text: str
    nodes: Optional[Tuple['TreeDocumentContentModel', ...]]
    markup: NodeMarkup = NodeMarkup()

    def to_content(self) -> TreeDocumentContent:
        return self.markup.to_doc(
            node_id=self.id,
            text=self.text,
            nodes=(node.to_content() for node in self.nodes) if self.nodes is not None else None,
            **self.metadata.parse()
        )

    @classmethod
    def build(cls, doc: TreeDocumentContent) -> 'TreeDocumentContentModel':
        metadata_type = cls.__fields__['metadata'].type_
        markup_type = cls.__fields__['markup'].type_

        return TreeDocumentContentModel(
            id=doc.id,
            metadata=metadata_type.build(doc),
            text=doc.node_text,
            nodes=tuple(cls.build(node) for node in doc.nodes) if doc.nodes is not None else None,
            markup=markup_type.build(doc)
        )


TreeDocumentContentModel.update_forward_refs()
