import allure

from clients.courses.courses_schema import CourseSchema, UpdateCourseRequestSchema, UpdateCourseResponseSchema, \
    GetCoursesResponseSchema, CreateCourseResponseSchema, CreateCourseRequestSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.files import assert_file
from tools.assertions.users import assert_user
from tools.logger import get_logger  # Импортируем функцию для создания логгера

logger = get_logger("COURSES_ASSERTIONS")  # Создаем логгер с именем "COURSES_ASSERTIONS"

@allure.step("Check create course response")  # Добавили allure шаг
def assert_create_course_response(
        request: CreateCourseRequestSchema,
        response: CreateCourseResponseSchema
):
    """
    Проверяет, что ответ на создание курса соответствует данным из запроса.

    Функция проверяет:
    - Наличие и корректность вложенного файла (preview_file)
    - Наличие и корректность вложенного пользователя (created_by_user)
    - Наличие ID курса

    :param request: Исходный запрос на создание курса.
    :param response: Ответ API с данными созданного курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает или вложенные сущности отсутствуют.
    """
    # Логируем факт начала проверки
    logger.info("Check create course response")

    # Проверяем, что в ответе присутствует объект курса
    assert response.course is not None, "Course object is missing in response"

    # Проверяем, что ID файла превью соответствует переданному
    assert response.course.preview_file is not None, "Preview file is missing in response"
    assert_equal(
        response.course.preview_file.id,
        request.preview_file_id,
        "preview_file_id"
    )

    # Проверяем, что ID создателя соответствует переданному
    assert response.course.created_by_user is not None, "Created by user is missing in response"
    assert_equal(
        response.course.created_by_user.id,
        request.created_by_user_id,
        "created_by_user_id"
    )

    # Проверяем, что ID курса присутствует (не None)
    assert response.course.id is not None, "Course ID is missing in response"

    # Проверяем, что ID имеет правильный формат (строка, не пустая)
    assert isinstance(response.course.id, str), "Course ID should be a string"
    assert len(response.course.id) > 0, "Course ID should not be empty"


@allure.step("Check update course response")  # Добавили allure шаг
def assert_update_course_response(
        request: UpdateCourseRequestSchema,
        response: UpdateCourseResponseSchema
):
    """
    Проверяет, что ответ на обновление курса соответствует данным из запроса.

    :param request: Исходный запрос на обновление курса.
    :param response: Ответ API с обновленными данными курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    # Логируем факт начала проверки
    logger.info("Check update course response")

    if request.title is not None:
        assert_equal(response.course.title, request.title, "title")

    if request.max_score is not None:
        assert_equal(response.course.max_score, request.max_score, "max_score")

    if request.min_score is not None:
        assert_equal(response.course.min_score, request.min_score, "min_score")

    if request.description is not None:
        assert_equal(response.course.description, request.description, "description")

    if request.estimated_time is not None:
        assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Check course")  # Добавили allure шаг
def assert_course(actual: CourseSchema, expected: CourseSchema):
    """
    Проверяет, что фактические данные курса соответствуют ожидаемым.

    :param actual: Фактические данные курса.
    :param expected: Ожидаемые данные курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    # Логируем факт начала проверки
    logger.info("Check course")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

    # Проверяем вложенные сущности
    assert_file(actual.preview_file, expected.preview_file)
    assert_user(actual.created_by_user, expected.created_by_user)


@allure.step("Check get courses response")  # Добавили allure шаг
def assert_get_courses_response(
        get_courses_response: GetCoursesResponseSchema,
        create_course_responses: list[CreateCourseResponseSchema]
):
    """
    Проверяет, что ответ на получение списка курсов соответствует ответам на их создание.

    :param get_courses_response: Ответ API при запросе списка курсов.
    :param create_course_responses: Список API ответов при создании курсов.
    :raises AssertionError: Если данные курсов не совпадают.
    """
    # Логируем факт начала проверки
    logger.info("Check get courses response")

    assert_length(get_courses_response.courses, create_course_responses, "courses")

    for index, create_course_response in enumerate(create_course_responses):
        assert_course(get_courses_response.courses[index], create_course_response.course)
