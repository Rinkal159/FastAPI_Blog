from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteException
from fastapi.responses import JSONResponse

def handlers(app: FastAPI, templates):
    @app.exception_handler(StarletteException)
    def exception_anything(request: Request, exception: StarletteException):
        # back-end response
        if request.url.path.startswith("/api"):
            return JSONResponse(
                status_code=exception.status_code, content={"error": exception.detail}
            )

        # front-end response
        return templates.TemplateResponse(
            request,
            "error.html",
            {"status_code": exception.status_code, "error_message": exception.detail},
            status_code=exception.status_code,
        )


    @app.exception_handler(RequestValidationError)
    def exception_422(request: Request, exception: RequestValidationError):

        # back-end response
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

        # front-end response
        return templates.TemplateResponse(
            request,
            "error.html",
            {
                "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
                "error_message": "Invalid request. Please check your input and try again.",
            },
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    return app