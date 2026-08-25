import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    cover_image_url: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    cover_image_url: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None

class BookRead(BookBase):
    id: uuid.UUID
    created_by_id: Optional[uuid.UUID] = None
    created_at: datetime
    average_rating: Optional[float] = None
    review_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)