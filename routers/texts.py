from typing import List

from fastapi import APIRouter, Path

from schemas.texts import TextResponse

router = APIRouter(prefix="/texts")


@router.get("")
def list_texts() -> List[TextResponse]:
    """Возвращает список всех текстов, загруженных в систему."""
    pass


@router.get("/{text_uuid}")
def text_details(text_uuid: str = Path(...)):
    """Возвращает полную информацию по конкретному тексту."""
    pass
