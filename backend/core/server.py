from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from api import health_router, router
from core.exceptions_listener import init_listeners
from core.middlewares import AuthBackend, AuthenticationMiddleware
from core.security import lifespan


def init_server(app_: FastAPI) -> None:
    app_.include_router(router=health_router)
    app_.include_router(router)


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
