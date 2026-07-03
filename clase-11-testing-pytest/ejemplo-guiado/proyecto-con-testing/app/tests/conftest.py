import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.auth.dependencies import get_current_user
from app.auth.hash import hash_password
from app.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user_data():
    return {"username": "ana", "email": "ana@mail.com", "password": "123456"}


@pytest.fixture()
def registered_user(client, test_user_data):
    response = client.post("/users/register", json=test_user_data)
    return response.json()


@pytest.fixture()
def token(client, test_user_data):
    client.post("/users/register", json=test_user_data)
    response = client.post("/token", data={
        "username": test_user_data["username"],
        "password": test_user_data["password"],
    })
    return response.json()["access_token"]


@pytest.fixture()
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def admin_token(client):
    user_data = {"username": "admin", "email": "admin@mail.com", "password": "admin123"}
    client.post("/users/register", json=user_data)
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == "admin").first()
    user.role = "admin"
    db.commit()
    db.close()
    response = client.post("/token", data={
        "username": "admin",
        "password": "admin123",
    })
    return response.json()["access_token"]


@pytest.fixture()
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture()
def course_data():
    return {"name": "Fisica", "credits": 4}


@pytest.fixture()
def created_course(client, auth_headers, course_data):
    response = client.post("/courses/", json=course_data, headers=auth_headers)
    return response.json()
