from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    cover_url: Optional[str] = None
    genre: Optional[str] = None
    page_count: Optional[int] = Field(None, ge=1)
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    cover_url: Optional[str] = None
    genre: Optional[str] = None
    page_count: Optional[int] = Field(None, ge=1)
    description: Optional[str] = None

class BookRead(BookBase):
    id: int
    created_by_id: Optional[int] = None
    created_at: datetime
    average_rating: Optional[float] = None
    review_count: int = 0

    model_config = ConfigDict(from_attributes=True)