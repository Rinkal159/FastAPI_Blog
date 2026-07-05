from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from exception_handling.exception_handlers import handlers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from auth.authentication import get_current_user
from model import lifespan

from model import User, Blog
from routers import auth_routers, blog_routers, user_routers

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")


# * FRONT-END
# get all the posts
@app.get("/", include_in_schema=False, name="home")
@app.get("/blogs", include_in_schema=False, name="blogs")
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog))
    blogs = result.scalars().all()
    return templates.TemplateResponse(
        request, "index.html", {"blogs": blogs, "title": "Index"}
    )


# get specific post
@app.get("/blogs/{id}", include_in_schema=False)
async def blog(id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.id == id))
    existed_blog = result.scalars().one_or_none()

    if not existed_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    return templates.TemplateResponse(
        request, "blog.html", {"blog": existed_blog, "title": existed_blog.title[:50]}
    )


# get all blogs of a user
@app.get("/blogs/individual/{id}")
async def get_individual_blogs(
    request: Request, id: int, db: AsyncSession = Depends(get_db)
):
    result_user = await db.execute(select(User).where(User.id == id))
    existed_user = result_user.scalars().one_or_none()

    if not existed_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )

    result_blogs = await db.execute(select(Blog).where(Blog.author_id == id))
    blogs = result_blogs.scalars().all()

    name = blogs[0].author.name
    return templates.TemplateResponse(
        request,
        "individual_blogs.html",
        {"blogs": blogs, "name": name, "title": f"Posts by {name[:50]}"},
    )


# * BACK-END
app.include_router(auth_routers.auth_router)
app.include_router(user_routers.user_router)
app.include_router(blog_routers.blog_router)


# * Exception handling
handlers(app, templates)
