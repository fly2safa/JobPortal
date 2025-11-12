"""
Tests for application endpoints.
"""
import pytest
from httpx import AsyncClient

from app.models.user import User
from app.models.job import Job
from app.models.application import Application


@pytest.mark.asyncio
async def test_create_application(
    test_client: AsyncClient,
    test_user: User,
    test_job: Job,
    auth_headers: dict
):
    """Test creating a job application."""
    response = await test_client.post(
        "/api/v1/applications",
        headers=auth_headers,
        json={
            "job_id": str(test_job.id),
            "cover_letter": "I am very interested in this position...",
            "resume_url": "/uploads/resumes/my_resume.pdf"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["job_id"] == str(test_job.id)
    assert data["applicant_id"] == str(test_user.id)
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_create_duplicate_application(
    test_client: AsyncClient,
    test_application: Application,
    auth_headers: dict
):
    """Test that users cannot apply to the same job twice."""
    response = await test_client.post(
        "/api/v1/applications",
        headers=auth_headers,
        json={
            "job_id": test_application.job_id,
            "cover_letter": "Another application...",
            "resume_url": "/uploads/resumes/my_resume.pdf"
        }
    )
    
    assert response.status_code == 400
    assert "already applied" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_my_applications(
    test_client: AsyncClient,
    test_application: Application,
    auth_headers: dict
):
    """Test getting user's own applications."""
    response = await test_client.get(
        "/api/v1/applications/my-applications",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0
    assert data["items"][0]["id"] == str(test_application.id)


@pytest.mark.asyncio
async def test_get_application_by_id(
    test_client: AsyncClient,
    test_application: Application,
    auth_headers: dict
):
    """Test getting a specific application by ID."""
    response = await test_client.get(
        f"/api/v1/applications/{test_application.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_application.id)


@pytest.mark.asyncio
async def test_get_job_applications_as_employer(
    test_client: AsyncClient,
    test_job: Job,
    test_application: Application,
    employer_auth_headers: dict
):
    """Test employer getting applications for their job."""
    response = await test_client.get(
        f"/api/v1/jobs/{test_job.id}/applications",
        headers=employer_auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_update_application_status_as_employer(
    test_client: AsyncClient,
    test_application: Application,
    employer_auth_headers: dict
):
    """Test employer updating application status."""
    response = await test_client.put(
        f"/api/v1/applications/{test_application.id}/status",
        headers=employer_auth_headers,
        json={"status": "reviewing"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "reviewing"


@pytest.mark.asyncio
async def test_shortlist_application(
    test_client: AsyncClient,
    test_application: Application,
    employer_auth_headers: dict
):
    """Test employer shortlisting an application."""
    response = await test_client.post(
        f"/api/v1/applications/{test_application.id}/shortlist",
        headers=employer_auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "shortlisted"


@pytest.mark.asyncio
async def test_reject_application(
    test_client: AsyncClient,
    test_application: Application,
    employer_auth_headers: dict
):
    """Test employer rejecting an application."""
    response = await test_client.post(
        f"/api/v1/applications/{test_application.id}/reject",
        headers=employer_auth_headers,
        json={"rejection_reason": "Not a good fit for the role"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rejected"
    assert data["rejection_reason"] == "Not a good fit for the role"


@pytest.mark.asyncio
async def test_withdraw_application(
    test_client: AsyncClient,
    test_application: Application,
    auth_headers: dict
):
    """Test applicant withdrawing their application."""
    response = await test_client.post(
        f"/api/v1/applications/{test_application.id}/withdraw",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "withdrawn"


@pytest.mark.asyncio
async def test_filter_applications_by_status(
    test_client: AsyncClient,
    test_job: Job,
    test_application: Application,
    employer_auth_headers: dict
):
    """Test filtering applications by status."""
    response = await test_client.get(
        f"/api/v1/jobs/{test_job.id}/applications?status_filter=pending",
        headers=employer_auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert all(app["status"] == "pending" for app in data["items"])

