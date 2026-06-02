from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    ExerciseSchema
)
from tools.assertions.base import assert_equal


def assert_create_exercise_response(
        request: CreateExerciseRequestSchema,
        response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на создание задания соответствует данным из запроса.

    Функция проверяет:
    - Наличие ID созданного задания
    - Соответствие ID курса переданному значению
    - Соответствие названия задания переданному значению
    - Соответствие описания задания переданному значению
    - Соответствие максимального балла переданному значению
    - Соответствие длительности выполнения переданному значению

    Args:
        request: Исходный запрос на создание задания (CreateExerciseRequestSchema)
        response: Ответ API с данными созданного задания (CreateExerciseResponseSchema)

    Returns:
        None

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает или отсутствует
    """
    # Проверяем, что в ответе присутствует объект задания
    assert response.exercise is not None, "Exercise object is missing in response"

    # Проверяем, что ID задания присутствует (не None)
    assert response.exercise.id is not None, "Exercise ID is missing in response"

    # Проверяем, что ID имеет правильный формат (строка, не пустая)
    assert isinstance(response.exercise.id, str), "Exercise ID should be a string"
    assert len(response.exercise.id) > 0, "Exercise ID should not be empty"

    # Проверяем соответствие всех полей задания
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.duration_minutes, request.duration_minutes, "duration_minutes")


def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что фактические данные задания соответствуют ожидаемым.

    Функция выполняет поэлементное сравнение всех ключевых полей модели задания.

    Args:
        actual: Фактические данные задания (из ответа API)
        expected: Ожидаемые данные задания (эталонные данные)

    Returns:
        None

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.duration_minutes, expected.duration_minutes, "duration_minutes")


def assert_get_exercise_response(
        get_exercise_response: GetExerciseResponseSchema,
        create_exercise_response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на получение задания соответствует ответу на его создание.

    Функция проверяет, что данные задания, полученные через GET-запрос,
    полностью совпадают с данными, которые были возвращены при создании задания.
    Это гарантирует, что задание корректно сохранилось в системе и доступно для чтения.

    Args:
        get_exercise_response: Ответ API при запросе данных задания (GetExerciseResponseSchema)
        create_exercise_response: Ответ API при создании задания (CreateExerciseResponseSchema)

    Returns:
        None

    Raises:
        AssertionError: Если данные задания не совпадают

    Examples:
        >>> get_response = exercises_client.get_exercise_api(exercise_id)
        >>> get_data = GetExerciseResponseSchema.model_validate_json(get_response.text)
        >>> assert_get_exercise_response(get_data, create_exercise_response)
    """
    # Проверяем, что оба объекта существуют
    assert get_exercise_response is not None, "Get exercise response is None"
    assert create_exercise_response is not None, "Create exercise response is None"
    assert get_exercise_response.exercise is not None, "Exercise in get response is None"
    assert create_exercise_response.exercise is not None, "Exercise in create response is None"

    # Сравниваем данные задания из GET-ответа с данными из CREATE-ответа
    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)
