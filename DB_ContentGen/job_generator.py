#!/usr/bin/env python3
"""
TalentNest Job Generator

This script generates fictitious job postings for the TalentNest job portal.
It uses OpenAI to create realistic job descriptions based on:
- Candidate skills from the database
- Employer information from the database
"""

import os
import json
import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


class JobGenerator:
    """Generates job postings using candidate skills and employer data."""
    
    EMPLOYMENT_TYPES = ["Full-Time", "Part-Time", "Contract"]
    REMOTE_OPTIONS = ["On-site", "Remote", "Hybrid"]
    
    # Mapping to backend enum values
    EMPLOYMENT_TYPE_MAP = {
        "Full-Time": "full_time",
        "Part-Time": "part_time",
        "Contract": "contract",
        "Internship": "internship",
        "Temporary": "temporary"
    }
    
    EXPERIENCE_LEVEL_MAP = {
        "junior": "junior",
        "mid": "mid",
        "senior": "senior",
        "lead": "lead",
        "principal": "executive"
    }
    
    # Salary ranges by job level (annual in USD)
    SALARY_RANGES = {
        "junior": (45000, 75000),
        "mid": (75000, 120000),
        "senior": (120000, 180000),
        "lead": (150000, 220000),
        "principal": (180000, 280000)
    }
    
    def __init__(self, api_key: str):
        """Initialize the generator with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)
        self.used_job_ids = set()
        self.job_id_counter = random.randint(10000, 99999)
        self.salary_cache = {}  # Cache for similar job titles
    
    def generate_job_id(self) -> str:
        """Generate a unique job ID starting with JID."""
        while True:
            job_id = f"JID{self.job_id_counter}"
            if job_id not in self.used_job_ids:
                self.used_job_ids.add(job_id)
                self.job_id_counter += 1
                return job_id
    
    def generate_posted_date(self) -> str:
        """Generate a random date within the past 6 months."""
        today = datetime.now()
        days_ago = random.randint(0, 180)  # 0 to 6 months
        posted_date = today - timedelta(days=days_ago)
        return posted_date.strftime("%Y-%m-%d")
    
    def determine_job_level(self, experience_years: int) -> str:
        """Determine job level based on years of experience."""
        if experience_years < 2:
            return "junior"
        elif experience_years < 5:
            return "mid"
        elif experience_years < 8:
            return "senior"
        elif experience_years < 12:
            return "lead"
        else:
            return "principal"
    
    def generate_salary_range(self, job_title: str, level: str, location: str = None) -> tuple[float, float]:
        """
        Generate salary range with consistency for similar jobs (+/- 10% variance).
        Returns (min_salary, max_salary) as floats.
        """
        # Create a cache key for similar jobs
        cache_key = f"{job_title.lower()}_{level}"
        
        if cache_key in self.salary_cache:
            # Use cached range with +/- 10% variance
            base_min, base_max = self.salary_cache[cache_key]
            variance = random.uniform(0.90, 1.10)
            min_salary = int(base_min * variance)
            max_salary = int(base_max * variance)
        else:
            # Generate new base range
            base_min, base_max = self.SALARY_RANGES[level]
            min_salary = base_min
            max_salary = base_max
            self.salary_cache[cache_key] = (min_salary, max_salary)
        
        # Round to nearest 5000
        min_salary = round(min_salary / 5000) * 5000
        max_salary = round(max_salary / 5000) * 5000
        
        return float(min_salary), float(max_salary)
    
    def generate_job_with_ai(self, candidate: Dict, employer: Dict) -> Dict:
        """Generate a job posting using AI based on candidate skills and employer info."""
        
        skills = candidate.get('skills', [])
        experience_years = candidate.get('experience_years', 0)
        company_name = employer.get('company_name', 'Unknown Company')
        company_desc = employer.get('company_description', '')
        industry = employer.get('industry', 'Technology')
        location = employer.get('location', 'Remote')
        
        # Determine job level
        level = self.determine_job_level(experience_years)
        level_prefix = {
            "junior": "Junior",
            "mid": "",
            "senior": "Senior",
            "lead": "Lead",
            "principal": "Principal"
        }[level]
        
        # Primary skill for job title
        primary_skill = skills[0] if skills else "Software"
        
        prompt = f"""Generate a realistic job posting for {company_name}.

