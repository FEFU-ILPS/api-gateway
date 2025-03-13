from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SERVICE")

    # ! Обязательные переменные
    HOST: str
    PORT: int


def get_service_configuration(service_name: str) -> ServiceConfiguration:
    env_namespace = f"BACKEND_SERVICE_{service_name.upper()}_"

    class SpecificServiceConfiguration(ServiceConfiguration):
        model_config = SettingsConfigDict(env_prefix=env_namespace)

    return SpecificServiceConfiguration()


class ServicesConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BACKEND_SERVICE_")

    # * Вложенные группы настроек
    auth: ServiceConfiguration = get_service_configuration("auth")
