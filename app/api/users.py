from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.reading_entry import ReadingEntry
from app.schemas.user import UserRead, UserUpdate
from app.schemas.reading_entry import ReadingEntryRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get the currently authenticated user's profile."""
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_my_profile(
        update_data: UserUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Update username, bio, or avatar."""
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(current_user, key, value)

    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.get("/{user_id}", response_model=UserRead)
async def get_user_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get a public user profile."""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}/reading-entries", response_model=List[ReadingEntryRead])
async def get_user_reading_entries(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get a user's public reading shelf."""
    query = select(ReadingEntry).where(ReadingEntry.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()