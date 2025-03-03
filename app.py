from contextlib import asynccontextmanager

from fastapi import FastAPI

from routers import health_router, auth_router, audio_router, text_router


@asynccontextmanager
async def server_lifespan(app: FastAPI):
    # До запуска приложения

    yield

    # После запуска


app = FastAPI(lifespan=server_lifespan)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(audio_router)
app.include_router(text_router)
