"""
Candidate matching service using AI and vector similarity to match candidates with job requirements.

This service uses:
1. ChromaDB vector similarity search (primary) - semantic matching
2. AI scoring with LLM (secondary) - detailed analysis
3. Keyword matching (fallback) - when AI fails
"""
from typing import List, Dict, Any, Optional
from bson import ObjectId
from app.models.job import Job
from app.models.application import Application
from app.models.user import User
from app.models.resume import Resume
from app.ai.providers import get_llm, ProviderError
from app.ai.rag.vectorstore import get_vector_store
from app.ai.chains.candidate_matching_chain import get_candidate_matching_chain
from app.core.logging import get_logger

logger = get_logger(__name__)


class CandidateMatchingService:
    """Service for generating AI-powered candidate recommendations for employers."""
    
    def __init__(self):
        self.vector_store = get_vector_store()
    
    async def get_recommended_candidates_for_job(
        self,
        job: Job,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recommended candidates for a job using vector similarity and AI scoring.
        
        Strategy:
        1. Get all applicants for the job
        2. Build job requirement text
        3. Use vector similarity to find best matching candidate profiles
        4. Enhance top matches with AI scoring for detailed reasons
        5. Fallback to keyword matching if vector search fails
        
        Args:
            job: Job object
            limit: Maximum number of recommendations
            
        Returns:
            List of candidate recommendations with match scores and reasons
        """
        try:
            # Get all applications for this job
            applications = await Application.find(
                Application.job_id == job.id
            ).to_list()
            
            if not applications:
                logger.info(f"No applications found for job {job.id}")
                return []
            
            # Get applicant user IDs
            applicant_ids = [app.applicant_id for app in applications]
            
            # Build job requirement text for vector search
            job_text = self._build_job_text(job)
            
            # Try vector similarity search first
            try:
                # Search for matching profiles in vector store
                vector_matches = self.vector_store.search_profiles(
                    query_text=job_text,
                    n_results=len(applicant_ids) * 2  # Get more candidates for filtering
                )
                
                if vector_matches:
                    logger.info(f"Found {len(vector_matches)} candidate matches via vector similarity")
                    
                    # Filter to only include actual applicants
                    filtered_matches = [
                        match for match in vector_matches
                        if ObjectId(match['user_id']) in applicant_ids
                    ]
                    
                    if filtered_matches:
                        recommendations = await self._enhance_vector_matches(
                            filtered_matches, job, applications, limit
                        )
                        
                        if recommendations:
                            logger.info(f"Generated {len(recommendations)} candidate recommendations for job {job.id}")
                            return recommendations
                
            except Exception as e:
                logger.warning(f"Vector search failed, falling back to traditional scoring: {e}")
            
            # Fallback: Score all applicants using AI or keyword matching
            recommendations = await self._score_all_applicants(
                job, applications, applicant_ids, limit
            )
            
            logger.info(f"Generated {len(recommendations)} candidate recommendations for job {job.id}")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating candidate recommendations: {e}")
            return []
    
    def _build_job_text(self, job: Job) -> str:
        """Build rich text representation of job requirements for vector search."""
        parts = []
        
        if job.title:
            parts.append(f"Position: {job.title}")
        
        if job.description:
            parts.append(f"Description: {job.description}")
        
        if job.requirements:
            if isinstance(job.requirements, list):
                parts.append(f"Requirements: {', '.join(job.requirements)}")
            else:
                parts.append(f"Requirements: {job.requirements}")
        
        if job.skills:
            if isinstance(job.skills, list):
                parts.append(f"Required Skills: {', '.join(job.skills)}")
            else:
                parts.append(f"Required Skills: {job.skills}")
        
        if job.experience_level:
            parts.append(f"Experience Level: {job.experience_level}")
        
        return "\n".join(parts)
    
    async def _enhance_vector_matches(
        self,
        vector_matches: List[Dict[str, Any]],
        job: Job,
        applications: List[Application],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Enhance vector similarity matches with AI scoring and detailed reasons.
        
        Args:
            vector_matches: List of candidates from vector similarity search
            job: Job object
            applications: List of applications for the job
            limit: Maximum number of recommendations
            
        Returns:
            List of enhanced recommendations
        """
        recommendations = []
        
        # Create application lookup
        app_lookup = {str(app.applicant_id): app for app in applications}
        
        for match in vector_matches[:limit * 2]:  # Process more than limit for filtering
            try:
                user_id = ObjectId(match['user_id'])
                
                # Get user and resume
                user = await User.get(user_id)
                if not user:
                    continue
                
                resume = await self._get_user_resume(user_id)
                
                # Get application
                application = app_lookup.get(str(user_id))
                if not application:
                    continue
                
                # Use vector similarity score as base
                vector_score = int(match['similarity_score'] * 100)
                
                # Optionally enhance with AI for top matches
                if len(recommendations) < 5:  # Only use AI for top 5 to save costs
                    try:
                        ai_result = await self._calculate_match_score(job, user, resume)
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
                    "user": user,
                    "resume": resume,
                    "application": application,
                    "match_score": final_score,
                    "reasons": reasons,
                })
                
                if len(recommendations) >= limit:
                    break
                
            except Exception as e:
                logger.error(f"Error enhancing match for candidate {match.get('user_id')}: {e}")
                continue
        
        # Sort by final score
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        return recommendations[:limit]
    
    async def _score_all_applicants(
        self,
        job: Job,
        applications: List[Application],
        applicant_ids: List[ObjectId],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Score all applicants using AI or keyword matching (fallback method).
        
        Args:
            job: Job object
            applications: List of applications
            applicant_ids: List of applicant user IDs
            limit: Maximum number of recommendations
            
        Returns:
            List of scored candidate recommendations
        """
        recommendations = []
        
        for applicant_id in applicant_ids:
            try:
                # Get user and resume
                user = await User.get(applicant_id)
                if not user:
                    continue
                
                resume = await self._get_user_resume(applicant_id)
                
                # Get application
                application = next((app for app in applications if app.applicant_id == applicant_id), None)
                if not application:
                    continue
                
                # Calculate match score using AI
                match_result = await self._calculate_match_score(job, user, resume)
                
                if match_result["score"] > 0:
                    recommendations.append({
                        "user": user,
                        "resume": resume,
                        "application": application,
                        "match_score": match_result["score"],
                        "reasons": match_result["reasons"],
                    })
            except Exception as e:
                logger.error(f"Error scoring applicant {applicant_id}: {e}")
                continue
        
        # Sort by match score and return top recommendations
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        return recommendations[:limit]
    
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
    
    async def _calculate_match_score(
        self,
        job: Job,
        user: User,
        resume: Optional[Resume]
    ) -> Dict[str, Any]:
        """
        Calculate match score between job and candidate using LangChain candidate matching chain.
        
        Args:
            job: Job object
            user: User object
            resume: Resume object (optional)
            
        Returns:
            Dictionary with score and reasons
        """
        try:
            # Get candidate matching chain
            chain = get_candidate_matching_chain(temperature=0.3, max_tokens=300)
            
            # Prepare job data
            job_data = {
                "title": job.title,
                "company_name": job.company_name,
                "skills": job.skills,
                "description": job.description,
                "experience_level": job.experience_level,
            }
            
            # Prepare candidate profile
            candidate_profile = {
                "full_name": user.full_name,
                "skills": resume.skills_extracted if resume else [],
                "experience": resume.parsed_data.get("experience", "Not specified") if resume and resume.parsed_data else "Not specified",
                "education": resume.parsed_data.get("education", "Not specified") if resume and resume.parsed_data else "Not specified",
            }
            
            # Invoke chain
            match_result = await chain.ainvoke(job_data, candidate_profile)
            
            return match_result
            
        except ProviderError as e:
            logger.error(f"All AI providers failed for candidate matching: {e}")
            # Fallback to simple keyword matching
            return self._simple_keyword_match(job, user, resume)
        except Exception as e:
            logger.error(f"Error calculating match score with chain: {e}")
            # Fallback to simple keyword matching
            return self._simple_keyword_match(job, user, resume)
    
    def _build_matching_prompt(self, job: Job, user: User, resume: Optional[Resume]) -> str:
        """Build prompt for AI matching."""
        # Candidate info
        candidate_skills = []
        candidate_experience = "Not specified"
        candidate_education = "Not specified"
        
        if resume:
            candidate_skills = resume.skills_extracted or []
            if resume.parsed_data:
                candidate_experience = resume.parsed_data.get("experience", "Not specified")
                candidate_education = resume.parsed_data.get("education", "Not specified")
        
        candidate_skills_text = ", ".join(candidate_skills[:10]) if candidate_skills else "No skills listed"
        
        # Job info
        job_skills = ", ".join(job.skills[:10]) if job.skills else "No specific skills required"
        
        prompt = f"""Analyze this candidate match:

CANDIDATE:
- Name: {user.full_name}
- Skills: {candidate_skills_text}
- Experience: {candidate_experience[:200]}
- Education: {candidate_education[:200]}

JOB REQUIREMENTS:
- Title: {job.title}
- Company: {job.company_name}
- Required Skills: {job_skills}
- Description: {job.description[:300]}
- Experience Level: {job.experience_level}

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
    
    def _simple_keyword_match(self, job: Job, user: User, resume: Optional[Resume]) -> Dict[str, Any]:
        """Simple keyword-based matching as fallback."""
        candidate_skills = set()
        if resume and resume.skills_extracted:
            candidate_skills = set(skill.lower() for skill in resume.skills_extracted)
        
        job_skills = set(skill.lower() for skill in job.skills) if job.skills else set()
        
        # Calculate skill overlap
        matching_skills = candidate_skills.intersection(job_skills)
        
        if not job_skills:
            score = 50  # Neutral score if no skills specified
        else:
            score = int((len(matching_skills) / len(job_skills)) * 100)
        
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
    
    async def sync_profile_to_vector_store(self, user: User, resume: Optional[Resume] = None) -> bool:
        """
        Sync a user profile to the vector store for semantic search.
        
        Args:
            user: User object
            resume: Resume object (optional, will fetch if not provided)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not resume:
                resume = await self._get_user_resume(user.id)
            
            profile_data = {
                "full_name": user.full_name,
                "email": user.email,
                "skills": resume.skills_extracted if resume else [],
                "experience_years": 0,  # Could be extracted from resume
                "education": resume.parsed_data.get("education", "") if resume and resume.parsed_data else "",
                "work_experience": resume.parsed_data.get("experience", "") if resume and resume.parsed_data else "",
                "summary": resume.parsed_data.get("summary", "") if resume and resume.parsed_data else "",
            }
            
            success = self.vector_store.add_profile(str(user.id), profile_data)
            
            if success:
                logger.debug(f"Synced profile {user.id} to vector store")
            else:
                logger.warning(f"Failed to sync profile {user.id} to vector store")
            
            return success
            
        except Exception as e:
            logger.error(f"Error syncing profile {user.id} to vector store: {e}")
            return False
    
    async def sync_all_profiles_to_vector_store(self) -> Dict[str, int]:
        """
        Sync all job seeker profiles to the vector store.
        
        Returns:
            Dictionary with sync statistics
        """
        try:
            # Get all job seeker users
            users = await User.find(User.role == "job_seeker").to_list()
            
            success_count = 0
            failed_count = 0
            
            for user in users:
                if await self.sync_profile_to_vector_store(user):
                    success_count += 1
                else:
                    failed_count += 1
            
            logger.info(f"Synced {success_count} profiles to vector store, {failed_count} failed")
            
            return {
                "total": len(users),
                "success": success_count,
                "failed": failed_count
            }
            
        except Exception as e:
            logger.error(f"Error syncing all profiles to vector store: {e}")
            return {"total": 0, "success": 0, "failed": 0}

