import httpx  # Импортируем библиотеку HTTPX

# Инициализируем JSON-данные, которые будем отправлять в API
payload = {
    "email": "user@example.com",
    "password": "string"
}

# Выполняем POST-запрос к эндпоинту /api/v1/authentication/login
response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=payload)

# Выводим JSON-ответ и статус-код
print(response.json())
print(response.status_code)