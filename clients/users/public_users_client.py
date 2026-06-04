from httpx import Response

from clients.api_client import APIClient
from clients.public_http_builder import get_public_http_client
from clients.api_coverage import tracker  # Импортируем трекер
from clients.users.users_schema import CreateUserResponseSchema, CreateUserRequestSchema, UserSchema
import allure  # Импортируем allure
from tools.routes import APIRoutes  # Импортируем enum APIRoutes


class CreateUserRequestSchema(CreateUserRequestSchema):
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


class CreateUserResponseDict(CreateUserResponseSchema):
    user: UserSchema


class PublicUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users (публичные методы)
    """

    @allure.step("Create user")  # Добавили allure шаг
    # Добавили сбор покрытия для эндпоинта POST /api/v1/users
    @tracker.track_coverage_httpx(APIRoutes.USERS)
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Метод создает пользователя.
        """
        # Вместо /api/v1/users используем APIRoutes.USERS
        return self.post(APIRoutes.USERS, json=request.model_dump(by_alias=True))

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        """
        Метод создает пользователя и возвращает JSON.
        """
        response = self.create_user_api(request)
        return response.json()


def get_public_users_client() -> PublicUsersClient:
    """
    Функция создаёт экземпляр PublicUsersClient с уже настроенным HTTP-клиентом.
    """
    return PublicUsersClient(client=get_public_http_client())
