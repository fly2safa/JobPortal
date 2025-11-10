"""
User model for job seekers and employers.
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from beanie import Document
from pydantic import EmailStr, Field


class UserRole(str, Enum):
    """User role enumeration."""
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"
    ADMIN = "admin"


class User(Document):
    """User document model."""
    
    email: EmailStr = Field(..., unique=True, index=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.JOB_SEEKER)
    
    # Profile information
    first_name: str
    last_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    
    # Job seeker specific fields
    skills: List[str] = Field(default_factory=list)
    experience_years: Optional[int] = None
    education: Optional[str] = None
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    
    # Employer specific fields
    company_id: Optional[str] = None
    job_title: Optional[str] = None
    
    # Metadata
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "role",
            "company_id",
        ]
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def dict(self, **kwargs):
        """Override dict to exclude sensitive fields."""
        d = super().dict(**kwargs)
        if 'hashed_password' in d:
            del d['hashed_password']
        return d

