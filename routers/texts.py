from typing import List

from fastapi import APIRouter, Path

from schemas.texts import TextResponse
from uuid import UUID

router = APIRouter(prefix="/texts")


@router.get("")
def list_texts() -> List[TextResponse]:
    """Возвращает список всех текстов, загруженных в систему."""
    pass


@router.get("/{text_uuid}")
def text_details(text_uuid: UUID = Path(...)):
    """Возвращает полную информацию по конкретному тексту."""
    pass
