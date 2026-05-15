from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel


class UserSchema(BaseModel):
    """
    Модель данных пользователя.

    Используется для представления пользователя в различных частях API.
    Содержит полную информацию о пользователе, включая идентификатор.

    Attributes:
        id: Уникальный идентификатор пользователя (строка)
        email: Электронная почта пользователя (валидируется как EmailStr)
        last_name: Фамилия пользователя
        first_name: Имя пользователя
        middle_name: Отчество пользователя (может отсутствовать)
    """

    # Настройка автоматического преобразования snake_case -> camelCase
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,  # Позволяет передавать как snake_case, так и camelCase
    )

    id: str = Field(
        ...,  # Обязательное поле
        description="Уникальный идентификатор пользователя",
        example="123e4567-e89b-12d3-a456-426614174000"
    )
    email: EmailStr = Field(
        ...,
        description="Электронная почта пользователя",
        example="user@example.com"
    )
    last_name: str = Field(
        ...,
        description="Фамилия пользователя",
        min_length=1,
        max_length=100,
        example="Doe"
    )
    first_name: str = Field(
        ...,
        description="Имя пользователя",
        min_length=1,
        max_length=100,
        example="John"
    )
    middle_name: str = Field(
        default="",  # Отчество может отсутствовать
        description="Отчество пользователя (опционально)",
        max_length=100,
        example="Michael"
    )

    def get_full_name(self) -> str:
        """
        Возвращает полное имя пользователя (Фамилия Имя Отчество).

        Returns:
            Строка с полным именем пользователя, где все части разделены пробелами.
            Отчество включается только если оно не пустое.

        """
        name_parts = [self.last_name, self.first_name]
        if self.middle_name:
            name_parts.append(self.middle_name)
        return " ".join(name_parts)


class CreateUserRequestSchema(BaseModel):
    """
    Модель запроса на создание нового пользователя.

    Используется для отправки данных на эндпоинт POST /api/v1/users.
    Содержит все необходимые данные для регистрации пользователя,
    включая пароль, который не возвращается в ответе API.

    Attributes:
        email: Электронная почта пользователя (должна быть уникальной)
        password: Пароль пользователя (требования к сложности)
        last_name: Фамилия пользователя
        first_name: Имя пользователя
        middle_name: Отчество пользователя (опционально)
    """

    # Настройка автоматического преобразования snake_case -> camelCase
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "string",
                "lastName": "string",
                "firstName": "string",
                "middleName": "string"
            }
        }
    )

    email: EmailStr = Field(
        ...,
        description="Электронная почта пользователя (должна быть уникальной)",
        example="user@example.com"
    )
    password: str = Field(
        ...,
        description="Пароль пользователя. Рекомендуется: минимум 8 символов, "
                    "содержать буквы разного регистра, цифры и спецсимволы",
        min_length=8,
        max_length=128,
        example="SecurePass123!"
    )
    last_name: str = Field(
        ...,
        description="Фамилия пользователя",
        min_length=1,
        max_length=100,
        example="Doe"
    )
    first_name: str = Field(
        ...,
        description="Имя пользователя",
        min_length=1,
        max_length=100,
        example="John"
    )
    middle_name: str = Field(
        default="",
        description="Отчество пользователя (опционально)",
        max_length=100,
        example="Michael"
    )


class CreateUserResponseSchema(BaseModel):
    """
    Модель ответа API на успешное создание пользователя.

    Возвращается эндпоинтом POST /api/v1/users после успешной регистрации.
    Содержит объект user с полными данными созданного пользователя.

    Attributes:
        user: Объект UserSchema с данными созданного пользователя

     """

    # Настройка автоматического преобразования snake_case -> camelCase
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@example.com",
                    "lastName": "string",
                    "firstName": "string",
                    "middleName": "string"
                }
            }
        }
    )

    user: UserSchema = Field(
        ...,
        description="Объект с данными созданного пользователя",
        example={
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "user@example.com",
            "lastName": "Doe",
            "firstName": "John",
            "middleName": "Michael"
        }
    )


# Пример использования и демонстрация работы моделей
if __name__ == "__main__":
    """
    Демонстрация работы Pydantic-моделей для создания пользователя.
    Показывает инициализацию, валидацию и сериализацию моделей.
    """

    print("Демонстрация работы Pydantic-моделей для создания пользователя")

    # 1. Создание запроса на регистрацию пользователя
    print("\n1. Создание запроса (CreateUserRequestSchema):")
    request_data = CreateUserRequestSchema(
        email="ivan.petrov@example.com",
        password="SecurePass123!",
        lastName="Petrov",  # Используем camelCase как в API
        firstName="Ivan",
        middleName="Ivanovich"
    )
    print(f"   Запрос (Python): {request_data}")
    print(f"   Сериализация в dict (snake_case): {request_data.model_dump()}")
    print(f"   Сериализация в dict (camelCase для API): "
          f"{request_data.model_dump(by_alias=True)}")

    # 2. Создание ответа API (имитируем получение от сервера)
    print("\n2. Создание ответа API (CreateUserResponseSchema):")
    response_data = CreateUserResponseSchema(
        user=UserSchema(
            id="550e8400-e29b-41d4-a716-446655440000",
            email="ivan.petrov@example.com",
            lastName="Petrov",
            firstName="Ivan",
            middleName="Ivanovich"
        )
    )
    print(f"   Ответ (Python): {response_data}")
    print(f"   Полное имя пользователя: {response_data.user.get_full_name()}")

    # 3. Валидация: демонстрация обработки ошибок
    print("\n3. Валидация данных (обработка ошибок):")

    # Тест 1: Некорректный email
    print("\n   Тест 1: Некорректный email")
    try:
        invalid_email = CreateUserRequestSchema(
            email="invalid-email",  # Невалидный email
            password="SecurePass123!",
            lastName="Test",
            firstName="Test",
        )
    except Exception as e:
        print(f" Ошибка валидации: {e.errors()[0]['msg']}")

    # Тест 2: Слишком короткий пароль
    print("\n   Тест 2: Слишком короткий пароль (менее 8 символов)")
    try:
        weak_password = CreateUserRequestSchema(
            email="test@example.com",
            password="123",  # Меньше 8 символов
            lastName="Test",
            firstName="Test",
        )
    except Exception as e:
        print(f" Ошибка валидации: {e.errors()[0]['msg']}")

    # Тест 3: Пустая фамилия
    print("\n   Тест 3: Пустая фамилия")
    try:
        empty_lastname = CreateUserRequestSchema(
            email="test@example.com",
            password="SecurePass123!",
            lastName="",  # Пустая строка
            firstName="Test",
        )
    except Exception as e:
        print(f" Ошибка валидации: {e.errors()[0]['msg']}")

    # 4. Инициализация через словарь (имитация получения из JSON)
    print("\n4. Инициализация через словарь (из JSON-ответа API):")
    response_dict = {
        "user": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "ivan.petrov@example.com",
            "lastName": "Petrov",
            "firstName": "Ivan",
            "middleName": "Ivanovich"
        }
    }
    parsed_response = CreateUserResponseSchema(**response_dict)
    print(f"   Распарсенный ответ: {parsed_response}")
    print(f"   Имя пользователя: {parsed_response.user.first_name}")
    print(f"   Email: {parsed_response.user.email}")

    print("\n" + "=" * 60)
    print("Демонстрация завершена. Все модели работают корректно!")
    print("=" * 60)
