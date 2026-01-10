from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from ...database import get_session
from ...models.user import User
from ...services.auth_service import get_password_hash, verify_password, create_access_token
from typing import Optional

router = APIRouter()

# Schema definitions
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime
    updated_at: datetime

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# Route handlers
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, session: AsyncSession = Depends(get_session)):
    # Check if user already exists
    statement = select(User).where(User.email == user_data.email)
    result = await session.execute(statement)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password)
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.post("/login", response_model=LoginResponse)
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    # Authenticate user
    statement = select(User).where(User.email == user_data.email)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 3600 * 24 # 24 hours
    }
