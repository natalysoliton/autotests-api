from typing import TypedDict
from pathlib import Path

from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client


class File(TypedDict):
    id: str
    url: str
    filename: str
    directory: str


class CreateFileRequestDict(TypedDict):
    filename: str
    directory: str
    upload_file: str


class CreateFileResponseDict(TypedDict):
    file: File


class FilesClient(APIClient):
    """
    Клиент для работы с /api/v1/files
    """

    def create_file_api(self, request: CreateFileRequestDict) -> Response:
        """
        Метод создания файла.
        """
        with open(request['upload_file'], 'rb') as f:
            files = {"upload_file": (request['filename'], f, "image/png")}
            data = {
                "filename": request['filename'],
                "directory": request['directory']
            }
            return self.post("/api/v1/files", data=data, files=files)

    def create_file(self, request: CreateFileRequestDict) -> CreateFileResponseDict:
        """
        Метод создания файла с автоматическим извлечением JSON.
        """
        response = self.create_file_api(request)
        return response.json()


def get_files_client(user: AuthenticationUserDict) -> FilesClient:
    """
    Функция создаёт экземпляр FilesClient с уже настроенным HTTP-клиентом.
    """
    return FilesClient(client=get_private_http_client(user))
