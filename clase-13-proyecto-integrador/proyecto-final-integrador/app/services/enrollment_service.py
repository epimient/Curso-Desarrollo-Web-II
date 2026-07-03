from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate
from app.errors.exceptions import NotFoundException, BusinessRuleException


def create_enrollment(data: EnrollmentCreate, db: Session) -> Enrollment:
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id,
        Enrollment.status != EnrollmentStatus.cancelled,
    ).first()
    if existing:
        raise BusinessRuleException("El estudiante ya está inscrito en este curso")
    enrollment = Enrollment(**data.model_dump())
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def list_enrollments(
    db: Session,
    student_id: int | None = None,
    course_id: int | None = None,
) -> list[Enrollment]:
    query = db.query(Enrollment)
    if student_id is not None:
        query = query.filter(Enrollment.student_id == student_id)
    if course_id is not None:
        query = query.filter(Enrollment.course_id == course_id)
    return query.all()


def get_enrollment(enrollment_id: int, db: Session) -> Enrollment:
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise NotFoundException("Matrícula", enrollment_id)
    return enrollment


def update_enrollment(enrollment_id: int, data: EnrollmentUpdate, db: Session) -> Enrollment:
    enrollment = get_enrollment(enrollment_id, db)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(enrollment, key, value)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def delete_enrollment(enrollment_id: int, db: Session) -> None:
    enrollment = get_enrollment(enrollment_id, db)
    db.delete(enrollment)
    db.commit()
