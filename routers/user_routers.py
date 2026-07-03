from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from utils.password_hashing import hash_password
from auth.authentication import get_current_user

from model import User
from schemas.user_schema import (
    UserCreate as UserCreateSchema,
    UserResponse as UserResponseSchema,
)

user_router = APIRouter(prefix="/api/users", tags=["Users"])


@user_router.get("/", response_model=UserResponseSchema)
def get_user_api(
    db: Session = Depends(get_db), current_user_id=Depends(get_current_user)
):
    existed_user = db.query(User).filter(User.id == current_user_id).one_or_none()

    if not existed_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return existed_user
