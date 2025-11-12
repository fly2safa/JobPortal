"""
Pytest configuration and fixtures for testing.
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.main import app
from app.models.user import User
from app.models.company import Company
from app.models.job import Job
from app.models.application import Application
from app.models.resume import Resume
from app.models.conversation import Conversation
from app.core.config import settings
from app.core.security import get_password_hash


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_client() -> AsyncGenerator:
    """
    Create a test database client.
    Uses a separate test database to avoid affecting production data.
    """
    # Use test database
    test_db_name = f"{settings.MONGODB_DB}_test"
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Initialize Beanie with test database
    await init_beanie(
        database=client[test_db_name],
        document_models=[User, Company, Job, Application, Resume, Conversation]
    )
    
    yield client
    
    # Cleanup: Drop test database after tests
    await client.drop_database(test_db_name)
    client.close()


@pytest.fixture(scope="function")
async def test_client(db_client) -> AsyncGenerator:
    """Create a test client for making HTTP requests."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def test_user(db_client) -> User:
    """Create a test job seeker user."""
    user = User(
        email="testuser@example.com",
        hashed_password=get_password_hash("Test123!"),
        role="job_seeker",
        first_name="Test",
        last_name="User",
        skills=["Python", "FastAPI", "React"],
        experience_years=3,
        education="Bachelor's in Computer Science",
        bio="Test user bio",
        is_active=True,
        is_verified=True
    )
    await user.insert()
    return user


@pytest.fixture(scope="function")
async def test_company(db_client) -> Company:
    """Create a test company."""
    company = Company(
        name="Test Company Inc.",
        description="A test company for testing purposes",
        industry="Technology",
        size="51-200",
        website="https://testcompany.com",
        email="contact@testcompany.com",
        headquarters="San Francisco, CA",
        is_verified=True
    )
    await company.insert()
    return company


@pytest.fixture(scope="function")
async def test_employer(db_client, test_company: Company) -> User:
    """Create a test employer user."""
    employer = User(
        email="employer@testcompany.com",
        hashed_password=get_password_hash("Test123!"),
        role="employer",
        first_name="Jane",
        last_name="Employer",
        company_id=str(test_company.id),
        job_title="HR Manager",
        is_active=True,
        is_verified=True
    )
    await employer.insert()
    return employer


@pytest.fixture(scope="function")
async def test_job(db_client, test_company: Company, test_employer: User) -> Job:
    """Create a test job posting."""
    job = Job(
        title="Senior Python Developer",
        description="We are looking for a senior Python developer...",
        requirements="5+ years of Python experience",
        responsibilities="Develop backend services",
        skills=["Python", "FastAPI", "MongoDB", "Docker"],
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker", "Kubernetes"],
        location="San Francisco, CA",
        is_remote=True,
        company_id=str(test_company.id),
        company_name=test_company.name,
        employer_id=str(test_employer.id),
        salary_min=120000,
        salary_max=180000,
        salary_currency="USD",
        job_type="full_time",
        experience_level="senior",
        experience_years_min=5,
        experience_years_max=10,
        status="active",
        benefits=["Health Insurance", "401k", "Remote Work"]
    )
    await job.insert()
    return job


@pytest.fixture(scope="function")
async def test_application(
    db_client,
    test_user: User,
    test_job: Job,
    test_company: Company
) -> Application:
    """Create a test job application."""
    application = Application(
        job_id=str(test_job.id),
        applicant_id=str(test_user.id),
        job_title=test_job.title,
        company_id=str(test_company.id),
        company_name=test_company.name,
        applicant_name=test_user.full_name,
        applicant_email=test_user.email,
        cover_letter="I am very interested in this position...",
        resume_url="/uploads/resumes/test_resume.pdf",
        status="pending"
    )
    await application.insert()
    return application


@pytest.fixture(scope="function")
async def test_resume(db_client, test_user: User) -> Resume:
    """Create a test resume."""
    resume = Resume(
        user_id=str(test_user.id),
        file_url="/uploads/resumes/test_resume.pdf",
        file_name="test_resume.pdf",
        file_size=102400,  # 100KB
        parsed_text="Test resume content...",
        skills_extracted=["Python", "FastAPI", "React", "MongoDB"],
        experience_years=3,
        education="Bachelor's in Computer Science",
        work_experience="Software Engineer at Tech Corp",
        summary="Experienced software engineer...",
        parsing_method="ai",
        parsing_confidence=0.85,
        ai_used=True
    )
    await resume.insert()
    return resume


@pytest.fixture(scope="function")
def auth_headers(test_user: User) -> dict:
    """Get authentication headers for test user."""
    from app.core.security import create_access_token
    
    token = create_access_token({"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def employer_auth_headers(test_employer: User) -> dict:
    """Get authentication headers for test employer."""
    from app.core.security import create_access_token
    
    token = create_access_token({"sub": test_employer.email})
    return {"Authorization": f"Bearer {token}"}

