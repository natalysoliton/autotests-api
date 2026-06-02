"""
Модуль с Pydantic-схемами для API заданий (exercises).
Содержит модели запросов и ответов для всех операций с заданиями.
"""

from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from tools.fakers import fake


class ExerciseSchema(BaseModel):
    """
    Описание структуры задания (базовая модель).
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: int = Field(alias="estimatedTime")  # int, а не str


class GetExercisesQuerySchema(BaseModel):
    """
    Описание структуры query-параметров для получения списка заданий.
    """
    model_config = ConfigDict(populate_by_name=True)

    course_id: Optional[str] = Field(default=None, alias="courseId")
    created_by_user_id: Optional[str] = Field(default=None, alias="createdByUserId")


class CreateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание задания.
    Все поля имеют значения по умолчанию для упрощения тестирования.
    """
    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(alias="courseId")
    title: Optional[str] = Field(default_factory=fake.sentence)
    description: Optional[str] = Field(default_factory=fake.text)
    max_score: Optional[int] = Field(default=100, alias="maxScore")
    min_score: Optional[int] = Field(default=0, alias="minScore")
    order_index: Optional[int] = Field(default=1, alias="orderIndex")
    estimated_time: Optional[int] = Field(default=60, alias="estimatedTime")


class UpdateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление задания (PATCH).
    Все поля опциональны для поддержки частичного обновления.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: Optional[str] = None  # Без default_factory!
    description: Optional[str] = None
    max_score: Optional[int] = Field(default=None, alias="maxScore")
    min_score: Optional[int] = Field(default=None, alias="minScore")
    order_index: Optional[int] = Field(default=None, alias="orderIndex")
    estimated_time: Optional[int] = Field(default=None, alias="estimatedTime")


# Response модели (все переиспользуют ExerciseSchema)
class CreateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    exercise: ExerciseSchema


class GetExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    exercise: ExerciseSchema


class UpdateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа на обновление задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    exercise: ExerciseSchema  # Возвращаем полный объект, а не отдельные поля


class GetExercisesResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение списка заданий.
    """
    model_config = ConfigDict(populate_by_name=True)

    exercises: List[ExerciseSchema]
