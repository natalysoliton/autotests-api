from httpx import Response
import allure  # Импортируем allure

from clients.api_client import APIClient
from clients.exercises.exercises_schema import GetExercisesQuerySchema, CreateExerciseRequestSchema, \
    UpdateExerciseRequestSchema, GetExercisesResponseSchema, GetExerciseResponseSchema, CreateExerciseResponseSchema, \
    UpdateExerciseResponseSchema
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from tools.routes import APIRoutes  # Импортируем enum APIRoutes


class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises
    """

    @allure.step("Get exercises")  # Добавили allure шаг
    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """
        Метод получения списка заданий.

        :param query: Словарь с courseId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        # Заменяем хардкод "/api/v1/exercises" на APIRoutes.EXERCISES
        return self.get(APIRoutes.EXERCISES, params=query.model_dump(by_alias=True))

    @allure.step("Get exercise by id {exercise_id}")  # Добавили allure шаг
    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод получения задания.

        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        # Заменяем хардкод "/api/v1/exercises" на APIRoutes.EXERCISES
        return self.get(f"{APIRoutes.EXERCISES}/{exercise_id}")

    @allure.step("Create exercise")  # Добавили allure шаг
    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """
        Метод создания задания.

        :param request: Словарь с title, courseId, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        # Заменяем хардкод "/api/v1/exercises" на APIRoutes.EXERCISES
        return self.post(APIRoutes.EXERCISES, json=request.model_dump(by_alias=True))

    @allure.step("Update exercise by id {exercise_id}")  # Добавили allure шаг
    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
        """
        Метод обновления задания.

        :param exercise_id: Идентификатор задания.
        :param request: Словарь с title, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        # Заменяем хардкод "/api/v1/exercises" на APIRoutes.EXERCISES
        return self.patch(
            f"{APIRoutes.EXERCISES}/{exercise_id}",
            json=request.model_dump(by_alias=True, exclude_none=True)
        )

    @allure.step("Delete exercise by id {exercise_id}")  # Добавили allure шаг
    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод удаления задания.

        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        # Заменяем хардкод "/api/v1/exercises" на APIRoutes.EXERCISES
        return self.delete(f"{APIRoutes.EXERCISES}/{exercise_id}")

    @allure.step("Get exercises and deserialize response")  # Добавили allure шаг
    def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        """
        Получает список заданий и десериализует ответ.

        :param query: Параметры запроса (courseId)
        :return: Десериализованный ответ API
        """
        response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    @allure.step("Get exercise by id {exercise_id} and deserialize response")  # Добавили allure шаг
    def get_exercise(self, exercise_id: str) -> GetExerciseResponseSchema:
        """
        Получает задание по ID и десериализует ответ.

        :param exercise_id: Идентификатор задания
        :return: Десериализованный ответ API
        """
        response = self.get_exercise_api(exercise_id)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Create exercise and deserialize response")  # Добавили allure шаг
    def create_exercise(self, request: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        """
        Создает задание и десериализует ответ.

        :param request: Данные для создания задания
        :return: Десериализованный ответ API
        """
        response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Update exercise by id {exercise_id} and deserialize response")  # Добавили allure шаг
    def update_exercise(
            self,
            exercise_id: str,
            request: UpdateExerciseRequestSchema
    ) -> UpdateExerciseResponseSchema:
        """
        Обновляет задание и десериализует ответ.

        :param exercise_id: Идентификатор задания
        :param request: Данные для обновления задания
        :return: Десериализованный ответ API
        """
        response = self.update_exercise_api(exercise_id, request)
        return UpdateExerciseResponseSchema.model_validate_json(response.text)


def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    :param user: Данные пользователя для аутентификации
    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))


class ExerciseSchema:
    pass