from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from app.errors.exceptions import NotFoundException, BusinessRuleException


def list_courses(
    db: Session,
    name: str | None = None,
    credits: int | None = None,
    active: bool | None = None,
) -> list[Course]:
    query = db.query(Course)
    if name:
        query = query.filter(Course.name.ilike(f"%{name}%"))
    if credits is not None:
        query = query.filter(Course.credits == credits)
    if active is not None:
        query = query.filter(Course.active == active)
    return query.all()


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


def update_course(course_id: int, course_data: CourseUpdate, db: Session) -> Course:
    course = get_course(course_id, db)
    update_data = course_data.model_dump(exclude_unset=True)
    if "name" in update_data:
        existing = db.query(Course).filter(
            Course.name.ilike(update_data["name"]),
            Course.id != course_id,
        ).first()
        if existing:
            raise BusinessRuleException("Ya existe un curso con ese nombre")
    for key, value in update_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course


def delete_course(course_id: int, db: Session) -> None:
    course = get_course(course_id, db)
    db.delete(course)
    db.commit()
