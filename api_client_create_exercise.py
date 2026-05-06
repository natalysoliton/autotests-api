"""
Скрипт для создания задания с использованием API-клиентов.
"""

import sys
import os

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from clients.users.public_users_client import get_public_users_client, CreateUserRequestDict
from clients.private_http_builder import AuthenticationUserDict
from clients.files.files_client import get_files_client, CreateFileRequestDict
from clients.courses.courses_client import get_courses_client, CreateCourseRequestDict
from clients.exercises.exercises_client import get_exercises_client, CreateExerciseRequestDict
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

    create_user_request = CreateUserRequestDict(
        email=get_random_email(),
        password="string123",
        lastName="Иванов",
        firstName="Иван",
        middleName="Петрович"
    )

    try:
        create_user_response = public_users_client.create_user(create_user_request)
        print(f"   Пользователь создан: {create_user_response['user']['email']}")
        print(f"   ID пользователя: {create_user_response['user']['id']}")
    except Exception as e:
        print(f"   Ошибка создания пользователя: {e}")
        return

    # 2. Инициализация приватных клиентов
    print("\n2. Инициализация приватных клиентов...")
    authentication_user = AuthenticationUserDict(
        email=create_user_request['email'],
        password=create_user_request['password']
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

    create_file_request = CreateFileRequestDict(
        filename="course_preview.png",
        directory="courses",
        upload_file=file_path
    )

    try:
        create_file_response = files_client.create_file(create_file_request)
        print(f"   Файл загружен")
        print(f"   ID файла: {create_file_response['file']['id']}")
    except Exception as e:
        print(f"   Ошибка загрузки файла: {e}")
        return

    # 4. Создание курса
    print("\n4. Создание курса...")
    create_course_request = CreateCourseRequestDict(
        title="Python API Course",
        maxScore=100,
        minScore=10,
        description="Курс по разработке API на Python",
        estimatedTime="2 weeks",
        previewFileId=create_file_response['file']['id'],
        createdByUserId=create_user_response['user']['id']
    )

    try:
        create_course_response = courses_client.create_course(create_course_request)
        print(f"   Курс создан: {create_course_response['course']['title']}")
        print(f"   ID курса: {create_course_response['course']['id']}")
    except Exception as e:
        print(f"   Ошибка создания курса: {e}")
        return

    # 5. Создание задания
    print("\n5. Создание задания...")
    create_exercise_request = CreateExerciseRequestDict(
        title="Exercise 1: Основы HTTP",
        courseId=create_course_response['course']['id'],
        maxScore=100,
        minScore=10,
        orderIndex=0,
        description="Первое упражнение: знакомство с HTTP-протоколом",
        estimatedTime="10 minutes"
    )

    try:
        create_exercise_response = exercises_client.create_exercise(create_exercise_request)
        print(f"  Задание создано: {create_exercise_response['exercise']['title']}")
        print(f"  ID задания: {create_exercise_response['exercise']['id']}")
        print(f"\n Данные задания: {create_exercise_response}")
    except Exception as e:
        print(f" Ошибка создания задания: {e}")
        return

    print("\n" + "=" * 60)
    print(" Задание успешно создано!")
    print("=" * 60)


if __name__ == "__main__":
    main()
