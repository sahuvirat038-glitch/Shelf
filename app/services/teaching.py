from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.teaching import Teaching
from app.schemas.teaching import TeachingCreate, TeachingUpdate


async def create_teaching(db: AsyncSession, user_id: int, teaching_in: TeachingCreate) -> Teaching:
    new_teaching = Teaching(
        user_id=user_id,
        book_id=teaching_in.book_id,
        content=teaching_in.content,
        is_public=teaching_in.is_public
    )
    db.add(new_teaching)
    await db.commit()
    await db.refresh(new_teaching)
    return new_teaching


async def update_teaching(db: AsyncSession, teaching: Teaching, update_data: TeachingUpdate) -> Teaching:
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(teaching, field, value)

    await db.commit()
    await db.refresh(teaching)
    return teaching