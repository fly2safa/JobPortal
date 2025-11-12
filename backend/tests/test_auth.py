"""
Tests for authentication endpoints.
"""
import pytest
from httpx import AsyncClient

from app.models.user import User


@pytest.mark.asyncio
async def test_register_job_seeker(test_client: AsyncClient):
    """Test job seeker registration."""
    response = await test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "Test123!",
            "role": "job_seeker",
            "first_name": "New",
            "last_name": "User"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "job_seeker"
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_employer(test_client: AsyncClient):
    """Test employer registration."""
    response = await test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "newemployer@example.com",
            "password": "Test123!",
            "role": "employer",
            "first_name": "New",
            "last_name": "Employer",
            "job_title": "HR Manager"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newemployer@example.com"
    assert data["role"] == "employer"


@pytest.mark.asyncio
async def test_register_duplicate_email(test_client: AsyncClient, test_user: User):
    """Test registration with duplicate email."""
    response = await test_client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "password": "Test123!",
            "role": "job_seeker",
            "first_name": "Duplicate",
            "last_name": "User"
        }
    )
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_invalid_email(test_client: AsyncClient):
    """Test registration with invalid email."""
    response = await test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "invalid-email",
            "password": "Test123!",
            "role": "job_seeker",
            "first_name": "Invalid",
            "last_name": "User"
        }
    )
    
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_login_success(test_client: AsyncClient, test_user: User):
    """Test successful login."""
    response = await test_client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "Test123!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(test_client: AsyncClient):
    """Test login with invalid credentials."""
    response = await test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "WrongPassword123!"
        }
    )
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_current_user(test_client: AsyncClient, test_user: User, auth_headers: dict):
    """Test getting current user information."""
    response = await test_client.get(
        "/api/v1/auth/me",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["first_name"] == test_user.first_name


@pytest.mark.asyncio
async def test_get_current_user_unauthorized(test_client: AsyncClient):
    """Test getting current user without authentication."""
    response = await test_client.get("/api/v1/auth/me")
    
    assert response.status_code == 401

