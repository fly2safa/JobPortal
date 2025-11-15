"""
Authentication routes for user registration and login.
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends, Request
from app.schemas.auth import UserRegister, UserLogin, Token
from app.schemas.user import UserResponse
from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.logging import get_logger
from app.core.rate_limiting import limiter, RATE_LIMIT_AUTH
from app.api.dependencies import get_current_user

logger = get_logger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit(RATE_LIMIT_AUTH)
async def register(request: Request, user_data: UserRegister):
    """
    Register a new user account.
    
    Args:
        user_data: User registration data
        
    Returns:
        Created user object
        
    Raises:
        HTTPException: If email already exists
    """
    logger.info(f"Registration attempt for email: {user_data.email}")
    
    # Check if user already exists
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        logger.warning(f"Registration failed: Email already exists - {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered. Please fix your email and try again"
        )
    
    # Create new user
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        phone=user_data.phone,
        location=user_data.location,
        company_name=user_data.company_name if user_data.role == "employer" else None,
    )
    
    await user.insert()
    logger.info(f"User registered successfully: {user.email} (ID: {user.id})")
    
    # Create access token for auto-login
    token_data = {
        "user_id": str(user.id),
        "email": user.email,
        "role": user.role,
    }
    access_token = create_access_token(token_data)
    
    # Convert to response model
    user_response = UserResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        phone=user.phone,
        location=user.location,
        skills=user.skills,
        experience_years=user.experience_years,
        education=user.education,
        bio=user.bio,
        linkedin_url=user.linkedin_url,
        portfolio_url=user.portfolio_url,
        company_id=user.company_id,
        company_name=user.company_name,
        job_title=user.job_title,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
    )
    
    return {
        "user": user_response,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login")
@limiter.limit(RATE_LIMIT_AUTH)
async def login(request: Request, credentials: UserLogin):
    """
    Authenticate user and return JWT token and user data.
    
    Args:
        credentials: User login credentials
        
    Returns:
        JWT access token and user object
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Log rate limiting check (for debugging)
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"Login attempt for email: {credentials.email} from IP: {client_ip}")
    
    # Find user by email
    user = await User.find_one(User.email == credentials.email)
    if not user:
        logger.warning(f"Login failed: User not found - {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        logger.warning(f"Login failed: Invalid password - {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        logger.warning(f"Login failed: Inactive account - {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    await user.save()
    
    # Create access token
    token_data = {
        "user_id": str(user.id),
        "email": user.email,
        "role": user.role,
    }
    access_token = create_access_token(token_data)
    
    # Convert to response model
    user_response = UserResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        phone=user.phone,
        location=user.location,
        skills=user.skills,
        experience_years=user.experience_years,
        education=user.education,
        bio=user.bio,
        linkedin_url=user.linkedin_url,
        portfolio_url=user.portfolio_url,
        company_id=user.company_id,
        company_name=user.company_name,
        job_title=user.job_title,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
    )
    
    logger.info(f"User logged in successfully: {user.email}")
    
    return {
        "user": user_response,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user object
    """
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        role=current_user.role,
        phone=current_user.phone,
        location=current_user.location,
        skills=current_user.skills,
        experience_years=current_user.experience_years,
        education=current_user.education,
        bio=current_user.bio,
        linkedin_url=current_user.linkedin_url,
        portfolio_url=current_user.portfolio_url,
        company_id=current_user.company_id,
        company_name=current_user.company_name,
        job_title=current_user.job_title,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
    )

