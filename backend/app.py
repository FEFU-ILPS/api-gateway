from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routes import health_router


@asynccontextmanager
async def server_lifespan(app: FastAPI):
    # До запуска прилдожения

    yield

    # После запуска


server = FastAPI(lifespan=server_lifespan)
server.include_router(health_router)
