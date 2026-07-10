from fastapi import APIRouter, HTTPException, status, Depends, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth.authentication import get_current_user
from sqlalchemy import select, and_, func
from typing import Annotated

from model import Blog
from schemas.blog_schema import (
    BlogCreate as BlogCreateSchema,
    BlogResponse as BlogResponseSchema,
    BlogUpdate as BlogUpdateSchema,
    PaginatedBlogResponse as PaginatedBlogResponseSchema,
)

blog_router = APIRouter(prefix="/api/blogs", tags=["Blogs"])


# * get all the blogs - pagination applied
@blog_router.get("/", response_model=PaginatedBlogResponseSchema)
async def get_blogs_api(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    page: int = 1,
    title: str = "",
    content: str = "",
):

    total_result = await db.execute(select(func.count()).select_from(Blog))
    total = total_result.scalar() or 0

    skip = limit * (page - 1)

    result = await db.execute(
        select(Blog)
        .where(and_(Blog.title.ilike(f"%{title}%"), Blog.content.ilike(f"%{content}%")))
        .order_by(Blog.posted_at.desc())
        .offset(skip)
        .limit(limit)
    )

    blogs = result.scalars().all()
    return PaginatedBlogResponseSchema(
        blogs=[BlogResponseSchema.model_validate(blog) for blog in blogs],
        page=page,
        skip=skip,
        limit=limit,
        has_more=skip + len(blogs) < total,
    )


# * get all your blogs
@blog_router.get("/individual", response_model=list[BlogResponseSchema])
async def get_blogs_individual_api(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    result = await db.execute(select(Blog).where(Blog.author_id == current_user.id))
    return result.scalars().all()


# * get specific blog by blog id
@blog_router.get("/{blog_id}", response_model=BlogResponseSchema)
async def get_blog_api(
    blog_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    existed_blog = result.scalars().one_or_none()

    if not existed_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    return existed_blog


# * create blog
@blog_router.post(
    "/", response_model=BlogResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_post_api(
    blog: BlogCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    blog_dict = blog.model_dump()
    blog_dict["author_id"] = current_user.id
    new_blog = Blog(**blog_dict)

    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog


# * update blog
@blog_router.patch("/{post_id}", response_model=BlogResponseSchema)
async def update_blog_api(
    post_id: int,
    post: BlogUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Blog).where(Blog.id == post_id))
    existed_post = result.scalars().one_or_none()

    if not existed_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    if existed_post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action",
        )

    update_data = post.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existed_post, field, value)

    await db.commit()
    await db.refresh(existed_post)
    return existed_post


# * delete blog
@blog_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_api(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Blog).where(Blog.id == post_id))
    existed_post = result.scalars().one_or_none()

    if not existed_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    if existed_post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action",
        )

    await db.delete(existed_post)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
