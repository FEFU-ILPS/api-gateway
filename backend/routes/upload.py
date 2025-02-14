from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Response, HTTPException
from config import configs
import aiofiles
import os

router = APIRouter()


def save_file(file):
    file_path = os.path.join(configs.upload.DIR, file.filename)
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    background: BackgroundTasks = BackgroundTasks(),
    response: Response = Response(),
):
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Файл должен быть в формате .wav")

    # Сохраняем временный файл
    background.add_task(save_file, file=file)

    response.status_code = 200
    return {"status": "Файл сохранён."}
