from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from authlib.integrations.starlette_client import OAuth
from app.db.session import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import User
from app.models.enums import OAuthProvider

router = APIRouter(prefix="/auth", tags=["auth"])

# Initialize Authlib OAuth
oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


async def get_or_create_oauth_user(
        db: AsyncSession,
        provider: OAuthProvider,
        oauth_id: str,
        email: str,
        name: str,
        avatar_url: str
) -> User:
    """Helper function to find an existing user or create a new one during callback."""
    query = select(User).where(User.oauth_provider == provider, User.oauth_id == oauth_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        # Check if email is already taken by another provider
        email_query = select(User).where(User.email == email)
        email_result = await db.execute(email_query)
        if email_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered with a different provider."
            )

        # Create base username from email or name
        base_username = email.split('@')[0] if email else name.replace(" ", "").lower()

        user = User(
            oauth_provider=provider,
            oauth_id=oauth_id,
            email=email,
            username=base_username,  # Note: In production, you'd add logic to handle duplicate usernames
            avatar_url=avatar_url
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user


@router.get("/{provider}/login")
async def oauth_login(provider: str, request: Request):
    """Redirects user to the Google/GitHub consent screen."""
    if provider not in ["google", "github"]:
        raise HTTPException(status_code=404, detail="Provider not supported")

    client = oauth.create_client(provider)
    redirect_uri = request.url_for('oauth_callback', provider=provider)
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/{provider}/callback")
async def oauth_callback(provider: str, request: Request, db: AsyncSession = Depends(get_db)):
    """Handles the callback from Google/GitHub, issues app JWT."""
    if provider not in ["google", "github"]:
        raise HTTPException(status_code=404, detail="Provider not supported")

    client = oauth.create_client(provider)
    try:
        token = await client.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    # Extract user info based on provider
    if provider == "google":
        user_info = token.get('userinfo')
        oauth_id = user_info.get("sub")
        email = user_info.get("email")
        name = user_info.get("name")
        avatar_url = user_info.get("picture")
    elif provider == "github":
        # GitHub requires a separate call to get user profile and emails
        resp = await client.get('user', token=token)
        user_info = resp.json()
        oauth_id = str(user_info.get("id"))
        name = user_info.get("name") or user_info.get("login")
        avatar_url = user_info.get("avatar_url")

        # Fetch GitHub emails
        emails_resp = await client.get('user/emails', token=token)
        emails = emails_resp.json()
        primary_email = next((e['email'] for e in emails if e['primary']), None)
        email = primary_email

    if not oauth_id or not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch required profile info")

    # Get or create user
    oauth_enum = OAuthProvider.GOOGLE if provider == "google" else OAuthProvider.GITHUB
    user = await get_or_create_oauth_user(db, oauth_enum, oauth_id, email, name, avatar_url)

    # Issue our own JWT
    access_token = create_access_token(subject=user.id)

    # In a real frontend scenario, you might redirect to your frontend domain with the token in the URL or set a cookie.
    # For now, we return it as JSON.
    return {"access_token": access_token, "token_type": "bearer"}