from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

async def create_comment(db: AsyncSession, user_id: int, club_id: int, comment_in: CommentCreate) -> Comment:
    new_comment = Comment(
        club_id=club_id,
        user_id=user_id,
        book_id=comment_in.book_id,
        content=comment_in.content,
        is_spoiler=comment_in.is_spoiler
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment