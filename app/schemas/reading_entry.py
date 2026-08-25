import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import ReadingStatus
from app.schemas.book import BookRead

class ReadingEntryBase(BaseModel):
    book_id: uuid.UUID
    status: ReadingStatus
    current_page: int = Field(0, ge=0)
    total_pages: Optional[int] = Field(None, ge=0)

class ReadingEntryCreate(ReadingEntryBase):
    pass

class ReadingEntryUpdate(BaseModel):
    status: Optional[ReadingStatus] = None
    current_page: Optional[int] = Field(None, ge=0)
    total_pages: Optional[int] = Field(None, ge=0)

class ReadingEntryRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    book_id: uuid.UUID
    status: ReadingStatus
    current_page: int
    total_pages: Optional[int]
    created_at: datetime
    updated_at: datetime
    book: Optional[BookRead] = None

    model_config = ConfigDict(from_attributes=True)