from pydantic_settings import BaseSettings, SettingsConfigDict


class ServicesConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BACKEND_SERVICE_")

    # ! Обязателньые переменные
    AUTH_ADDRESS: str
