from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from clients.users.users_schema import (
    CreateUserRequestSchema,
    GetUserResponseSchema
)
from clients.private_http_builder import AuthenticationUserSchema
from tools.assertions.schema import validate_json_schema
from tools.fakers import get_random_email


def main():
    # 1. Создаем пользователя
    public_client = get_public_users_client()

    create_request = CreateUserRequestSchema(
        email=get_random_email(),
        password="password123",
        last_name="Иванов",
        first_name="Иван",
        middle_name="Иванович"
    )

    create_response = public_client.create_user(create_request)
    print(f"Создан пользователь с ID: {create_response.user.id}")

    # 2. Получаем данные пользователя через приватный клиент
    auth_user = AuthenticationUserSchema(
        email=create_request.email,
        password=create_request.password
    )

    private_client = get_private_users_client(auth_user)
    user_id = create_response.user.id

    # Используем get_user_api для получения сырого ответа
    response = private_client.get_user_api(user_id)
    response_data = response.json()

    # 3. Валидируем JSON Schema
    schema = GetUserResponseSchema.model_json_schema()
    validate_json_schema(
        instance=response_data,
        schema=schema,
        schema_name="GetUserResponseSchema"
    )

    print("✅ JSON Schema валидация успешно пройдена!")
    print(f"Данные пользователя: {response_data}")


if __name__ == "__main__":
    main()
