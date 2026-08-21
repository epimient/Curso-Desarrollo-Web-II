from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate
from app.errors.exceptions import NotFoundException, BusinessRuleException


def list_courses(db: Session) -> list[Course]:
    return db.query(Course).all()


def get_course(course_id: int, db: Session) -> Course:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise NotFoundException("Course", course_id)
    return course


def create_course(course_data: CourseCreate, db: Session) -> Course:
    exists = db.query(Course).filter(
        Course.name.ilike(course_data.name)
    ).first()
    if exists:
        raise BusinessRuleException("El curso ya existe")

    course = Course(
        name=course_data.name,
        credits=course_data.credits,
        active=True,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def delete_course(course_id: int, db: Session) -> None:
    course = get_course(course_id, db)
    db.delete(course)
    db.commit()
