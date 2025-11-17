"""
Job repository for database operations.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from beanie.operators import Or, And, In, RegEx, Text
from app.models.job import Job, JobStatus, JobType, ExperienceLevel
from app.core.logging import get_logger

logger = get_logger(__name__)


class JobRepository:
    """Repository for job-related database operations."""
    
    @staticmethod
    async def search_jobs(
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
    ) -> tuple[List[Job], int]:
        """
        Search jobs with various filters.
        
        Args:
            query: Search query for title and description
            location: Filter by location
            skills: Filter by skills (any match)
            company_name: Filter by company name
            job_type: Filter by job type
            experience_level: Filter by experience level
            is_remote: Filter remote jobs
            salary_min: Minimum salary filter
            salary_max: Maximum salary filter
            page: Page number
            page_size: Number of results per page
            
        Returns:
            Tuple of (list of jobs, total count)
        """
        logger.info(f"Searching jobs with query: {query}, location: {location}, skills: {skills}")
        
        # Build query filters
        filters = [Job.status == JobStatus.ACTIVE]
        
        # Text search on title, description, and company name
        if query:
            query_lower = query.lower()
            filters.append(
                Or(
                    RegEx(Job.title, query_lower, "i"),
                    RegEx(Job.description, query_lower, "i"),
                    RegEx(Job.company_name, query_lower, "i")
                )
            )
        
        # Location filter - match as whole words or phrases with word boundaries
        if location:
            # Escape special regex characters and add word boundaries
            import re
            location_escaped = re.escape(location)
            # Match location as a word or phrase (case-insensitive)
            location_pattern = f"\\b{location_escaped}"
            filters.append(RegEx(Job.location, location_pattern, "i"))
        
        # Skills filter (any of the provided skills should match)
        if skills:
            filters.append(In(Job.skills, skills))
        
        # Company name filter
        if company_name:
            filters.append(RegEx(Job.company_name, company_name, "i"))
        
        # Job type filter
        if job_type:
            filters.append(Job.job_type == job_type)
        
        # Experience level filter
        if experience_level:
            filters.append(Job.experience_level == experience_level)
        
        # Remote filter
        if is_remote is not None:
            filters.append(Job.is_remote == is_remote)
        
        # Salary filters
        if salary_min is not None:
            filters.append(Job.salary_max >= salary_min)
        
        if salary_max is not None:
            filters.append(Job.salary_min <= salary_max)
        
        # Build query
        if len(filters) == 1:
            query_builder = Job.find(filters[0])
        else:
            query_builder = Job.find(And(*filters))
        
        # Get total count
        total = await query_builder.count()
        
        # Get paginated results sorted by posted date (newest first)
        skip = (page - 1) * page_size
        jobs = await query_builder.sort(-Job.posted_date).skip(skip).limit(page_size).to_list()
        
        logger.info(f"Found {total} jobs matching criteria, returning page {page}")
        
        return jobs, total
    
    @staticmethod
    async def get_job_by_id(job_id: str) -> Optional[Job]:
        """
        Get a job by ID.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job object or None if not found
        """
        try:
            job = await Job.get(job_id)
            return job
        except Exception as e:
            logger.error(f"Error fetching job {job_id}: {str(e)}")
            return None
    
    @staticmethod
    async def get_active_jobs(
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[Job], int]:
        """
        Get all active jobs with pagination.
        
        Args:
            page: Page number
            page_size: Number of results per page
            
        Returns:
            Tuple of (list of jobs, total count)
        """
        query = Job.find(Job.status == JobStatus.ACTIVE)
        
        # Get total count
        total = await query.count()
        
        # Get paginated results
        skip = (page - 1) * page_size
        jobs = await query.sort(-Job.posted_date).skip(skip).limit(page_size).to_list()
        
        logger.info(f"Retrieved {len(jobs)} active jobs (page {page})")
        
        return jobs, total
    
    @staticmethod
    async def get_jobs_by_employer(
        employer_id: str,
        status_filter: Optional[JobStatus] = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[Job], int]:
        """
        Get jobs posted by a specific employer.
        
        Args:
            employer_id: Employer user ID
            status_filter: Optional status filter
            page: Page number
            page_size: Number of results per page
            
        Returns:
            Tuple of (list of jobs, total count)
        """
        # Build query
        if status_filter:
            query = Job.find(
                Job.employer_id == employer_id,
                Job.status == status_filter
            )
        else:
            query = Job.find(Job.employer_id == employer_id)
        
        # Get total count
        total = await query.count()
        
        # Get paginated results
        skip = (page - 1) * page_size
        jobs = await query.sort(-Job.created_at).skip(skip).limit(page_size).to_list()
        
        logger.info(f"Retrieved {len(jobs)} jobs for employer {employer_id}")
        
        return jobs, total
    
    @staticmethod
    async def get_jobs_by_company(
        company_id: str,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[Job], int]:
        """
        Get active jobs by company.
        
        Args:
            company_id: Company ID
            page: Page number
            page_size: Number of results per page
            
        Returns:
            Tuple of (list of jobs, total count)
        """
        query = Job.find(
            Job.company_id == company_id,
            Job.status == JobStatus.ACTIVE
        )
        
        # Get total count
        total = await query.count()
        
        # Get paginated results
        skip = (page - 1) * page_size
        jobs = await query.sort(-Job.posted_date).skip(skip).limit(page_size).to_list()
        
        logger.info(f"Retrieved {len(jobs)} jobs for company {company_id}")
        
        return jobs, total
    
    @staticmethod
    async def increment_view_count(job_id: str) -> bool:
        """
        Increment the view count for a job.
        
        Args:
            job_id: Job ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            job = await Job.get(job_id)
            if job:
                job.view_count += 1
                await job.save()
                return True
            return False
        except Exception as e:
            logger.error(f"Error incrementing view count for job {job_id}: {str(e)}")
            return False
    
    @staticmethod
    async def increment_application_count(job_id: str) -> bool:
        """
        Increment the application count for a job.
        
        Args:
            job_id: Job ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            job = await Job.get(job_id)
            if job:
                job.application_count += 1
                await job.save()
                return True
            return False
        except Exception as e:
            logger.error(f"Error incrementing application count for job {job_id}: {str(e)}")
            return False
    
    @staticmethod
    async def get_featured_jobs(limit: int = 10) -> List[Job]:
        """
        Get featured/popular jobs based on view count and recency.
        
        Args:
            limit: Number of jobs to return
            
        Returns:
            List of featured jobs
        """
        query = Job.find(Job.status == JobStatus.ACTIVE)
        
        # Sort by view count (descending) and posted date (descending)
        jobs = await query.sort(
            -Job.view_count,
            -Job.posted_date
        ).limit(limit).to_list()
        
        logger.info(f"Retrieved {len(jobs)} featured jobs")
        
        return jobs
    
    @staticmethod
    async def get_similar_jobs(
        job_id: str,
        limit: int = 5
    ) -> List[Job]:
        """
        Get similar jobs based on skills and location.
        
        Args:
            job_id: Reference job ID
            limit: Number of similar jobs to return
            
        Returns:
            List of similar jobs
        """
        try:
            reference_job = await Job.get(job_id)
            if not reference_job:
                return []
            
            # Find jobs with similar skills or same location
            query = Job.find(
                Job.status == JobStatus.ACTIVE,
                Job.id != reference_job.id,
                Or(
                    In(Job.skills, reference_job.skills[:3]),  # Match top 3 skills
                    Job.location == reference_job.location
                )
            )
            
            jobs = await query.sort(-Job.posted_date).limit(limit).to_list()
            
            logger.info(f"Found {len(jobs)} similar jobs for job {job_id}")
            
            return jobs
        except Exception as e:
            logger.error(f"Error finding similar jobs: {str(e)}")
            return []

