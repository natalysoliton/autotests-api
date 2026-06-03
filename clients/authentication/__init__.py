"""
Модуль для работы с API аутентификации.
"""

from clients.authentication.authentication_client import (
    AuthenticationClient,
    get_authentication_client,
)
from clients.authentication.authentication_schema import (
    LoginRequestSchema,
    LoginResponseSchema,
    RefreshRequestSchema,
    TokenSchema,
)

__all__ = [
    'AuthenticationClient',
    'get_authentication_client',
    'LoginRequestSchema',
    'LoginResponseSchema',
    'RefreshRequestSchema',
    'TokenSchema',
]
