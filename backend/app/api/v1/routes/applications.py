"""
Application routes for job applications.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query, Request
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationListResponse,
    ApplicationStatusUpdate,
    ApplicationEmployerNotes,
    ApplicationStats,
    StatusHistoryItem
)
from app.models.application import ApplicationStatus
from app.models.user import User
from app.api.dependencies import get_current_user, get_current_job_seeker, get_current_employer
from app.services.application_service import application_service
from app.repositories.job_repository import JobRepository
from app.core.logging import get_logger
from app.core.rate_limiting import limiter, RATE_LIMIT_APPLICATION

logger = get_logger(__name__)
router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ApplicationResponse)
@limiter.limit(RATE_LIMIT_APPLICATION)
async def apply_to_job(
    request: Request,
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_job_seeker)
):
    """
    Apply to a job (Job Seeker only).
    
    Args:
        application_data: Application creation data
        current_user: Current authenticated job seeker
        
    Returns:
        Created application object
        
    Raises:
        HTTPException: If job not found, already applied, or job is closed
    """
    logger.info(f"Job application attempt by {current_user.email} for job {application_data.job_id}")
    
    application = await application_service.create_application(
        job_id=application_data.job_id,
        applicant=current_user,
        cover_letter=application_data.cover_letter,
        resume_url=application_data.resume_url,
        additional_info=application_data.additional_info
    )
    
    return _application_to_response(application)


@router.get("/me", response_model=ApplicationListResponse)
async def get_my_applications(
    current_user: User = Depends(get_current_job_seeker),
    status_filter: Optional[ApplicationStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Get current user's job applications (Job Seeker only).
    
    Args:
        current_user: Current authenticated job seeker
        status_filter: Optional filter by application status
        page: Page number (default: 1)
        page_size: Number of applications per page (default: 10, max: 100)
        
    Returns:
        Paginated list of user's applications
    """
    logger.info(f"Fetching applications for user: {current_user.email}")
    
    applications, total = await application_service.get_applicant_applications(
        applicant_id=str(current_user.id),
        status_filter=status_filter,
        page=page,
        page_size=page_size
    )
    
    application_responses = [_application_to_response(app) for app in applications]
    total_pages = (total + page_size - 1) // page_size
    
    logger.info(f"Retrieved {len(application_responses)} applications for user {current_user.email}")
    
    return ApplicationListResponse(
        applications=application_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/me/stats", response_model=ApplicationStats)
async def get_my_application_stats(
    current_user: User = Depends(get_current_job_seeker)
):
    """
    Get application statistics for current user (Job Seeker only).
    
    Args:
        current_user: Current authenticated job seeker
        
    Returns:
        Application statistics
    """
    logger.info(f"Fetching application stats for user: {current_user.email}")
    
    stats = await application_service.get_applicant_stats(str(current_user.id))
    
    return ApplicationStats(**stats)


@router.get("/job/{job_id}", response_model=ApplicationListResponse)
async def get_job_applications(
    job_id: str,
    current_user: User = Depends(get_current_employer),
    status_filter: Optional[ApplicationStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Get applications for a specific job (Employer only - must own the job).
    
    Args:
        job_id: Job ID
        current_user: Current authenticated employer
        status_filter: Optional filter by application status
        page: Page number (default: 1)
        page_size: Number of applications per page (default: 10, max: 100)
        
    Returns:
        Paginated list of job applications
        
    Raises:
        HTTPException: If job not found or user not authorized
    """
    logger.info(f"Fetching applications for job {job_id} by employer: {current_user.email}")
    
    applications, total = await application_service.get_job_applications(
        job_id=job_id,
        employer_id=str(current_user.id),
        status_filter=status_filter,
        page=page,
        page_size=page_size
    )
    
    application_responses = [_application_to_response(app) for app in applications]
    total_pages = (total + page_size - 1) // page_size
    
    logger.info(f"Retrieved {len(application_responses)} applications for job {job_id}")
    
    return ApplicationListResponse(
        applications=application_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/job/{job_id}/stats", response_model=ApplicationStats)
async def get_job_application_stats(
    job_id: str,
    current_user: User = Depends(get_current_employer)
):
    """
    Get application statistics for a job (Employer only - must own the job).
    
    Args:
        job_id: Job ID
        current_user: Current authenticated employer
        
    Returns:
        Application statistics
        
    Raises:
        HTTPException: If job not found or user not authorized
    """
    logger.info(f"Fetching application stats for job {job_id} by employer: {current_user.email}")
    
    stats = await application_service.get_job_stats(job_id, str(current_user.id))
    
    return ApplicationStats(**stats)


@router.get("/company/{company_id}", response_model=ApplicationListResponse)
async def get_company_applications(
    company_id: str,
    current_user: User = Depends(get_current_employer),
    status_filter: Optional[ApplicationStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Get applications for a company (Employer only - must be associated with company).
    
    Args:
        company_id: Company ID
        current_user: Current authenticated employer
        status_filter: Optional filter by application status
        page: Page number (default: 1)
        page_size: Number of applications per page (default: 10, max: 100)
        
    Returns:
        Paginated list of company applications
        
    Raises:
        HTTPException: If user not authorized
    """
    logger.info(f"Fetching applications for company {company_id} by employer: {current_user.email}")
    
    applications, total = await application_service.get_company_applications(
        company_id=company_id,
        employer_id=str(current_user.id),
        status_filter=status_filter,
        page=page,
        page_size=page_size
    )
    
    application_responses = [_application_to_response(app) for app in applications]
    total_pages = (total + page_size - 1) // page_size
    
    logger.info(f"Retrieved {len(application_responses)} applications for company {company_id}")
    
    return ApplicationListResponse(
        applications=application_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific application by ID.
    
    User must be either the applicant or the employer who owns the job.
    
    Args:
        application_id: Application ID
        current_user: Current authenticated user
        
    Returns:
        Application object
        
    Raises:
        HTTPException: If application not found or user not authorized
    """
    logger.info(f"Fetching application {application_id} by user: {current_user.email}")
    
    application = await application_service.get_application(application_id)
    
    # Check authorization
    job_repository = JobRepository()
    job = await job_repository.get_job_by_id(application.job_id)
    
    is_applicant = application.applicant_id == str(current_user.id)
    is_employer = job and job.employer_id == str(current_user.id)
    
    if not (is_applicant or is_employer):
        logger.warning(
            f"Unauthorized access attempt to application {application_id} by {current_user.email}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this application"
        )
    
    return _application_to_response(application)


@router.put("/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: str,
    status_data: ApplicationStatusUpdate,
    current_user: User = Depends(get_current_employer)
):
    """
    Update application status (Employer only - must own the job).
    
    Args:
        application_id: Application ID
        status_data: Status update data
        current_user: Current authenticated employer
        
    Returns:
        Updated application object
        
    Raises:
        HTTPException: If application not found or user not authorized
    """
    logger.info(
        f"Application status update for {application_id} by employer: {current_user.email}"
    )
    
    application = await application_service.update_application_status(
        application_id=application_id,
        employer_id=str(current_user.id),
        new_status=status_data.status,
        notes=status_data.notes,
        rejection_reason=status_data.rejection_reason
    )
    
    return _application_to_response(application)


@router.put("/{application_id}/notes", response_model=ApplicationResponse)
async def update_employer_notes(
    application_id: str,
    notes_data: ApplicationEmployerNotes,
    current_user: User = Depends(get_current_employer)
):
    """
    Update employer notes on application (Employer only - must own the job).
    
    Args:
        application_id: Application ID
        notes_data: Notes data
        current_user: Current authenticated employer
        
    Returns:
        Updated application object
        
    Raises:
        HTTPException: If application not found or user not authorized
    """
    logger.info(f"Updating notes for application {application_id} by employer: {current_user.email}")
    
    application = await application_service.update_employer_notes(
        application_id=application_id,
        employer_id=str(current_user.id),
        notes=notes_data.employer_notes
    )
    
    return _application_to_response(application)


@router.post("/{application_id}/withdraw", response_model=ApplicationResponse)
async def withdraw_application(
    application_id: str,
    current_user: User = Depends(get_current_job_seeker)
):
    """
    Withdraw application (Job Seeker only - must be the applicant).
    
    Args:
        application_id: Application ID
        current_user: Current authenticated job seeker
        
    Returns:
        Updated application object
        
    Raises:
        HTTPException: If application not found, user not authorized, or already in final state
    """
    logger.info(f"Withdrawing application {application_id} by user: {current_user.email}")
    
    application = await application_service.withdraw_application(
        application_id=application_id,
        applicant_id=str(current_user.id)
    )
    
    return _application_to_response(application)


@router.post("/{application_id}/shortlist", response_model=ApplicationResponse)
async def shortlist_application(
    application_id: str,
    current_user: User = Depends(get_current_employer)
):
    """
    Shortlist an application (Employer only - must own the job).
    
    Convenience endpoint for updating status to SHORTLISTED.
    
    Args:
        application_id: Application ID
        current_user: Current authenticated employer
        
    Returns:
        Updated application object
        
    Raises:
        HTTPException: If application not found or user not authorized
    """
    logger.info(f"Shortlisting application {application_id} by employer: {current_user.email}")
    
    application = await application_service.update_application_status(
        application_id=application_id,
        employer_id=str(current_user.id),
        new_status=ApplicationStatus.SHORTLISTED,
        notes="Candidate shortlisted for further review"
    )
    
    return _application_to_response(application)


@router.post("/{application_id}/reject", response_model=ApplicationResponse)
async def reject_application(
    application_id: str,
    rejection_reason: Optional[str] = None,
    current_user: User = Depends(get_current_employer)
):
    """
    Reject an application (Employer only - must own the job).
    
    Convenience endpoint for updating status to REJECTED.
    
    Args:
        application_id: Application ID
        rejection_reason: Optional reason for rejection
        current_user: Current authenticated employer
        
    Returns:
        Updated application object
        
    Raises:
        HTTPException: If application not found or user not authorized
    """
    logger.info(f"Rejecting application {application_id} by employer: {current_user.email}")
    
    application = await application_service.update_application_status(
        application_id=application_id,
        employer_id=str(current_user.id),
        new_status=ApplicationStatus.REJECTED,
        notes="Application rejected",
        rejection_reason=rejection_reason
    )
    
    return _application_to_response(application)


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: str,
    current_user: User = Depends(get_current_job_seeker)
):
    """
    Delete application (Job Seeker only - must be the applicant and pending status).
    
    Args:
        application_id: Application ID
        current_user: Current authenticated job seeker
        
    Raises:
        HTTPException: If application not found, user not authorized, or not pending
    """
    logger.info(f"Deleting application {application_id} by user: {current_user.email}")
    
    await application_service.delete_application(
        application_id=application_id,
        applicant_id=str(current_user.id)
    )
    
    logger.info(f"Application deleted successfully: {application_id}")


def _application_to_response(application) -> ApplicationResponse:
    """
    Convert Application model to ApplicationResponse schema.
    
    Args:
        application: Application object
        
    Returns:
        ApplicationResponse object
    """
    return ApplicationResponse(
        id=str(application.id),
        job_id=application.job_id,
        applicant_id=application.applicant_id,
        job_title=application.job_title,
        company_id=application.company_id,
        company_name=application.company_name,
        applicant_name=application.applicant_name,
        applicant_email=application.applicant_email,
        cover_letter=application.cover_letter,
        resume_url=application.resume_url,
        additional_info=application.additional_info,
        status=application.status,
        status_history=[
            StatusHistoryItem(**item) for item in application.status_history
        ],
        employer_notes=application.employer_notes,
        rejection_reason=application.rejection_reason,
        applied_at=application.applied_at,
        updated_at=application.updated_at,
        reviewed_at=application.reviewed_at,
    )

