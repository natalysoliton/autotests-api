import httpx
from tools.fakers import get_random_email

BASE_URL = "http://localhost:8000"

# 1. Создаем пользователя
print("=" * 50)
print("ШАГ 1: Создание пользователя")
print("=" * 50)

create_user_payload = {
    "email": get_random_email(),
    "password": "Fg!23$test$fake",
    "lastName": "Тестов",
    "firstName": "Тест",
    "middleName": "Тестович"
}

create_user_response = httpx.post(f"{BASE_URL}/api/v1/users", json=create_user_payload)

if create_user_response.status_code != 200:
    print(f"Ошибка создания пользователя: {create_user_response.status_code}")
    print(f"Ответ: {create_user_response.text}")
    exit(1)

create_user_data = create_user_response.json()
print(f"Пользователь создан:")
print(f"   ID: {create_user_data['user']['id']}")
print(f"   Email: {create_user_data['user']['email']}")
print(f"   Имя: {create_user_data['user']['firstName']}")
print(f"   Фамилия: {create_user_data['user']['lastName']}")

# 2. Авторизуемся
print("\n" + "=" * 50)
print("ШАГ 2: Авторизация")
print("=" * 50)

login_payload = {
    "email": create_user_payload['email'],
    "password": create_user_payload['password']
}

login_response = httpx.post(f"{BASE_URL}/api/v1/authentication/login", json=login_payload)

if login_response.status_code != 200:
    print(f"Ошибка авторизации: {login_response.status_code}")
    print(f"Ответ: {login_response.text}")
    exit(1)

login_data = login_response.json()
access_token = login_data['token']['accessToken']
print(f" Авторизация успешна")
print(f"   Access Token получен")

# 3. Обновляем данные пользователя (PATCH)
print("\n" + "=" * 50)
print("ШАГ 3: Обновление пользователя (PATCH)")
print("=" * 50)

user_id = create_user_data['user']['id']
new_email = get_random_email()  # Генерируем новый уникальный email

update_payload = {
    "email": new_email,
    "lastName": "Петров",
    "firstName": "Петр",
    "middleName": "Петрович"
}

update_headers = {
    "Authorization": f"Bearer {access_token}"
}

update_response = httpx.patch(
    f"{BASE_URL}/api/v1/users/{user_id}",
    json=update_payload,
    headers=update_headers
)

if update_response.status_code != 200:
    print(f"Ошибка обновления пользователя: {update_response.status_code}")
    print(f"Ответ: {update_response.text}")
    exit(1)

update_response_data = update_response.json()
print(f"Пользователь обновлен:")
print(f"   Новый email: {update_response_data['user']['email']}")
print(f"   Новое имя: {update_response_data['user']['firstName']}")
print(f"   Новая фамилия: {update_response_data['user']['lastName']}")

# 4. Дополнительная проверка: получаем обновленные данные пользователя
print("\n" + "=" * 50)
print("ШАГ 4: Проверка обновленных данных (GET)")
print("=" * 50)

get_headers = {
    "Authorization": f"Bearer {access_token}"
}

get_response = httpx.get(
    f"{BASE_URL}/api/v1/users/{user_id}",
    headers=get_headers
)

if get_response.status_code != 200:
    print(f"Ошибка получения пользователя: {get_response.status_code}")
    exit(1)

get_data = get_response.json()
print(f" Данные получены:")
print(f"   Email: {get_data['user']['email']}")
print(f"   Имя: {get_data['user']['firstName']}")
print(f"   Фамилия: {get_data['user']['lastName']}")

# 5. Финальная проверка: соответствует ли обновление ожидаемому?
print("\n" + "=" * 50)
print("ШАГ 5: Финальная проверка")
print("=" * 50)

if (get_data['user']['email'] == new_email and
    get_data['user']['firstName'] == "Петр" and
    get_data['user']['lastName'] == "Петров"):
    print(" ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ! Пользователь успешно обновлен.")
else:
    print(" ОШИБКА: Данные не совпадают с ожидаемыми!")

print("\n" + "=" * 50)
print("ИТОГОВЫЙ РЕЗУЛЬТАТ")
print("=" * 50)
print(f"Статус создания пользователя: {create_user_response.status_code}")
print(f"Статус авторизации: {login_response.status_code}")
print(f"Статус обновления (PATCH): {update_response.status_code}")
print(f"Статус проверки (GET): {get_response.status_code}")
