"""
Job recommendation service using AI and vector similarity to match users with suitable jobs.

This service uses:
1. ChromaDB vector similarity search (primary) - semantic matching
2. AI scoring with LLM (secondary) - detailed analysis
3. Keyword matching (fallback) - when AI fails
"""
from typing import List, Dict, Any, Optional
from bson import ObjectId
from app.models.user import User
from app.models.job import Job
from app.models.resume import Resume
from app.repositories.job_repository import JobRepository
from app.ai.providers import get_llm, ProviderError
from app.ai.rag.vectorstore import get_vector_store
from app.ai.chains.recommendation_chain import get_recommendation_chain
from app.core.logging import get_logger

logger = get_logger(__name__)


class RecommendationService:
    """Service for generating AI-powered job recommendations using vector similarity."""
    
    def __init__(self):
        self.job_repository = JobRepository()
        self.vector_store = get_vector_store()
    
    async def get_recommendations_for_user(
        self,
        user: User,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get personalized job recommendations for a user using vector similarity.
        
        Strategy:
        1. Build user profile text from resume and skills
        2. Use vector similarity search to find semantically similar jobs
        3. Enhance top matches with AI scoring for detailed reasons
        4. Fallback to keyword matching if vector search fails
        
        Args:
            user: User object
            limit: Maximum number of recommendations
            
        Returns:
            List of job recommendations with match scores and reasons
        """
        try:
            # Get user's resume for skills and experience
            resume = await self._get_user_resume(user.id)
            
            # Build user profile
            user_profile = self._build_user_profile(user, resume)
            user_profile_text = self._build_profile_text(user_profile)
            
            # First, try vector similarity search
            try:
                vector_matches = self.vector_store.search_jobs(
                    query_text=user_profile_text,
                    n_results=limit * 2  # Get more candidates for AI refinement
                )
                
                if vector_matches:
                    logger.info(f"Found {len(vector_matches)} jobs via vector similarity")
                    recommendations = await self._enhance_vector_matches(
                        vector_matches, user_profile, limit
                    )
                    
                    if recommendations:
                        logger.info(f"Generated {len(recommendations)} recommendations for user {user.email}")
                        return recommendations
                
            except Exception as e:
                logger.warning(f"Vector search failed, falling back to traditional scoring: {e}")
            
            # Fallback: Get all active jobs and score them
            jobs = await self.job_repository.get_active_jobs(limit=100)
            
            if not jobs:
                logger.info(f"No active jobs found for recommendations")
                return []
            
            # Score and rank jobs using AI
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
    
    def _build_profile_text(self, user_profile: Dict[str, Any]) -> str:
        """Build rich text representation of user profile for vector search."""
        parts = []
        
        if user_profile.get("full_name"):
            parts.append(f"Candidate: {user_profile['full_name']}")
        
        if user_profile.get("skills"):
            skills_text = ", ".join(user_profile["skills"])
            parts.append(f"Skills: {skills_text}")
        
        if user_profile.get("experience"):
            parts.append(f"Experience: {user_profile['experience']}")
        
        if user_profile.get("education"):
            parts.append(f"Education: {user_profile['education']}")
        
        return "\n".join(parts)
    
    async def _enhance_vector_matches(
        self,
        vector_matches: List[Dict[str, Any]],
        user_profile: Dict[str, Any],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Enhance vector similarity matches with AI scoring and detailed reasons.
        
        Args:
            vector_matches: List of jobs from vector similarity search
            user_profile: User profile data
            limit: Maximum number of recommendations
            
        Returns:
            List of enhanced recommendations
        """
        recommendations = []
        
        for match in vector_matches[:limit]:
            try:
                # Get full job details
                job_id = match['job_id']
                job = await self.job_repository.get_job_by_id(job_id)
                
                if not job:
                    continue
                
                # Use vector similarity score as base
                vector_score = int(match['similarity_score'] * 100)
                
                # Optionally enhance with AI for top matches
                if len(recommendations) < 5:  # Only use AI for top 5 to save costs
                    try:
                        ai_result = await self._calculate_match_score(user_profile, job)
                        # Blend vector and AI scores (70% vector, 30% AI)
                        final_score = int(vector_score * 0.7 + ai_result["score"] * 0.3)
                        reasons = ai_result["reasons"] or [f"Semantic similarity: {vector_score}%"]
                    except Exception as e:
                        logger.warning(f"AI scoring failed, using vector score only: {e}")
                        final_score = vector_score
                        reasons = [f"Semantic similarity: {vector_score}%"]
                else:
                    # For remaining matches, use vector score only
                    final_score = vector_score
                    reasons = [f"Semantic similarity: {vector_score}%"]
                
                recommendations.append({
                    "job": job,
                    "match_score": final_score,
                    "reasons": reasons,
                })
                
            except Exception as e:
                logger.error(f"Error enhancing match for job {match.get('job_id')}: {e}")
                continue
        
        # Sort by final score
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        return recommendations[:limit]
    
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
        Calculate match score between user and job using LangChain recommendation chain.
        
        Args:
            user_profile: User profile data
            job: Job to match against
            
        Returns:
            Dictionary with score and reasons
        """
        try:
            # Get recommendation chain
            chain = get_recommendation_chain(temperature=0.3, max_tokens=300)
            
            # Prepare job data
            job_data = {
                "title": job.title,
                "company_name": job.company_name,
                "skills": job.skills,
                "description": job.description,
                "experience_level": job.experience_level,
                "location": job.location,
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
            }
            
            # Invoke chain
            match_result = await chain.ainvoke(user_profile, job_data)
            
            return match_result
            
        except ProviderError as e:
            logger.error(f"All AI providers failed for job matching: {e}")
            # Fallback to simple keyword matching
            return self._simple_keyword_match(user_profile, job)
        except Exception as e:
            logger.error(f"Error calculating match score with chain: {e}")
            # Fallback to simple keyword matching
            return self._simple_keyword_match(user_profile, job)
    
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
    
    async def sync_job_to_vector_store(self, job: Job) -> bool:
        """
        Sync a job to the vector store for semantic search.
        
        Args:
            job: Job object to sync
            
        Returns:
            True if successful, False otherwise
        """
        try:
            job_data = {
                "title": job.title,
                "company_name": job.company_name,
                "location": job.location,
                "description": job.description,
                "requirements": job.requirements,
                "skills": job.skills,
                "experience_level": job.experience_level,
                "job_type": job.job_type,
            }
            
            success = self.vector_store.add_job(str(job.id), job_data)
            
            if success:
                logger.debug(f"Synced job {job.id} to vector store")
            else:
                logger.warning(f"Failed to sync job {job.id} to vector store")
            
            return success
            
        except Exception as e:
            logger.error(f"Error syncing job {job.id} to vector store: {e}")
            return False
    
    async def sync_all_jobs_to_vector_store(self) -> Dict[str, int]:
        """
        Sync all active jobs to the vector store.
        
        Returns:
            Dictionary with sync statistics
        """
        try:
            jobs = await self.job_repository.get_active_jobs(limit=1000)
            
            success_count = 0
            failed_count = 0
            
            for job in jobs:
                if await self.sync_job_to_vector_store(job):
                    success_count += 1
                else:
                    failed_count += 1
            
            logger.info(f"Synced {success_count} jobs to vector store, {failed_count} failed")
            
            return {
                "total": len(jobs),
                "success": success_count,
                "failed": failed_count
            }
            
        except Exception as e:
            logger.error(f"Error syncing all jobs to vector store: {e}")
            return {"total": 0, "success": 0, "failed": 0}
