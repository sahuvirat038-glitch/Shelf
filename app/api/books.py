from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.book import Book
from app.schemas.book import BookRead, BookCreate
from app.services.book import get_or_create_book

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
    """Browse the shared book catalog."""
    query = select(Book).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific book."""
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book