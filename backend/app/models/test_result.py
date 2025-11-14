"""
Testing Data Models

These collections store manual testing results and are separate from
JobPortal production data.

Collections:
- test_sessions: Real testing data for QA tracking
- test_sessions_mockup: Practice/training data (can be reset anytime)

Note: Collections are auto-created by Beanie ODM on first insert.
No manual MongoDB setup required.
"""

from beanie import Document
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Bug(BaseModel):
    """Embedded bug report within a test session"""
    bug_id: str
    test_id: str
    severity: str
    description: str
    steps_to_reproduce: str
    expected: str
    actual: str
    reported_by: str
    reported_date: datetime


class TestCaseResult(BaseModel):
    """Embedded test case result (not a separate collection)"""
    test_id: str
    section: str
    title: str
    status: str  # Pass, Fail, Blocked, Not Started
    actual_results: str = ""
    notes: str = ""
    tested_date: Optional[datetime] = None


class TestSession(Document):
    """
    Test session with embedded test cases.
    
    Collection: test_sessions
    Each session contains all 40 test cases as an embedded array.
    Estimated size: ~5-10 KB per session
    """
    session_id: str
    tester_name: str
    browser: str
    test_date: datetime = Field(default_factory=datetime.now)
    test_cases: List[TestCaseResult] = []
    bugs: List[Bug] = []
    is_master: bool = False
    version: str = "2.0.0"
    
    class Settings:
        name = "test_sessions"
        
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "Alice_20240113_143022",
                "tester_name": "Alice",
                "browser": "Chrome 120",
                "test_date": "2024-01-13T14:30:22",
                "is_master": False,
                "version": "2.0.0"
            }
        }


class TestSessionMockup(Document):
    """
    Mockup/practice test session with embedded test cases.
    
    Collection: test_sessions_mockup
    Same structure as TestSession, but for practice/training.
    Can be reset anytime without affecting real test data.
    """
    session_id: str
    tester_name: str
    browser: str
    test_date: datetime = Field(default_factory=datetime.now)
    test_cases: List[TestCaseResult] = []
    bugs: List[Bug] = []
    is_master: bool = False
    version: str = "2.0.0"
    
    class Settings:
        name = "test_sessions_mockup"
        
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "Alice_MOCKUP_20240113_143022",
                "tester_name": "Alice",
                "browser": "Chrome 120",
                "test_date": "2024-01-13T14:30:22",
                "is_master": False,
                "version": "2.0.0"
            }
        }

