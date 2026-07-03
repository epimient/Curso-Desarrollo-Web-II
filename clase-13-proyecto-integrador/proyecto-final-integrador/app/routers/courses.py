from math import ceil
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.services.course_service import (
    list_courses,
    get_course,
    create_course,
    update_course,
    delete_course,
)
from app.auth.dependencies import get_current_user
from app.errors.exceptions import ForbiddenException

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/")
def read_courses(
    name: str | None = None,
    credits: int | None = None,
    active: bool | None = None,
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db),
):
    courses = list_courses(db, name=name, credits=credits, active=active)
    total = len(courses)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "items": courses[start:end],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": ceil(total / per_page) if total > 0 else 0,
    }


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


@router.put("/{course_id}", response_model=CourseResponse)
def edit_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_course(course_id, course_data, db)


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
