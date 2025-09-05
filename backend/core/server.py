from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api import health_router, router
from core.middlewares import AuthBackend, AuthenticationMiddleware
from core.security import lifespan


def init_server(app_: FastAPI) -> None:
    app_.include_router(router=health_router)
    app_.include_router(router)


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(Exception)
    async def custom_exception_handler(request: Request, exc: Exception):  # type: ignore
        if isinstance(exc, HTTPException):
            code, message = exc.status_code, exc.detail
        else:
            code, message = 500, "Internal Server Error"

        return JSONResponse(status_code=code, content={"error_code": code, "message": message})


def make_middleware() -> List[Middleware]:
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(AuthenticationMiddleware, backend=AuthBackend()),
    ]


def server() -> FastAPI:
    app_ = FastAPI(
        title="VitalMind Insight",
        description="VitalMind Description",
        lifespan=lifespan,
        middleware=make_middleware(),
    )

    init_server(app_)
    init_listeners(app_)
    return app_


app: FastAPI = server()
