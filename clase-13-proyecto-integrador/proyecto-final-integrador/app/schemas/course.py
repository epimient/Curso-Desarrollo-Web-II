from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CourseCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    credits: int = Field(ge=1, le=6)


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=80)
    credits: Optional[int] = Field(default=None, ge=1, le=6)
    active: Optional[bool] = None


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    credits: int
    active: bool
