from pydantic_settings import BaseSettings, SettingsConfigDict
from .services import ServicesConfiguration


class ProjectConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BACKEND_")

    # * Вложенные группы настроек
    services: ServicesConfiguration = ServicesConfiguration()

    # * Опциональные переменные
    DEBUG_MODE: bool = False
    SERVICE_NAME: str = "ilps-backend-api-gateway"


configs = ProjectConfiguration()

__all__ = ("configs",)
