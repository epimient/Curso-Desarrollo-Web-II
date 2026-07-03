from fastapi import APIRouter, status

from app.schemas.course import CourseCreate, CourseResponse
from app.services.course_service import create_course, get_course, list_courses

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=list[CourseResponse])
def read_courses():
    return list_courses()


@router.get("/{course_id}", response_model=CourseResponse)
def read_course(course_id: int):
    return get_course(course_id)


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_course(course_data: CourseCreate):
    return create_course(course_data)
