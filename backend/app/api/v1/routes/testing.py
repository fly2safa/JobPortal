"""
Testing routes for test session management.
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query, Request
from beanie import PydanticObjectId
from app.models.test_session import TestSession
from app.schemas.test_session import TestSessionCreate, TestSessionResponse
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/testing", tags=["Testing"])
router_mockup = APIRouter(prefix="/testing/mockup", tags=["Testing Mockup"])


@router.post("/test-sessions", status_code=status.HTTP_201_CREATED, response_model=TestSessionResponse)
async def create_test_session(request: Request, session_data: TestSessionCreate):
    """
    Create a new test session (real mode).
    """
    return await _create_test_session_impl(request, session_data)

@router_mockup.post("/test-sessions", status_code=status.HTTP_201_CREATED, response_model=TestSessionResponse)
async def create_mockup_test_session(request: Request, session_data: TestSessionCreate):
    """
    Create a new test session (mockup mode).
    """
    return await _create_test_session_impl(request, session_data)

async def _create_test_session_impl(request: Request, session_data: TestSessionCreate):
    """
    Create a new test session.
    
    Args:
        request: FastAPI request object
        session_data: Test session data
        
    Returns:
        Created test session
    """
    try:
        logger.info(f"Creating test session: {session_data.session_id} by {session_data.tester_name}")
        
        # Determine mode from request path
        mode = "mockup" if "/mockup" in str(request.url.path) else "real"
        
        # Parse test_date if it's a string
        test_date = datetime.utcnow()
        if session_data.test_date:
            try:
                if isinstance(session_data.test_date, str):
                    # Handle ISO format strings (with or without timezone)
                    date_str = session_data.test_date
                    if date_str.endswith('Z'):
                        date_str = date_str[:-1] + '+00:00'
                    elif '+' not in date_str and 'T' in date_str:
                        # No timezone info, assume UTC
                        date_str = date_str + '+00:00'
                    test_date = datetime.fromisoformat(date_str)
                else:
                    test_date = session_data.test_date
            except Exception as e:
                logger.warning(f"Failed to parse test_date '{session_data.test_date}': {e}, using current time")
                test_date = datetime.utcnow()
        
        # Check if session already exists
        existing_session = await TestSession.find_one(TestSession.session_id == session_data.session_id)
        if existing_session:
            # Update existing session
            existing_session.tester_name = session_data.tester_name
            existing_session.browser = session_data.browser
            existing_session.test_date = test_date
            existing_session.test_cases = session_data.test_cases  # Already dicts
            existing_session.bugs = session_data.bugs  # Already dicts
            existing_session.is_master = session_data.is_master
            existing_session.version = session_data.version
            existing_session.mode = mode  # Update mode in case it changed
            existing_session.updated_at = datetime.utcnow()
            
            await existing_session.save()
            logger.info(f"Updated test session: {session_data.session_id}")
            
            return TestSessionResponse(
                id=str(existing_session.id),
                session_id=existing_session.session_id,
                tester_name=existing_session.tester_name,
                browser=existing_session.browser,
                test_date=existing_session.test_date,
                test_cases=existing_session.test_cases,
                bugs=existing_session.bugs,
                is_master=existing_session.is_master,
                mode=existing_session.mode,
                version=existing_session.version,
                created_at=existing_session.created_at,
                updated_at=existing_session.updated_at
            )
        
        # Create new session
        test_session = TestSession(
            session_id=session_data.session_id,
            tester_name=session_data.tester_name,
            browser=session_data.browser,
            test_date=test_date,
            test_cases=session_data.test_cases,  # Already dicts
            bugs=session_data.bugs,  # Already dicts
            is_master=session_data.is_master,
            mode=mode,
            version=session_data.version
        )
        
        await test_session.insert()
        logger.info(f"Created test session: {session_data.session_id}")
        
        return TestSessionResponse(
            id=str(test_session.id),
            session_id=test_session.session_id,
            tester_name=test_session.tester_name,
            browser=test_session.browser,
            test_date=test_session.test_date,
            test_cases=test_session.test_cases,
            bugs=test_session.bugs,
            is_master=test_session.is_master,
            mode=test_session.mode,
            version=test_session.version,
            created_at=test_session.created_at,
            updated_at=test_session.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating test session: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create test session: {str(e)}"
        )


@router.get("/test-sessions/master", response_model=Optional[TestSessionResponse])
@router_mockup.get("/test-sessions/master", response_model=Optional[TestSessionResponse])
async def get_master_test_session(request: Request, mode: str = Query(default=None, description="Mode: real or mockup")):
    """
    Get the master test session (TEAM_MASTER or MOCKUP_MASTER).
    
    Args:
        mode: Session mode (real or mockup)
        
    Returns:
        Master test session or None if not found
    """
    try:
        # Determine mode from request path if not provided
        if mode is None:
            mode = "mockup" if "/mockup" in str(request.url.path) else "real"
        
        logger.info(f"Fetching master test session for mode: {mode}")
        
        master_session = await TestSession.find_one(
            TestSession.is_master == True,
            TestSession.mode == mode
        ).sort(-TestSession.updated_at)
        
        if not master_session:
            logger.info(f"No master test session found for mode: {mode}")
            return None
        
        logger.info(f"Found master test session: {master_session.session_id}")
        
        return TestSessionResponse(
            id=str(master_session.id),
            session_id=master_session.session_id,
            tester_name=master_session.tester_name,
            browser=master_session.browser,
            test_date=master_session.test_date,
            test_cases=master_session.test_cases,
            bugs=master_session.bugs,
            is_master=master_session.is_master,
            mode=master_session.mode,
            version=master_session.version,
            created_at=master_session.created_at,
            updated_at=master_session.updated_at
        )
        
    except Exception as e:
        logger.error(f"Error fetching master test session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch master test session: {str(e)}"
        )


@router.get("/test-sessions/{session_id}", response_model=TestSessionResponse)
@router_mockup.get("/test-sessions/{session_id}", response_model=TestSessionResponse)
async def get_test_session(session_id: str):
    """
    Get a specific test session by session_id.
    
    Args:
        session_id: Session ID
        
    Returns:
        Test session
    """
    try:
        session = await TestSession.find_one(TestSession.session_id == session_id)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Test session not found: {session_id}"
            )
        
        return TestSessionResponse(
            id=str(session.id),
            session_id=session.session_id,
            tester_name=session.tester_name,
            browser=session.browser,
            test_date=session.test_date,
            test_cases=session.test_cases,
            bugs=session.bugs,
            is_master=session.is_master,
            mode=session.mode,
            version=session.version,
            created_at=session.created_at,
            updated_at=session.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching test session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch test session: {str(e)}"
        )


@router.get("/test-sessions", response_model=list[TestSessionResponse])
@router_mockup.get("/test-sessions", response_model=list[TestSessionResponse])
async def list_test_sessions(
    request: Request,
    mode: Optional[str] = Query(default=None, description="Filter by mode: real or mockup"),
    tester_name: Optional[str] = Query(default=None, description="Filter by tester name"),
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of sessions to return")
):
    """
    List test sessions with optional filters.
    
    Args:
        mode: Filter by mode (real or mockup)
        tester_name: Filter by tester name
        limit: Maximum number of sessions to return
        
    Returns:
        List of test sessions
    """
    try:
        # Determine mode from request path if not provided
        if mode is None:
            mode = "mockup" if "/mockup" in str(request.url.path) else "real"
        
        query = {"mode": mode}  # Always filter by mode
        if tester_name:
            query["tester_name"] = tester_name
        
        sessions = await TestSession.find(query).sort(-TestSession.updated_at).limit(limit).to_list()
        
        return [
            TestSessionResponse(
                id=str(session.id),
                session_id=session.session_id,
                tester_name=session.tester_name,
                browser=session.browser,
                test_date=session.test_date,
                test_cases=session.test_cases,
                bugs=session.bugs,
                is_master=session.is_master,
                mode=session.mode,
                version=session.version,
                created_at=session.created_at,
                updated_at=session.updated_at
            )
            for session in sessions
        ]
        
    except Exception as e:
        logger.error(f"Error listing test sessions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list test sessions: {str(e)}"
        )

