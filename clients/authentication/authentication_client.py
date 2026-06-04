from httpx import Response
from tools.routes import APIRoutes  # Импортируем enum APIRoutes
from clients.api_client import APIClient
from clients.authentication.authentication_schema import (
    LoginRequestSchema,
    RefreshRequestSchema,
    LoginResponseSchema
)
from clients.public_http_builder import get_public_http_client
from clients.api_coverage import tracker  # Импортируем трекер из api_coverage.py
import allure  # Импортируем allure

class Token:
    """
    Класс для хранения токена аутентификации.
    """

    def __init__(self, access_token: str, refresh_token: str = None, token_type: str = "bearer"):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type

    def __str__(self):
        return f"{self.token_type} {self.access_token}"

    @property
    def authorization_header(self) -> dict:
        """
        Возвращает заголовок авторизации для HTTP-запросов.
        """
        return {"Authorization": str(self)}


class AuthenticationClient(APIClient):
    """
    Клиент для работы с /api/v1/authentication
    """

    @allure.step("Authenticate user")  # Добавили allure шаг
    # Добавили сбор покрытия для эндпоинта POST /api/v1/authentication/login
    @tracker.track_coverage_httpx(f"{APIRoutes.AUTHENTICATION}/login")
    def login_api(self, request: LoginRequestSchema) -> Response:
        """
        Метод выполняет аутентификацию пользователя.

        :param request: Модель с email и password.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        # Вместо /api/v1/authentication используем APIRoutes.AUTHENTICATION
        return self.post(
            f"{APIRoutes.AUTHENTICATION}/login",
            json=request.model_dump(by_alias=True)
        )

    @allure.step("Refresh authentication token")  # Добавили allure шаг
    # Добавили сбор покрытия для эндпоинта POST /api/v1/authentication/refresh
    @tracker.track_coverage_httpx(f"{APIRoutes.AUTHENTICATION}/refresh")
    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        """
        Метод обновляет токен авторизации.

        :param request: Модель с refreshToken.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        # Вместо /api/v1/authentication используем APIRoutes.AUTHENTICATION
        return self.post(
            f"{APIRoutes.AUTHENTICATION}/refresh",
            json=request.model_dump(by_alias=True)
        )

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        """
        Выполняет вход и возвращает десериализованный ответ.
        """
        response = self.login_api(request)
        return LoginResponseSchema.model_validate_json(response.text)


def get_authentication_client() -> AuthenticationClient:
    """
    Функция создаёт экземпляр AuthenticationClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AuthenticationClient.
    """
    return AuthenticationClient(client=get_public_http_client())
