from http import HTTPStatus

import pytest

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
    assert_update_exercise_response
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
        exercise_id = function_exercise.response.exercise.id
        response = exercises_client.get_exercise_api(exercise_id)
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
        Тест проверяет успешное обновление задания через API (PATCH-запрос).

        Шаги теста:
        1. Использовать фикстуру function_exercise для создания тестового задания
        2. Сформировать запрос на обновление задания с новыми значениями полей
        3. Отправить PATCH-запрос на эндпоинт /api/v1/exercises/{exercise_id}
        4. Проверить статус-код ответа (200 OK)
        5. Проверить, что обновленные данные соответствуют запросу
        6. Валидировать JSON-схему ответа

        :param exercises_client: Фикстура с клиентом для работы с API заданий
        :param function_exercise: Фикстура с данными созданного задания
        """
        # Arrange: Получаем ID созданного задания из фикстуры
        exercise_id = function_exercise.response.exercise.id

        # Формируем данные для обновления задания
        request = UpdateExerciseRequestSchema(
            title="Обновленное название задания",
            description="Обновленное описание задания",
            max_score=150,
            min_score=30,
            order_index=5,
            estimated_time=90
        )

        # Act: Отправляем PATCH-запрос на обновление задания
        response = exercises_client.update_exercise_api(exercise_id, request)

        # Assert: Проверяем ответ API
        # 1. Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # 2. Десериализуем JSON-ответ в Pydantic-модель
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        # 3. Проверяем, что обновленные данные соответствуют запросу
        assert_update_exercise_response(request, response_data)

        # 4. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())
