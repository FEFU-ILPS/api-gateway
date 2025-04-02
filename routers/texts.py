from fastapi import APIRouter

router = APIRouter(prefix="/texts")


@router.get("/")
def get_texts():
    pass


@router.get("/{id}")
def get_text():
    pass
