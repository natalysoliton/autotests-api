from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import UpdateCourseRequestSchema, UpdateCourseResponseSchema, GetCoursesQuerySchema, \
    GetCoursesResponseSchema, CreateCourseRequestSchema, CreateCourseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.files import FileFixture
from fixtures.users import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.courses import assert_update_course_response, assert_get_courses_response, \
    assert_create_course_response
from tools.assertions.schema import validate_json_schema
from tools.allure.tags import AllureTag
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory


@pytest.mark.courses
@pytest.mark.regression
@allure.tag(AllureTag.COURSES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.parent_suite(AllureEpic.LMS)  # Добавили parent_suite
@allure.suite(AllureFeature.COURSES)  # Добавили suite
class TestCourses:

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)  # Добавили sub_suite
    @allure.title("Create course")
    @allure.severity(Severity.BLOCKER)
    def test_create_course(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # Arrange: Подготавливаем данные для создания курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id
        )

        # Act: Отправляем запрос на создание курса
        response = courses_client.create_course_api(request)

        # Assert: Проверяем ответ API
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        assert_create_course_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)  # Добавили sub_suite
    @allure.title("Get courses")
    @allure.severity(Severity.BLOCKER)
    def test_get_courses(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_course: CourseFixture
    ):
        # Arrange: Формируем параметры запроса, передавая user_id
        query = GetCoursesQuerySchema(user_id=function_user.response.user.id)

        # Act: Отправляем GET-запрос на получение списка курсов
        response = courses_client.get_courses_api(query)

        # Assert: Проверяем ответ API
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetCoursesResponseSchema.model_validate_json(response.text)
        assert_get_courses_response(response_data, [function_course.response])
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)  # Добавили sub_suite
    @allure.title("Update course")
    @allure.severity(Severity.CRITICAL)
    def test_update_course(self, courses_client: CoursesClient, function_course: CourseFixture):
        # Arrange: Получаем ID созданного курса из фикстуры
        course_id = function_course.response.course.id

        # Формируем данные для обновления курса
        request = UpdateCourseRequestSchema(
            title="Обновленное название курса",
            description="Обновленное описание курса",
            max_score=150,
            min_score=30,
            estimated_time=90
        )

        # Act: Отправляем PATCH-запрос на обновление курса
        response = courses_client.update_course_api(course_id, request)

        # Assert: Проверяем ответ API
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)
        assert_update_course_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())
