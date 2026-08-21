from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.services.enrollment_service import create_enrollment

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post(
    "/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_enrollment(
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db),
):
    return create_enrollment(
        enrollment_data.course_id, enrollment_data.student_id, db
    )
