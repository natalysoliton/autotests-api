from http import HTTPStatus

import pytest

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema
)
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import (
    assert_create_exercise_response,
    assert_get_exercise_response,
    assert_update_exercise_response,
    assert_exercise_not_found_response
)
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    """
    Тестовый класс для проверки API работы с заданиями (exercises).
    """

    def test_create_exercise(
            self,
            function_course: CourseFixture,
            exercises_client: ExercisesClient
    ):
        """
        Тест проверяет успешное создание задания через API.

        :param function_course: Фикстура с данными созданного курса
        :param exercises_client: Фикстура с клиентом для работы с API заданий
        """
        request = CreateExerciseRequestSchema(
            course_id=function_course.response.course.id
        )
        response = exercises_client.create_exercise_api(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_exercise_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        """
        Тест проверяет успешное получение задания по ID через API.

        :param exercises_client: Фикстура с клиентом для работы с API заданий
        :param function_exercise: Фикстура с данными созданного задания
        """
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_response(response_data, function_exercise.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        """
        Тест проверяет успешное обновление задания через API.

        :param exercises_client: Фикстура с клиентом для работы с API заданий
        :param function_exercise: Фикстура с данными созданного задания
        """
        request = UpdateExerciseRequestSchema()
        response = exercises_client.update_exercise_api(
            function_exercise.response.exercise.id,
            request
        )
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_exercise_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        """
        Тест проверяет успешное удаление задания через API.

        Шаги теста:
        1. Использовать фикстуру function_exercise для создания тестового задания
        2. Отправить DELETE-запрос на эндпоинт /api/v1/exercises/{exercise_id}
        3. Проверить, что задание успешно удалено (статус 200 OK)
        4. Отправить GET-запрос на получение удаленного задания
        5. Проверить, что задание не найдено (статус 404 Not Found)
        6. Проверить, что тело ответа содержит ошибку "Exercise not found"
        7. Валидировать JSON-схему ответа с ошибкой

        :param exercises_client: Фикстура с клиентом для работы с API заданий
        :param function_exercise: Фикстура с данными созданного задания
        """
        # Arrange: Получаем ID созданного задания из фикстуры
        exercise_id = function_exercise.response.exercise.id

        # Act 1: Отправляем DELETE-запрос на удаление задания
        delete_response = exercises_client.delete_exercise_api(exercise_id)

        # Assert 1: Проверяем успешное удаление
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # Act 2: Пытаемся получить удаленное задание
        get_response = exercises_client.get_exercise_api(exercise_id)

        # Assert 2: Проверяем, что задание не найдено
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        # Десериализуем ответ с ошибкой
        error_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        # Проверяем, что ошибка соответствует ожидаемой
        assert_exercise_not_found_response(error_response_data)

        # Валидируем JSON-схему ответа с ошибкой
        validate_json_schema(get_response.json(), error_response_data.model_json_schema())
