from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    credits = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
