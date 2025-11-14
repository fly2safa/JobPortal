"""
Job recommendation service using AI to match users with suitable jobs.
"""
from typing import List, Dict, Any, Optional
from bson import ObjectId
from app.models.user import User
from app.models.job import Job
from app.models.resume import Resume
from app.repositories.job_repository import JobRepository
from app.ai.providers import get_llm, ProviderError
from app.core.logging import get_logger

logger = get_logger(__name__)


class RecommendationService:
    """Service for generating AI-powered job recommendations."""
    
    def __init__(self):
        self.job_repository = JobRepository()
    
    async def get_recommendations_for_user(
        self,
        user: User,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get personalized job recommendations for a user.
        
        Args:
            user: User object
            limit: Maximum number of recommendations
            
        Returns:
            List of job recommendations with match scores
        """
        try:
            # Get user's resume for skills and experience
            resume = await self._get_user_resume(user.id)
            
            # Get active jobs
            jobs = await self.job_repository.get_active_jobs(limit=100)
            
            if not jobs:
                logger.info(f"No active jobs found for recommendations")
                return []
            
            # Get user profile data
            user_profile = self._build_user_profile(user, resume)
            
            # Score and rank jobs
            recommendations = await self._score_jobs(user_profile, jobs, limit)
            
            logger.info(f"Generated {len(recommendations)} recommendations for user {user.email}")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return []
    
    async def _get_user_resume(self, user_id: ObjectId) -> Optional[Resume]:
        """Get user's most recent resume."""
        try:
            resumes = await Resume.find(
                Resume.user_id == user_id
            ).sort(-Resume.created_at).limit(1).to_list()
            
            return resumes[0] if resumes else None
        except Exception as e:
            logger.error(f"Error fetching user resume: {e}")
            return None
    
    def _build_user_profile(self, user: User, resume: Optional[Resume]) -> Dict[str, Any]:
        """Build user profile for matching."""
        profile = {
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "skills": [],
            "experience": "",
            "education": "",
        }
        
        if resume:
            profile["skills"] = resume.skills_extracted or []
            profile["experience"] = resume.parsed_data.get("experience", "") if resume.parsed_data else ""
            profile["education"] = resume.parsed_data.get("education", "") if resume.parsed_data else ""
        
        return profile
    
    async def _score_jobs(
        self,
        user_profile: Dict[str, Any],
        jobs: List[Job],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Score jobs based on user profile using AI.
        
        Args:
            user_profile: User profile data
            jobs: List of jobs to score
            limit: Maximum number of recommendations
            
        Returns:
            List of scored job recommendations
        """
        recommendations = []
        
        for job in jobs:
            try:
                # Calculate match score using AI
                match_result = await self._calculate_match_score(user_profile, job)
                
                if match_result["score"] > 0:
                    recommendations.append({
                        "job": job,
                        "match_score": match_result["score"],
                        "reasons": match_result["reasons"],
                    })
            except Exception as e:
                logger.error(f"Error scoring job {job.id}: {e}")
                continue
        
        # Sort by match score and return top recommendations
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        return recommendations[:limit]
    
    async def _calculate_match_score(
        self,
        user_profile: Dict[str, Any],
        job: Job
    ) -> Dict[str, Any]:
        """
        Calculate match score between user and job using AI.
        
        Args:
            user_profile: User profile data
            job: Job to match against
            
        Returns:
            Dictionary with score and reasons
        """
        try:
            # Build prompt for AI
            prompt = self._build_matching_prompt(user_profile, job)
            
            # Get LLM with automatic fallback
            llm = get_llm(temperature=0.3, max_tokens=300)
            
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert career advisor. Analyze job matches and provide match scores (0-100) with brief reasons."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Invoke LLM
            response = llm.invoke(messages).content
            
            # Parse response
            match_result = self._parse_match_response(response)
            
            return match_result
            
        except ProviderError as e:
            logger.error(f"All AI providers failed for job matching: {e}")
            # Fallback to simple keyword matching
            return self._simple_keyword_match(user_profile, job)
        except Exception as e:
            logger.error(f"Error calculating match score: {e}")
            return {"score": 0, "reasons": []}
    
    def _build_matching_prompt(self, user_profile: Dict[str, Any], job: Job) -> str:
        """Build prompt for AI matching."""
        user_skills = ", ".join(user_profile["skills"][:10]) if user_profile["skills"] else "No skills listed"
        job_skills = ", ".join(job.skills[:10]) if job.skills else "No specific skills required"
        
        prompt = f"""Analyze this job match:

USER PROFILE:
- Skills: {user_skills}
- Experience: {user_profile.get('experience', 'Not specified')[:200]}
- Education: {user_profile.get('education', 'Not specified')[:200]}

JOB:
- Title: {job.title}
- Company: {job.company_name}
- Required Skills: {job_skills}
- Description: {job.description[:300]}
- Location: {job.location}
- Salary: ${job.salary_min:,} - ${job.salary_max:,}

Provide a match score (0-100) and 2-3 brief reasons. Format:
SCORE: [number]
REASONS:
- [reason 1]
- [reason 2]
- [reason 3]"""
        
        return prompt
    
    def _parse_match_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for match score and reasons."""
        try:
            lines = response.strip().split('\n')
            score = 0
            reasons = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('SCORE:'):
                    score_str = line.replace('SCORE:', '').strip()
                    score = int(''.join(filter(str.isdigit, score_str)))
                elif line.startswith('-'):
                    reason = line.lstrip('- ').strip()
                    if reason:
                        reasons.append(reason)
            
            # Ensure score is within 0-100
            score = max(0, min(100, score))
            
            return {
                "score": score,
                "reasons": reasons[:3]  # Limit to 3 reasons
            }
        except Exception as e:
            logger.error(f"Error parsing match response: {e}")
            return {"score": 0, "reasons": []}
    
    def _simple_keyword_match(self, user_profile: Dict[str, Any], job: Job) -> Dict[str, Any]:
        """Simple keyword-based matching as fallback."""
        user_skills_lower = set(skill.lower() for skill in user_profile["skills"])
        job_skills_lower = set(skill.lower() for skill in job.skills)
        
        # Calculate skill overlap
        matching_skills = user_skills_lower.intersection(job_skills_lower)
        
        if not job_skills_lower:
            score = 50  # Neutral score if no skills specified
        else:
            score = int((len(matching_skills) / len(job_skills_lower)) * 100)
        
        reasons = []
        if matching_skills:
            reasons.append(f"Matching skills: {', '.join(list(matching_skills)[:3])}")
        if score >= 70:
            reasons.append("Strong skill match")
        elif score >= 40:
            reasons.append("Moderate skill match")
        else:
            reasons.append("Limited skill overlap")
        
        return {
            "score": score,
            "reasons": reasons
        }
