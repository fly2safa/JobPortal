"""
Company model for employer profiles.
"""
from datetime import datetime
from typing import Optional, List
from beanie import Document
from pydantic import Field, HttpUrl


class Company(Document):
    """Company document model."""
    
    name: str = Field(..., index=True)
    description: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None  # e.g., "1-10", "11-50", "51-200", "201-500", "500+"
    
    # Contact information
    website: Optional[HttpUrl] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    
    # Location
    headquarters: Optional[str] = None
    locations: List[str] = Field(default_factory=list)
    
    # Social media
    linkedin_url: Optional[HttpUrl] = None
    twitter_url: Optional[HttpUrl] = None
    
    # Logo and branding
    logo_url: Optional[str] = None
    
    # Metadata
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "companies"
        indexes = [
            "name",
            "industry",
        ]




