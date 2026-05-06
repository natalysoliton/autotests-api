import httpx

"""
Скрипт для получения данных пользователя через API с использованием JWT-аутентификации.
Шаги:
1. POST /api/v1/authentication/login - получаем accessToken
2. GET /api/v1/users/me - получаем данные пользователя с использованием токена
"""

# Данные для аутентификации
login_payload = {
    "email": "natalysoliton@mail.ru",
    "password": "Fg!23$test$fake"
}

# Базовый URL API (локальный сервер)
BASE_URL = "http://localhost:8000"

print("=" * 60)
print("ШАГ 1: Аутентификация и получение accessToken")
print("=" * 60)

try:
    # Выполняем POST-запрос к эндпоинту /api/v1/authentication/login
    login_response = httpx.post(
        f"{BASE_URL}/api/v1/authentication/login",
        json=login_payload,
        timeout=10.0  # Добавляем таймаут
    )

    # Выводим статус-код ответа
    print(f"Статус-код ответа: {login_response.status_code}")

    # Проверяем успешность запроса
    login_response.raise_for_status()

    # Парсим JSON-ответ
    login_response_data = login_response.json()

    # Извлекаем accessToken из ответа
    access_token = login_response_data["token"]["accessToken"]

    print("Аутентификация успешна!")
    print(f"accessToken получен: {access_token[:50]}...")  # Показываем только начало токена
    print(f"Статус: {login_response.status_code}")

except httpx.HTTPStatusError as e:
    print(f"Ошибка аутентификации: {e}")
    print(f"Ответ сервера: {e.response.text}")
    exit(1)
except httpx.TimeoutException:
    print("Превышено время ожидания ответа от сервера")
    exit(1)
except Exception as e:
    print(f"Непредвиденная ошибка: {e}")
    exit(1)

print("\n" + "=" * 60)
print("ШАГ 2: Получение данных о пользователе через /api/v1/users/me")
print("=" * 60)

try:
    # Формируем заголовок с Bearer-токеном
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Выполняем GET-запрос к эндпоинту /api/v1/users/me
    user_response = httpx.get(
        f"{BASE_URL}/api/v1/users/me",
        headers=headers,
        timeout=10.0  # Добавляем таймаут
    )

    # Выводим статус-код
    print(f"Статус-код ответа: {user_response.status_code}")

    # Проверяем успешность запроса
    user_response.raise_for_status()

    # Парсим JSON-ответ с данными пользователя
    user_data = user_response.json()

    print("\nДанные пользователя успешно получены!")
    print(f"Статус: {user_response.status_code}")

    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТ:")
    print("=" * 60)

    # выводим JSON-ответ в консоль
    import json

    print(json.dumps(user_data, indent=2, ensure_ascii=False))

    print("\n" + "=" * 60)
    print(f"ИТОГОВЫЙ СТАТУС-КОД: {user_response.status_code}")
    print("=" * 60)

except httpx.HTTPStatusError as e:
    print(f"Ошибка при получении данных пользователя: {e}")
    print(f"Статус-код: {e.response.status_code}")
    print(f"Ответ сервера: {e.response.text}")

    # Дополнительная диагностика
    if e.response.status_code == 401:
        print("\nВозможные причины:")
        print("- accessToken истек или недействителен")
        print("- Заголовок Authorization сформирован неправильно")
        print("- Токен не передан в запросе")
    elif e.response.status_code == 403:
        print("\nДоступ запрещен. Возможно, у пользователя недостаточно прав.")
    exit(1)

except httpx.TimeoutException:
    print("Превышено время ожидания ответа от сервера")
    exit(1)
except Exception as e:
    print(f"Непредвиденная ошибка: {e}")
    exit(1)

print("\nСкрипт выполнен успешно!")
