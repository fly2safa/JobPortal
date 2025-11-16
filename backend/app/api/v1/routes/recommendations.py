"""
API routes for job recommendations.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.schemas.job import JobResponse
from app.services.recommendation_service import RecommendationService
from app.api.dependencies import get_current_user
from app.core.logging import get_logger
from pydantic import BaseModel

logger = get_logger(__name__)

router = APIRouter()


class JobRecommendationResponse(BaseModel):
    """Job recommendation with match score."""
    job: JobResponse
    match_score: int
    reasons: List[str]
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[JobRecommendationResponse])
async def get_recommendations(
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized job recommendations for the current user.
    
    Args:
        limit: Maximum number of recommendations (default: 10)
        current_user: Authenticated user
        
    Returns:
        List of job recommendations with match scores
    """
    logger.info(f"Fetching recommendations for user: {current_user.email} (role: {current_user.role})")
    
    try:
        # Only job seekers can get recommendations
        if current_user.role != "job_seeker":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only job seekers can access recommendations"
            )
        
        # Get recommendations
        recommendation_service = RecommendationService()
        recommendations = await recommendation_service.get_recommendations_for_user(
            user=current_user,
            limit=limit
        )
        
        logger.info(f"Service returned {len(recommendations)} recommendations (raw)")
        
        # Format response
        response = []
        for rec in recommendations:
            job = rec["job"]
            response.append(JobRecommendationResponse(
                job=JobResponse(
                    id=str(job.id),
                    title=job.title,
                    company_name=job.company_name,
                    company_id=str(job.company_id),
                    employer_id=str(job.employer_id),
                    description=job.description,
                    requirements=job.requirements,
                    responsibilities=job.responsibilities,
                    skills=job.skills,
                    required_skills=job.required_skills or [],
                    preferred_skills=job.preferred_skills or [],
                    location=job.location,
                    is_remote=job.is_remote,
                    job_type=job.job_type,
                    experience_level=job.experience_level,
                    experience_years_min=job.experience_years_min,
                    experience_years_max=job.experience_years_max,
                    salary_min=job.salary_min,
                    salary_max=job.salary_max,
                    salary_currency=job.salary_currency or "USD",
                    posted_date=job.posted_date,
                    closing_date=job.closing_date,
                    status=job.status,
                    application_count=job.application_count,
                    view_count=job.view_count,
                    benefits=job.benefits or [],
                    application_instructions=job.application_instructions,
                    created_at=job.created_at,
                    updated_at=job.updated_at,
                ),
                match_score=rec["match_score"],
                reasons=rec["reasons"]
            ))
        
        logger.info(f"Returning {len(response)} recommendations for user {current_user.email}")
        
        if len(response) == 0:
            logger.warning(f"No recommendations found for user {current_user.email}. Possible reasons: no active jobs, no resume/profile data, or vector search failed.")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recommendations"
        )
