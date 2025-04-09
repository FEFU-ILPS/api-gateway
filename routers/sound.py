from fastapi import APIRouter, UploadFile, HTTPException
from fastapi import status


router = APIRouter(prefix="/sound")


@router.post("", summary="Загрузить аудиофайл для обработки")
async def upload_audio(uploaded: UploadFile):
    """Получает аудиофайл, выполняет предобработку и извлекает транскрипционную запись."""

    # TODO: Перенести эту логику в Sound Gateway
    extension = uploaded.filename.split(".")[1]
    if extension != "wav":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The service supports the 'wav' extension, not {extension}.",
        )

    if uploaded.content_type != "audio/mpeg":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The service supports the 'wav' extension, not {extension}.",
        )
