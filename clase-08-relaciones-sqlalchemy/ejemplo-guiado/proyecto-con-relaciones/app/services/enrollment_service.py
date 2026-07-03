from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException

from app.models.enrollment import Enrollment
from app.models.course import Course
from app.models.student import Student


def create_enrollment(
    course_id: int, student_id: int, db: Session
) -> Enrollment:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    existing = db.query(Enrollment).filter(
        and_(
            Enrollment.course_id == course_id,
            Enrollment.student_id == student_id,
        )
    ).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Already enrolled in this course"
        )

    enrollment = Enrollment(course_id=course_id, student_id=student_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def get_students_by_course(
    course_id: int, db: Session
) -> list[Student]:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return [enrollment.student for enrollment in course.enrollments]


def get_courses_by_student(
    student_id: int, db: Session
) -> list[Course]:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return [enrollment.course for enrollment in student.enrollments]
