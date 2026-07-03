import enum
from sqlalchemy import Column, Integer, Float, ForeignKey, String, Enum as SAEnum
from app.database import Base


class EnrollmentStatus(str, enum.Enum):
    enrolled = "enrolled"
    completed = "completed"
    cancelled = "cancelled"


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    grade = Column(Float, nullable=True)
    status = Column(SAEnum(EnrollmentStatus), default=EnrollmentStatus.enrolled, nullable=False)