Company: {company_name}
Industry: {industry}
Required Skills: {', '.join(skills[:5])}
Experience Level: {level_prefix} ({experience_years} years)
Location: {location}

Create a job posting with:
- job_title: A specific job title using the primary skill "{primary_skill}" (e.g., "Senior Python Developer", "React Engineer", "Data Scientist")
- description: 3-4 sentences describing the role and what the person will do at {company_name}
- requirements: List of 5-7 specific requirements including the skills: {', '.join(skills[:5])}

IMPORTANT:
- Job title should include "{primary_skill}" or a closely related term
- Make requirements specific and technical
- Reference {company_name} in the description
- Match the {level_prefix} level in requirements

Return ONLY valid JSON with these fields: job_title, description, requirements (as array)
No markdown formatting or code blocks."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates realistic job postings. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=600
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            ai_data = json.loads(content)
            
            # Build complete job posting
            job_title = ai_data.get("job_title", f"{level_prefix} {primary_skill} Developer").strip()
            
            # Get salary range as tuple
            salary_min, salary_max = self.generate_salary_range(job_title, level, location)
            
            # Determine remote status
            remote_option = random.choice(self.REMOTE_OPTIONS)
            is_remote = remote_option == "Remote"
            
            # Map employment type to backend enum
            employment_type_str = random.choice(self.EMPLOYMENT_TYPES)
            job_type = self.EMPLOYMENT_TYPE_MAP.get(employment_type_str, "full_time")
            
            # Map experience level to backend enum
            experience_level = self.EXPERIENCE_LEVEL_MAP.get(level, "mid")
            
            # Parse requirements
            requirements_list = ai_data.get("requirements", skills[:5])
            requirements_str = "\n".join(f"• {req}" for req in requirements_list) if isinstance(requirements_list, list) else requirements_list
            
            # Generate posted date
            posted_date_str = self.generate_posted_date()
            posted_date = datetime.strptime(posted_date_str, "%Y-%m-%d")
            
            # NEW SCHEMA - Backend compatible
            job = {
                # Core fields
                "title": job_title,
                "description": ai_data.get("description", f"Exciting opportunity at {company_name}."),
                "requirements": requirements_str,
                "responsibilities": None,
                
                # Skills
                "skills": skills[:10],
                "required_skills": skills[:5],
                "preferred_skills": skills[5:10] if len(skills) > 5 else [],
                
                # Location
                "location": location,
                "is_remote": is_remote,
                
                # Company/Employer
                "company_id": str(employer.get("_id", "default_company")),
                "company_name": company_name,
                "employer_id": str(employer.get("_id", "default_employer")),
                
                # Salary
                "salary_min": salary_min,
                "salary_max": salary_max,
                "salary_currency": "USD",
                
                # Job details
                "job_type": job_type,
                "experience_level": experience_level,
                "experience_years_min": max(0, experience_years - 2),
                "experience_years_max": experience_years + 2,
                
                # Status
                "status": "active",
                "posted_date": posted_date,
                "closing_date": None,
                
                # Tracking
                "application_count": 0,
                "view_count": 0,
                
                # Additional
                "benefits": [],
                "application_instructions": None,
                
                # Metadata
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                
                # Legacy reference (optional)
                "_legacy_job_id": self.generate_job_id(),
            }
            
            return job
            
        except Exception as e:
            print(f"⚠️  Error generating job with AI: {e}")
            return self._generate_fallback_job(candidate, employer)
    
    def _generate_fallback_job(self, candidate: Dict, employer: Dict) -> Dict:
        """Generate a basic job posting without AI."""
        skills = candidate.get('skills', ['Software Development'])
        experience_years = candidate.get('experience_years', 0)
        company_name = employer.get('company_name', 'Unknown Company')
        location = employer.get('location', 'Remote')
        
        level = self.determine_job_level(experience_years)
        level_prefix = ["Junior", "", "Senior", "Lead", "Principal"][
            ["junior", "mid", "senior", "lead", "principal"].index(level)
        ]
        
        primary_skill = skills[0] if skills else "Software"
        job_title = f"{level_prefix} {primary_skill} Developer".strip()
        
        # Get salary range as tuple
        salary_min, salary_max = self.generate_salary_range(job_title, level, location)
        
        # Determine remote status
        remote_option = random.choice(self.REMOTE_OPTIONS)
        is_remote = remote_option == "Remote"
        
        # Map employment type to backend enum
        employment_type_str = random.choice(self.EMPLOYMENT_TYPES)
        job_type = self.EMPLOYMENT_TYPE_MAP.get(employment_type_str, "full_time")
        
        # Map experience level to backend enum
        experience_level = self.EXPERIENCE_LEVEL_MAP.get(level, "mid")
        
        # Format requirements
        requirements_str = "\n".join(f"• {skill}" for skill in skills[:5])
        
        # Generate posted date
        posted_date_str = self.generate_posted_date()
        posted_date = datetime.strptime(posted_date_str, "%Y-%m-%d")
        
        # NEW SCHEMA - Backend compatible
        return {
            # Core fields
            "title": job_title,
            "description": f"Join {company_name} as a {job_title}. Work with cutting-edge technologies and contribute to innovative projects.",
            "requirements": requirements_str,
            "responsibilities": None,
            
            # Skills
            "skills": skills[:10],
            "required_skills": skills[:5],
            "preferred_skills": skills[5:10] if len(skills) > 5 else [],
            
            # Location
            "location": location,
            "is_remote": is_remote,
            
            # Company/Employer
            "company_id": str(employer.get("_id", "default_company")),
            "company_name": company_name,
            "employer_id": str(employer.get("_id", "default_employer")),
            
            # Salary
            "salary_min": salary_min,
            "salary_max": salary_max,
            "salary_currency": "USD",
            
            # Job details
            "job_type": job_type,
            "experience_level": experience_level,
            "experience_years_min": max(0, experience_years - 2),
            "experience_years_max": experience_years + 2,
            
            # Status
            "status": "active",
            "posted_date": posted_date,
            "closing_date": None,
            
            # Tracking
            "application_count": 0,
            "view_count": 0,
            
            # Additional
            "benefits": [],
            "application_instructions": None,
            
            # Metadata
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            
            # Legacy reference (optional)
            "_legacy_job_id": self.generate_job_id(),
        }


