from http import HTTPStatus

import pytest

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from fixtures.users import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake


@pytest.mark.users
@pytest.mark.regression
@pytest.mark.parametrize("email_domain", [
    "mail.ru",
    "gmail.com",
    "example.com"
], ids=[
    "mail.ru domain",
    "gmail.com domain",
    "example.com domain"
])
def test_create_user(email_domain: str, public_users_client: PublicUsersClient):
    """
    Тест проверяет создание пользователя с различными доменами email.
    Параметризация выполняется по домену email-адреса.
    """
    # Генерируем email с указанным доменом
    generated_email = fake.email(domain=email_domain)

    # Создаем запрос с параметризованным email
    request = CreateUserRequestSchema(email=generated_email)
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_create_user_response(request, response_data)

    # Дополнительная проверка, что email создан с правильным доменом
    assert response_data.user.email.endswith(f"@{email_domain}"), \
        f"Expected email to end with @{email_domain}, but got {response_data.user.email}"

    validate_json_schema(response.json(), response_data.model_json_schema())


@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(
        function_user: UserFixture,
        private_users_client: PrivateUsersClient
):
    """
    Тест проверяет получение данных текущего авторизованного пользователя
    через эндпоинт GET /api/v1/users/me.
    """
    # Отправляем GET-запрос для получения текущего пользователя
    response = private_users_client.get_user_me_api()

    # Десериализуем JSON-ответ в GetUserResponseSchema
    response_data = GetUserResponseSchema.model_validate_json(response.text)

    # Проверяем статус-код ответа
    assert_status_code(response.status_code, HTTPStatus.OK)

    # Проверяем, что данные пользователя соответствуют созданному пользователю
    assert_get_user_response(response_data, function_user.response)

    # Выполняем валидацию JSON-схемы
    validate_json_schema(response.json(), response_data.model_json_schema())
