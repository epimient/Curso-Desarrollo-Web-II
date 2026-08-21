from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.student import Student
from app.schemas.student import StudentCreate


def list_students(db: Session) -> list[Student]:
    return db.query(Student).all()


def get_student(student_id: int, db: Session) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


def create_student(student_data: StudentCreate, db: Session) -> Student:
    student = Student(
        name=student_data.name,
        email=student_data.email,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
