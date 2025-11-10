"""
Search service for job search functionality.
"""
from typing import List, Optional, Dict, Any
from app.models.job import Job, JobType, ExperienceLevel
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobResponse, JobListResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


class SearchService:
    """Service for handling job search operations."""
    
    def __init__(self):
        self.repository = JobRepository()
    
    async def search_jobs(
        self,
        query: Optional[str] = None,
        location: Optional[str] = None,
        skills: Optional[List[str]] = None,
        company_name: Optional[str] = None,
        job_type: Optional[JobType] = None,
        experience_level: Optional[ExperienceLevel] = None,
        is_remote: Optional[bool] = None,
        salary_min: Optional[float] = None,
        salary_max: Optional[float] = None,
        page: int = 1,
        page_size: int = 20
    ) -> JobListResponse:
        """
        Search for jobs with various filters.
        
        Args:
            query: Search query for title and description
            location: Filter by location
            skills: Filter by skills
            company_name: Filter by company name
            job_type: Filter by job type
            experience_level: Filter by experience level
            is_remote: Filter remote jobs
            salary_min: Minimum salary
            salary_max: Maximum salary
            page: Page number
            page_size: Results per page
            
        Returns:
            JobListResponse with paginated results
        """
        logger.info(
            f"Search request - query: {query}, location: {location}, "
            f"skills: {skills}, company: {company_name}"
        )
        
        # Call repository to search jobs
        jobs, total = await self.repository.search_jobs(
            query=query,
            location=location,
            skills=skills,
            company_name=company_name,
            job_type=job_type,
            experience_level=experience_level,
            is_remote=is_remote,
            salary_min=salary_min,
            salary_max=salary_max,
            page=page,
            page_size=page_size
        )
        
        # Convert to response models
        job_responses = [self._job_to_response(job) for job in jobs]
        
        # Calculate total pages
        total_pages = (total + page_size - 1) // page_size
        
        logger.info(f"Search completed - found {total} jobs, page {page}/{total_pages}")
        
        return JobListResponse(
            jobs=job_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    async def get_all_active_jobs(
        self,
        page: int = 1,
        page_size: int = 20
    ) -> JobListResponse:
        """
        Get all active jobs with pagination.
        
        Args:
            page: Page number
            page_size: Results per page
            
        Returns:
            JobListResponse with paginated results
        """
        logger.info(f"Fetching all active jobs - page {page}")
        
        jobs, total = await self.repository.get_active_jobs(
            page=page,
            page_size=page_size
        )
        
        # Convert to response models
        job_responses = [self._job_to_response(job) for job in jobs]
        
        # Calculate total pages
        total_pages = (total + page_size - 1) // page_size
        
        logger.info(f"Retrieved {len(job_responses)} active jobs")
        
        return JobListResponse(
            jobs=job_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    async def get_job_details(self, job_id: str) -> Optional[JobResponse]:
        """
        Get detailed information about a specific job.
        
        Args:
            job_id: Job ID
            
        Returns:
            JobResponse or None if not found
        """
        logger.info(f"Fetching job details for {job_id}")
        
        job = await self.repository.get_job_by_id(job_id)
        
        if not job:
            logger.warning(f"Job not found: {job_id}")
            return None
        
        # Increment view count
        await self.repository.increment_view_count(job_id)
        
        return self._job_to_response(job)
    
    async def get_featured_jobs(self, limit: int = 10) -> List[JobResponse]:
        """
        Get featured/popular jobs.
        
        Args:
            limit: Number of jobs to return
            
        Returns:
            List of featured jobs
        """
        logger.info(f"Fetching {limit} featured jobs")
        
        jobs = await self.repository.get_featured_jobs(limit=limit)
        
        return [self._job_to_response(job) for job in jobs]
    
    async def get_similar_jobs(
        self,
        job_id: str,
        limit: int = 5
    ) -> List[JobResponse]:
        """
        Get similar jobs based on skills and location.
        
        Args:
            job_id: Reference job ID
            limit: Number of similar jobs to return
            
        Returns:
            List of similar jobs
        """
        logger.info(f"Fetching similar jobs for {job_id}")
        
        jobs = await self.repository.get_similar_jobs(
            job_id=job_id,
            limit=limit
        )
        
        return [self._job_to_response(job) for job in jobs]
    
    async def get_jobs_by_company(
        self,
        company_id: str,
        page: int = 1,
        page_size: int = 20
    ) -> JobListResponse:
        """
        Get all active jobs for a specific company.
        
        Args:
            company_id: Company ID
            page: Page number
            page_size: Results per page
            
        Returns:
            JobListResponse with paginated results
        """
        logger.info(f"Fetching jobs for company {company_id}")
        
        jobs, total = await self.repository.get_jobs_by_company(
            company_id=company_id,
            page=page,
            page_size=page_size
        )
        
        # Convert to response models
        job_responses = [self._job_to_response(job) for job in jobs]
        
        # Calculate total pages
        total_pages = (total + page_size - 1) // page_size
        
        logger.info(f"Retrieved {len(job_responses)} jobs for company")
        
        return JobListResponse(
            jobs=job_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    def _job_to_response(self, job: Job) -> JobResponse:
        """
        Convert Job model to JobResponse schema.
        
        Args:
            job: Job model instance
            
        Returns:
            JobResponse schema
        """
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
    
    async def search_by_title(
        self,
        title: str,
        page: int = 1,
        page_size: int = 20
    ) -> JobListResponse:
        """
        Search jobs by title only.
        
        Args:
            title: Job title to search
            page: Page number
            page_size: Results per page
            
        Returns:
            JobListResponse with matching jobs
        """
        return await self.search_jobs(
            query=title,
            page=page,
            page_size=page_size
        )
    
    async def search_by_location(
        self,
        location: str,
        page: int = 1,
        page_size: int = 20
    ) -> JobListResponse:
        """
        Search jobs by location.
        
        Args:
            location: Location to search
            page: Page number
            page_size: Results per page
            
        Returns:
            JobListResponse with matching jobs
        """
        return await self.search_jobs(
            location=location,
            page=page,
            page_size=page_size
        )
    
    async def search_by_skills(
        self,
        skills: List[str],
        page: int = 1,
        page_size: int = 20
    ) -> JobListResponse:
        """
        Search jobs by skills.
        
        Args:
            skills: List of skills to search
            page: Page number
            page_size: Results per page
            
        Returns:
            JobListResponse with matching jobs
        """
        return await self.search_jobs(
            skills=skills,
            page=page,
            page_size=page_size
        )
    
    async def search_remote_jobs(
        self,
        page: int = 1,
        page_size: int = 20
    ) -> JobListResponse:
        """
        Get all remote jobs.
        
        Args:
            page: Page number
            page_size: Results per page
            
        Returns:
            JobListResponse with remote jobs
        """
        return await self.search_jobs(
            is_remote=True,
            page=page,
            page_size=page_size
        )

