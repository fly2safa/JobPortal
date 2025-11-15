"""
LangChain prompt chain for AI-powered candidate matching.

This module implements a LangChain chain that analyzes candidate profiles against
job requirements to generate match scores and recommendations for employers.
"""
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from app.ai.providers import get_llm
from app.core.logging import get_logger

logger = get_logger(__name__)


class CandidateMatchOutput(BaseModel):
    """Output schema for candidate matching."""
    match_score: int = Field(
        description="Match score from 0 to 100 indicating how well the candidate matches the job requirements",
        ge=0,
        le=100
    )
    reasons: List[str] = Field(
        description="List of 2-3 specific reasons explaining why this candidate is a good match",
        min_items=1,
        max_items=3
    )


class CandidateMatchingChain:
    """
    LangChain chain for generating candidate recommendations for employers.
    
    This chain takes a job description and candidate profile as input and outputs
    a structured match score with detailed reasons.
    """
    
    def __init__(self, temperature: float = 0.3, max_tokens: int = 300):
        """
        Initialize the candidate matching chain.
        
        Args:
            temperature: LLM temperature for response generation
            max_tokens: Maximum tokens for LLM response
        """
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.parser = JsonOutputParser(pydantic_object=CandidateMatchOutput)
        self.chain = self._build_chain()
    
    def _build_chain(self):
        """Build the LangChain prompt chain."""
        # Define the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert recruiter and candidate matching AI.
Your task is to analyze a candidate's profile against a job's requirements and provide:
1. A match score from 0-100 (higher = better match)
2. 2-3 specific, actionable reasons explaining the match

Consider:
- Skill alignment (technical and soft skills)
- Experience level and years
- Education requirements
- Cultural and role fit
- Career trajectory
- Specific achievements

{format_instructions}"""),
            ("user", """Analyze this candidate match:

JOB REQUIREMENTS:
Title: {job_title}
Company: {job_company}
Required Skills: {job_skills}
Description: {job_description}
Experience Level: {job_experience_level}

CANDIDATE PROFILE:
Name: {candidate_name}
Skills: {candidate_skills}
Experience: {candidate_experience}
Education: {candidate_education}

Provide your analysis as JSON with match_score and reasons.""")
        ])
        
        # Build the chain: prompt -> LLM -> parser
        chain = (
            {
                "job_title": lambda x: x["job_title"],
                "job_company": lambda x: x["job_company"],
                "job_skills": lambda x: x["job_skills"],
                "job_description": lambda x: x["job_description"],
                "job_experience_level": lambda x: x["job_experience_level"],
                "candidate_name": lambda x: x["candidate_name"],
                "candidate_skills": lambda x: x["candidate_skills"],
                "candidate_experience": lambda x: x["candidate_experience"],
                "candidate_education": lambda x: x["candidate_education"],
                "format_instructions": lambda x: self.parser.get_format_instructions(),
            }
            | prompt
            | get_llm(temperature=self.temperature, max_tokens=self.max_tokens)
            | self.parser
        )
        
        return chain
    
    def invoke(self, job: Dict[str, Any], candidate_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the candidate matching chain.
        
        Args:
            job: Dictionary containing job data
            candidate_profile: Dictionary containing candidate profile data
            
        Returns:
            Dictionary with match_score and reasons
        """
        try:
            # Prepare input data
            input_data = {
                "job_title": job.get("title", ""),
                "job_company": job.get("company_name", ""),
                "job_skills": ", ".join(job.get("skills", [])[:10]) or "No specific skills required",
                "job_description": str(job.get("description", ""))[:300],
                "job_experience_level": job.get("experience_level", "Not specified"),
                "candidate_name": candidate_profile.get("full_name", "Unknown"),
                "candidate_skills": ", ".join(candidate_profile.get("skills", [])[:10]) or "No skills listed",
                "candidate_experience": str(candidate_profile.get("experience", "Not specified"))[:200],
                "candidate_education": str(candidate_profile.get("education", "Not specified"))[:200],
            }
            
            # Invoke the chain
            result = self.chain.invoke(input_data)
            
            logger.debug(f"Candidate matching chain generated match score: {result.get('match_score')}")
            
            return {
                "score": result.get("match_score", 0),
                "reasons": result.get("reasons", [])
            }
            
        except Exception as e:
            logger.error(f"Error in candidate matching chain: {e}")
            raise
    
    async def ainvoke(self, job: Dict[str, Any], candidate_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Async invoke the candidate matching chain.
        
        Args:
            job: Dictionary containing job data
            candidate_profile: Dictionary containing candidate profile data
            
        Returns:
            Dictionary with match_score and reasons
        """
        try:
            # Prepare input data
            input_data = {
                "job_title": job.get("title", ""),
                "job_company": job.get("company_name", ""),
                "job_skills": ", ".join(job.get("skills", [])[:10]) or "No specific skills required",
                "job_description": str(job.get("description", ""))[:300],
                "job_experience_level": job.get("experience_level", "Not specified"),
                "candidate_name": candidate_profile.get("full_name", "Unknown"),
                "candidate_skills": ", ".join(candidate_profile.get("skills", [])[:10]) or "No skills listed",
                "candidate_experience": str(candidate_profile.get("experience", "Not specified"))[:200],
                "candidate_education": str(candidate_profile.get("education", "Not specified"))[:200],
            }
            
            # Invoke the chain asynchronously
            result = await self.chain.ainvoke(input_data)
            
            logger.debug(f"Candidate matching chain generated match score: {result.get('match_score')}")
            
            return {
                "score": result.get("match_score", 0),
                "reasons": result.get("reasons", [])
            }
            
        except Exception as e:
            logger.error(f"Error in candidate matching chain: {e}")
            raise


def get_candidate_matching_chain(temperature: float = 0.3, max_tokens: int = 300) -> CandidateMatchingChain:
    """
    Factory function to get a candidate matching chain instance.
    
    Args:
        temperature: LLM temperature for response generation
        max_tokens: Maximum tokens for LLM response
        
    Returns:
        CandidateMatchingChain instance
    """
    return CandidateMatchingChain(temperature=temperature, max_tokens=max_tokens)








