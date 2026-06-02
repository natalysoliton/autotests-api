from http import HTTPStatus

import pytest

from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from fixtures.files import FileFixture
from fixtures.users import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.courses import assert_create_course_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.courses
@pytest.mark.regression
class TestCourses:
    """
    Тестовый класс для проверки API работы с курсами.
    """

    def test_create_course(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        """
        Тест проверяет успешное создание курса через API.

        Шаги теста:
        1. Сформировать запрос на создание курса с использованием:
           - ID файла для превью (из фикстуры function_file)
           - ID пользователя-создателя (из фикстуры function_user)
        2. Отправить POST-запрос на эндпоинт /api/v1/courses
        3. Проверить, что API вернул статус-код 200 OK
        4. Проверить, что данные в ответе соответствуют запросу
        5. Валидировать JSON-схему ответа

        Args:
            courses_client: Фикстура с клиентом для работы с API курсов
            function_user: Фикстура с данными тестового пользователя
            function_file: Фикстура с данными загруженного файла для превью
        """
        # Arrange: Подготавливаем данные для создания курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id
        )

        # Act: Отправляем запрос на создание курса
        response = courses_client.create_course_api(request)

        # Assert: Проверяем ответ API
        # 1. Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # 2. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)

        # 3. Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)

        # 4. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())
