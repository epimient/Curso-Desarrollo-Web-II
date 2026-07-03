from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.enrollment import EnrollmentStatus


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentUpdate(BaseModel):
    grade: Optional[float] = None
    status: Optional[EnrollmentStatus] = None


class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    course_id: int
    grade: Optional[float] = None
    status: EnrollmentStatus
