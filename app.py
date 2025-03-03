from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config import configs
from routers import audio_router, auth_router, health_router, text_router


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


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8061,
        reload=configs.DEBUG_MODE,
        use_colors=True,
        proxy_headers=True,
    )
