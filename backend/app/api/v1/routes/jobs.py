"""
Job routes for job postings and management.
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from beanie import PydanticObjectId
from app.schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
    JobListResponse,
    JobPublish,
    JobStatusUpdate
)
from app.models.job import Job, JobStatus, JobType, ExperienceLevel
from app.models.user import User
from app.models.company import Company
from app.api.dependencies import get_current_user, get_current_employer
from app.services.search_service import SearchService
from app.services.candidate_matching_service import candidate_matching_service
from app.core.logging import get_logger
from pydantic import BaseModel, Field

logger = get_logger(__name__)
router = APIRouter(prefix="/jobs", tags=["Jobs"])
search_service = SearchService()


@router.get("/search", response_model=JobListResponse)
async def search_jobs(
    query: Optional[str] = Query(None, description="Search query for title and description"),
    location: Optional[str] = Query(None, description="Filter by location"),
    skills: Optional[str] = Query(None, description="Comma-separated list of skills"),
    company_name: Optional[str] = Query(None, description="Filter by company name"),
    job_type: Optional[JobType] = Query(None, description="Filter by job type"),
    experience_level: Optional[ExperienceLevel] = Query(None, description="Filter by experience level"),
    is_remote: Optional[bool] = Query(None, description="Filter remote jobs"),
    salary_min: Optional[float] = Query(None, ge=0, description="Minimum salary"),
    salary_max: Optional[float] = Query(None, ge=0, description="Maximum salary"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Results per page"),
):
    """
    Search and filter jobs (Public endpoint).
    
    Supports multiple filters:
    - Text search in title, description, and company name
    - Location filter
    - Skills filter (provide comma-separated skills)
    - Company name filter
    - Job type filter
    - Experience level filter
    - Remote jobs filter
    - Salary range filter
    
    Args:
        query: Search query string
        location: Location filter
        skills: Comma-separated skills (e.g., "Python,React,AWS")
        company_name: Company name filter
        job_type: Job type filter
        experience_level: Experience level filter
        is_remote: Remote jobs filter
        salary_min: Minimum salary
        salary_max: Maximum salary
        page: Page number
        page_size: Results per page
        
    Returns:
        Paginated list of matching jobs
    """
    logger.info(f"Job search request - query: {query}, location: {location}")
    
    # Parse skills from comma-separated string
    skills_list = None
    if skills:
        skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    
    # Call search service
    result = await search_service.search_jobs(
        query=query,
        location=location,
        skills=skills_list,
        company_name=company_name,
        job_type=job_type,
        experience_level=experience_level,
        is_remote=is_remote,
        salary_min=salary_min,
        salary_max=salary_max,
        page=page,
        page_size=page_size
    )
    
    return result


@router.get("/featured", response_model=List[JobResponse])
async def get_featured_jobs(
    limit: int = Query(10, ge=1, le=50, description="Number of featured jobs")
):
    """
    Get featured/popular jobs (Public endpoint).
    
    Returns jobs sorted by view count and recency.
    
    Args:
        limit: Number of jobs to return (max 50)
        
    Returns:
        List of featured jobs
    """
    logger.info(f"Fetching {limit} featured jobs")
    
    jobs = await search_service.get_featured_jobs(limit=limit)
    
    return jobs


@router.get("/remote", response_model=JobListResponse)
async def get_remote_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Get all remote jobs (Public endpoint).
    
    Args:
        page: Page number
        page_size: Results per page
        
    Returns:
        Paginated list of remote jobs
    """
    logger.info(f"Fetching remote jobs - page {page}")
    
    result = await search_service.search_remote_jobs(
        page=page,
        page_size=page_size
    )
    
    return result


