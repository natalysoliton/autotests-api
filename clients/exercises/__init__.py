from clients.exercises.exercises_client import (
    ExercisesClient,
    get_exercises_client,
    ExerciseSchema,
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExercisesQuerySchema,
    GetExercisesResponseSchema,
)

__all__ = [
    'ExercisesClient',
    'get_exercises_client',
    'ExerciseSchema',
    'CreateExerciseRequestSchema',
    'CreateExerciseResponseSchema',
    'GetExercisesQuerySchema',
    'GetExercisesResponseSchema',
]

from clients.exercises.exercises_schema import ExerciseSchema
