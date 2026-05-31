from httpx import Client
from pydantic import BaseModel

from clients.authentication.authentication_client import get_authentication_client
# Импортируем модель LoginRequestSchema
from clients.authentication.authentication_schema import LoginRequestSchema


# Добавили суффикс Schema вместо Dict
class AuthenticationUserSchema(BaseModel):  # Наследуем от BaseModel вместо TypedDict
    email: str
    password: str


def get_private_http_client(user: AuthenticationUserSchema) -> Client:
    authentication_client = get_authentication_client()

    # Используем модель LoginRequestSchema
    # Значения теперь извлекаем не по ключу, а через атрибуты
    login_request = LoginRequestSchema(email=user.email, password=user.password)
    login_response = authentication_client.login(login_request)

    return Client(
        timeout=100,
        base_url="http://localhost:8000",
        # Значения теперь извлекаем не по ключу, а через атрибуты
        headers={"Authorization": f"Bearer {login_response.token.access_token}"}
    )
