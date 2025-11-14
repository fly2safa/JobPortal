"""
LangChain-based recommendation chain for job and candidate matching.
Uses prompts and LLM to generate intelligent recommendations.
"""
from typing import List, Dict, Any, Optional
from app.ai.providers.openai_client import openai_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class RecommendationChain:
    """
    Chain for generating job recommendations with reasoning.
    Uses OpenAI to analyze user profiles and job descriptions.
    """
    
    def __init__(self):
        """Initialize the recommendation chain."""
        self.client = openai_client
    
    async def generate_job_recommendation_reasons(
        self,
        user_profile: Dict[str, Any],
        job: Dict[str, Any],
        match_score: float
    ) -> List[str]:
        """
        Generate human-readable reasons for why a job matches a user's profile.
        
        Args:
            user_profile: Dictionary with user skills, experience, etc.
            job: Dictionary with job details
            match_score: Numerical match score (0-1)
            
        Returns:
            List of reason strings explaining the match
        """
        if not self.client.is_available:
            logger.warning("OpenAI not available, returning generic reasons")
            return self._generate_fallback_reasons(user_profile, job, match_score)
        
        try:
            # Build prompt for LLM
            prompt = self._build_recommendation_prompt(user_profile, job, match_score)
            
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert career advisor and job matching specialist. "
                               "Provide concise, specific reasons why a job matches a candidate's profile. "
                               "Keep each reason to one short sentence (max 10 words)."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Get LLM response
            response = await self.client.chat_completion_async(
                messages=messages,
                temperature=0.7,
                max_tokens=200
            )
            
            if not response:
                logger.warning("No response from LLM, using fallback")
                return self._generate_fallback_reasons(user_profile, job, match_score)
            
            # Parse response into list of reasons
            reasons = self._parse_reasons(response)
            logger.debug(f"Generated {len(reasons)} recommendation reasons")
            
            return reasons[:3]  # Return top 3 reasons
            
        except Exception as e:
            logger.error(f"Error generating recommendation reasons: {str(e)}")
            return self._generate_fallback_reasons(user_profile, job, match_score)
    
    def _build_recommendation_prompt(
        self,
        user_profile: Dict[str, Any],
        job: Dict[str, Any],
        match_score: float
    ) -> str:
        """Build the prompt for recommendation reasoning."""
        user_skills = ", ".join(user_profile.get("skills", []))
        job_skills = ", ".join(job.get("skills", []))
        
        prompt = f"""Analyze why this job is a good match (score: {match_score:.0%}) for the candidate:

Candidate Profile:
- Skills: {user_skills or 'Not specified'}
- Experience: {user_profile.get('experience_years', 'N/A')} years
- Location: {user_profile.get('location', 'Not specified')}
- Bio: {user_profile.get('bio', 'Not provided')[:200]}

Job Details:
- Title: {job.get('title')}
- Company: {job.get('company_name')}
- Required Skills: {job_skills or 'Not specified'}
- Experience Level: {job.get('experience_level')}
- Location: {job.get('location')}
- Remote: {job.get('is_remote', False)}

Provide exactly 3 specific, concise reasons (one per line) why this job matches the candidate.
Format: - Reason text (max 10 words each)"""
        
        return prompt
    
    def _parse_reasons(self, response: str) -> List[str]:
        """Parse LLM response into a list of reasons."""
        reasons = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            # Remove bullet points, numbers, etc.
            if line.startswith('-'):
                line = line[1:].strip()
            elif line.startswith('•'):
                line = line[1:].strip()
            elif len(line) > 2 and line[0].isdigit() and line[1] in ['.', ')']:
                line = line[2:].strip()
            
            if line and len(line) > 10:  # Minimum reasonable length
                reasons.append(line)
        
        return reasons
    
    def _generate_fallback_reasons(
        self,
        user_profile: Dict[str, Any],
        job: Dict[str, Any],
        match_score: float
    ) -> List[str]:
        """Generate fallback reasons without LLM."""
        reasons = []
        
        # Check skill match
        user_skills = set(s.lower() for s in user_profile.get("skills", []))
        job_skills = set(s.lower() for s in job.get("skills", []))
        matching_skills = user_skills.intersection(job_skills)
        
        if matching_skills:
            top_skills = list(matching_skills)[:2]
            if len(top_skills) == 1:
                reasons.append(f"Strong match in {top_skills[0]}")
            else:
                reasons.append(f"Skills match: {', '.join(top_skills)}")
        
        # Check experience match
        user_exp = user_profile.get("experience_years", 0)
        job_level = job.get("experience_level", "").lower()
        
        if job_level:
            if ("junior" in job_level or "entry" in job_level) and user_exp <= 3:
                reasons.append("Experience level aligns well")
            elif "mid" in job_level and 3 <= user_exp <= 7:
                reasons.append("Perfect experience level match")
            elif ("senior" in job_level or "lead" in job_level) and user_exp >= 5:
                reasons.append("Senior experience matches requirements")
        
        # Check location
        user_loc = user_profile.get("location", "").lower()
        job_loc = job.get("location", "").lower()
        
        if job.get("is_remote"):
            reasons.append("Remote work opportunity")
        elif user_loc and job_loc and user_loc in job_loc:
            reasons.append("Location matches your preferences")
        
        # Check salary if available
        if job.get("salary_max"):
            reasons.append(f"Competitive salary up to ${int(job['salary_max']):,}")
        
        # Default high score reason
        if match_score >= 0.8 and not reasons:
            reasons.append("Excellent overall match for your profile")
        
        # Ensure we have at least one reason
        if not reasons:
            reasons.append("Good fit based on your profile")
        
        return reasons[:3]
    
    async def rank_candidates_for_job(
        self,
        job: Dict[str, Any],
        candidates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Rank candidates for a job position using LLM analysis.
        
        Args:
            job: Job details
            candidates: List of candidate profiles with match scores
            
        Returns:
            Ranked list of candidates with enhanced reasoning
        """
        if not self.client.is_available:
            logger.warning("OpenAI not available, returning candidates as-is")
            return candidates
        
        try:
            # For each candidate, generate reasoning
            ranked_candidates = []
            for candidate in candidates:
                reasons = await self.generate_job_recommendation_reasons(
                    user_profile=candidate,
                    job=job,
                    match_score=candidate.get("match_score", 0.0)
                )
                candidate["match_reasons"] = reasons
                ranked_candidates.append(candidate)
            
            return ranked_candidates
            
        except Exception as e:
            logger.error(f"Error ranking candidates: {str(e)}")
            return candidates


# Global recommendation chain instance
recommendation_chain = RecommendationChain()

