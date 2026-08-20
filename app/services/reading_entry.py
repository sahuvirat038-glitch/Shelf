from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.reading_entry import ReadingEntry
from app.models.enums import ReadingStatus
from app.schemas.reading_entry import ReadingEntryCreate, ReadingEntryUpdate


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


async def add_book_to_shelf(db: AsyncSession, user_id: int, entry_in: ReadingEntryCreate) -> ReadingEntry:
    # Check if entry already exists
    query = select(ReadingEntry).where(
        ReadingEntry.user_id == user_id,
        ReadingEntry.book_id == entry_in.book_id
    )
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Book is already on your shelf.")

    new_entry = ReadingEntry(
        user_id=user_id,
        book_id=entry_in.book_id,
        status=entry_in.status,
        current_page=entry_in.current_page,
        rating=entry_in.rating,
        private_notes=entry_in.private_notes
    )

    # Auto-set timestamps based on initial status
    if entry_in.status == ReadingStatus.CURRENTLY_READING:
        new_entry.started_at = utc_now()
    elif entry_in.status == ReadingStatus.FINISHED:
        new_entry.started_at = utc_now()
        new_entry.finished_at = utc_now()

    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry


async def update_reading_entry(db: AsyncSession, entry: ReadingEntry, update_data: ReadingEntryUpdate) -> ReadingEntry:
    old_status = entry.status

    # Apply updates
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(entry, field, value)

    # State machine logic for timestamps
    new_status = entry.status
    if old_status != new_status:
        if new_status == ReadingStatus.CURRENTLY_READING and not entry.started_at:
            entry.started_at = utc_now()
        elif new_status == ReadingStatus.FINISHED:
            if not entry.started_at:
                entry.started_at = utc_now()
            entry.finished_at = utc_now()

    await db.commit()
    await db.refresh(entry)
    return entry