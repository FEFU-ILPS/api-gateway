from fastapi import APIRouter, File, UploadFile
from uuid import UUID

router = APIRouter("/audio")


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)) -> UUID:
    """Переводит речь, которая находится на загружаемом аудиофайле в транскрипцию.
    Результат сохраняется в БД. Возвращает UUID задачи расшифровки.
    """
    pass
