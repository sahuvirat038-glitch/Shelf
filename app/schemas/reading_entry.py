from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import ReadingStatus
from app.schemas.book import BookRead

class ReadingEntryBase(BaseModel):
    status: ReadingStatus = ReadingStatus.WANT_TO_READ
    current_page: Optional[int] = Field(0, ge=0)
    rating: Optional[int] = Field(None, ge=1, le=5)
    private_notes: Optional[str] = None

class ReadingEntryCreate(ReadingEntryBase):
    book_id: int

class ReadingEntryUpdate(BaseModel):
    status: Optional[ReadingStatus] = None
    current_page: Optional[int] = Field(None, ge=0)
    rating: Optional[int] = Field(None, ge=1, le=5)
    private_notes: Optional[str] = None

class ReadingEntryRead(ReadingEntryBase):
    id: int
    user_id: int
    book_id: int
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    book: Optional[BookRead] = None

    model_config = ConfigDict(from_attributes=True)