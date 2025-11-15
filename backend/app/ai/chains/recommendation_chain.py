"""
LangChain prompt chain for AI-powered job recommendations.

This module implements a LangChain chain that analyzes user profiles and job descriptions
to generate match scores and recommendations. Also supports simpler reason generation for
backward compatibility.
"""
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from app.ai.providers import get_llm
from app.core.logging import get_logger

logger = get_logger(__name__)


class JobMatchOutput(BaseModel):
    """Output schema for job matching."""
    match_score: int = Field(
        description="Match score from 0 to 100 indicating how well the job matches the user's profile",
        ge=0,
        le=100
    )
    reasons: List[str] = Field(
        description="List of 2-3 specific reasons explaining why this job is a good match",
        min_items=1,
        max_items=3
    )


class RecommendationChain:
    """
    LangChain chain for generating job recommendations.
    
    This chain takes a user profile and job description as input and outputs
    a structured match score with detailed reasons. Also supports simpler
    reason generation for backward compatibility.
    """
    
    def __init__(self, temperature: float = 0.3, max_tokens: int = 300):
        """
        Initialize the recommendation chain.
        
        Args:
            temperature: LLM temperature for response generation
            max_tokens: Maximum tokens for LLM response
        """
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.parser = JsonOutputParser(pydantic_object=JobMatchOutput)
        self.chain = self._build_chain()
    
    def _build_chain(self):
        """Build the LangChain prompt chain."""
        # Define the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert career advisor and job matching AI.
Your task is to analyze a user's profile against a job description and provide:
1. A match score from 0-100 (higher = better match)
2. 2-3 specific, actionable reasons explaining the match

Consider:
- Skill alignment (technical and soft skills)
- Experience level match
- Education requirements
- Career progression fit
- Industry relevance

{format_instructions}"""),
            ("user", """Analyze this job match:

USER PROFILE:
Name: {user_name}
Skills: {user_skills}
Experience: {user_experience}
Education: {user_education}

JOB:
Title: {job_title}
Company: {job_company}
Required Skills: {job_skills}
Description: {job_description}
Experience Level: {job_experience_level}
Location: {job_location}
Salary: ${job_salary_min:,} - ${job_salary_max:,}

Provide your analysis as JSON with match_score and reasons.""")
        ])
        
        # Build the chain: prompt -> LLM -> parser
        chain = (
            {
                "user_name": lambda x: x["user_name"],
                "user_skills": lambda x: x["user_skills"],
                "user_experience": lambda x: x["user_experience"],
                "user_education": lambda x: x["user_education"],
                "job_title": lambda x: x["job_title"],
                "job_company": lambda x: x["job_company"],
                "job_skills": lambda x: x["job_skills"],
                "job_description": lambda x: x["job_description"],
                "job_experience_level": lambda x: x["job_experience_level"],
                "job_location": lambda x: x["job_location"],
                "job_salary_min": lambda x: x["job_salary_min"],
                "job_salary_max": lambda x: x["job_salary_max"],
                "format_instructions": lambda x: self.parser.get_format_instructions(),
            }
            | prompt
            | get_llm(temperature=self.temperature, max_tokens=self.max_tokens)
            | self.parser
        )
        
        return chain
    
    def invoke(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the recommendation chain.
        
        Args:
            user_profile: Dictionary containing user profile data
            job: Dictionary containing job data
            
        Returns:
            Dictionary with match_score and reasons
        """
        try:
            # Prepare input data
            input_data = {
                "user_name": user_profile.get("full_name", "Unknown"),
                "user_skills": ", ".join(user_profile.get("skills", [])[:10]) or "No skills listed",
                "user_experience": str(user_profile.get("experience", "Not specified"))[:200],
                "user_education": str(user_profile.get("education", "Not specified"))[:200],
                "job_title": job.get("title", ""),
                "job_company": job.get("company_name", ""),
                "job_skills": ", ".join(job.get("skills", [])[:10]) or "No specific skills required",
                "job_description": str(job.get("description", ""))[:300],
                "job_experience_level": job.get("experience_level", "Not specified"),
                "job_location": job.get("location", ""),
                "job_salary_min": job.get("salary_min", 0),
                "job_salary_max": job.get("salary_max", 0),
            }
            
            # Invoke the chain
            result = self.chain.invoke(input_data)
            
            logger.debug(f"Recommendation chain generated match score: {result.get('match_score')}")
            
            return {
                "score": result.get("match_score", 0),
                "reasons": result.get("reasons", [])
            }
            
        except Exception as e:
            logger.error(f"Error in recommendation chain: {e}")
            raise
    
    async def ainvoke(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Async invoke the recommendation chain.
        
        Args:
            user_profile: Dictionary containing user profile data
            job: Dictionary containing job data
            
        Returns:
            Dictionary with match_score and reasons
        """
        try:
            # Prepare input data
            input_data = {
                "user_name": user_profile.get("full_name", "Unknown"),
                "user_skills": ", ".join(user_profile.get("skills", [])[:10]) or "No skills listed",
                "user_experience": str(user_profile.get("experience", "Not specified"))[:200],
                "user_education": str(user_profile.get("education", "Not specified"))[:200],
                "job_title": job.get("title", ""),
                "job_company": job.get("company_name", ""),
                "job_skills": ", ".join(job.get("skills", [])[:10]) or "No specific skills required",
                "job_description": str(job.get("description", ""))[:300],
                "job_experience_level": job.get("experience_level", "Not specified"),
                "job_location": job.get("location", ""),
                "job_salary_min": job.get("salary_min", 0),
                "job_salary_max": job.get("salary_max", 0),
            }
            
            # Invoke the chain asynchronously
            result = await self.chain.ainvoke(input_data)
            
            logger.debug(f"Recommendation chain generated match score: {result.get('match_score')}")
            
            return {
                "score": result.get("match_score", 0),
                "reasons": result.get("reasons", [])
            }
            
        except Exception as e:
            logger.error(f"Error in recommendation chain: {e}")
            raise
    
    async def generate_job_recommendation_reasons(
        self,
        user_profile: Dict[str, Any],
        job: Dict[str, Any],
        match_score: float
    ) -> List[str]:
        """
        Generate human-readable reasons for why a job matches a user's profile.
        This method is for backward compatibility when match_score is already calculated.
        
        Args:
            user_profile: Dictionary with user skills, experience, etc.
            job: Dictionary with job details
            match_score: Numerical match score (0-1)
            
        Returns:
            List of reason strings explaining the match
        """
        try:
            # Use LangChain chain to generate reasons, but we already have the score
            # So we'll use the chain but extract just the reasons
            result = await self.ainvoke(user_profile, job)
            return result.get("reasons", [])[:3]
        except Exception as e:
            logger.warning(f"Error generating reasons with chain, using fallback: {e}")
            return self._generate_fallback_reasons(user_profile, job, match_score)
    
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


def get_recommendation_chain(temperature: float = 0.3, max_tokens: int = 300) -> RecommendationChain:
    """
    Factory function to get a recommendation chain instance.
    
    Args:
        temperature: LLM temperature for response generation
        max_tokens: Maximum tokens for LLM response
        
    Returns:
        RecommendationChain instance
    """
    return RecommendationChain(temperature=temperature, max_tokens=max_tokens)


# Global recommendation chain instance (for backward compatibility)
recommendation_chain = RecommendationChain()