@router.get("/company/{company_id}", response_model=JobListResponse)
async def get_company_jobs(
    company_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Get all active jobs for a specific company (Public endpoint).
    
    Args:
        company_id: Company ID
        page: Page number
        page_size: Results per page
        
    Returns:
        Paginated list of company's jobs
    """
    logger.info(f"Fetching jobs for company {company_id}")
    
    result = await search_service.get_jobs_by_company(
        company_id=company_id,
        page=page,
        page_size=page_size
    )
    
    return result


@router.get("/{job_id}/similar", response_model=List[JobResponse])
async def get_similar_jobs(
    job_id: str,
    limit: int = Query(5, ge=1, le=20, description="Number of similar jobs")
):
    """
    Get similar jobs based on skills and location (Public endpoint).
    
    Args:
        job_id: Reference job ID
        limit: Number of similar jobs to return
        
    Returns:
        List of similar jobs
    """
    logger.info(f"Fetching similar jobs for {job_id}")
    
    # Check if job exists
    job = await Job.get(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    similar_jobs = await search_service.get_similar_jobs(
        job_id=job_id,
        limit=limit
    )
    
    return similar_jobs


@router.get("", response_model=JobListResponse)
async def get_all_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Get all active jobs with pagination (Public endpoint).
    
    Returns all active job postings sorted by posted date (newest first).
    
    Args:
        page: Page number
        page_size: Results per page
        
    Returns:
        Paginated list of all active jobs
    """
    logger.info(f"Fetching all active jobs - page {page}")
    
    result = await search_service.get_all_active_jobs(
        page=page,
        page_size=page_size
    )
    
    return result


@router.post("", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_employer)
):
    """
    Create a new job posting (Employer only).
    
    Args:
        job_data: Job creation data
        current_user: Current authenticated employer
        
    Returns:
        Created job object
        
    Raises:
        HTTPException: If company not found or user not authorized
    """
    logger.info(f"Job creation attempt by employer: {current_user.email}")
    
    # Verify company exists
    company = await Company.get(job_data.company_id)
    if not company:
        logger.warning(f"Job creation failed: Company not found - {job_data.company_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Verify user is associated with the company
    if current_user.company_id != job_data.company_id:
        logger.warning(
            f"Job creation failed: User {current_user.email} not authorized for company {job_data.company_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to post jobs for this company"
        )
    
    # Create job
    job = Job(
        title=job_data.title,
        description=job_data.description,
        requirements=job_data.requirements,
        responsibilities=job_data.responsibilities,
        skills=job_data.skills,
        required_skills=job_data.required_skills,
        preferred_skills=job_data.preferred_skills,
        location=job_data.location,
        is_remote=job_data.is_remote,
        company_id=job_data.company_id,
        company_name=company.name,  # Denormalized for faster queries
        employer_id=str(current_user.id),
        salary_min=job_data.salary_min,
        salary_max=job_data.salary_max,
        salary_currency=job_data.salary_currency,
        job_type=job_data.job_type,
        experience_level=job_data.experience_level,
        experience_years_min=job_data.experience_years_min,
        experience_years_max=job_data.experience_years_max,
        status=job_data.status,
        benefits=job_data.benefits,
        application_instructions=job_data.application_instructions,
    )
    
    # If status is active, set posted_date
    if job.status == JobStatus.ACTIVE:
        job.posted_date = datetime.utcnow()
    
    await job.insert()
    logger.info(f"Job created successfully: {job.title} (ID: {job.id}) by {current_user.email}")
    
    return JobResponse(
        id=str(job.id),
        title=job.title,
        description=job.description,
        requirements=job.requirements,
        responsibilities=job.responsibilities,
        skills=job.skills,
        required_skills=job.required_skills,
        preferred_skills=job.preferred_skills,
        location=job.location,
        is_remote=job.is_remote,
        company_id=job.company_id,
        company_name=job.company_name,
        employer_id=job.employer_id,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        salary_currency=job.salary_currency,
        job_type=job.job_type,
        experience_level=job.experience_level,
        experience_years_min=job.experience_years_min,
        experience_years_max=job.experience_years_max,
        status=job.status,
        posted_date=job.posted_date,
        closing_date=job.closing_date,
        application_count=job.application_count,
        view_count=job.view_count,
        benefits=job.benefits,
        application_instructions=job.application_instructions,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


@router.get("/employer/me", response_model=JobListResponse)
async def get_employer_jobs(
    current_user: User = Depends(get_current_employer),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status_filter: Optional[JobStatus] = None
):
    """
    Get all jobs posted by the current employer.
    
    Args:
        current_user: Current authenticated employer
        page: Page number (default: 1)
        page_size: Number of jobs per page (default: 10, max: 100)
        status_filter: Optional filter by job status
        
    Returns:
        Paginated list of employer's jobs
    """
    logger.info(f"Fetching jobs for employer: {current_user.email}")
    
    # Build query
    query = Job.find(Job.employer_id == str(current_user.id))
    
    if status_filter:
        query = query.find(Job.status == status_filter)
    
    # Get total count
    total = await query.count()
    
    # Get paginated results
    skip = (page - 1) * page_size
    jobs = await query.sort(-Job.created_at).skip(skip).limit(page_size).to_list()
    
    # Convert to response models
    job_responses = [
        JobResponse(
            id=str(job.id),
            title=job.title,
            description=job.description,
            requirements=job.requirements,
            responsibilities=job.responsibilities,
            skills=job.skills,
            required_skills=job.required_skills,
            preferred_skills=job.preferred_skills,
            location=job.location,
            is_remote=job.is_remote,
            company_id=job.company_id,
            company_name=job.company_name,
            employer_id=job.employer_id,
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            salary_currency=job.salary_currency,
            job_type=job.job_type,
            experience_level=job.experience_level,
            experience_years_min=job.experience_years_min,
            experience_years_max=job.experience_years_max,
            status=job.status,
            posted_date=job.posted_date,
            closing_date=job.closing_date,
            application_count=job.application_count,
            view_count=job.view_count,
            benefits=job.benefits,
            application_instructions=job.application_instructions,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
        for job in jobs
    ]
    
    total_pages = (total + page_size - 1) // page_size
    
    logger.info(f"Retrieved {len(job_responses)} jobs for employer {current_user.email}")
    
    return JobListResponse(
        jobs=job_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    """
    Get a specific job by ID (Public endpoint).
    
    Automatically increments the view count when accessed.
    
    Args:
        job_id: Job ID
        
    Returns:
        Job object
        
    Raises:
        HTTPException: If job not found
    """
    logger.info(f"Fetching job: {job_id}")
    
    # Use search service to get job details (includes view count increment)
    job_response = await search_service.get_job_details(job_id)
    
    if not job_response:
        logger.warning(f"Job not found: {job_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job_response


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    job_data: JobUpdate,
    current_user: User = Depends(get_current_employer)
):
    """
    Update a job posting (Employer only - must own the job).
    
    Args:
        job_id: Job ID
        job_data: Job update data
        current_user: Current authenticated employer
        
    Returns:
        Updated job object
        
    Raises:
        HTTPException: If job not found or user not authorized
    """
    logger.info(f"Job update attempt for job {job_id} by employer: {current_user.email}")
    
    job = await Job.get(job_id)
    if not job:
        logger.warning(f"Job update failed: Job not found - {job_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Verify user owns this job
    if job.employer_id != str(current_user.id):
        logger.warning(
            f"Job update failed: User {current_user.email} not authorized for job {job_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this job"
        )
    
    # Update fields (only non-None values)
    update_data = job_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)
    
    # Update timestamp
    job.updated_at = datetime.utcnow()
    
    # If status changed to active and posted_date not set, set it now
    if job.status == JobStatus.ACTIVE and not job.posted_date:
        job.posted_date = datetime.utcnow()
    
    await job.save()
    logger.info(f"Job updated successfully: {job.title} (ID: {job.id})")
    
    return JobResponse(
        id=str(job.id),
        title=job.title,
        description=job.description,
        requirements=job.requirements,
        responsibilities=job.responsibilities,
        skills=job.skills,
        required_skills=job.required_skills,
        preferred_skills=job.preferred_skills,
        location=job.location,
        is_remote=job.is_remote,
        company_id=job.company_id,
        company_name=job.company_name,
        employer_id=job.employer_id,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        salary_currency=job.salary_currency,
        job_type=job.job_type,
        experience_level=job.experience_level,
        experience_years_min=job.experience_years_min,
        experience_years_max=job.experience_years_max,
        status=job.status,
        posted_date=job.posted_date,
        closing_date=job.closing_date,
        application_count=job.application_count,
        view_count=job.view_count,
        benefits=job.benefits,
        application_instructions=job.application_instructions,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: str,
    current_user: User = Depends(get_current_employer)
):
    """
    Delete a job posting (Employer only - must own the job).
    
    Args:
        job_id: Job ID
        current_user: Current authenticated employer
        
    Raises:
        HTTPException: If job not found or user not authorized
    """
    logger.info(f"Job deletion attempt for job {job_id} by employer: {current_user.email}")
    
    job = await Job.get(job_id)
    if not job:
        logger.warning(f"Job deletion failed: Job not found - {job_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Verify user owns this job
    if job.employer_id != str(current_user.id):
        logger.warning(
            f"Job deletion failed: User {current_user.email} not authorized for job {job_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this job"
        )
    
    await job.delete()
    logger.info(f"Job deleted successfully: {job.title} (ID: {job_id})")


# Candidate Matching Response Models
class CandidateRankingResponse(BaseModel):
    """Single candidate ranking response."""
    candidate_id: str
    candidate_name: str
    current_role: str
    match_score: int = Field(..., ge=0, le=100)
    match_reason: str
    skills_match: dict
    experience_relevance: str
    concerns: str


class CandidateRankingsListResponse(BaseModel):
    """List of candidate rankings."""
    rankings: List[CandidateRankingResponse]
    total: int
    job_id: str
    job_title: str


@router.get("/{job_id}/recommended-candidates", response_model=CandidateRankingsListResponse)
async def get_recommended_candidates(
    job_id: str,
    limit: int = Query(10, ge=1, le=50, description="Maximum number of candidates"),
    use_ai: bool = Query(True, description="Use AI chain for intelligent ranking"),
    applicants_only: bool = Query(False, description="Only rank existing applicants"),
    current_user: User = Depends(get_current_employer)
):
    """
    Get AI-powered candidate recommendations for a job posting.
    
    Uses vector similarity search and LangChain to analyze candidate profiles
    against job requirements and provide intelligent rankings with match scores.
    
    **Employer only endpoint** - requires employer authentication.
    """
    try:
        # Verify the job exists and belongs to the employer
        job = await Job.get(PydanticObjectId(job_id))
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Verify ownership
        if job.employer_id != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to view candidates for this job"
            )
        
        # Get candidate rankings
        rankings = await candidate_matching_service.get_recommended_candidates(
            job_id=job_id,
            limit=limit,
            use_ai=use_ai,
            include_applicants_only=applicants_only
        )
        
        return CandidateRankingsListResponse(
            rankings=rankings,
            total=len(rankings),
            job_id=job_id,
            job_title=job.title
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting candidate recommendations for job {job_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate candidate recommendations. Please try again later."
        )



