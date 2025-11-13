"""
Job schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.job import JobStatus, JobType, ExperienceLevel


class JobBase(BaseModel):
    """Base job schema with common fields."""
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    
    skills: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    
    location: str = Field(..., min_length=2)
    is_remote: bool = False
    
    salary_min: Optional[float] = Field(None, ge=0)
    salary_max: Optional[float] = Field(None, ge=0)
    salary_currency: str = "USD"
    
    job_type: JobType = JobType.FULL_TIME
    experience_level: ExperienceLevel = ExperienceLevel.MID
    experience_years_min: Optional[int] = Field(None, ge=0)
    experience_years_max: Optional[int] = Field(None, ge=0)
    
    benefits: List[str] = Field(default_factory=list)
    application_instructions: Optional[str] = None


class JobCreate(JobBase):
    """Schema for creating a new job."""
    company_id: Optional[str] = None  # Optional - will use employer's company_name if not provided
    status: JobStatus = JobStatus.DRAFT


class JobUpdate(BaseModel):
    """Schema for updating a job (all fields optional)."""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    
    skills: Optional[List[str]] = None
    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None
    
    location: Optional[str] = Field(None, min_length=2)
    is_remote: Optional[bool] = None
    
    salary_min: Optional[float] = Field(None, ge=0)
    salary_max: Optional[float] = Field(None, ge=0)
    salary_currency: Optional[str] = None
    
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    experience_years_min: Optional[int] = Field(None, ge=0)
    experience_years_max: Optional[int] = Field(None, ge=0)
    
    status: Optional[JobStatus] = None
    
    benefits: Optional[List[str]] = None
    application_instructions: Optional[str] = None


class JobResponse(JobBase):
    """Schema for job response."""
    id: str
    company_id: str
    company_name: str
    employer_id: str
    
    status: JobStatus
    posted_date: Optional[datetime] = None
    closing_date: Optional[datetime] = None
    
    application_count: int = 0
    view_count: int = 0
    
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    """Schema for paginated job list response."""
    jobs: List[JobResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class JobPublish(BaseModel):
    """Schema for publishing a job."""
    publish: bool = True


class JobStatusUpdate(BaseModel):
    """Schema for updating job status."""
    status: JobStatus



