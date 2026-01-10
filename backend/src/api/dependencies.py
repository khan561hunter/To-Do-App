from fastapi import Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session
from ..models.user import User
from ..middleware.auth_middleware import get_token_claims
from uuid import UUID

async def get_current_user(
    claims: dict = Depends(get_token_claims),
    session: AsyncSession = Depends(get_session)
) -> User:
    user_id = claims.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject claim",
        )

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format in token",
        )

    statement = select(User).where(User.id == user_uuid)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user
