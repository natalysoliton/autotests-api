# tools/allure/environment.py
import platform
import sys
from config import settings


def create_allure_environment_file():
    """
    Создает файл environment.properties в директории allure-results.
    Файл содержит информацию об окружении: настройки проекта, ОС, версию Python.
    """
    # Получаем информацию об операционной системе
    os_info = f"{platform.system()}, {platform.release()}"

    # Получаем информацию о версии Python
    python_version = sys.version

    # Создаем список из элементов в формате {key}={value}
    items = []

    # Добавляем информацию об ОС и Python
    items.append(f"os_info={os_info}")
    items.append(f"python_version={python_version}")

    # Добавляем остальные настройки проекта
    for key, value in settings.model_dump().items():
        items.append(f'{key}={value}')

    # Собираем все элементы в единую строку с переносами
    properties = '\n'.join(items)

    # Открываем файл ./allure-results/environment.properties на запись
    env_file_path = settings.allure_results_dir.joinpath('environment.properties')
    with open(env_file_path, 'w+', encoding='utf-8') as file:
        file.write(properties)
