from pydantic import BaseModel, Field, HttpUrl, FilePath  # Добавили FilePath
from tools.fakers import fake


class FileSchema(BaseModel):
    """
    Описание структуры файла.
    """
    id: str
    url: HttpUrl
    filename: str
    directory: str


class CreateFileRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание файла.
    """
    # Добавили генерацию случайного названия файла с расширением PNG
    filename: str = Field(default_factory=lambda: f"{fake.uuid4()}.png")
    # Директорию оставляем статичной, чтобы все тестовые файлы на сервере попадали в одну папку
    directory: str = Field(default="tests")
    upload_file: FilePath  # Изменили тип с str на FilePath


class CreateFileResponseSchema(BaseModel):
    """
    Описание структуры ответа создания файла.
    """
    file: FileSchema


class GetFileResponseSchema(BaseModel):  # Исправили класс (был неправильно определен)
    """
    Описание структуры ответа получения файла.
    """
    file: FileSchema
