from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course import CourseCreate, CourseResponse
from app.services.course_service import create_course, get_course, list_courses

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=list[CourseResponse])
def read_courses(db: Session = Depends(get_db)):
    return list_courses(db)


@router.get("/{course_id}", response_model=CourseResponse)
def read_course(course_id: int, db: Session = Depends(get_db)):
    return get_course(course_id, db)


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    return create_course(course_data, db)
