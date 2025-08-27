import uvicorn
from fastapi import FastAPI

from core.server import server

app: FastAPI = server()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
