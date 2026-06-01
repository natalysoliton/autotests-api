import httpx

# Вместо get_random_email импортируем fake
from tools.fakers import fake

payload = {
    "email": fake.email(),  # Вместо get_random_email() используем fake.email()
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}
response = httpx.post("http://localhost:8000/api/v1/users", json=payload)

print(response.status_code)
print(response.json())
