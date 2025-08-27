from fastapi import FastAPI

from api import router, system_router


def init_server(app_: FastAPI) -> None:
    app_.include_router(router=system_router)
    app_.include_router(router)


def server() -> FastAPI:
    app_ = FastAPI(
        title="VitalMind Insight",
        description="VitalMind Description",
    )

    init_server(app_)

    return app_
