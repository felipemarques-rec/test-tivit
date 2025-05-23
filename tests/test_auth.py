import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Teste Tivit API"


def test_health_endpoint_public(client):
    """Test public health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_login_with_valid_user_credentials(client, test_user_credentials):
    """Test login with valid user credentials."""
    response = client.post("/auth/token-json", json=test_user_credentials)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_valid_admin_credentials(client, test_admin_credentials):
    """Test login with valid admin credentials."""
    response = client.post("/auth/token-json", json=test_admin_credentials)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post(
        "/auth/token-json",
        json={"username": "invalid", "password": "invalid"}
    )
    assert response.status_code == 401
    response_data = response.json()
    assert "error" in response_data
    assert "Incorrect username or password" in response_data["error"]


def test_login_with_form_data(client, test_user_credentials):
    """Test login with form data."""
    response = client.post("/auth/token", data=test_user_credentials)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_detailed_endpoint(client, test_user_credentials):
    """Test detailed login endpoint."""
    response = client.post("/auth/login", json=test_user_credentials)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "user" in data


def test_access_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without token."""
    response = client.get("/user")
    assert response.status_code == 403


def test_access_user_endpoint_with_user_token(client, test_user_credentials):
    """Test accessing user endpoint with user token."""
    # First, get a token
    login_response = client.post("/auth/token-json", json=test_user_credentials)
    token = login_response.json()["access_token"]
    
    # Then access the protected endpoint
    response = client.get("/user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_access_admin_endpoint_with_admin_token(client, test_admin_credentials):
    """Test accessing admin endpoint with admin token."""
    # First, get an admin token
    login_response = client.post("/auth/token-json", json=test_admin_credentials)
    token = login_response.json()["access_token"]
    
    # Then access the admin endpoint
    response = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_access_admin_endpoint_with_user_token(client, test_user_credentials):
    """Test accessing admin endpoint with user token (should fail)."""
    # First, get a user token
    login_response = client.post("/auth/token-json", json=test_user_credentials)
    token = login_response.json()["access_token"]
    
    # Then try to access the admin endpoint
    response = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    # The important thing is that access is denied with 403 status


def test_access_profile_endpoint(client, test_user_credentials):
    """Test accessing profile endpoint."""
    # First, get a token
    login_response = client.post("/auth/token-json", json=test_user_credentials)
    token = login_response.json()["access_token"]
    
    # Then access the profile endpoint
    response = client.get("/profile", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "username" in data["data"]
    assert "role" in data["data"]
    assert "permissions" in data["data"]


def test_access_external_health_endpoint_authenticated(client, test_user_credentials):
    """Test accessing authenticated external health endpoint."""
    # First, get a token
    login_response = client.post("/auth/token-json", json=test_user_credentials)
    token = login_response.json()["access_token"]
    
    # Then access the external health endpoint
    response = client.get("/external-health", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_invalid_token(client):
    """Test with invalid token."""
    response = client.get(
        "/user", 
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401


def test_malformed_authorization_header(client):
    """Test with malformed authorization header."""
    response = client.get("/user", headers={"Authorization": "InvalidFormat"})
    assert response.status_code == 403


def test_empty_credentials(client):
    """Test login with empty credentials."""
    response = client.post("/auth/token-json", json={"username": "", "password": ""})
    assert response.status_code == 422  # Validation error


def test_missing_credentials(client):
    """Test login with missing credentials."""
    response = client.post("/auth/token-json", json={})
    assert response.status_code == 422  # Validation error


def test_whitespace_username(client):
    """Test login with whitespace username."""
    response = client.post(
        "/auth/token-json", 
        json={"username": "   ", "password": "password"}
    )
    assert response.status_code == 422  # Validation error
