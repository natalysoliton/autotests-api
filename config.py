# config.py
from typing import Self
from pathlib import Path

from pydantic import BaseModel, HttpUrl, FilePath, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPClientConfig(BaseModel):
    url: HttpUrl
    timeout: float

    @property
    def client_url(self) -> str:
        return str(self.url)


class TestDataConfig(BaseModel):
    image_png_file: FilePath


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='allow',  # Разрешаем дополнительные переменные окружения
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
    )

    test_data: TestDataConfig
    http_client: HTTPClientConfig
    allure_results_dir: DirectoryPath

    @classmethod
    def initialize(cls) -> Self:
        """Инициализирует настройки и создает необходимые директории."""
        # Создаем объект пути к папке allure-results
        allure_results_dir = DirectoryPath("./allure-results")
        # Создаем папку allure-results, если она не существует
        allure_results_dir.mkdir(exist_ok=True)
        # Возвращаем экземпляр настроек
        return cls(allure_results_dir=allure_results_dir)


# Инициализируем настройки через метод initialize
settings = Settings.initialize()
