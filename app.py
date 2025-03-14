from contextlib import asynccontextmanager

from fastapi import FastAPI

from routers import auth_router, health_router


@asynccontextmanager
async def server_lifespan(_: FastAPI):
    # До запуска приложения

    yield

    # После запуска


gateway = FastAPI(lifespan=server_lifespan)
gateway.include_router(health_router)
gateway.include_router(auth_router)
