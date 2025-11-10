"""
User profile management routes.
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.user import UserResponse, UserUpdate
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User profile data
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
        job_title=current_user.job_title,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
    )


@router.put("/me", response_model=UserResponse)
async def update_profile(
    profile_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update current user's profile.
    
    Args:
        profile_data: Profile update data
        current_user: Current authenticated user
        
    Returns:
        Updated user profile data
    """
    logger.info(f"Profile update request from user {current_user.id}")
    
    # Update only provided fields
    update_data = profile_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    # Update timestamp
    current_user.updated_at = datetime.utcnow()
    
    # Save to database
    await current_user.save()
    
    logger.info(f"Profile updated for user {current_user.id}")
    
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
        job_title=current_user.job_title,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
    )

