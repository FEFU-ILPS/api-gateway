from pydantic_settings import BaseSettings, SettingsConfigDict


class GraylogConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GATEWAY_GRAYLOG_")

    # ! Обязательные переменные
    HOST: str
    PORT: int

    # * Опциональные переменные
    ENABLE: bool = False
