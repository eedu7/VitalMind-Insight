from fastapi import FastAPI

from api import router


def init_router(app_: FastAPI) -> None:
    app_.include_router(router)


def create_app() -> FastAPI:
    app_ = FastAPI(title="Large Language Model", description="Backend for VitalMind Insight")
    init_router(app_)
    return app_


app = create_app()
