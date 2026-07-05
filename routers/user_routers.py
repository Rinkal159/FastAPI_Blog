from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from utils.password_hashing import hash_password
from auth.authentication import get_current_user
from sqlalchemy import select

from model import User
from schemas.user_schema import (
    UserUpdate as UserUpdateSchema,
    UserResponse as UserResponseSchema,
)

user_router = APIRouter(prefix="/api/users", tags=["Users"])


@user_router.get("/", response_model=UserResponseSchema)
async def get_user_api(
    db: AsyncSession = Depends(get_db), current_user_id=Depends(get_current_user)
):
    result = await db.execute(select(User).where(User.id == current_user_id))
    existed_user = result.scalars().one_or_none()

    if not existed_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return existed_user


# * update user
@user_router.patch("/", response_model=UserResponseSchema)
async def update_user(
    user: UserUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user_id=Depends(get_current_user),
):
    result = await db.execute(select(User).where(User.id == current_user_id))
    existed_user = result.scalars().one_or_none()

    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existed_user, field, value)

    await db.commit()
    await db.refresh(existed_user)
    return existed_user


# * delete user
@user_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: AsyncSession = Depends(get_db), current_user_id=Depends(get_current_user)
):
    result = await db.execute(select(User).where(User.id == current_user_id))
    existed_user = result.scalars().one_or_none()

    await db.delete(existed_user)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
