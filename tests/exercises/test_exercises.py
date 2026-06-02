from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema
)
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import (
    assert_create_exercise_response,
    assert_get_exercise_response
)
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    """
    Тестовый класс для проверки API работы с заданиями (exercises).
    Группирует все тесты, связанные с функциональностью заданий.
    """

    def test_create_exercise(
            self,
            exercises_client: ExercisesClient,
            function_course: CourseFixture
    ):
        """
        Тест проверяет успешное создание задания через API.

        Шаги теста:
        1. Сформировать запрос на создание задания с использованием:
           - ID курса (из фикстуры function_course)
           - Названия задания
           - Описания задания
           - Максимального балла
           - Длительности выполнения в минутах
        2. Отправить POST-запрос на эндпоинт /api/v1/exercises
        3. Проверить, что API вернул статус-код 200 OK
        4. Проверить, что данные в ответе соответствуют запросу
        5. Валидировать JSON-схему ответа

        Args:
            exercises_client: Фикстура с клиентом для работы с API заданий
            function_course: Фикстура с данными созданного курса

        Returns:
            None
        """
        # Arrange: Подготавливаем данные для создания задания
        request = CreateExerciseRequestSchema(
            course_id=function_course.response.course.id,
            title="Тестовое задание",
            description="Это тестовое задание, созданное автоматически",
            max_score=100,
            duration_minutes=60
        )

        # Act: Отправляем запрос на создание задания
        response = exercises_client.create_exercise_api(request)

        # Assert: Проверяем ответ API
        # 1. Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # 2. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        # 3. Проверяем, что данные в ответе соответствуют запросу
        assert_create_exercise_response(request, response_data)

        # 4. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        """
        Тест проверяет успешное получение задания по ID через API.

        Шаги теста:
        1. Использовать фикстуру function_exercise для создания тестового задания
        2. Отправить GET-запрос на эндпоинт /api/v1/exercises/{exercise_id}
        3. Проверить, что API вернул статус-код 200 OK
        4. Проверить, что данные полученного задания совпадают с созданным
        5. Валидировать JSON-схему ответа

        Args:
            exercises_client: Фикстура с клиентом для работы с API заданий
            function_exercise: Фикстура с данными созданного задания

        Returns:
            None
        """
        # Arrange: Получаем ID созданного задания из фикстуры
        exercise_id = function_exercise.response.exercise.id

        # Act: Отправляем GET-запрос на получение задания по ID
        response = exercises_client.get_exercise_api(exercise_id)

        # Assert: Проверяем ответ API
        # 1. Проверяем статус-код ответа (ожидаем 200 OK)
        assert_status_code(response.status_code, HTTPStatus.OK)

        # 2. Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        # 3. Проверяем, что данные полученного задания соответствуют созданному
        assert_get_exercise_response(response_data, function_exercise.response)

        # 4. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

