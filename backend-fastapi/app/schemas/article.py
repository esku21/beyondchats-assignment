from pydantic import BaseModel
from typing import Optional, List

class Citation(BaseModel):
    title: Optional[str] = None
    url: str

class ArticleCreate(BaseModel):
    title: str
    url: Optional[str] = None
    content_html: Optional[str] = None
    content_text: Optional[str] = None
    is_updated_version: bool = False
    origin_id: Optional[int] = None
    citations: Optional[List[Citation]] = None

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    content_html: Optional[str] = None
    content_text: Optional[str] = None
    is_updated_version: Optional[bool] = None
    origin_id: Optional[int] = None
    citations: Optional[List[Citation]] = None

class ArticleOut(BaseModel):
    id: int
    title: str
    url: Optional[str]
    content_html: Optional[str]
    content_text: Optional[str]
    is_updated_version: bool
    origin_id: Optional[int]
    citations: Optional[List[Citation]]

    class Config:
        from_attributes = True
