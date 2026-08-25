import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import ClubRole
from app.schemas.user import UserPublic

class ClubBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_public: bool = True

class ClubCreate(ClubBase):
    pass

class ClubUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_public: Optional[bool] = None
    current_book_id: Optional[uuid.UUID] = None

class ClubRead(ClubBase):
    id: uuid.UUID
    created_at: datetime
    current_book_id: Optional[uuid.UUID] = None
    member_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)

class ClubMembershipRead(BaseModel):
    id: uuid.UUID
    club_id: uuid.UUID
    user_id: uuid.UUID
    role: ClubRole
    joined_at: datetime
    user: Optional[UserPublic] = None

    model_config = ConfigDict(from_attributes=True)