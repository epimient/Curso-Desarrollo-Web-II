from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.schemas.course import CourseResponse
from app.services.student_service import create_student, get_student, list_students
from app.services.enrollment_service import get_courses_by_student

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=list[StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return list_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    return get_student(student_id, db)


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    return create_student(student_data, db)


@router.get("/{student_id}/courses", response_model=list[CourseResponse])
def read_student_courses(student_id: int, db: Session = Depends(get_db)):
    return get_courses_by_student(student_id, db)
