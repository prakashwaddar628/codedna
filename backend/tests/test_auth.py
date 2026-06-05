import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.base import Base
from app.dependencies.database import get_db

# Setup test database (SQLite in-memory with StaticPool)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    # Create tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "securepassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data

def test_register_existing_user():
    # Register first time
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "securepassword"
        }
    )
    # Register again with same email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Another User",
            "email": "test@example.com",
            "password": "securepassword"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

def test_login_success():
    # Register user
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "securepassword"
        }
    )
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "securepassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password():
    # Register user
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "securepassword"
        }
    )
    # Login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_non_existent_user():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "somepassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
