import sys
import os

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.exercises.exercises_client import get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema
from tools.fakers import get_random_email


def main():
    """
    Основная функция скрипта для создания задания.
    """
    print("=" * 60)
    print("Начало создания задания (упражнения)")
    print("=" * 60)

    # 1. Создание пользователя
    print("\n1. Создание пользователя...")
    public_users_client = get_public_users_client()

    create_user_request = CreateUserRequestSchema(
        email=get_random_email(),
        password="string123",
        last_name="Иванов",  # snake_case вместо lastName
        first_name="Иван",  # snake_case вместо firstName
        middle_name="Петрович"  # snake_case вместо middleName
    )

    try:
        create_user_response = public_users_client.create_user(create_user_request)
        print(f"   Пользователь создан: {create_user_response.user.email}")  # Используем атрибут
        print(f"   ID пользователя: {create_user_response.user.id}")  # Используем атрибут
    except Exception as e:
        print(f"   Ошибка создания пользователя: {e}")
        return

    # 2. Инициализация приватных клиентов
    print("\n2. Инициализация приватных клиентов...")
    authentication_user = AuthenticationUserSchema(
        email=create_user_request.email,  # Используем атрибут
        password=create_user_request.password  # Используем атрибут
    )

    try:
        files_client = get_files_client(authentication_user)
        courses_client = get_courses_client(authentication_user)
        exercises_client = get_exercises_client(authentication_user)
        print("  Клиенты успешно инициализированы")
    except Exception as e:
        print(f"   Ошибка инициализации клиентов: {e}")
        return

    # 3. Загрузка файла
    print("\n3. Загрузка файла...")
    file_path = "./testdata/files/image.png"

    if not os.path.exists(file_path):
        print(f"   Файл не найден: {file_path}")
        print("   Создайте файл image.png в папке testdata/files/")
        return

    create_file_request = CreateFileRequestSchema(
        filename="course_preview.png",
        directory="courses",
        upload_file=file_path
    )

    try:
        create_file_response = files_client.create_file(create_file_request)
        print(f"   Файл загружен")
        print(f"   ID файла: {create_file_response.file.id}")  # Используем атрибут
    except Exception as e:
        print(f"   Ошибка загрузки файла: {e}")
        return

    # 4. Создание курса
    print("\n4. Создание курса...")
    create_course_request = CreateCourseRequestSchema(
        title="Python API Course",
        max_score=100,  # snake_case
        min_score=10,
        description="Курс по разработке API на Python",
        estimated_time="2 weeks",
        preview_file_id=create_file_response.file.id,  # Используем атрибут
        created_by_user_id=create_user_response.user.id  # Используем атрибут
    )

    try:
        create_course_response = courses_client.create_course(create_course_request)
        print(f"   Курс создан: {create_course_response.course.title}")
        print(f"   ID курса: {create_course_response.course.id}")
    except Exception as e:
        print(f"   Ошибка создания курса: {e}")
        return

    # 5. Создание задания
    print("\n5. Создание задания...")
    create_exercise_request = CreateExerciseRequestSchema(
        title="Exercise 1: Основы HTTP",
        course_id=create_course_response.course.id,  # snake_case, используем атрибут
        max_score=100,
        min_score=10,
        order_index=0,
        description="Первое упражнение: знакомство с HTTP-протоколом",
        estimated_time="10 minutes"
    )

    try:
        create_exercise_response = exercises_client.create_exercise(create_exercise_request)
        print(f"  Задание создано: {create_exercise_response.exercise.title}")
        print(f"  ID задания: {create_exercise_response.exercise.id}")
        print(f"\n Данные задания: {create_exercise_response}")

        # Демонстрация доступа к данным через атрибуты
        print(f"\nДетали задания:")
        print(f"  Название: {create_exercise_response.exercise.title}")
        print(f"  Max Score: {create_exercise_response.exercise.max_score}")
        print(f"  Order Index: {create_exercise_response.exercise.order_index}")
        print(f"  Description: {create_exercise_response.exercise.description}")
    except Exception as e:
        print(f" Ошибка создания задания: {e}")
        return

    print("\n" + "=" * 60)
    print(" Задание успешно создано!")
    print("=" * 60)


if __name__ == "__main__":
    main()
