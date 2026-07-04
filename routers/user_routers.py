from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db
from utils.password_hashing import hash_password
from auth.authentication import get_current_user

from model import User
from schemas.user_schema import (
    UserUpdate as UserUpdateSchema,
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


# * update user
@user_router.patch("/", response_model=UserResponseSchema)
def update_user(user: UserUpdateSchema, db: Session = Depends(get_db), current_user_id=Depends(get_current_user)):
    existed_user = db.query(User).filter(User.id == current_user_id).one_or_none()

    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existed_user, field, value)
        
    db.commit()
    db.refresh(existed_user)
    return existed_user


# * delete user
@user_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), current_user_id=Depends(get_current_user)):
    existed_user = db.query(User).filter(User.id == current_user_id).one_or_none()
    
    db.delete(existed_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
