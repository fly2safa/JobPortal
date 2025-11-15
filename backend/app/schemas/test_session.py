"""
Schemas for test session API requests and responses.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TestCaseDataSchema(BaseModel):
    """Test case data schema."""
    
    test_id: str
    section: str
    title: str
    status: str
    actual_results: Optional[str] = None
    notes: Optional[str] = None
    tested_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class BugDataSchema(BaseModel):
    """Bug data schema."""
    
    bug_id: str
    test_id: str
    severity: str
    description: str
    steps_to_reproduce: str
    expected: str
    actual: str
    reported_by: Optional[str] = None
    reported_date: Optional[str] = None
    
    class Config:
        from_attributes = True


class TestSessionCreate(BaseModel):
    """Schema for creating a test session."""
    
    session_id: str
    tester_name: str
    browser: str
    test_date: Optional[str] = None  # Accept ISO string from frontend
    test_cases: List[dict] = Field(default_factory=list)  # Accept dict directly
    bugs: List[dict] = Field(default_factory=list)  # Accept dict directly
    is_master: bool = False
    version: Optional[str] = None
    
    class Config:
        from_attributes = True


class TestSessionResponse(BaseModel):
    """Schema for test session response."""
    
    id: str
    session_id: str
    tester_name: str
    browser: str
    test_date: datetime
    test_cases: List[dict]
    bugs: List[dict]
    is_master: bool
    mode: str
    version: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

