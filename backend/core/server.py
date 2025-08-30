from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from api import health_router, router
from core.middlewares import AuthBackend, AuthenticationMiddleware


def init_server(app_: FastAPI) -> None:
    app_.include_router(router=health_router)
    app_.include_router(router)


def make_middleware() -> List[Middleware]:
    return [
        Middleware(AuthenticationMiddleware, backend=AuthBackend()),
        Middleware(
            CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
        ),
    ]


def server() -> FastAPI:
    app_ = FastAPI(title="VitalMind Insight", description="VitalMind Description", middleware=make_middleware())

    init_server(app_)

    return app_


app: FastAPI = server()
