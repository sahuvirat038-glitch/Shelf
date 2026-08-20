from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.book import Book
from app.schemas.book import BookRead, BookCreate
from app.services.book import get_or_create_book
from app.models.review import Review

router = APIRouter(prefix="/books", tags=["books"])

@router.post("", response_model=BookRead)
async def add_book(
    book_in: BookCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new book to the shared catalog (avoids duplicates)."""
    return await get_or_create_book(db, book_in, current_user.id)


@router.get("", response_model=List[BookRead])
async def list_books(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Browse the shared book catalog with stats."""
    query = (
        select(Book, func.coalesce(func.avg(Review.rating), 0.0), func.count(Review.id))
        .outerjoin(Review, Review.book_id == Book.id)
        .group_by(Book.id)
        .offset(skip).limit(limit)
    )
    results = await db.execute(query)

    books = []
    for book, avg, count in results.all():
        book.average_rating = round(float(avg), 1) if count > 0 else None
        book.review_count = count
        books.append(book)
    return books


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific book with stats."""
    query = (
        select(Book, func.coalesce(func.avg(Review.rating), 0.0), func.count(Review.id))
        .outerjoin(Review, Review.book_id == Book.id)
        .where(Book.id == book_id)
        .group_by(Book.id)
    )
    result = await db.execute(query)
    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Book not found")

    book, avg, count = row
    book.average_rating = round(float(avg), 1) if count > 0 else None
    book.review_count = count
    return book