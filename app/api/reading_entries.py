from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.reading_entry import ReadingEntry
from app.schemas.reading_entry import ReadingEntryCreate, ReadingEntryRead, ReadingEntryUpdate
from app.services.reading_entry import add_book_to_shelf, update_reading_entry

router = APIRouter(prefix="/reading-entries", tags=["reading_entries"])


@router.post("", response_model=ReadingEntryRead)
async def create_reading_entry(
        entry_in: ReadingEntryCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Add a book to your personal shelf."""
    return await add_book_to_shelf(db, current_user.id, entry_in)


@router.get("/me", response_model=List[ReadingEntryRead])
async def get_my_shelf(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get your own complete reading shelf."""
    query = select(ReadingEntry).where(ReadingEntry.user_id == current_user.id)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/{entry_id}", response_model=ReadingEntryRead)
async def patch_reading_entry(
        entry_id: int,
        update_data: ReadingEntryUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Update status, current page, or rating of an entry on your shelf."""
    entry = await db.get(ReadingEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    if entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this entry")

    return await update_reading_entry(db, entry, update_data)


@router.delete("/{entry_id}", status_code=204)
async def delete_reading_entry(
        entry_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Remove a book entirely from your shelf."""
    entry = await db.get(ReadingEntry, entry_id)
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Entry not found")

    await db.delete(entry)
    await db.commit()
    return None