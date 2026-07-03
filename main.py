from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from exception_handling.exception_handlers import handlers
from sqlalchemy.orm import Session
from database import get_db
from auth.authentication import get_current_user

from model import User, Blog

from routers import auth_routers, blog_routers, user_routers

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")


# * FRONT-END
# get all the posts
@app.get("/", include_in_schema=False, name="home")
@app.get("/blogs", include_in_schema=False, name="blogs")
def home(request: Request, db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return templates.TemplateResponse(
        request, "index.html", {"blogs": blogs, "title": "Index"}
    )


# get specific post
@app.get("/blogs/{id}", include_in_schema=False)
def blog(id: int, request: Request, db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    for blog in blogs:
        if blog.id == id:
            return templates.TemplateResponse(
                request, "blog.html", {"blog": blog, "title": blog.title[:50]}
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")


# get all blogs of a user
@app.get("/blogs/individual/{id}")
def get_individual_blogs(request: Request, id: int, db: Session = Depends(get_db)):
    existed_user = db.query(User).filter(User.id == id).one_or_none()

    if not existed_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )

    blogs = db.query(Blog).filter(Blog.author_id == id).all()
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
