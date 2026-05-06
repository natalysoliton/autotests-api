"""
Модуль для работы с API заданий (exercises).

Содержит клиент ExercisesClient для взаимодействия с эндпоинтами /api/v1/exercises.
"""

from clients.exercises.exercises_client import ExercisesClient

__all__ = ["ExercisesClient"]
