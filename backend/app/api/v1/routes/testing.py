"""
Testing API Routes

Provides endpoints for the manual testing tracker to save/load test sessions.

Endpoints:
- Real testing data: /api/v1/testing/*
- Mockup/practice data: /api/v1/testing/mockup/*
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.models.test_result import TestSession, TestSessionMockup

router = APIRouter(prefix="/testing", tags=["testing"])


# ============================================================================
# REAL TESTING ENDPOINTS
# ============================================================================

@router.post("/test-sessions", response_model=TestSession)
async def save_test_session(session: TestSession):
    """
    Save a test session to the database.
    
    Args:
        session: TestSession object with test results
        
    Returns:
        Saved TestSession with generated ID
    """
    await session.insert()
    return session


@router.get("/test-sessions/master", response_model=Optional[TestSession])
async def get_master_session():
    """
    Get the latest TEAM_MASTER session.
    
    Returns:
        Latest TestSession marked as master, or None if not found
    """
    master = await TestSession.find_one(
        TestSession.is_master == True,
        sort=[("test_date", -1)]
    )
    return master


@router.get("/test-sessions", response_model=List[TestSession])
async def get_test_sessions(
    tester_name: Optional[str] = None,
    limit: int = Query(default=10, le=100, description="Maximum number of sessions to return")
):
    """
    Get test sessions, optionally filtered by tester.
    
    Args:
        tester_name: Filter by tester name (optional)
        limit: Maximum number of sessions to return (default: 10, max: 100)
        
    Returns:
        List of TestSession objects, sorted by date (newest first)
    """
    query = TestSession.find()
    
    if tester_name:
        query = query.find(TestSession.tester_name == tester_name)
    
    sessions = await query.sort([("test_date", -1)]).limit(limit).to_list()
    return sessions


@router.get("/test-sessions/{session_id}", response_model=TestSession)
async def get_test_session(session_id: str):
    """
    Get a specific test session by ID.
    
    Args:
        session_id: The session ID to retrieve
        
    Returns:
        TestSession object
        
    Raises:
        HTTPException: 404 if session not found
    """
    session = await TestSession.find_one(TestSession.session_id == session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.delete("/test-sessions/{session_id}")
async def delete_test_session(session_id: str):
    """
    Delete a test session.
    
    Args:
        session_id: The session ID to delete
        
    Returns:
        Success message
        
    Raises:
        HTTPException: 404 if session not found
    """
    session = await TestSession.find_one(TestSession.session_id == session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    await session.delete()
    return {"message": "Session deleted successfully"}


# ============================================================================
# MOCKUP/PRACTICE ENDPOINTS
# ============================================================================

@router.post("/mockup/test-sessions", response_model=TestSessionMockup)
async def save_mockup_session(session: TestSessionMockup):
    """
    Save a mockup/practice test session.
    
    Args:
        session: TestSessionMockup object with test results
        
    Returns:
        Saved TestSessionMockup with generated ID
    """
    await session.insert()
    return session


@router.get("/mockup/test-sessions/master", response_model=Optional[TestSessionMockup])
async def get_mockup_master():
    """
    Get the latest MOCKUP TEAM_MASTER session.
    
    Returns:
        Latest TestSessionMockup marked as master, or None if not found
    """
    master = await TestSessionMockup.find_one(
        TestSessionMockup.is_master == True,
        sort=[("test_date", -1)]
    )
    return master


@router.get("/mockup/test-sessions", response_model=List[TestSessionMockup])
async def get_mockup_sessions(
    tester_name: Optional[str] = None,
    limit: int = Query(default=10, le=100)
):
    """
    Get mockup test sessions, optionally filtered by tester.
    
    Args:
        tester_name: Filter by tester name (optional)
        limit: Maximum number of sessions to return (default: 10, max: 100)
        
    Returns:
        List of TestSessionMockup objects, sorted by date (newest first)
    """
    query = TestSessionMockup.find()
    
    if tester_name:
        query = query.find(TestSessionMockup.tester_name == tester_name)
    
    sessions = await query.sort([("test_date", -1)]).limit(limit).to_list()
    return sessions


@router.get("/mockup/test-sessions/{session_id}", response_model=TestSessionMockup)
async def get_mockup_session(session_id: str):
    """
    Get a specific mockup test session by ID.
    
    Args:
        session_id: The session ID to retrieve
        
    Returns:
        TestSessionMockup object
        
    Raises:
        HTTPException: 404 if session not found
    """
    session = await TestSessionMockup.find_one(TestSessionMockup.session_id == session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Mockup session not found")
    return session


@router.delete("/mockup/test-sessions/{session_id}")
async def delete_mockup_session(session_id: str):
    """
    Delete a mockup test session.
    
    Args:
        session_id: The session ID to delete
        
    Returns:
        Success message
        
    Raises:
        HTTPException: 404 if session not found
    """
    session = await TestSessionMockup.find_one(TestSessionMockup.session_id == session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Mockup session not found")
    await session.delete()
    return {"message": "Mockup session deleted successfully"}


@router.delete("/mockup/reset")
async def reset_mockup_data():
    """
    Delete ALL mockup test data.
    
    Useful for resetting the practice environment.
    
    Returns:
        Success message with count of deleted sessions
    """
    result = await TestSessionMockup.find().delete()
    return {
        "message": "Mockup data reset successfully",
        "deleted_count": result.deleted_count if result else 0
    }

