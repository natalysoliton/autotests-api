import pytest
from pydantic import BaseModel

from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema
)
from fixtures.courses import CourseFixture
from fixtures.users import UserFixture


class ExerciseFixture(BaseModel):
    """Фикстура для хранения данных о созданном задании"""
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture(scope="function")
def exercises_client(function_user: UserFixture) -> ExercisesClient:
    """
    Фикстура для создания клиента API заданий.

    Args:
        function_user: Фикстура с данными тестового пользователя

    Returns:
        ExercisesClient: Экземпляр клиента для работы с API заданий
    """
    return get_exercises_client(function_user.authentication_user)


@pytest.fixture(scope="function")
def function_exercise(
        exercises_client: ExercisesClient,
        function_course: CourseFixture,
        function_user: UserFixture
) -> ExerciseFixture:
    """
    Фикстура для автоматического создания тестового задания перед каждым тестом.

    Args:
        exercises_client: Клиент для работы с API заданий
        function_course: Фикстура с данными созданного курса
        function_user: Фикстура с данными тестового пользователя

    Returns:
        ExerciseFixture: Объект с данными запроса и ответа при создании задания
    """
    # Создаем запрос на создание задания
    request = CreateExerciseRequestSchema(
        course_id=function_course.response.course.id,
        created_by_user_id=function_user.response.user.id,
        title="Тестовое задание",
        description="Это автоматически созданное тестовое задание",
        max_score=100,
        duration_minutes=60
    )

    # Отправляем запрос на создание задания
    response = exercises_client.create_exercise(request)

    # Возвращаем объект с данными запроса и ответа
    return ExerciseFixture(request=request, response=response)
