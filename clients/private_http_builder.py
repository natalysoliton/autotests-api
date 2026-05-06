"""
Приватный билдер для создания HTTP-клиента с авторизацией.
"""

from typing import TypedDict

from httpx import Client

# Используем абсолютный импорт
from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_client import LoginRequestDict


class AuthenticationUserDict(TypedDict):
    """
    Структура данных пользователя для авторизации.
    """
    email: str
    password: str


def get_private_http_client(user: AuthenticationUserDict) -> Client:
    """
    Функция создаёт экземпляр httpx.Client с аутентификацией пользователя.

    :param user: Объект AuthenticationUserDict с email и паролем пользователя.
    :return: Готовый к использованию объект httpx.Client с установленным заголовком Authorization.
    """
    # Инициализируем AuthenticationClient для аутентификации
    authentication_client = get_authentication_client()

    # Инициализируем запрос на аутентификацию
    login_request = LoginRequestDict(
        email=user['email'],
        password=user['password']
    )

    # Выполняем POST запрос и аутентифицируемся
    login_response = authentication_client.login(login_request)

    return Client(
        timeout=100,
        base_url="http://localhost:8000",
        # Добавляем заголовок авторизации
        headers={"Authorization": f"Bearer {login_response['token']['accessToken']}"}
    )
