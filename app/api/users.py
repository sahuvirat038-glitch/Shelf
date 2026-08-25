import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate, UserPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_me(
        update_data: UserUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(current_user, key, value)

    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.get("/{user_id}", response_model=UserPublic)
async def get_user_profile(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user