import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.reading_entry import ReadingEntry
from app.schemas.reading_entry import ReadingEntryCreate, ReadingEntryRead, ReadingEntryUpdate
from app.services.reading_entry import create_or_update_entry

router = APIRouter(prefix="/reading-entries", tags=["reading-entries"])


@router.post("", response_model=ReadingEntryRead)
async def log_reading(
        entry_in: ReadingEntryCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await create_or_update_entry(db, current_user.id, entry_in)


@router.get("/me", response_model=List[ReadingEntryRead])
async def my_library(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = select(ReadingEntry).where(ReadingEntry.user_id == current_user.id)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/{entry_id}", response_model=ReadingEntryRead)
async def update_reading_progress(
        entry_id: uuid.UUID,
        update_data: ReadingEntryUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    entry = await db.get(ReadingEntry, entry_id)
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Entry not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(entry, k, v)

    await db.commit()
    await db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=204)
async def remove_entry(entry_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    entry = await db.get(ReadingEntry, entry_id)
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Entry not found")

    await db.delete(entry)
    await db.commit()
    return None