from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/health")
async def check_health(response: Response):
    response.status_code = 200
    response.headers["X-Health-Check"] = "Passed"
    return {"status": "ok"}
