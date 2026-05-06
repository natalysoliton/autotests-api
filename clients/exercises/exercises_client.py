from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class GetExercisesQueryDict(TypedDict):
    """
    Описание структуры запроса на получение списка заданий.
    """
    courseId: str


class CreateExerciseRequestDict(TypedDict):
    """
    Описание структуры запроса на создание задания.
    """
    title: str
    description: str
    maxScore: int
    courseId: str


class UpdateExerciseRequestDict(TypedDict):
    """
    Описание структуры запроса на обновление задания.

    Поля имеют тип str | None или int | None, так как PATCH-запрос
    обновляет только те поля, которые явно указаны в запросе.
    Если поле не передано (None), оно остается неизменным.
    """
    title: str | None
    description: str | None
    maxScore: int | None


class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises.

    Предоставляет методы для выполнения операций CRUD с заданиями:
    - получение списка заданий для определенного курса
    - получение информации о конкретном задании
    - создание нового задания
    - обновление существующего задания
    - удаление задания
    """

    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """
        Получение списка заданий для определенного курса.

        Метод выполняет GET-запрос к эндпоинту /api/v1/exercises
        и передает courseId в качестве query-параметра.

        :param query: Словарь с courseId - идентификатор курса,
                      для которого необходимо получить список заданий.
        :return: Ответ от сервера в виде объекта httpx.Response.
                 В случае успеха (200 OK) тело ответа содержит список заданий.
        """
        return self.get("/api/v1/exercises", params=query)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Получение информации о задании по его идентификатору.

        :param exercise_id: Идентификатор задания (строка UUID).
        :return: Ответ от сервера в виде объекта httpx.Response.
                 При успешном выполнении (200 OK) тело ответа содержит
                 полную информацию о задании: id, title, description,
                 maxScore, courseId.
        """
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
        """
        Создание нового задания.

        Метод отправляет POST-запрос с данными нового задания в формате JSON.

        :param request: Словарь с обязательными полями:
                       - title: Название задания
                       - description: Описание задания
                       - maxScore: Максимальный балл за задание
                       - courseId: Идентификатор курса, к которому относится задание
        :return: Ответ от сервера в виде объекта httpx.Response.
                 При успешном создании (201 Created) тело ответа содержит
                 созданный объект задания с присвоенным id.
        """
        return self.post("/api/v1/exercises", json=request)

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Response:
        """
        Обновление данных существующего задания.

        Метод выполняет PATCH-запрос, который обновляет только те поля,
        которые явно указаны в запросе. Поля со значением None игнорируются.

        :param exercise_id: Идентификатор обновляемого задания.
        :param request: Словарь с необязательными полями для обновления:
                       - title: Новое название задания (или None)
                       - description: Новое описание задания (или None)
                       - maxScore: Новый максимальный балл (или None)
        :return: Ответ от сервера в виде объекта httpx.Response.
                 При успешном обновлении (200 OK) тело ответа содержит
                 обновленный объект задания.
        """
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Удаление задания по его идентификатору.

        :param exercise_id: Идентификатор задания для удаления.
        :return: Ответ от сервера в виде объекта httpx.Response.
                 При успешном удалении возвращается статус 204 No Content.
                 Тело ответа пустое.
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")
