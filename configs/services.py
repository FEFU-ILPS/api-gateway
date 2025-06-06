from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceConfiguration(BaseSettings):
    # ! Обязательные переменные
    HOST: str
    PORT: int

    # * Опциональные переменные
    PROTOCOL: str = "http"

    @property
    def URL(self) -> str:
        return f"{self.PROTOCOL}://{self.HOST}:{self.PORT}"


def get_service_configuration(service_name: str) -> ServiceConfiguration:
    env_namespace = f"GATEWAY_SERVICE_{service_name.upper()}_"

    class SpecificServiceConfiguration(ServiceConfiguration):
        model_config = SettingsConfigDict(env_prefix=env_namespace)

    return SpecificServiceConfiguration()


class ServicesConfiguration(BaseSettings):
    # * Вложенные группы настроек
    auth: ServiceConfiguration = get_service_configuration("auth")
    texts: ServiceConfiguration = get_service_configuration("texts")
    manager: ServiceConfiguration = get_service_configuration("manager")
    exercises: ServiceConfiguration = get_service_configuration("exercises")
