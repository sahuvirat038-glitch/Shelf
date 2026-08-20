from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import ClubRole
from app.schemas.book import BookRead
from app.schemas.user import UserPublic

class ClubBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    cover_url: Optional[str] = None
    is_public: bool = True

class ClubCreate(ClubBase):
    current_book_id: Optional[int] = None

class ClubUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    is_public: Optional[bool] = None
    current_book_id: Optional[int] = None

class ClubRead(ClubBase):
    id: int
    owner_id: int
    current_book_id: Optional[int] = None
    created_at: datetime
    current_book: Optional[BookRead] = None
    member_count: int = 0

    model_config = ConfigDict(from_attributes=True)

class ClubMembershipRead(BaseModel):
    id: int
    club_id: int
    user_id: int
    role: ClubRole
    joined_at: datetime
    user: Optional[UserPublic] = None

    model_config = ConfigDict(from_attributes=True)