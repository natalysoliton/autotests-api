import pytest
from pydantic import BaseModel, EmailStr

from clients.authentication.authentication_client import AuthenticationClient, get_authentication_client
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.private_users_client import get_private_users_client, PrivateUsersClient
from clients.users.public_users_client import get_public_users_client, PublicUsersClient
# Импортируем запрос и ответ создания пользователя, модель данных пользователя
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, UserSchema


# Модель для агрегации возвращаемых данных фикстурой function_user
class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def email(self) -> EmailStr:  # Быстрый доступ к email пользователя
        return self.request.email

    @property
    def password(self) -> str:  # Быстрый доступ к password пользователя
        return self.request.password

    @property
    def authentication_user(self) -> AuthenticationUserSchema:
        """
        Возвращает модель аутентификации для использования в приватных API-клиентах.
        """
        return AuthenticationUserSchema(
            email=self.request.email,
            password=self.request.password
        )


@pytest.fixture
def authentication_client() -> AuthenticationClient:
    return get_authentication_client()


@pytest.fixture
def public_users_client() -> PublicUsersClient:
    return get_public_users_client()


# Фикстура для создания пользователя
@pytest.fixture
# Используем фикстуру public_users_client, которая создает нужный API клиент
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)
    return UserFixture(request=request, response=response)  # Возвращаем все нужные данные


# Фикстура для создания приватного API клиента
@pytest.fixture
def private_users_client(function_user: UserFixture) -> PrivateUsersClient:
    """
    Создает приватный API клиент для работы с пользователями,
    используя аутентификационные данные созданного пользователя.
    """
    return get_private_users_client(function_user.authentication_user)
