from typing import AsyncGenerator

import httpx
from fastapi import HTTPException

from configs import configs


async def sse_proxy(task_id: str, user_id: str) -> AsyncGenerator[str, None]:
    """Асинхронный генератор для проксирования SSE-стрима.

    Args:
        task_id (str): ID задачи для подключения к стриму.
        user_id (str): ID пользователя, создавшего задачу.

    Yields:
        str: JSON-строка с событием SSE.
    """
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream(
                "POST",
                f"{configs.services.manager.URL}/{task_id}/stream",
                json={"user_id": user_id},
                timeout=100,
            ) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        yield line[5:].strip()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )
