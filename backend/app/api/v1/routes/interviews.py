"""
Interview routes for scheduling and managing interviews.
"""
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.schemas.interview import (
    InterviewCreate,
    InterviewUpdate,
    InterviewReschedule,
    InterviewCancel,
    InterviewComplete,
    InterviewResponse,
    InterviewListResponse
)
from app.models.interview import Interview, InterviewStatus
from app.models.application import Application
from app.models.job import Job
from app.models.user import User, UserRole
from app.api.dependencies import get_current_user, get_current_employer
from app.services.email_service import email_service
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/interviews", tags=["Interviews"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=InterviewResponse)
async def schedule_interview(
    interview_data: InterviewCreate,
    current_user: User = Depends(get_current_employer)
):
    """
    Schedule an interview with a candidate (Employer only).
    
    Args:
        interview_data: Interview creation data
        current_user: Current authenticated employer
        
    Returns:
        Created interview object
        
    Raises:
        HTTPException: If job or application not found, or unauthorized
    """
    logger.info(
        f"Interview scheduling attempt by {current_user.email} for application {interview_data.application_id}"
    )
    
    # Verify application exists
    application = await Application.get(interview_data.application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Verify job exists and employer owns it
    job = await Job.get(interview_data.job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    if job.employer_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to schedule interviews for this job"
        )
    
    # Get candidate info
    from app.models.user import User as UserModel
    candidate = await UserModel.get(application.applicant_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Create interview
    interview = Interview(
        job_id=interview_data.job_id,
        application_id=interview_data.application_id,
        candidate_id=str(candidate.id),
        candidate_name=candidate.full_name,
        candidate_email=candidate.email,
        employer_id=str(current_user.id),
        employer_name=current_user.full_name,
        employer_email=current_user.email,
        company_id=job.company_id,
        company_name=job.company_name,
        job_title=job.title,
        scheduled_time=interview_data.scheduled_time,
        duration_minutes=interview_data.duration_minutes,
        interview_type=interview_data.interview_type,
        meeting_link=interview_data.meeting_link,
        meeting_location=interview_data.meeting_location,
        meeting_instructions=interview_data.meeting_instructions,
        notes=interview_data.notes,
        created_by=str(current_user.id)
    )
    
    await interview.insert()
    
    # Update application status to interview
    from app.models.application import ApplicationStatus
    application.update_status(
        ApplicationStatus.INTERVIEW,
        "Interview scheduled"
    )
    await application.save()
    
    # Send email notifications
    scheduled_time_str = interview.scheduled_time.strftime("%B %d, %Y at %I:%M %p")
    
    # Send to candidate
    await email_service.send_interview_scheduled_email(
        to_email=candidate.email,
        recipient_name=candidate.full_name,
        job_title=job.title,
        company_name=job.company_name,
        scheduled_time=scheduled_time_str,
        duration_minutes=interview.duration_minutes,
        meeting_link=interview.meeting_link,
        meeting_location=interview.meeting_location,
        notes=interview.notes,
        is_candidate=True
    )
    
    # Send to employer
    await email_service.send_interview_scheduled_email(
        to_email=current_user.email,
        recipient_name=current_user.full_name,
        job_title=job.title,
        company_name=job.company_name,
        scheduled_time=scheduled_time_str,
        duration_minutes=interview.duration_minutes,
        meeting_link=interview.meeting_link,
        meeting_location=interview.meeting_location,
        notes=interview.notes,
        is_candidate=False
    )
    
    interview.candidate_notified = True
    interview.employer_notified = True
    await interview.save()
    
    logger.info(f"Interview scheduled: {interview.id}")
    
    return _interview_to_response(interview)


@router.get("", response_model=InterviewListResponse)
async def get_interviews(
    current_user: User = Depends(get_current_user),
    status_filter: Optional[InterviewStatus] = None,
    job_id: Optional[str] = None,
    application_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Get interviews based on user role.
    - Job seekers see their interviews
    - Employers see interviews for their jobs
    
    Args:
        current_user: Current authenticated user
        status_filter: Optional filter by interview status
        job_id: Optional filter by job ID (employer only)
        application_id: Optional filter by application ID
        page: Page number (default: 1)
        page_size: Number of interviews per page (default: 10, max: 100)
        
    Returns:
        Paginated list of interviews
    """
    logger.info(f"Fetching interviews for user: {current_user.email}")
    
    # Build query based on user role
    query = {}
    
    if current_user.role == UserRole.JOB_SEEKER:
        query["candidate_id"] = str(current_user.id)
    elif current_user.role == UserRole.EMPLOYER:
        query["employer_id"] = str(current_user.id)
        if job_id:
            query["job_id"] = job_id
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user role"
        )
    
    if status_filter:
        query["status"] = status_filter
    
    if application_id:
        query["application_id"] = application_id
    
    # Get total count
    total = await Interview.find(query).count()
    
    # Get paginated results
    skip = (page - 1) * page_size
    interviews = await Interview.find(query).sort("-scheduled_time").skip(skip).limit(page_size).to_list()
    
    interview_responses = [_interview_to_response(interview) for interview in interviews]
    
    logger.info(f"Retrieved {len(interview_responses)} interviews for user {current_user.email}")
    
    return InterviewListResponse(
        interviews=interview_responses,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{interview_id}", response_model=InterviewResponse)
async def get_interview(
    interview_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific interview by ID.
    
    Args:
        interview_id: Interview ID
        current_user: Current authenticated user
        
    Returns:
        Interview object
        
    Raises:
        HTTPException: If interview not found or unauthorized
    """
    interview = await Interview.get(interview_id)
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Check authorization
    user_id = str(current_user.id)
    if interview.candidate_id != user_id and interview.employer_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this interview"
        )
    
    return _interview_to_response(interview)


@router.put("/{interview_id}", response_model=InterviewResponse)
async def update_interview(
    interview_id: str,
    interview_data: InterviewUpdate,
    current_user: User = Depends(get_current_employer)
):
    """
    Update an interview (Employer only).
    
    Args:
        interview_id: Interview ID
        interview_data: Interview update data
        current_user: Current authenticated employer
        
    Returns:
        Updated interview object
        
    Raises:
        HTTPException: If interview not found or unauthorized
    """
    interview = await Interview.get(interview_id)
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Check authorization
    if interview.employer_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this interview"
        )
    
    # Update fields
    update_data = interview_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if value is not None:
            setattr(interview, field, value)
    
    interview.updated_at = datetime.utcnow()
    await interview.save()
    
    logger.info(f"Interview updated: {interview_id}")
    
    return _interview_to_response(interview)


@router.post("/{interview_id}/reschedule", response_model=InterviewResponse)
async def reschedule_interview(
    interview_id: str,
    reschedule_data: InterviewReschedule,
    current_user: User = Depends(get_current_employer)
):
    """
    Reschedule an interview (Employer only).
    
    Args:
        interview_id: Interview ID
        reschedule_data: Reschedule data with new time
        current_user: Current authenticated employer
        
    Returns:
        Updated interview object
        
    Raises:
        HTTPException: If interview not found or unauthorized
    """
    interview = await Interview.get(interview_id)
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Check authorization
    if interview.employer_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to reschedule this interview"
        )
    
    # Save old time for notification
    old_time = interview.scheduled_time.strftime("%B %d, %Y at %I:%M %p")
    
    # Reschedule
    interview.reschedule(reschedule_data.scheduled_time, reschedule_data.reason)
    await interview.save()
    
    # Send email notifications
    new_time = interview.scheduled_time.strftime("%B %d, %Y at %I:%M %p")
    
    # Send to candidate
    await email_service.send_interview_rescheduled_email(
        to_email=interview.candidate_email,
        recipient_name=interview.candidate_name,
        job_title=interview.job_title,
        company_name=interview.company_name,
        old_time=old_time,
        new_time=new_time,
        duration_minutes=interview.duration_minutes,
        reason=reschedule_data.reason,
        meeting_link=interview.meeting_link,
        is_candidate=True
    )
    
    # Send to employer
    await email_service.send_interview_rescheduled_email(
        to_email=interview.employer_email,
        recipient_name=interview.employer_name,
        job_title=interview.job_title,
        company_name=interview.company_name,
        old_time=old_time,
        new_time=new_time,
        duration_minutes=interview.duration_minutes,
        reason=reschedule_data.reason,
        meeting_link=interview.meeting_link,
        is_candidate=False
    )
    
    logger.info(f"Interview rescheduled: {interview_id}")
    
    return _interview_to_response(interview)


@router.post("/{interview_id}/cancel", response_model=InterviewResponse)
async def cancel_interview(
    interview_id: str,
    cancel_data: InterviewCancel,
    current_user: User = Depends(get_current_user)
):
    """
    Cancel an interview (Employer or Candidate).
    
    Args:
        interview_id: Interview ID
        cancel_data: Cancellation data with optional reason
        current_user: Current authenticated user
        
    Returns:
        Updated interview object
        
    Raises:
        HTTPException: If interview not found or unauthorized
    """
    interview = await Interview.get(interview_id)
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Check authorization
    user_id = str(current_user.id)
    if interview.candidate_id != user_id and interview.employer_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to cancel this interview"
        )
    
    # Cancel
    interview.cancel(cancel_data.reason)
    await interview.save()
    
    # Send email notifications
    scheduled_time = interview.scheduled_time.strftime("%B %d, %Y at %I:%M %p")
    
    # Send to candidate
    await email_service.send_interview_cancelled_email(
        to_email=interview.candidate_email,
        recipient_name=interview.candidate_name,
        job_title=interview.job_title,
        company_name=interview.company_name,
        scheduled_time=scheduled_time,
        reason=cancel_data.reason,
        is_candidate=True
    )
    
    # Send to employer
    await email_service.send_interview_cancelled_email(
        to_email=interview.employer_email,
        recipient_name=interview.employer_name,
        job_title=interview.job_title,
        company_name=interview.company_name,
        scheduled_time=scheduled_time,
        reason=cancel_data.reason,
        is_candidate=False
    )
    
    logger.info(f"Interview cancelled: {interview_id} by {current_user.email}")
    
    return _interview_to_response(interview)


