from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):  # type: ignore
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": exc.status_code,
                "message": exc.detail,
                "path": str(request.url),
            },
        )

    @app_.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):  # type: ignore
        return JSONResponse(
            status_code=500,
            content={
                "error_code": 500,
                "message": "Internal Server Error",
                "path": str(request.url),
            },
        )
