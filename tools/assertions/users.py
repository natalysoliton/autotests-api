import allure

from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema, \
    UserSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger  # Импортируем функцию для создания логгера

logger = get_logger("USERS_ASSERTIONS")  # Создаем логгер с именем "USERS_ASSERTIONS"


@allure.step("Check create user response")  # Добавили allure шаг
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """
    Проверяет, что ответ на создание пользователя соответствует запросу.
    """
    # Логируем факт начала проверки
    logger.info("Check create user response")

    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")


@allure.step("Check user")  # Добавили allure шаг
def assert_user(actual: UserSchema, expected: UserSchema):
    """
    Проверяет, что данные пользователя соответствуют ожидаемым.
    """
    # Логируем факт начала проверки
    logger.info("Check user")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.last_name, expected.last_name, "last_name")
    assert_equal(actual.first_name, expected.first_name, "first_name")
    assert_equal(actual.middle_name, expected.middle_name, "middle_name")


@allure.step("Check get user response")  # Добавили allure шаг
def assert_get_user_response(get_user_response: GetUserResponseSchema, create_user_response: CreateUserResponseSchema):
    """
    Проверяет, что данные пользователя при создании и при запросе совпадают.

    :param get_user_response: Ответ API при запросе пользователя (GetUserResponseSchema).
    :param create_user_response: Ответ API при создании пользователя (CreateUserResponseSchema).
    """
    # Логируем факт начала проверки
    logger.info("Check get user response")

    assert_user(get_user_response.user, create_user_response.user)
