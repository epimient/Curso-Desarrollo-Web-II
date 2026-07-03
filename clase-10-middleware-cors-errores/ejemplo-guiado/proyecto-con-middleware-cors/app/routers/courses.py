from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.course import CourseCreate, CourseResponse
from app.services.course_service import create_course, get_course, list_courses, delete_course
from app.auth.dependencies import get_current_user
from app.errors.exceptions import ForbiddenException

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
def add_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_course(course_data, db)


@router.delete("/{course_id}")
def remove_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise ForbiddenException()
    delete_course(course_id, db)
    return {"detail": "Course deleted"}
