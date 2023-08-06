from abc import abstractmethod
from typing import Optional, Tuple, Type, TypeVar


from pydantic import BaseModel

from .datamodel import AbstractTreeDocumentContent

_AbstractContentModel = TypeVar('_AbstractContentModel', bound='AbstractContentModel')


class AbstractContentModel(BaseModel):
    @abstractmethod
    def to_content(self) -> AbstractTreeDocumentContent:
        pass

    @classmethod
    @abstractmethod
    def build(cls: Type[_AbstractContentModel], doc: AbstractTreeDocumentContent) -> _AbstractContentModel:
        pass


class DocumentMetadataFields(BaseModel):
    title: Optional[str]
    file_name: Optional[str]
    file_type: Optional[str]
    size: Optional[int]
    created_time: Optional[int]
    access_time: Optional[int]
    modified_time: Optional[int]
    publication_date: Optional[int]
    publication_author: Optional[str]
    description: Optional[str]
    parent_uuid: Optional[str]
    url: Optional[str]
    access_level: Optional[str]
    user: Optional[str]
    path: Optional[str]
    trust_level: Optional[float]
    markers: Optional[Tuple[str, ...]]
    related_concept_id: Optional[str]

    class Config:
        extra = 'allow'  # any other extra fields will be kept


class FactMetadataFields(BaseModel):
    created_time: Optional[int]
    modified_time: Optional[int]

    class Config:
        extra = 'allow'  # any other extra fields will be kept
