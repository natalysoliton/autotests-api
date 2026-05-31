from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.fakers import get_random_email

public_users_client = get_public_users_client()

# Создаем пользователя
create_user_request = CreateUserRequestSchema(
    email=get_random_email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)
create_user_response = public_users_client.create_user(create_user_request)

# Инициализируем клиенты
authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,  # Используем атрибут вместо ключа
    password=create_user_request.password  # Используем атрибут вместо ключа
)
files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)

# Загружаем файл
create_file_request = CreateFileRequestSchema(
    filename="image.png",
    directory="courses",
    upload_file="./testdata/files/image.png"
)
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

# Создаем курс - используем Pydantic модель вместо TypedDict
create_course_request = CreateCourseRequestSchema(
    title="Python",
    max_score=100,  # snake_case вместо camelCase
    min_score=10,
    description="Python API course",
    estimated_time="2 weeks",
    preview_file_id=create_file_response.file.id,  # Используем атрибут
    created_by_user_id=create_user_response.user.id  # Используем атрибут
)
create_course_response = courses_client.create_course(create_course_request)
print('Create course data:', create_course_response)

# Демонстрация доступа к данным через атрибуты
print(f"\nСозданный курс:")
print(f"  ID: {create_course_response.course.id}")
print(f"  Title: {create_course_response.course.title}")
print(f"  Max Score: {create_course_response.course.max_score}")
print(f"  Created by: {create_course_response.course.created_by_user.email}")
