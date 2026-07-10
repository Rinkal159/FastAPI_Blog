from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from utils.password_hashing import hash_password
from auth.authentication import get_current_user
from sqlalchemy import select
from utils.password_hashing import hash_password, verify_password
from utils.encrypt_profile_picture_name import encrypt
import os
import shutil

from model import User
from schemas.user_schema import (
    UserUpdate as UserUpdateSchema,
    UserResponse as UserResponseSchema,
    UserPassword as UserPasswordSchema
)

user_router = APIRouter(prefix="/api/users", tags=["Users"])

#* get user
@user_router.get("/", response_model=UserResponseSchema)
async def get_user_api(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    return current_user


# * update user
@user_router.patch("/", response_model=UserResponseSchema)
async def update_user_api(
    user: UserUpdateSchema = Depends(UserUpdateSchema.as_form),
    profilePicture: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    
    if profilePicture:
        if profilePicture.filename:
            print("PROFILE PICTURE: ", profilePicture)
            filename = encrypt(profilePicture.filename)
            
            if (current_user.profile_picture):
                # remove existing picture
                path = os.path.join("media/profile_pictures", current_user.profile_picture)
                
                if (os.path.exists(path)):
                    os.remove(path)
                    
                    
            # save the picture in media
            with open(f"media/profile_pictures/{filename}", "wb") as buffer:
                shutil.copyfileobj(profilePicture.file, buffer)
            
            # save the filname in database
            current_user.profile_picture = filename
                
                

    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    await db.commit()
    await db.refresh(current_user)
    return current_user


# * delete user
@user_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_api(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    await db.delete(current_user)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#* change password
@user_router.patch("/password", response_model=UserResponseSchema)
async def update_password_api(password: UserPasswordSchema, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    
    if not verify_password(password.current_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Current password is incorrect")
    
    current_user.password = hash_password(password.new_password)
    await db.commit()
    await db.refresh(current_user)
    return current_user
    
    