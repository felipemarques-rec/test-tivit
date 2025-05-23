import sys
import os
import warnings
from pathlib import Path

# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", message=".*'crypt' is deprecated.*", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*Support for class-based.*", category=DeprecationWarning)

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.database import get_db, Base

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def test_db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Create test client with database override."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_credentials():
    """Test user credentials."""
    return {
        "username": "usuario",
        "password": "L0XuwPOdS5U"
    }


@pytest.fixture
def test_admin_credentials():
    """Test admin credentials."""
    return {
        "username": "admin", 
        "password": "JKSipm0YH"
    }


@pytest.fixture
async def user_token(client, test_user_credentials):
    """Get user token for testing."""
    response = client.post("/auth/token-json", json=test_user_credentials)
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
async def admin_token(client, test_admin_credentials):
    """Get admin token for testing."""
    response = client.post("/auth/token-json", json=test_admin_credentials)
    assert response.status_code == 200
    return response.json()["access_token"]
