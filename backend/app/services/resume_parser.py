"""
Hybrid resume parser: Algorithmic first, AI fallback with GPT-4o-mini.
"""
import re
import json
from typing import Dict, List, Optional
from openai import OpenAI
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class ResumeParser:
    """Hybrid resume parser with algorithmic and AI fallback."""
    
    def __init__(self):
        self.skills_database = self._load_skills_database()
        self.ai_client = None
        if settings.OPENAI_API_KEY:
            self.ai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def parse_resume_text(self, text: str) -> Dict:
        """
        Parse resume text using hybrid approach.
        
        Args:
            text: Extracted text from resume file
            
        Returns:
            Dictionary with parsed resume data
        """
        logger.info("Starting hybrid resume parsing")
        
        # Step 1: Algorithmic parsing (fast, free)
        algorithmic_result = self._parse_algorithmic(text)
        confidence = self._calculate_confidence(algorithmic_result)
        
        logger.info(f"Algorithmic parsing confidence: {confidence:.2f}")
        
        # Step 2: Check if AI fallback is needed
        needs_ai = confidence < 0.7  # Threshold for AI fallback
        ai_used = False
        
        if needs_ai and self.ai_client:
            logger.info("Confidence low, using AI fallback (GPT-4o-mini)")
            try:
                ai_result = self._parse_with_ai(text)
                ai_used = True
                
                # Merge results: AI fills gaps in algorithmic extraction
                final_result = self._merge_results(algorithmic_result, ai_result)
                final_result['parsing_method'] = 'hybrid'
                final_result['parsing_confidence'] = max(confidence, 0.8)  # AI is more confident
                final_result['ai_used'] = True
                
                logger.info("AI parsing completed successfully")
                return final_result
                
            except Exception as e:
                logger.warning(f"AI parsing failed: {str(e)}, using algorithmic results")
                # Fall back to algorithmic if AI fails
        
        # Use algorithmic results
        algorithmic_result['parsing_method'] = 'algorithmic'
        algorithmic_result['parsing_confidence'] = confidence
        algorithmic_result['ai_used'] = False
        
        return algorithmic_result
    
    def _parse_algorithmic(self, text: str) -> Dict:
        """Extract data using algorithmic/rule-based methods."""
        return {
            'skills': self._extract_skills_algorithmic(text),
            'experience_years': self._extract_experience_algorithmic(text),
            'education': self._extract_education_algorithmic(text),
            'work_experience': None,  # Too complex for algorithmic
            'summary': None,  # Too complex for algorithmic
        }
    
    def _extract_skills_algorithmic(self, text: str) -> List[str]:
        """Extract skills using keyword matching."""
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.skills_database:
            # Case-insensitive matching with word boundaries
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                if skill not in found_skills:
                    found_skills.append(skill)
        
        return found_skills
    
    def _extract_experience_algorithmic(self, text: str) -> Optional[int]:
        """Extract years of experience using regex patterns."""
        # Patterns: "5 years", "5+ years", "5-7 years", "5 to 7 years"
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience[:\s]+(\d+)\+?\s*years?',
            r'(\d+)\s*-\s*(\d+)\s*years?\s*experience',
            r'(\d+)\s*to\s*(\d+)\s*years?\s*experience',
        ]
        
        max_years = 0
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 2:  # Range like "5-7 years"
                    years = int(match.group(2))  # Take the higher number
                else:
                    years = int(match.group(1))
                max_years = max(max_years, years)
        
        # Also try to calculate from date ranges
        date_years = self._calculate_experience_from_dates(text)
        if date_years:
            max_years = max(max_years, date_years)
        
        return max_years if max_years > 0 else None
    
    def _calculate_experience_from_dates(self, text: str) -> Optional[int]:
        """Calculate experience from date ranges (e.g., "2020 - 2024")."""
        # Pattern: "2020 - 2024" or "Jan 2020 - Dec 2024"
        date_pattern = r'(\d{4})\s*[-–—]\s*(\d{4})'
        matches = re.findall(date_pattern, text)
        
        if matches:
            years_list = []
            for start, end in matches:
                try:
                    years = int(end) - int(start)
                    if 0 < years < 50:  # Sanity check
                        years_list.append(years)
                except ValueError:
                    continue
            
            if years_list:
                return max(years_list)
        
        return None
    
    def _extract_education_algorithmic(self, text: str) -> Optional[str]:
        """Extract education using regex patterns."""
        # Look for degree patterns
        degree_patterns = [
            r'(Bachelor[^\s]*|BS|B\.S\.|B\.A\.|BA)\s+(?:of\s+)?(?:Science|Arts)?\s*(?:in\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(Master[^\s]*|MS|M\.S\.|M\.A\.|MA|MBA)\s+(?:of\s+)?(?:Science|Arts|Business)?\s*(?:in\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(Ph\.?D\.?|Doctorate)\s+(?:in\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        ]
        
        for pattern in degree_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                degree = match.group(0)
                # Try to find university name nearby
                university = self._find_university_near_match(text, match.start())
                if university:
                    return f"{degree}, {university}"
                return degree
        
        return None
    
    def _find_university_near_match(self, text: str, position: int) -> Optional[str]:
        """Find university name near a position in text."""
        # Look for common university indicators
        context = text[max(0, position-100):position+100]
        university_patterns = [
            r'University of ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+University',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+Institute',
        ]
        
        for pattern in university_patterns:
            match = re.search(pattern, context)
            if match:
                return match.group(0)
        
        return None
    
    def _calculate_confidence(self, result: Dict) -> float:
        """Calculate confidence score for algorithmic parsing."""
        confidence = 0.0
        
        # Skills found: 0.4 weight
        if result.get('skills'):
            skill_confidence = min(len(result['skills']) / 10, 1.0)  # Cap at 10 skills
            confidence += skill_confidence * 0.4
        
        # Experience found: 0.3 weight
        if result.get('experience_years'):
            confidence += 0.3
        
        # Education found: 0.3 weight
        if result.get('education'):
            confidence += 0.3
        
        return min(confidence, 1.0)
    
    def _parse_with_ai(self, text: str) -> Dict:
        """Parse resume using GPT-4o-mini."""
        if not self.ai_client:
            raise ValueError("OpenAI client not initialized")
        
        # Limit text to avoid token limits
        text_truncated = text[:4000] if len(text) > 4000 else text
        
        prompt = f"""Extract structured information from this resume text. Return ONLY valid JSON with these fields:
- skills: array of technical/professional skills
- experience_years: integer (total years of experience)
- education: string (degree and university)
- work_experience: string (brief summary of work history, 2-3 sentences)
- summary: string (resume summary/bio if present, otherwise null)

Resume text:
{text_truncated}

Return ONLY valid JSON, no markdown formatting or code blocks."""

        try:
            response = self.ai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a resume parser. Extract structured data from resumes. Always return valid JSON only."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent extraction
                max_tokens=500,
                response_format={"type": "json_object"}  # Force JSON response
            )
            
            content = response.choices[0].message.content
            ai_data = json.loads(content)
            
            return {
                'skills': ai_data.get('skills', []),
                'experience_years': ai_data.get('experience_years'),
                'education': ai_data.get('education'),
                'work_experience': ai_data.get('work_experience'),
                'summary': ai_data.get('summary'),
            }
            
        except Exception as e:
            logger.error(f"AI parsing error: {str(e)}")
            raise
    
    def _merge_results(self, algorithmic: Dict, ai: Dict) -> Dict:
        """Merge algorithmic and AI results, preferring AI for complex fields."""
        # Combine skills from both sources
        combined_skills = list(set(
            algorithmic.get('skills', []) + ai.get('skills', [])
        ))
        
        return {
            'skills': combined_skills,
            'experience_years': ai.get('experience_years') or algorithmic.get('experience_years'),
            'education': ai.get('education') or algorithmic.get('education'),
            'work_experience': ai.get('work_experience'),  # AI only
            'summary': ai.get('summary'),  # AI only
        }
    
    def _load_skills_database(self) -> List[str]:
        """Load common technical/professional skills database."""
        return [
            # Programming Languages
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust', 
            'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'Perl',
            # Web Technologies
            'HTML', 'CSS', 'React', 'Vue', 'Vue.js', 'Angular', 'Node.js', 'Express', 
            'Express.js', 'Django', 'Flask', 'FastAPI', 'Spring Boot', 'ASP.NET', 
            'Laravel', 'Next.js', 'Nuxt.js', 'Svelte', 'jQuery',
            # Databases
            'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Oracle', 'SQL Server',
            'DynamoDB', 'Cassandra', 'Elasticsearch', 'SQLite', 'MariaDB', 'Neo4j',
            # Cloud & DevOps
            'AWS', 'Azure', 'GCP', 'Google Cloud', 'Docker', 'Kubernetes', 'Jenkins', 
            'CI/CD', 'Terraform', 'Ansible', 'Git', 'GitHub', 'GitLab', 'CircleCI',
            'Travis CI', 'Heroku', 'Netlify', 'Vercel',
            # Data & ML
            'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Keras',
            'Pandas', 'NumPy', 'Scikit-learn', 'Data Science', 'Data Analysis', 
            'Tableau', 'Power BI', 'Matplotlib', 'Seaborn', 'Jupyter',
            # Mobile
            'iOS', 'Android', 'React Native', 'Flutter', 'SwiftUI', 'Jetpack Compose',
            # Testing
            'Jest', 'Pytest', 'JUnit', 'Selenium', 'Cypress', 'Mocha', 'Chai',
            # Other
            'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum', 'Linux', 'Unix',
            'API Development', 'System Design', 'OOP', 'Functional Programming',
        ]

