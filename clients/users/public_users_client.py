from typing import TypedDict
from httpx import Response

from clients.api_client import APIClient


class CreateUserRequestDict(TypedDict):
    """
    Структура данных для запроса создания пользователя.

    Атрибуты:
        email: Адрес электронной почты пользователя
        password: Пароль пользователя
        lastName: Фамилия пользователя
        firstName: Имя пользователя
        middleName: Отчество пользователя
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


class PublicUsersClient(APIClient):
    """
    Клиент для работы с публичными эндпоинтами /api/v1/users.

    Содержит методы, не требующие авторизации, такие как создание пользователя.
    Для работы с приватными эндпоинтами (получение, обновление, удаление)
    используется PrivateUsersClient.

    Пример использования:
        # Инициализация клиента с настроенным httpx.Client
        client = PublicUsersClient(httpx_client)

        # Создание пользователя
        user_data: CreateUserRequestDict = {
            "email": "user@example.com",
            "password": "secure_password",
            "lastName": "Иванов",
            "firstName": "Иван",
            "middleName": "Иванович"
        }
        response = client.create_user_api(user_data)

        # Проверка результата
        assert response.status_code == 201
        user_id = response.json()["user"]["id"]
    """

    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """
        Создание нового пользователя в системе.

        Выполняет POST-запрос к эндпоинту /api/v1/users для регистрации
        нового пользователя. Этот метод является публичным и не требует
        предварительной авторизации.

        Args:
            request (CreateUserRequestDict): Словарь с данными пользователя,
                содержащий обязательные поля:
                - email: Адрес электронной почты
                - password: Пароль пользователя
                - lastName: Фамилия
                - firstName: Имя
                - middleName: Отчество

        Returns:
            Response: Объект httpx.Response, содержащий ответ сервера.
                При успешном создании (статус 201) ответ содержит:
                {
                    "user": {
                        "id": "uuid",
                        "email": "user@example.com",
                        "lastName": "Иванов",
                        "firstName": "Иван",
                        "middleName": "Иванович"
                    }
                }

        Raises:
            httpx.HTTPStatusError: Если запрос завершился с ошибкой (4xx, 5xx)
            httpx.RequestError: При проблемах сетевого соединения или таймауте

        Примеры:
            Успешное создание пользователя:
            >>> request = CreateUserRequestDict(
            ...     email="test@example.com",
            ...     password="pass123",
            ...     lastName="Петров",
            ...     firstName="Петр",
            ...     middleName="Петрович"
            ... )
            >>> response = client.create_user_api(request)
            >>> response.status_code
            201

            Ошибка при создании дубликата:
            >>> response = client.create_user_api(request)
            >>> response.status_code
            409
        """
        return self.post("/api/v1/users", json=request)
