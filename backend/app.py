from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routes import health_router
import os
from config import configs


@asynccontextmanager
async def server_lifespan(app: FastAPI):
    # До запуска приложения
    os.makedirs(configs.upload.DIR, exist_ok=True)

    yield

    # После запуска


server = FastAPI(lifespan=server_lifespan)
server.include_router(health_router)
