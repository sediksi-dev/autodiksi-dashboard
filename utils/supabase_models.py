from pydantic import BaseModel, model_serializer
from typing import Literal, Optional, Any
from enum import Enum


class WebConfigKey(str, Enum):
    auth_username = "auth_username"
    auth_token = "auth_token"
    rewrite_mode = "rewrite_mode"
    post_status = "post_status"
    language = "language"


class SourceWebConfig(BaseModel):
    language: str = ""


class TargetWebConfig(BaseModel):
    auth_username: str = ""
    auth_token: str = ""
    post_status: str = "draft"
    rewrite_mode: str = "default"
    language: str = ""


class WebData(BaseModel):
    id: Optional[int] = None
    url: str
    api_endpoint: str = "wp-json/wp/v2"
    role_key: Literal["source", "target"]
    post_type: str = "posts"

    @model_serializer
    def to_dict(self):
        if self.id is None:
            return {
                "url": self.url,
                "api_endpoint": self.api_endpoint,
                "post_type": self.post_type,
                "role_key": self.role_key,
            }


class WebConfigData(BaseModel):
    id: Optional[int] = None
    key: WebConfigKey
    value: Any
    web_id: int

    @model_serializer
    def to_dict(self):
        if self.id is None:
            return {
                "key": self.key,
                "value": self.value,
                "web_id": self.web_id,
            }


class TaxonomyData(BaseModel):
    id: Optional[int] = None
    term_name: str = "categories"
    taxonomy_id: int
    taxonomy_name: str
    web_id: int

    @model_serializer
    def to_dict(self):
        if self.id is None:
            return {
                "taxonomy_id": self.taxonomy_id,
                "taxonomy_name": self.taxonomy_name,
                "term_name": self.term_name,
                "web_id": self.web_id,
            }


class TaxonomyMappingData(BaseModel):
    id: Optional[int] = None
    source_id: int
    target_id: int

    @model_serializer
    def to_dict(self):
        if self.id is None:
            return {
                "source_id": self.source_id,
                "target_id": self.target_id,
            }
