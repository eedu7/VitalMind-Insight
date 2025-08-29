from fastapi import FastAPI

from api import health_router, router


def init_server(app_: FastAPI) -> None:
    app_.include_router(router=health_router)
    app_.include_router(router)


def server() -> FastAPI:
    app_ = FastAPI(
        title="VitalMind Insight",
        description="VitalMind Description",
    )

    init_server(app_)

    return app_


app: FastAPI = server()
