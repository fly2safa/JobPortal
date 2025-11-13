"""
Tests for job endpoints.
"""
import pytest
from httpx import AsyncClient

from app.models.user import User
from app.models.company import Company
from app.models.job import Job


@pytest.mark.asyncio
async def test_get_jobs_public(test_client: AsyncClient, test_job: Job):
    """Test getting jobs without authentication."""
    response = await test_client.get("/api/v1/jobs")
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) > 0
    assert data["items"][0]["title"] == test_job.title


@pytest.mark.asyncio
async def test_get_job_by_id(test_client: AsyncClient, test_job: Job):
    """Test getting a specific job by ID."""
    response = await test_client.get(f"/api/v1/jobs/{test_job.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_job.id)
    assert data["title"] == test_job.title


@pytest.mark.asyncio
async def test_get_nonexistent_job(test_client: AsyncClient):
    """Test getting a job that doesn't exist."""
    fake_id = "507f1f77bcf86cd799439011"
    response = await test_client.get(f"/api/v1/jobs/{fake_id}")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_search_jobs_by_keyword(test_client: AsyncClient, test_job: Job):
    """Test searching jobs by keyword."""
    response = await test_client.get("/api/v1/jobs?search=Python")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_filter_jobs_by_location(test_client: AsyncClient, test_job: Job):
    """Test filtering jobs by location."""
    response = await test_client.get("/api/v1/jobs?location=San Francisco")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_filter_jobs_by_remote(test_client: AsyncClient, test_job: Job):
    """Test filtering jobs by remote option."""
    response = await test_client.get("/api/v1/jobs?is_remote=true")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0
    assert data["items"][0]["is_remote"] is True


@pytest.mark.asyncio
async def test_create_job_as_employer(
    test_client: AsyncClient,
    test_employer: User,
    test_company: Company,
    employer_auth_headers: dict
):
    """Test creating a job as an employer."""
    response = await test_client.post(
        "/api/v1/jobs",
        headers=employer_auth_headers,
        json={
            "title": "Full Stack Developer",
            "description": "We are looking for a full stack developer...",
            "requirements": "3+ years of experience",
            "responsibilities": "Develop web applications",
            "skills": ["JavaScript", "React", "Node.js"],
            "location": "New York, NY",
            "is_remote": False,
            "company_id": str(test_company.id),
            "salary_min": 80000,
            "salary_max": 120000,
            "job_type": "full_time",
            "experience_level": "mid"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Full Stack Developer"
    assert data["company_id"] == str(test_company.id)


@pytest.mark.asyncio
async def test_create_job_as_job_seeker(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict
):
    """Test that job seekers cannot create jobs."""
    response = await test_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json={
            "title": "Test Job",
            "description": "Test description",
            "location": "Test Location",
            "company_id": "507f1f77bcf86cd799439011"
        }
    )
    
    assert response.status_code == 403  # Forbidden


@pytest.mark.asyncio
async def test_update_job_as_owner(
    test_client: AsyncClient,
    test_job: Job,
    employer_auth_headers: dict
):
    """Test updating a job as the owner."""
    response = await test_client.put(
        f"/api/v1/jobs/{test_job.id}",
        headers=employer_auth_headers,
        json={
            "title": "Updated Job Title",
            "description": test_job.description,
            "location": test_job.location,
            "salary_min": 130000,
            "salary_max": 190000
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Job Title"
    assert data["salary_min"] == 130000


@pytest.mark.asyncio
async def test_delete_job_as_owner(
    test_client: AsyncClient,
    test_job: Job,
    employer_auth_headers: dict
):
    """Test deleting a job as the owner."""
    response = await test_client.delete(
        f"/api/v1/jobs/{test_job.id}",
        headers=employer_auth_headers
    )
    
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_employer_jobs(
    test_client: AsyncClient,
    test_job: Job,
    employer_auth_headers: dict
):
    """Test getting jobs posted by the employer."""
    response = await test_client.get(
        "/api/v1/jobs/employer/my-jobs",
        headers=employer_auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0

