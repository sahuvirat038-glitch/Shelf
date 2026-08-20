from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import decode_access_token
from app.models.user import User

# We use OAuth2PasswordBearer just to tell FastAPI's swagger UI where to pass the token
# Since we are doing OAuth callbacks, we don't strictly have a token URL, but this enables the "Authorize" button in docs.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = await db.get(User, int(user_id))
    if user is None:
        raise credentials_exception

    return user