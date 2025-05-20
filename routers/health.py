import datetime
import platform
import socket

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from service_logging import logger

router = APIRouter(prefix="/health")


@router.get(path="", summary="Проверка состояния", tags=["Health"])
async def health_check() -> JSONResponse:
    """Подтверждает работоспособность сервиса, отправляя данные о текущей хост-системе."""

    logger.info("Checking the service health...")
    try:
        health_status = {
            "status": "healthy",
            "system": {
                "hostname": socket.gethostname(),
                "os": platform.system(),
                "os_version": platform.version(),
            },
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

        logger.success("Service health OK.")
        return JSONResponse(content=health_status)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
