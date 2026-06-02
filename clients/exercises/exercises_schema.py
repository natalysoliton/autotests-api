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
    estimated_time: int = Field(alias="estimatedTime")


class GetExercisesQuerySchema(BaseModel):
    """
    Описание структуры query-параметров для получения списка заданий.
    """
    model_config = ConfigDict(populate_by_name=True)

    course_id: Optional[str] = Field(default=None, alias="courseId")


class CreateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание задания.
    Все поля генерируются автоматически с помощью fake-данных.
    """
    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(alias="courseId")
    title: str = Field(default_factory=fake.sentence)
    description: str = Field(default_factory=fake.text)
    max_score: int = Field(default=100, alias="maxScore")
    min_score: int = Field(default=0, alias="minScore")
    order_index: int = Field(default=1, alias="orderIndex")
    estimated_time: int = Field(default=60, alias="estimatedTime")


class UpdateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление задания (PATCH).
    Все поля опциональны и генерируются автоматически.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: Optional[str] = Field(default_factory=fake.sentence)
    description: Optional[str] = Field(default_factory=fake.text)
    max_score: Optional[int] = Field(default=150, alias="maxScore")
    min_score: Optional[int] = Field(default=30, alias="minScore")
    order_index: Optional[int] = Field(default=5, alias="orderIndex")
    estimated_time: Optional[int] = Field(default=90, alias="estimatedTime")


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

    exercise: ExerciseSchema


class GetExercisesResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение списка заданий.
    """
    model_config = ConfigDict(populate_by_name=True)

    exercises: List[ExerciseSchema]
