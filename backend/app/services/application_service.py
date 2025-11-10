"""
Application service for business logic.
"""
from typing import List, Optional, Dict
from fastapi import HTTPException, status
from app.models.application import Application, ApplicationStatus
from app.models.job import Job, JobStatus
from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.repositories.job_repository import JobRepository
from app.services.email_service import email_service
from app.core.logging import get_logger

logger = get_logger(__name__)


class ApplicationService:
    """Service for application business logic."""
    
    def __init__(self):
        self.repository = ApplicationRepository()
        self.job_repository = JobRepository()
    
    async def create_application(
        self,
        job_id: str,
        applicant: User,
        cover_letter: Optional[str] = None,
        resume_url: Optional[str] = None,
        additional_info: Optional[Dict] = None
    ) -> Application:
        """
        Create a new job application.
        
        Args:
            job_id: Job ID
            applicant: Applicant user object
            cover_letter: Optional cover letter
            resume_url: Optional resume URL
            additional_info: Optional additional information
            
        Returns:
            Created application object
            
        Raises:
            HTTPException: If job not found, already applied, or job is closed
        """
        # Check if job exists
        job = await self.job_repository.get_job_by_id(job_id)
        if not job:
            logger.warning(f"Application failed: Job not found - {job_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Check if job is active
        if job.status != JobStatus.ACTIVE:
            logger.warning(f"Application failed: Job not active - {job_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This job is not accepting applications"
            )
        
        # Check if already applied
        existing_application = await self.repository.get_by_applicant_and_job(
            str(applicant.id),
            job_id
        )
        if existing_application:
            logger.warning(
                f"Application failed: Already applied - User {applicant.id} to Job {job_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already applied to this job"
            )
        
        # Create application
        application_data = {
            "job_id": job_id,
            "applicant_id": str(applicant.id),
            "job_title": job.title,
            "company_id": job.company_id,
            "company_name": job.company_name,
            "applicant_name": applicant.full_name,
            "applicant_email": applicant.email,
            "cover_letter": cover_letter,
            "resume_url": resume_url,
            "additional_info": additional_info or {}
        }
        
        application = await self.repository.create_application(application_data)
        
        # Update job application count
        await self.job_repository.increment_application_count(job_id)
        
        # Send confirmation email to applicant
        try:
            await email_service.send_application_submitted_email(
                to_email=applicant.email,
                applicant_name=applicant.full_name,
                job_title=job.title,
                company_name=job.company_name
            )
        except Exception as e:
            logger.error(f"Failed to send application confirmation email: {str(e)}")
        
        logger.info(
            f"Application created: {application.id} by {applicant.email} for job {job_id}"
        )
        
        return application
    
    async def get_application(self, application_id: str) -> Application:
        """
        Get application by ID.
        
        Args:
            application_id: Application ID
            
        Returns:
            Application object
            
        Raises:
            HTTPException: If application not found
        """
        application = await self.repository.get_by_id(application_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )
        return application
    
    async def get_applicant_applications(
        self,
        applicant_id: str,
        status_filter: Optional[ApplicationStatus] = None,
        page: int = 1,
        page_size: int = 10
    ) -> tuple[List[Application], int]:
        """
        Get applications for an applicant.
        
        Args:
            applicant_id: Applicant user ID
            status_filter: Optional status filter
            page: Page number
            page_size: Items per page
            
        Returns:
            Tuple of (list of applications, total count)
        """
        skip = (page - 1) * page_size
        return await self.repository.get_applicant_applications(
            applicant_id,
            status_filter,
            skip,
            page_size
        )
    
    async def get_job_applications(
        self,
        job_id: str,
        employer_id: str,
        status_filter: Optional[ApplicationStatus] = None,
        page: int = 1,
        page_size: int = 10
    ) -> tuple[List[Application], int]:
        """
        Get applications for a job (employer only).
        
        Args:
            job_id: Job ID
            employer_id: Employer user ID (for authorization)
            status_filter: Optional status filter
            page: Page number
            page_size: Items per page
            
        Returns:
            Tuple of (list of applications, total count)
            
        Raises:
            HTTPException: If job not found or user not authorized
        """
        # Verify job exists and employer owns it
        job = await self.job_repository.get_job_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        if job.employer_id != employer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to view applications for this job"
            )
        
        skip = (page - 1) * page_size
        return await self.repository.get_job_applications(
            job_id,
            status_filter,
            skip,
            page_size
        )
    
    async def get_company_applications(
        self,
        company_id: str,
        employer_id: str,
        status_filter: Optional[ApplicationStatus] = None,
        page: int = 1,
        page_size: int = 10
    ) -> tuple[List[Application], int]:
        """
        Get applications for a company (employer only).
        
        Args:
            company_id: Company ID
            employer_id: Employer user ID (for authorization)
            status_filter: Optional status filter
            page: Page number
            page_size: Items per page
            
        Returns:
            Tuple of (list of applications, total count)
            
        Raises:
            HTTPException: If user not authorized
        """
        # Verify employer is associated with the company
        employer = await User.get(employer_id)
        if not employer or employer.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to view applications for this company"
            )
        
        skip = (page - 1) * page_size
        return await self.repository.get_company_applications(
            company_id,
            status_filter,
            skip,
            page_size
        )
    
    async def update_application_status(
        self,
        application_id: str,
        employer_id: str,
        new_status: ApplicationStatus,
        notes: Optional[str] = None,
        rejection_reason: Optional[str] = None
    ) -> Application:
        """
        Update application status (employer only).
        
        Args:
            application_id: Application ID
            employer_id: Employer user ID (for authorization)
            new_status: New status
            notes: Optional notes about the change
            rejection_reason: Optional rejection reason
            
        Returns:
            Updated application object
            
        Raises:
            HTTPException: If application not found or user not authorized
        """
        application = await self.get_application(application_id)
        
        # Verify employer owns the job
        job = await self.job_repository.get_job_by_id(application.job_id)
        if not job or job.employer_id != employer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to update this application"
            )
        
        # Update status
        application = await self.repository.update_status(
            application,
            new_status,
            notes,
            rejection_reason
        )
        
        # Send status update email to applicant
        try:
            await email_service.send_application_status_update_email(
                to_email=application.applicant_email,
                applicant_name=application.applicant_name,
                job_title=application.job_title,
                company_name=application.company_name,
                new_status=new_status.value
            )
        except Exception as e:
            logger.error(f"Failed to send status update email: {str(e)}")
        
        logger.info(
            f"Application status updated: {application.id} -> {new_status} by employer {employer_id}"
        )
        
        return application
    
    async def update_employer_notes(
        self,
        application_id: str,
        employer_id: str,
        notes: str
    ) -> Application:
        """
        Update employer notes on application.
        
        Args:
            application_id: Application ID
            employer_id: Employer user ID (for authorization)
            notes: Employer notes
            
        Returns:
            Updated application object
            
        Raises:
            HTTPException: If application not found or user not authorized
        """
        application = await self.get_application(application_id)
        
        # Verify employer owns the job
        job = await self.job_repository.get_job_by_id(application.job_id)
        if not job or job.employer_id != employer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to update this application"
            )
        
        application.employer_notes = notes
        application = await self.repository.update_application(application)
        
        logger.info(f"Employer notes updated: {application.id} by employer {employer_id}")
        
        return application
    
    async def withdraw_application(
        self,
        application_id: str,
        applicant_id: str
    ) -> Application:
        """
        Withdraw application (applicant only).
        
        Args:
            application_id: Application ID
            applicant_id: Applicant user ID (for authorization)
            
        Returns:
            Updated application object
            
        Raises:
            HTTPException: If application not found or user not authorized
        """
        application = await self.get_application(application_id)
        
        # Verify applicant owns the application
        if application.applicant_id != applicant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to withdraw this application"
            )
        
        # Check if already in final state
        if application.status in [ApplicationStatus.REJECTED, ApplicationStatus.ACCEPTED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot withdraw an application that is already rejected or accepted"
            )
        
        application.withdraw()
        application = await self.repository.update_application(application)
        
        logger.info(f"Application withdrawn: {application.id} by applicant {applicant_id}")
        
        return application
    
    async def delete_application(
        self,
        application_id: str,
        applicant_id: str
    ) -> None:
        """
        Delete application (applicant only, only if pending).
        
        Args:
            application_id: Application ID
            applicant_id: Applicant user ID (for authorization)
            
        Raises:
            HTTPException: If application not found, user not authorized, or not pending
        """
        application = await self.get_application(application_id)
        
        # Verify applicant owns the application
        if application.applicant_id != applicant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to delete this application"
            )
        
        # Only allow deletion if pending
        if application.status != ApplicationStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only delete pending applications. Use withdraw instead."
            )
        
        # Update job application count (decrement)
        job = await self.job_repository.get_job_by_id(application.job_id)
        if job and job.application_count > 0:
            job.application_count -= 1
            await job.save()
        
        await self.repository.delete_application(application)
        
        logger.info(f"Application deleted: {application.id} by applicant {applicant_id}")
    
    async def get_applicant_stats(self, applicant_id: str) -> Dict:
        """
        Get application statistics for an applicant.
        
        Args:
            applicant_id: Applicant user ID
            
        Returns:
            Dictionary with application statistics
        """
        return await self.repository.get_applicant_stats(applicant_id)
    
    async def get_job_stats(self, job_id: str, employer_id: str) -> Dict:
        """
        Get application statistics for a job (employer only).
        
        Args:
            job_id: Job ID
            employer_id: Employer user ID (for authorization)
            
        Returns:
            Dictionary with application statistics
            
        Raises:
            HTTPException: If job not found or user not authorized
        """
        # Verify job exists and employer owns it
        job = await self.job_repository.get_job_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        if job.employer_id != employer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to view statistics for this job"
            )
        
        return await self.repository.get_job_stats(job_id)


# Global service instance
application_service = ApplicationService()

