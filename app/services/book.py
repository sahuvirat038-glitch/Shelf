import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.book import Book
from app.schemas.book import BookCreate

async def get_or_create_book(db: AsyncSession, book_in: BookCreate, user_id: uuid.UUID) -> Book:
    # Check for case-insensitive duplicate
    query = select(Book).where(
        func.lower(Book.title) == book_in.title.lower(),
        func.lower(Book.author) == book_in.author.lower()
    )
    result = await db.execute(query)
    existing_book = result.scalar_one_or_none()

    if existing_book:
        return existing_book

    # Create new if it doesn't exist
    new_book = Book(
        title=book_in.title,
        author=book_in.author,
        cover_url=book_in.cover_url,
        genre=book_in.genre,
        page_count=book_in.page_count,
        description=book_in.description,
        created_by_id=user_id
    )
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

async def get_book_by_id(db: AsyncSession, book_id: int) -> Book | None:
    return await db.get(Book, book_id)