from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from database import get_db
from auth.authentication import get_current_user

from model import Blog
from schemas.blog_schema import (
    BlogCreate as BlogCreateSchema,
    BlogResponse as BlogResponseSchema,
    BlogUpdate as BlogUpdateSchema
)

blog_router = APIRouter(prefix="/api/blogs", tags=["Blogs"])


# * get all the blogs
@blog_router.get("/", response_model=list[BlogResponseSchema])
def get_blogs_api(
    db: Session = Depends(get_db), current_user_id=Depends(get_current_user)
):
    return db.query(Blog).all()


# * get all your blogs
@blog_router.get("/individual", response_model=list[BlogResponseSchema])
def get_blogs_individual_api(
    db: Session = Depends(get_db), 
    current_user_id=Depends(get_current_user)
):
    existed_blog = db.query(Blog).filter(Blog.author_id == current_user_id).all()
    return existed_blog


# * get specific blog by blog id
@blog_router.get("/{blog_id}", response_model=BlogResponseSchema)
def get_blog_api(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user_id=Depends(get_current_user),
):
    existed_blog = db.query(Blog).filter(Blog.id == blog_id).one_or_none()
    if not existed_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    return existed_blog


# * create blog
@blog_router.post(
    "/", response_model=BlogResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_post_api(
    blog: BlogCreateSchema,
    db: Session = Depends(get_db),
    current_user_id=Depends(get_current_user),
):
    blog_dict = blog.model_dump()
    blog_dict["author_id"] = current_user_id
    new_blog = Blog(**blog_dict)
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# * update blog
@blog_router.patch("/{post_id}", response_model=BlogResponseSchema)
def update_blog(post_id: int, post: BlogUpdateSchema, db: Session = Depends(get_db), current_user_id=Depends(get_current_user)):
    existed_post = db.query(Blog).filter(Blog.id == post_id).one_or_none()
    
    if not existed_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    if existed_post.author_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform request action")

    update_data = post.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existed_post, field, value)
        
    db.commit()
    db.refresh(existed_post)
    return existed_post


# * delete blog
@blog_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(post_id: int, db: Session = Depends(get_db), current_user_id=Depends(get_current_user)):
    existed_post = db.query(Blog).filter(Blog.id == post_id).one_or_none()
    
    if not existed_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    if existed_post.author_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform request action")
    
    db.delete(existed_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
