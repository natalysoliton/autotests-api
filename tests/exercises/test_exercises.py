from http import HTTPStatus

import pytest

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema,
    GetExercisesQuerySchema,
    GetExercisesResponseSchema,
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
    assert_get_exercises_response,
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

        :param exercises_client: Фикстура с клиентом для работы с API заданий
        :param function_exercise: Фикстура с данными созданного задания
        """
        exercise_id = function_exercise.response.exercise.id

        # Удаляем задание
        delete_response = exercises_client.delete_exercise_api(exercise_id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # Пытаемся получить удаленное задание
        get_response = exercises_client.get_exercise_api(exercise_id)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        error_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)
        assert_exercise_not_found_response(error_response_data)

        validate_json_schema(get_response.json(), error_response_data.model_json_schema())

    def test_get_exercises(
            self,
            exercises_client: ExercisesClient,
            function_course: CourseFixture,
            function_exercise: ExerciseFixture
    ):
        """
        Тест проверяет успешное получение списка заданий через API.

        Шаги теста:
        1. Создать тестовое задание (через фикстуру function_exercise)
        2. Отправить GET-запрос на эндпоинт /api/v1/exercises с фильтрацией по course_id
        3. Проверить, что API вернул статус-код 200 OK
        4. Проверить, что список заданий содержит созданное задание
        5. Валидировать JSON-схему ответа

        :param exercises_client: Фикстура с клиентом для работы с API заданий
        :param function_course: Фикстура с данными созданного курса
        :param function_exercise: Фикстура с данными созданного задания
        """
        # Arrange: Формируем query-параметры для фильтрации по course_id
        query = GetExercisesQuerySchema(
            course_id=function_course.response.course.id
        )

        # Act: Отправляем GET-запрос на получение списка заданий
        response = exercises_client.get_exercises_api(query)

        # Assert: Проверяем ответ API
        # 1. Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # 2. Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        # 3. Проверяем, что список заданий содержит созданное задание
        # Передаем список с одним заданием (function_exercise.response)
        assert_get_exercises_response(response_data, [function_exercise.response])

        # 4. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())