def fetch_candidates_from_db(db_url: str, db_name: str, limit: int = 50) -> List[Dict]:
    """Fetch candidates from MongoDB."""
    try:
        client = MongoClient(db_url, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        candidates = list(db['Candidates'].find().limit(limit))
        client.close()
        
        print(f"✅ Fetched {len(candidates)} candidates from database")
        return candidates
        
    except Exception as e:
        print(f"❌ Error fetching candidates: {e}")
        return []


def fetch_employers_from_db(db_url: str, db_name: str) -> List[Dict]:
    """Fetch employers from MongoDB."""
    try:
        client = MongoClient(db_url, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        employers = list(db['Employers'].find())
        client.close()
        
        print(f"✅ Fetched {len(employers)} employers from database")
        return employers
        
    except Exception as e:
        print(f"❌ Error fetching employers: {e}")
        return []


def display_job(job: Dict, index: Optional[int] = None) -> None:
    """Display a job posting in a formatted way."""
    header = f"\n{'='*70}\n"
    if index is not None:
        header += f"JOB POSTING #{index + 1}\n{'='*70}\n"
    else:
        header += f"JOB POSTING\n{'='*70}\n"
    
    print(header)
    print(f"🆔 Job ID:           {job['job_id']}")
    print(f"💼 Title:            {job['job_title']}")
    print(f"🏢 Company:          {job['company_name']}")
    print(f"📋 Description:      {job['description'][:80]}...")
    print(f"✅ Requirements:     {len(job['requirements'])} items")
    for i, req in enumerate(job['requirements'][:3], 1):
        print(f"                     {i}. {req}")
    if len(job['requirements']) > 3:
        print(f"                     ... and {len(job['requirements']) - 3} more")
    print(f"💰 Salary:           {job['salary_range']}")
    print(f"📍 Location:         {job['location']}")
    print(f"🏠 Remote:           {job['remote']}")
    print(f"⏰ Type:             {job['employment_type']}")
    print(f"📅 Posted:           {job['posted_date']}")
    print("=" * 70)


def get_yes_no_input(prompt: str) -> bool:
    """Get yes/no input from user."""
    while True:
        response = input(f"{prompt} (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'")


def save_jobs_to_json(jobs: List[Dict], filename: str = "generated_jobs.json") -> None:
    """Save accepted jobs to a JSON file."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    # Load existing jobs if file exists
    existing_jobs = []
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                existing_jobs = json.load(f)
        except:
            existing_jobs = []
    
    # Append new jobs
    existing_jobs.extend(jobs)
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(existing_jobs, f, indent=2)
    
    print(f"\n✅ Saved {len(jobs)} job(s) to {filename}")
    print(f"📊 Total jobs in file: {len(existing_jobs)}")


def save_jobs_to_mongodb(jobs: List[Dict], db_url: str, db_name: str, collection_name: str = "jobs") -> bool:
    """Save accepted jobs to MongoDB."""
    try:
        # Connect to MongoDB
        print(f"\n🔄 Connecting to MongoDB...")
        client = MongoClient(db_url, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        client.admin.command('ping')
        print(f"✅ Connected to MongoDB successfully!")
        
        # Get database and collection
        db = client[db_name]
        collection = db[collection_name]
        
        # Insert jobs
        if len(jobs) == 1:
            result = collection.insert_one(jobs[0])
            print(f"✅ Inserted 1 job into MongoDB")
            print(f"   Document ID: {result.inserted_id}")
        else:
            result = collection.insert_many(jobs)
            print(f"✅ Inserted {len(result.inserted_ids)} jobs into MongoDB")
            print(f"   Document IDs: {result.inserted_ids[:3]}{'...' if len(result.inserted_ids) > 3 else ''}")
        
        # Get total count
        total_count = collection.count_documents({})
        print(f"📊 Total jobs in MongoDB collection: {total_count}")
        
        client.close()
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("   Please check your database URL and ensure MongoDB is running.")
        return False
    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")
        return False


def save_jobs(jobs: List[Dict], db_url: Optional[str] = None, db_name: Optional[str] = None) -> None:
    """Save accepted jobs to both JSON file and MongoDB (if configured)."""
    # Always save to JSON as backup
    save_jobs_to_json(jobs)
    
    # Save to MongoDB if database URL is provided
    if db_url and db_name:
        mongodb_success = save_jobs_to_mongodb(jobs, db_url, db_name)
        if not mongodb_success:
            print("⚠️  Jobs were saved to JSON file but not to MongoDB.")
    else:
        print("ℹ️  MongoDB not configured - only saved to JSON file.")


def main():
    """Main CLI interface."""
    print("\n" + "="*70)
    print("💼  TalentNest Job Generator  💼")
    print("="*70)
    
    # Load environment variables from multiple possible locations
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(os.path.dirname(script_dir), 'backend')
    
    # Try loading from current directory first, then backend directory
    env_loaded = False
    if os.path.exists(os.path.join(script_dir, '.env')):
        load_dotenv(os.path.join(script_dir, '.env'))
        env_loaded = True
        print(f"✓ Loaded .env from: {script_dir}")
    elif os.path.exists(os.path.join(backend_dir, '.env')):
        load_dotenv(os.path.join(backend_dir, '.env'))
        env_loaded = True
        print(f"✓ Loaded .env from: {backend_dir}")
    else:
        load_dotenv()  # Try default locations
        print("⚠️  .env file not found in DB_ContentGen or backend directories")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n❌ Error: OPENAI_API_KEY not found in .env file")
        print(f"Please add your OpenAI API key to .env in {script_dir} or {backend_dir}")
        return
    
    # Load database configuration
    db_url = os.getenv('project_db_url')
    db_name = os.getenv('project_db_name')
    
    if not db_url or not db_name:
        print("\n❌ Error: Database configuration not found in .env file")
        print("Please ensure project_db_url and project_db_name are set")
        return
    
    print(f"✅ MongoDB configured: {db_name}")
    
    # Fetch candidates and employers from database
    print("\n🔄 Fetching data from database...")
    candidates = fetch_candidates_from_db(db_url, db_name, limit=100)
    employers = fetch_employers_from_db(db_url, db_name)
    
    if not candidates:
        print("\n❌ No candidates found in database!")
        print("Please run candidate_generator.py first to create candidates.")
        return
    
    if not employers:
        print("\n❌ No employers found in database!")
        print("Please run employer_generator.py first to create employers.")
        return
    
    # Initialize generator
    generator = JobGenerator(api_key)
    
    print(f"\n📊 Available data:")
    print(f"   - {len(candidates)} candidates")
    print(f"   - {len(employers)} employers")
    
    print("\n📝 How many job postings would you like to generate?")
    print("   (Script will match candidates with employers to create relevant jobs)")
    
    user_input = input("\n👉 Number of jobs: ").strip()
    
    if user_input.lower() in ['q', 'quit', 'exit']:
        print("\n👋 Goodbye!")
        return
    
    try:
        num_jobs = int(user_input)
        if num_jobs <= 0:
            print("❌ Please enter a positive number")
            return
        
        # Generate jobs by pairing candidates with employers
        print(f"\n🔄 Generating {num_jobs} job posting(s)...")
        
        jobs = []
        for i in range(num_jobs):
            # Randomly select a candidate and employer
            candidate = random.choice(candidates)
            employer = random.choice(employers)
            
            print(f"\n⏳ Generating job {i+1}/{num_jobs}...")
            print(f"   Candidate skills: {', '.join(candidate.get('skills', [])[:3])}")
            print(f"   Employer: {employer.get('company_name')}")
            
            job = generator.generate_job_with_ai(candidate, employer)
            jobs.append(job)
        
        # Display all jobs and get individual approval
        accepted_jobs = []
        
        print("\n" + "="*70)
        print("REVIEW GENERATED JOBS")
        print("="*70)
        
        # Option to accept/reject all
        print("\nWould you like to:")
        print("1. Review each job individually")
        print("2. Accept all jobs")
        print("3. Reject all jobs")
        
        choice = input("\n👉 Enter choice (1/2/3): ").strip()
        
        if choice == '2':
            accepted_jobs = jobs
            print(f"\n✅ Accepted all {len(jobs)} jobs!")
        elif choice == '3':
            print(f"\n❌ Rejected all {len(jobs)} jobs!")
        else:
            # Review individually
            for i, job in enumerate(jobs):
                display_job(job, i)
                if get_yes_no_input("\n✅ Accept this job?"):
                    accepted_jobs.append(job)
                    print("   ✓ Job accepted!")
                else:
                    print("   ✗ Job rejected!")
        
        # Save accepted jobs
        if accepted_jobs:
            save_jobs(accepted_jobs, db_url, db_name)
        else:
            print("\n⚠️  No jobs were accepted.")
    
    except ValueError:
        print("❌ Please enter a valid number")
        return
    
    print("\n" + "="*70)
    print("Thank you for using TalentNest Job Generator! 💼")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

