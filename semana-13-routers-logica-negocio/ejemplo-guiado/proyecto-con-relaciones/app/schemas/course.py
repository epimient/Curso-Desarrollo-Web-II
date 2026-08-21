from pydantic import BaseModel, Field, ConfigDict

from app.schemas.student import StudentResponse


class CourseCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    credits: int = Field(ge=1, le=6)


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    credits: int
    active: bool


class CourseWithStudentsResponse(CourseResponse):
    students: list[StudentResponse] = []
