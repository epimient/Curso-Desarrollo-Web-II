from fastapi import HTTPException

from app.schemas.course import CourseCreate

_courses = [
    {"id": 1, "name": "Desarrollo Web II", "credits": 3, "active": True},
]
_next_id = 2


def list_courses() -> list[dict]:
    return _courses


def get_course(course_id: int) -> dict:
    for course in _courses:
        if course["id"] == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")


def create_course(course_data: CourseCreate) -> dict:
    global _next_id

    exists = any(
        course["name"].lower() == course_data.name.lower()
        for course in _courses
    )

    if exists:
        raise HTTPException(status_code=400, detail="Course already exists")

    course = {
        "id": _next_id,
        "name": course_data.name,
        "credits": course_data.credits,
        "active": True,
    }
    _courses.append(course)
    _next_id += 1
    return course
