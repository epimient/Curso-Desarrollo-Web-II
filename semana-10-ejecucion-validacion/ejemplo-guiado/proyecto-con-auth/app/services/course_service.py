from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.course import Course
from app.schemas.course import CourseCreate


def list_courses(db: Session) -> list[Course]:
    return db.query(Course).all()


def get_course(course_id: int, db: Session) -> Course:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


def create_course(course_data: CourseCreate, db: Session) -> Course:
    exists = db.query(Course).filter(
        Course.name.ilike(course_data.name)
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Course already exists")

    course = Course(
        name=course_data.name,
        credits=course_data.credits,
        active=True,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