@router.post("/{interview_id}/complete", response_model=InterviewResponse)
async def complete_interview(
    interview_id: str,
    complete_data: InterviewComplete,
    current_user: User = Depends(get_current_employer)
):
    """
    Mark an interview as completed (Employer only).
    
    Args:
        interview_id: Interview ID
        complete_data: Completion data with optional feedback
        current_user: Current authenticated employer
        
    Returns:
        Updated interview object
        
    Raises:
        HTTPException: If interview not found or unauthorized
    """
    interview = await Interview.get(interview_id)
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Check authorization
    if interview.employer_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to complete this interview"
        )
    
    # Complete
    interview.complete(complete_data.feedback)
    if complete_data.interviewer_notes:
        interview.interviewer_notes = complete_data.interviewer_notes
    await interview.save()
    
    logger.info(f"Interview completed: {interview_id}")
    
    return _interview_to_response(interview)


def _interview_to_response(interview: Interview) -> InterviewResponse:
    """Convert Interview model to InterviewResponse schema."""
    return InterviewResponse(
        id=str(interview.id),
        job_id=interview.job_id,
        application_id=interview.application_id,
        candidate_id=interview.candidate_id,
        candidate_name=interview.candidate_name,
        candidate_email=interview.candidate_email,
        employer_id=interview.employer_id,
        employer_name=interview.employer_name,
        employer_email=interview.employer_email,
        company_id=interview.company_id,
        company_name=interview.company_name,
        job_title=interview.job_title,
        scheduled_time=interview.scheduled_time,
        duration_minutes=interview.duration_minutes,
        interview_type=interview.interview_type,
        meeting_link=interview.meeting_link,
        meeting_location=interview.meeting_location,
        meeting_instructions=interview.meeting_instructions,
        status=interview.status,
        status_history=interview.status_history,
        notes=interview.notes,
        feedback=interview.feedback,
        interviewer_notes=interview.interviewer_notes,
        candidate_notified=interview.candidate_notified,
        employer_notified=interview.employer_notified,
        reminder_sent=interview.reminder_sent,
        created_at=interview.created_at,
        updated_at=interview.updated_at,
        created_by=interview.created_by
    )

