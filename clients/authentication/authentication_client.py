from httpx import Response

from clients.api_client import APIClient
# Добавили импорт моделей
from clients.authentication.authentication_schema import LoginRequestSchema, RefreshRequestSchema, LoginResponseSchema
from clients.public_http_builder import get_public_http_client


# Старые модели с использованием TypedDict были удалены

class AuthenticationClient(APIClient):
    """
    Клиент для работы с /api/v1/authentication
    """

    # Теперь используем pydantic-модель для аннотации
    def login_api(self, request: LoginRequestSchema) -> Response:
        """
        Метод выполняет аутентификацию пользователя.

        :param request: Словарь с email и password.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(
            "/api/v1/authentication/login",
            # Сериализуем модель в словарь с использованием alias
            json=request.model_dump(by_alias=True)
        )

    # Теперь используем pydantic-модель для аннотации
    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        """
        Метод обновляет токен авторизации.

        :param request: Словарь с refreshToken.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(
            "/api/v1/authentication/refresh",
            # Сериализуем модель в словарь с использованием alias
            json=request.model_dump(by_alias=True)
        )

    # Теперь используем pydantic-модель для аннотации
    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        response = self.login_api(request)
        # Инициализируем модель через валидацию JSON строки
        return LoginResponseSchema.model_validate_json(response.text)


def get_authentication_client() -> AuthenticationClient:
    """
    Функция создаёт экземпляр AuthenticationClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AuthenticationClient.
    """
    return AuthenticationClient(client=get_public_http_client())
