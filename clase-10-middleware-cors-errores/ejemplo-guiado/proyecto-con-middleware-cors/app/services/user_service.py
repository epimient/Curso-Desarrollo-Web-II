from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.hash import hash_password
from app.errors.exceptions import BusinessRuleException


def create_user(user_data: UserCreate, db: Session) -> User:
    existing = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing:
        raise BusinessRuleException("Username or email already exists")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="student",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(user_id: int, db: Session) -> User:
    from app.errors.exceptions import NotFoundException

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User", user_id)
    return user
