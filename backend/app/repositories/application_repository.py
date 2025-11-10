"""
Application repository for database operations.
"""
from typing import List, Optional, Dict
from datetime import datetime
from app.models.application import Application, ApplicationStatus
from app.core.logging import get_logger

logger = get_logger(__name__)


class ApplicationRepository:
    """Repository for application database operations."""
    
    @staticmethod
    async def create_application(application_data: Dict) -> Application:
        """
        Create a new application.
        
        Args:
            application_data: Dictionary containing application data
            
        Returns:
            Created application object
        """
        application = Application(**application_data)
        await application.insert()
        logger.info(f"Application created: {application.id} for job {application.job_id}")
        return application
    
    @staticmethod
    async def get_by_id(application_id: str) -> Optional[Application]:
        """
        Get application by ID.
        
        Args:
            application_id: Application ID
            
        Returns:
            Application object or None if not found
        """
        return await Application.get(application_id)
    
    @staticmethod
    async def get_by_applicant_and_job(
        applicant_id: str,
        job_id: str
    ) -> Optional[Application]:
        """
        Get application by applicant and job.
        
        Args:
            applicant_id: Applicant user ID
            job_id: Job ID
            
        Returns:
            Application object or None if not found
        """
        return await Application.find_one(
            Application.applicant_id == applicant_id,
            Application.job_id == job_id
        )
    
    @staticmethod
    async def get_applicant_applications(
        applicant_id: str,
        status: Optional[ApplicationStatus] = None,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[Application], int]:
        """
        Get applications for an applicant with pagination.
        
        Args:
            applicant_id: Applicant user ID
            status: Optional status filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (list of applications, total count)
        """
        query = Application.find(Application.applicant_id == applicant_id)
        
        if status:
            query = query.find(Application.status == status)
        
        total = await query.count()
        applications = await query.sort(-Application.applied_at).skip(skip).limit(limit).to_list()
        
        logger.info(f"Retrieved {len(applications)} applications for applicant {applicant_id}")
        return applications, total
    
    @staticmethod
    async def get_job_applications(
        job_id: str,
        status: Optional[ApplicationStatus] = None,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[Application], int]:
        """
        Get applications for a job with pagination.
        
        Args:
            job_id: Job ID
            status: Optional status filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (list of applications, total count)
        """
        query = Application.find(Application.job_id == job_id)
        
        if status:
            query = query.find(Application.status == status)
        
        total = await query.count()
        applications = await query.sort(-Application.applied_at).skip(skip).limit(limit).to_list()
        
        logger.info(f"Retrieved {len(applications)} applications for job {job_id}")
        return applications, total
    
    @staticmethod
    async def get_company_applications(
        company_id: str,
        status: Optional[ApplicationStatus] = None,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[Application], int]:
        """
        Get applications for a company with pagination.
        
        Args:
            company_id: Company ID
            status: Optional status filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (list of applications, total count)
        """
        query = Application.find(Application.company_id == company_id)
        
        if status:
            query = query.find(Application.status == status)
        
        total = await query.count()
        applications = await query.sort(-Application.applied_at).skip(skip).limit(limit).to_list()
        
        logger.info(f"Retrieved {len(applications)} applications for company {company_id}")
        return applications, total
    
    @staticmethod
    async def update_application(
        application: Application
    ) -> Application:
        """
        Update an application.
        
        Args:
            application: Application object to update
            
        Returns:
            Updated application object
        """
        application.updated_at = datetime.utcnow()
        await application.save()
        logger.info(f"Application updated: {application.id}")
        return application
    
    @staticmethod
    async def update_status(
        application: Application,
        new_status: ApplicationStatus,
        notes: Optional[str] = None,
        rejection_reason: Optional[str] = None
    ) -> Application:
        """
        Update application status.
        
        Args:
            application: Application object
            new_status: New status
            notes: Optional notes about the change
            rejection_reason: Optional rejection reason
            
        Returns:
            Updated application object
        """
        application.update_status(new_status, notes)
        
        if rejection_reason:
            application.rejection_reason = rejection_reason
        
        await application.save()
        logger.info(f"Application status updated: {application.id} -> {new_status}")
        return application
    
    @staticmethod
    async def delete_application(application: Application) -> None:
        """
        Delete an application.
        
        Args:
            application: Application object to delete
        """
        await application.delete()
        logger.info(f"Application deleted: {application.id}")
    
    @staticmethod
    async def get_applicant_stats(applicant_id: str) -> Dict:
        """
        Get application statistics for an applicant.
        
        Args:
            applicant_id: Applicant user ID
            
        Returns:
            Dictionary with application statistics
        """
        applications = await Application.find(
            Application.applicant_id == applicant_id
        ).to_list()
        
        stats = {
            "total": len(applications),
            "pending": 0,
            "reviewing": 0,
            "shortlisted": 0,
            "interview": 0,
            "rejected": 0,
            "accepted": 0,
            "withdrawn": 0,
        }
        
        for app in applications:
            status_key = app.status.value
            if status_key in stats:
                stats[status_key] += 1
        
        return stats
    
    @staticmethod
    async def get_job_stats(job_id: str) -> Dict:
        """
        Get application statistics for a job.
        
        Args:
            job_id: Job ID
            
        Returns:
            Dictionary with application statistics
        """
        applications = await Application.find(
            Application.job_id == job_id
        ).to_list()
        
        stats = {
            "total": len(applications),
            "pending": 0,
            "reviewing": 0,
            "shortlisted": 0,
            "interview": 0,
            "rejected": 0,
            "accepted": 0,
            "withdrawn": 0,
        }
        
        for app in applications:
            status_key = app.status.value
            if status_key in stats:
                stats[status_key] += 1
        
        return stats

