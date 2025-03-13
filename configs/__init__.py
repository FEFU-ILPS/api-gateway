from pydantic_settings import BaseSettings, SettingsConfigDict
from .services import ServicesConfiguration


class ProjectConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BACKEND_")

    # * Вложенные группы настроек
    service: ServicesConfiguration = ServicesConfiguration()

    # * Опциональные переменные
    DEBUG_MODE: bool = False


configs = ProjectConfiguration()

__all__ = ("configs",)
