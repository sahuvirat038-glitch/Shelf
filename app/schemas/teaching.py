from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class TeachingBase(BaseModel):
    content: str = Field(..., min_length=1)
    is_public: bool = True

class TeachingCreate(TeachingBase):
    book_id: int

class TeachingUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)
    is_public: Optional[bool] = None

class TeachingRead(TeachingBase):
    id: int
    user_id: int
    book_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)