from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    UpdateCourseRequestSchema,
    UpdateCourseResponseSchema,
    GetCourseResponseSchema,
    GetCoursesResponseSchema
)


class CoursesClient(APIClient):
    """
    Клиент для работы с /api/v1/courses
    """

    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        """
        Метод создания курса.

        :param request: Модель запроса на создание курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post("/api/v1/courses", json=request.model_dump(by_alias=True))

    def get_course_api(self, course_id: str) -> Response:
        """
        Метод получения курса по идентификатору.

        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"/api/v1/courses/{course_id}")

    def get_courses_api(self) -> Response:
        """
        Метод получения списка всех курсов.

        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get("/api/v1/courses")

    def update_course_api(self, course_id: str, request: UpdateCourseRequestSchema) -> Response:
        """
        Метод обновления курса.

        :param course_id: Идентификатор курса.
        :param request: Модель запроса на обновление курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(f"/api/v1/courses/{course_id}", json=request.model_dump(by_alias=True, exclude_none=True))

    def delete_course_api(self, course_id: str) -> Response:
        """
        Метод удаления курса.

        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"/api/v1/courses/{course_id}")

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        """
        Метод создания курса с автоматической десериализацией ответа.

        :param request: Модель запроса на создание курса.
        :return: Модель ответа с данными созданного курса.
        """
        response = self.create_course_api(request)
        return CreateCourseResponseSchema.model_validate_json(response.text)

    def get_course(self, course_id: str) -> GetCourseResponseSchema:
        """
        Метод получения курса с автоматической десериализацией ответа.

        :param course_id: Идентификатор курса.
        :return: Модель ответа с данными курса.
        """
        response = self.get_course_api(course_id)
        return GetCourseResponseSchema.model_validate_json(response.text)

    def get_courses(self) -> GetCoursesResponseSchema:
        """
        Метод получения списка курсов с автоматической десериализацией ответа.

        :return: Модель ответа со списком курсов.
        """
        response = self.get_courses_api()
        return GetCoursesResponseSchema.model_validate_json(response.text)

    def update_course(self, course_id: str, request: UpdateCourseRequestSchema) -> UpdateCourseResponseSchema:
        """
        Метод обновления курса с автоматической десериализацией ответа.

        :param course_id: Идентификатор курса.
        :param request: Модель запроса на обновление курса.
        :return: Модель ответа с обновленными данными курса.
        """
        response = self.update_course_api(course_id, request)
        return UpdateCourseResponseSchema.model_validate_json(response.text)


def get_courses_client(user: AuthenticationUserSchema) -> CoursesClient:
    """
    Функция создаёт экземпляр CoursesClient с уже настроенным HTTP-клиентом.

    :param user: Модель аутентификации пользователя.
    :return: Готовый к использованию CoursesClient.
    """
    return CoursesClient(client=get_private_http_client(user))
