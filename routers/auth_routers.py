from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from utils.password_hashing import hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from auth.authentication import create_token

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
def create_user_api(user: UserCreateSchema, db: Session = Depends(get_db)):
    existed_user = db.query(User).filter(User.email == user.email).one_or_none()

    # user already exists
    if existed_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists. PLease try again with different email.",
        )

    user.password = hash_password(user.password)
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# * login
@auth_router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existed_user = db.query(User).filter(User.email == user.username).one_or_none()

    # user doesn't exist or password is'nt matching
    if not existed_user or not verify_password(user.password, existed_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # creating a token
    token = create_token({"id": existed_user.id})

    return {"access_token": token, "token_type": "bearer"}
