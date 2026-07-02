from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime

from schemas.blog_schema import BlogResponse as BlogResponseSchema

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


blogs = [
    {
        "id": 1,
        "title": "First Blog of Rinkal",
        "content": "Content of first blog",
        "author": "Rinkal Singapuri",
        "posted_at": datetime.now().date(),
    },
    {
        "id": 2,
        "title": "First Blog of Krina",
        "content": "Content of first blog",
        "author": "Krina Singapuri",
        "posted_at": datetime.now().date(),
    },
]


# * FRONT-END
@app.get("/", include_in_schema=False, name="home")
@app.get("/blogs", include_in_schema=False, name="blogs")
def home(request: Request):
    return templates.TemplateResponse(
        request, "index.html", {"blogs": blogs, "title": "Index"}
    )


@app.get("/blogs/{id}", include_in_schema=False)
def blog(id: int, request: Request):
    for blog in blogs:
        if blog["id"] == id:
            return templates.TemplateResponse(request, "blog.html", {"blog": blog})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")


# * BACK-END
# ^ home
@app.get("/api/blogs", response_model=list[BlogResponseSchema])
def get_blogs_api():
    return blogs


# ^ blog
@app.get("/api/blogs/{id}", response_model=BlogResponseSchema)
def get_blog_api(id: int):
    for blog in blogs:
        if blog["id"] == id:
            return blog
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")


# * Exception handling
@app.exception_handler(StarletteException)
def exception_anything(request: Request, exception: StarletteException):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code, content={"error": exception.detail}
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {"status_code": exception.status_code, "error_message": exception.detail},
        status_code=exception.status_code
    )


@app.exception_handler(RequestValidationError)
def exception_422(request: Request, exception: RequestValidationError):

    if request.url.path.startswith("/api"):
        errors = []

        for error in exception.errors():
            individual = {
                "field": error.get("loc")[1],
                "error_message": error.get("msg"),
            }
            errors.append(individual)

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"error": errors}
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "error_message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
