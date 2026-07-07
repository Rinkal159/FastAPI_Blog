from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
from utils.password_hashing import hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from auth.authentication import create_token
from fastapi.responses import JSONResponse, RedirectResponse

from model import User
from schemas.user_schema import (
    UserCreate as UserCreateSchema,
    UserResponse as UserResponseSchema,
)

auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])


# * create user
@auth_router.post(
    "/signup",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_api(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    user.email = user.email.lower()
    
    result = await db.execute(select(User).where(func.lower(User.email) == user.email))
    existed_user = result.scalars().one_or_none()

    # user already exists
    if existed_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists. PLease try again with different email.",
        )

    user.password = hash_password(user.password)
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# * login
@auth_router.post("/login")
async def login_api(
    user: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(func.lower(User.email) == user.username.lower()))
    existed_user = result.scalars().one_or_none()

    # user doesn't exist or password is'nt matching
    if not existed_user or not verify_password(user.password, existed_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # creating a token
    token = create_token({"id": existed_user.id})
    
    response = JSONResponse({
        "message" : "Login successful"
    })
    
    # wrapping token inside a cookie and send it to the browser
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600
    )

    return response



# Logout
@auth_router.get("/logout")
def logout_api():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    response.delete_cookie(key="access_token", httponly=True, secure=False, samesite="lax")
    
    return response
