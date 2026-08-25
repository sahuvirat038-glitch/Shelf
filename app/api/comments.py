import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.comment import Comment
from app.models.club import ClubMembership, ClubRole
from app.schemas.comment import CommentCreate, CommentRead
from app.services.comment import create_comment

router = APIRouter(prefix="/clubs", tags=["comments"])


@router.get("/{club_id}/comments", response_model=List[CommentRead])
async def get_club_comments(club_id: uuid.UUID, book_id: Optional[uuid.UUID] = None,
                            db: AsyncSession = Depends(get_db)):
    query = select(Comment).where(Comment.club_id == club_id)
    if book_id:
        query = query.where(Comment.book_id == book_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/{club_id}/comments", response_model=CommentRead)
async def post_club_comment(
        club_id: uuid.UUID,
        comment_in: CommentCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    mem_query = select(ClubMembership).where(ClubMembership.club_id == club_id,
                                             ClubMembership.user_id == current_user.id)
    mem_result = await db.execute(mem_query)
    if not mem_result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Must be a member to comment")

    return await create_comment(db, current_user.id, club_id, comment_in)


@router.delete("/comments/{comment_id}", status_code=204)
async def delete_club_comment(comment_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                              current_user: User = Depends(get_current_user)):
    comment = await db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        owner_query = select(ClubMembership).where(
            ClubMembership.club_id == comment.club_id,
            ClubMembership.user_id == current_user.id,
            ClubMembership.role == ClubRole.OWNER
        )
        owner_result = await db.execute(owner_query)
        if not owner_result.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    await db.delete(comment)
    await db.commit()
    return None