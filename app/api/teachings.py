import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.teaching import Teaching
from app.schemas.teaching import TeachingCreate, TeachingRead, TeachingUpdate
from app.services.teaching import create_teaching, update_teaching

router = APIRouter(prefix="/teachings", tags=["teachings"])


@router.post("", response_model=TeachingRead)
async def post_teaching(
        teaching_in: TeachingCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await create_teaching(db, current_user.id, teaching_in)


@router.get("/me", response_model=List[TeachingRead])
async def my_teachings(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = select(Teaching).where(Teaching.user_id == current_user.id)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/{teaching_id}", response_model=TeachingRead)
async def edit_teaching(
        teaching_id: uuid.UUID,
        update_data: TeachingUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    teaching = await db.get(Teaching, teaching_id)
    if not teaching or teaching.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Teaching not found")
    return await update_teaching(db, teaching, update_data)


@router.delete("/{teaching_id}", status_code=204)
async def delete_teaching(teaching_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    teaching = await db.get(Teaching, teaching_id)
    if not teaching or teaching.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Teaching not found")

    await db.delete(teaching)
    await db.commit()
    return None