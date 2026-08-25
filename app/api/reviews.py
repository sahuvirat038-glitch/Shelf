import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate
from app.services.review import create_review

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("", response_model=ReviewRead)
async def post_review(
        review_in: ReviewCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await create_review(db, current_user.id, review_in)


@router.patch("/{review_id}", response_model=ReviewRead)
async def edit_review(
        review_id: uuid.UUID,
        update_data: ReviewUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    review = await db.get(Review, review_id)
    if not review or review.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Review not found or not yours")

    update_dict = update_data.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(review, k, v)

    await db.commit()
    await db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=204)
async def delete_review(review_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    review = await db.get(Review, review_id)
    if not review or review.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Review not found")

    await db.delete(review)
    await db.commit()
    return None