from typing import Any
from httpx import Client, URL, Response, QueryParams
from httpx._types import RequestData, RequestFiles


class APIClient:
    """Базовый API клиент, предоставляющий основные HTTP-методы."""

    def __init__(self, client: Client):
        """
        Инициализация базового API клиента.

        Args:
            client: Экземпляр httpx.Client для выполнения HTTP-запросов
        """
        self.client = client

    def get(self, url: URL | str, params: QueryParams | None = None) -> Response:
        """Выполняет GET-запрос."""
        return self.client.get(url, params=params)

    def post(
            self,
            url: URL | str,
            json: Any | None = None,
            data: RequestData | None = None,
            files: RequestFiles | None = None
    ) -> Response:
        """Выполняет POST-запрос."""
        return self.client.post(url, json=json, data=data, files=files)

    def patch(self, url: URL | str, json: Any | None = None) -> Response:
        """Выполняет PATCH-запрос (частичное обновление)."""
        return self.client.patch(url, json=json)

    def delete(self, url: URL | str) -> Response:
        """Выполняет DELETE-запрос (удаление)."""
        return self.client.delete(url)
