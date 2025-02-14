from pydantic_settings import BaseSettings, SettingsConfigDict


class UploadSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BACKEND_UPLOAD_")

    # Опциональные переменные
    DIR: str = "uploads"
