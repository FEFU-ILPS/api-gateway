from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth_router, health_router, texts_router, tasks_router, exercises_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # До запуска приложения

    yield

    # После запуска


gateway = FastAPI(lifespan=lifespan)

gateway.include_router(health_router)
gateway.include_router(auth_router)
gateway.include_router(texts_router)
gateway.include_router(tasks_router)
gateway.include_router(exercises_router)

gateway.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Изменить в проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
