from http import HTTPStatus

import pytest

from clients.errors_schema import ValidationErrorResponseSchema, InternalErrorResponseSchema
from clients.files.files_client import FilesClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema, GetFileResponseSchema
from fixtures.files import FileFixture
from tools.assertions.base import assert_status_code
from tools.assertions.files import (
    assert_create_file_response,
    assert_get_file_response,
    assert_create_file_with_empty_filename_response,
    assert_create_file_with_empty_directory_response,
    assert_file_not_found_response,
    assert_get_file_with_incorrect_file_id_response  # Импортируем новую функцию
)
from tools.assertions.schema import validate_json_schema


@pytest.mark.files
@pytest.mark.regression
class TestFiles:
    # Остальные тесты (test_create_file, test_get_file,
    # test_create_file_with_empty_filename, test_create_file_with_empty_directory,
    # test_delete_file) остаются без изменений

    def test_get_file_with_incorrect_file_id(self, files_client: FilesClient):
        """
        Негативный тест для проверки получения файла с некорректным идентификатором.

        Тест проверяет, что API корректно обрабатывает ситуацию, когда вместо
        валидного UUID в параметре file_id передается некорректная строка.

        Шаги теста:
        1. Отправить запрос на получение файла с file_id = "incorrect-file-id"
        2. Проверить, что API возвращает статус-код 422 (Unprocessable Entity)
        3. Проверить, что валидационная ошибка соответствует ожидаемой
        4. Проверить, что структура JSON-ответа соответствует схеме ошибки валидации

        Args:
            files_client: Фикстура с клиентом для работы с API файлов
        """
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
