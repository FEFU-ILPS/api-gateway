from pydantic_settings import BaseSettings, SettingsConfigDict
from .upload import UploadSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BACKEND_")

    upload = UploadSettings()

    # Опциональные переменные
    DEBUG_MODE: bool = False


configs = Settings()

__all__ = ("configs",)
