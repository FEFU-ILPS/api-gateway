from fastapi import APIRouter, Path

router = APIRouter("/texts")


@router.get("")
def list_texts():
    """Возвращает список всех текстов, загруженных в систему."""
    pass


@router.get("/{text_uuid}")
def text_details(text_uuid: str = Path(...)):
    """Возвращает полную информацию по конкретному тексту."""
    pass
