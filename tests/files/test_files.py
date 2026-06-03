from http import HTTPStatus

import allure  # Импортируем allure
from allure_commons.types import Severity  # Импортируем enum Severity из Allure
from tools.allure.tags import AllureTag  # Импортируем enum с тегами
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory

import pytest

from clients.errors_schema import ValidationErrorResponseSchema, InternalErrorResponseSchema
from clients.files.files_client import FilesClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema, GetFileResponseSchema
from fixtures.files import FileFixture
from tools.assertions.base import assert_status_code
from tools.assertions.files import assert_create_file_response, assert_create_file_with_empty_filename_response, \
    assert_create_file_with_empty_directory_response, assert_file_not_found_response, \
    assert_get_file_with_incorrect_file_id_response, assert_get_file_response
from tools.assertions.schema import validate_json_schema



@pytest.mark.files
@pytest.mark.regression
@allure.tag(AllureTag.FILES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.FILES)
class TestFiles:
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create file")
    @allure.severity(Severity.BLOCKER)  # Добавили severity
    def test_create_file(self, files_client: FilesClient):
        # Arrange: Подготавливаем данные для создания файла
        request = CreateFileRequestSchema(upload_file="./testdata/files/image.png")

        # Act: Отправляем запрос на создание файла
        response = files_client.create_file_api(request)

        # Assert: Проверяем ответ API
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateFileResponseSchema.model_validate_json(response.text)

        # Проверяем, что данные в ответе соответствуют запросу
        assert_create_file_response(request, response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.title("Get file")
    @allure.severity(Severity.BLOCKER)  # Добавили severity
    def test_get_file(self, files_client: FilesClient, function_file: FileFixture):
        # Arrange: Получаем ID созданного файла из фикстуры
        file_id = function_file.response.file.id

        # Act: Отправляем GET-запрос на получение файла по ID
        response = files_client.get_file_api(file_id)

        # Assert: Проверяем ответ API
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetFileResponseSchema.model_validate_json(response.text)

        # Проверяем, что данные полученного файла соответствуют созданному
        assert_get_file_response(response_data, function_file.response)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.title("Delete file")
    @allure.severity(Severity.NORMAL)  # Добавили severity
    def test_delete_file(self, files_client: FilesClient, function_file: FileFixture):

        # Arrange: Получаем ID созданного файла из фикстуры
        file_id = function_file.response.file.id

        # Act 1: Отправляем DELETE-запрос на удаление файла
        delete_response = files_client.delete_file_api(file_id)

        # Assert 1: Проверяем успешное удаление
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # Act 2: Пытаемся получить удаленный файл
        get_response = files_client.get_file_api(file_id)

        # Assert 2: Проверяем, что файл не найден
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        # Десериализуем ответ с ошибкой
        error_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        # Проверяем, что ошибка соответствует ожидаемой
        assert_file_not_found_response(error_response_data)

        # Валидируем JSON-схему ответа с ошибкой
        validate_json_schema(get_response.json(), error_response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("Create file with empty filename")
    @allure.severity(Severity.NORMAL)  # Добавили severity
    def test_create_file_with_empty_filename(self, files_client: FilesClient):

        # Arrange: Подготавливаем данные с пустым именем файла
        request = CreateFileRequestSchema(
            filename="",
            upload_file="./testdata/files/image.png"
        )

        # Act: Отправляем запрос на создание файла
        response = files_client.create_file_api(request)

        # Assert: Проверяем ответ API
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        # Десериализуем ответ в модель ValidationErrorResponseSchema
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        # Проверяем, что ответ API соответствует ожидаемой валидационной ошибке
        assert_create_file_with_empty_filename_response(response_data)

        # Валидируем JSON-схему ответа с ошибкой
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("Create file with empty directory")
    @allure.severity(Severity.NORMAL)  # Добавили severity
    def test_create_file_with_empty_directory(self, files_client: FilesClient):

        # Arrange: Подготавливаем данные с пустой директорией
        request = CreateFileRequestSchema(
            directory="",
            upload_file="./testdata/files/image.png"
        )

        # Act: Отправляем запрос на создание файла
        response = files_client.create_file_api(request)

        # Assert: Проверяем ответ API
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        # Десериализуем ответ в модель ValidationErrorResponseSchema
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        # Проверяем, что ответ API соответствует ожидаемой валидационной ошибке
        assert_create_file_with_empty_directory_response(response_data)

        # Валидируем JSON-схему ответа с ошибкой
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("Get file with incorrect file id")
    @allure.severity(Severity.NORMAL)  # Добавили severity
    def test_get_file_with_incorrect_file_id(self, files_client: FilesClient):

        # Arrange: Некорректный идентификатор файла (не соответствует формату UUID)
        incorrect_file_id = "incorrect-file-id"

        # Act: Отправляем запрос на получение файла с некорректным ID
        response = files_client.get_file_api(incorrect_file_id)

        # Assert: Проверяем, что API вернул ошибку валидации
        # Десериализуем ответ в модель ValidationErrorResponseSchema
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        # Проверка статус-кода (ожидаем 422 Unprocessable Entity)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        # Проверка, что ответ API соответствует ожидаемой валидационной ошибке
        assert_get_file_with_incorrect_file_id_response(response_data)

        # Дополнительная проверка структуры JSON,
        # чтобы убедиться, что схема валидационного ответа не изменилась
        validate_json_schema(response.json(), response_data.model_json_schema())
