from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BACKEND_")

    # Опциональные переменные
    DEBUG_MODE: bool = False


configs = Settings()

__all__ = ("configs",)
