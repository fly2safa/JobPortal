"""
Job model for job postings.
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from beanie import Document, Link
from pydantic import Field


class JobStatus(str, Enum):
    """Job status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"


class JobType(str, Enum):
    """Job type enumeration."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"


class ExperienceLevel(str, Enum):
    """Experience level enumeration."""
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"


class Job(Document):
    """Job posting document model."""
    
    # Basic information
    title: str = Field(..., index=True)
    description: str
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    
    # Skills and qualifications
    skills: List[str] = Field(default_factory=list, index=True)
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    
    # Location
    location: str = Field(..., index=True)
    is_remote: bool = Field(default=False)
    
    # Company and employer
    company_id: str = Field(..., index=True)
    company_name: str = Field(..., index=True)  # Denormalized for faster queries
    employer_id: str = Field(..., index=True)  # User who posted the job
    
    # Compensation
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: str = Field(default="USD")
    
    # Job details
    job_type: JobType = Field(default=JobType.FULL_TIME)
    experience_level: ExperienceLevel = Field(default=ExperienceLevel.MID)
    experience_years_min: Optional[int] = None
    experience_years_max: Optional[int] = None
    
    # Status and metadata
    status: JobStatus = Field(default=JobStatus.DRAFT, index=True)
    posted_date: Optional[datetime] = None
    closing_date: Optional[datetime] = None
    
    # Application tracking
    application_count: int = Field(default=0)
    view_count: int = Field(default=0)
    
    # Additional information
    benefits: List[str] = Field(default_factory=list)
    application_instructions: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "jobs"
        indexes = [
            "title",
            "company_id",
            "employer_id",
            "status",
            "location",
            "skills",
            "company_name",
            "posted_date",
        ]
    
    def dict(self, **kwargs):
        """Override dict to include custom serialization."""
        d = super().dict(**kwargs)
        return d
    
    def publish(self):
        """Publish the job (change status from draft to active)."""
        if self.status == JobStatus.DRAFT:
            self.status = JobStatus.ACTIVE
            self.posted_date = datetime.utcnow()
            self.updated_at = datetime.utcnow()
    
    def close(self):
        """Close the job (no longer accepting applications)."""
        if self.status == JobStatus.ACTIVE:
            self.status = JobStatus.CLOSED
            self.closing_date = datetime.utcnow()
            self.updated_at = datetime.utcnow()
    
    def archive(self):
        """Archive the job."""
        self.status = JobStatus.ARCHIVED
        self.updated_at = datetime.utcnow()



