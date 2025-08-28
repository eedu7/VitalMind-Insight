import uvicorn

from core.config import settings

if __name__ == "__main__":
    uvicorn.run("core.server:app", port=settings.PORT, reload=True)
