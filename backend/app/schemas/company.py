"""
Company schemas for request/response validation.
"""
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime


class CompanyCreate(BaseModel):
    """Schema for company creation during registration."""
    name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    industry: Optional[str] = Field(None, max_length=100)
    size: Optional[str] = Field(None, description="Company size (e.g., '1-10', '11-50', '51-200', '201-500', '500+')")
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    headquarters: Optional[str] = None


class CompanyUpdate(BaseModel):
    """Schema for updating company information."""
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    industry: Optional[str] = Field(None, max_length=100)
    size: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    headquarters: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    logo_url: Optional[str] = None


class CompanyResponse(BaseModel):
    """Schema for company response."""
    id: str
    name: str
    description: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    headquarters: Optional[str] = None
    locations: List[str] = []
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    logo_url: Optional[str] = None
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

