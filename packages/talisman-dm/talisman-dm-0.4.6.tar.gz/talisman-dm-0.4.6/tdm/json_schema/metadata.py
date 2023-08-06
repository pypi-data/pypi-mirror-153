from typing import Any, Dict

from pydantic import BaseModel

from tdm.abstract.json_schema import DocumentMetadataFields, FactMetadataFields


class MetadataModel(BaseModel):

    def to_metadata(self) -> Dict[str, Any]:
        return self.dict(exclude_none=True)


class DocumentMetadataModel(DocumentMetadataFields, MetadataModel):
    pass


class FactMetadataModel(FactMetadataFields, MetadataModel):
    pass
