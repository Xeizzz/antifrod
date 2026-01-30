from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings
import yaml
import os

class Settings(BaseSettings):
    """Конфигурация сервиса."""

    app_name: str
    version: str
    host: str
    port: int
    environment: str
    debug: bool


    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))

    @classmethod
    def from_yaml(cls) -> 'Settings':
        """Метод для создания pydantic объекта из yaml-конфига."""
        config_path = Path(__file__).parent.parent / "config" / "local.yaml"
        with open(config_path, "r") as cfg_file:
            config_data = yaml.safe_load(cfg_file)

        config_data["redis_host"] = os.getenv("REDIS_HOST", config_data.get("redis_host", "localhost"))
        config_data["redis_port"] = int(os.getenv("REDIS_PORT", config_data.get("redis_port", 6379)))

        return cls(**config_data)


@lru_cache
def get_settings() -> Settings:
    """
    Получить настройки приложения.

    Используем @lru_cache чтобы создавать объект Settings только один раз.
    """
    return Settings.from_yaml()
