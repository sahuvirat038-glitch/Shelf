from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.review import Review
from app.schemas.review import ReviewCreate


async def create_review(db: AsyncSession, user_id: int, review_in: ReviewCreate) -> Review:
    # Ensure user hasn't already reviewed this book
    query = select(Review).where(
        Review.user_id == user_id,
        Review.book_id == review_in.book_id
    )
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="You have already reviewed this book.")

    new_review = Review(
        user_id=user_id,
        book_id=review_in.book_id,
        rating=review_in.rating,
        body=review_in.content
    )

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review