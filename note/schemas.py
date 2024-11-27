from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(min_length=1, max_length=64)


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoteBase(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1)
    memo_date: str = Field(min_length=8, max_length=8)


class NoteCreate(NoteBase):
    tags: Optional[List[str]] = Field(default=[], min_items=0)


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=64)
    content: Optional[str] = Field(None, min_length=1)
    memo_date: Optional[str] = Field(None, min_length=8, max_length=8)
    tags: Optional[List[str]] = Field(None, min_items=0)


class NoteResponse(NoteBase):
    id: str
    user_id: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoteList(BaseModel):
    total_count: int
    page: int
    items_per_page: int
    notes: List[NoteResponse]
