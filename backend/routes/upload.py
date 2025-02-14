from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Response, HTTPException
from pydub import AudioSegment
import aiofiles
import requests
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

PROCESSING_SERVER_URL = "https://example.com/process_audio"


def send_to_llm(file_path: str):
    print(f"Отправка в LLM: {file_path}")
    files = {"file": open(file_path, "rb")}
    response = requests.post("https://example.com/llm", files=files)
    if response.status_code == 200:
        print("Файл успешно отправлен в LLM")
    else:
        print("Ошибка отправки в LLM")


def send_to_processing_server(file_path: str) -> str:
    print(f"Отправка на сервер обработки: {file_path}")
    files = {"file": open(file_path, "rb")}
    response = requests.post(PROCESSING_SERVER_URL, files=files)

    if response.status_code == 200:
        processed_file_path = os.path.join(UPLOAD_DIR, f"processed_{os.path.basename(file_path)}")
        with open(processed_file_path, "wb") as f:
            f.write(response.content)
        print("Файл успешно обработан и сохранён.")
        return processed_file_path
    else:
        raise HTTPException(status_code=500, detail="Ошибка обработки на сервере")


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    background: BackgroundTasks = BackgroundTasks(),
    response: Response = Response(),
):
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Файл должен быть в формате .wav")

    # Сохраняем временный файл
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    audio = AudioSegment.from_wav(file_path)
    sample_rate = audio.frame_rate
    channels = audio.channels
    print(f"Частота дискретизации: {sample_rate} Гц, Каналы: {channels}")

    if sample_rate == 16000 and channels == 1:
        background.add_task(send_to_llm, file_path)
        response.status_code = 200
        return {"status": "Файл отправлен в LLM на обработку"}

    else:
        try:
            processed_file = send_to_processing_server(file_path)
            background.add_task(send_to_llm, processed_file)
            response.status_code = 202
            return {"status": "Файл обработан и отправлен в LLM"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
