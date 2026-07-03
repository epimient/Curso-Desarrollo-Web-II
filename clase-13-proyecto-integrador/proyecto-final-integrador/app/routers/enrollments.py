from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse
from app.services.enrollment_service import (
    create_enrollment,
    list_enrollments,
    get_enrollment,
    update_enrollment,
    delete_enrollment,
)
from app.auth.dependencies import get_current_user
from app.errors.exceptions import ForbiddenException
from app.models.user import User

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def add_enrollment(
    data: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_enrollment(data, db)


@router.get("/", response_model=list[EnrollmentResponse])
def read_enrollments(
    student_id: int | None = None,
    course_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_enrollments(db, student_id, course_id)


@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def read_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_enrollment(enrollment_id, db)


@router.patch("/{enrollment_id}", response_model=EnrollmentResponse)
def patch_enrollment(
    enrollment_id: int,
    data: EnrollmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_enrollment(enrollment_id, data, db)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise ForbiddenException()
    delete_enrollment(enrollment_id, db)
