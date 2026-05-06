from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client
from clients.files.files_client import File
from clients.users.public_users_client import User


class Course(TypedDict):
    id: str
    title: str
    maxScore: int
    minScore: int
    description: str
    previewFile: File
    estimatedTime: str
    createdByUser: User


class CreateCourseRequestDict(TypedDict):
    title: str
    maxScore: int
    minScore: int
    description: str
    estimatedTime: str
    previewFileId: str
    createdByUserId: str


class CreateCourseResponseDict(TypedDict):
    course: Course


class CoursesClient(APIClient):
    """
    Клиент для работы с /api/v1/courses
    """

    def create_course_api(self, request: CreateCourseRequestDict) -> Response:
        """
        Метод создания курса.
        """
        return self.post("/api/v1/courses", json=request)

    def create_course(self, request: CreateCourseRequestDict) -> CreateCourseResponseDict:
        """
        Метод создания курса с автоматическим извлечением JSON.
        """
        response = self.create_course_api(request)
        return response.json()


def get_courses_client(user: AuthenticationUserDict) -> CoursesClient:
    """
    Функция создаёт экземпляр CoursesClient с уже настроенным HTTP-клиентом.
    """
    return CoursesClient(client=get_private_http_client(user))
