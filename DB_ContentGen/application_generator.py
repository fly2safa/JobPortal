#!/usr/bin/env python3
"""
TalentNest Application Generator

This script generates fictitious job applications for the TalentNest job portal.
It matches candidates with jobs and creates realistic application submissions.
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


class ApplicationGenerator:
    """Generates job applications using candidate and job data."""
    
    STATUSES = ["pending", "reviewed", "rejected", "accepted"]
    
    # Realistic status distribution
    STATUS_WEIGHTS = {
        "pending": 0.30,      # 30% still pending
        "reviewed": 0.25,     # 25% under review
        "rejected": 0.30,     # 30% rejected
        "accepted": 0.15      # 15% accepted
    }
    
    def __init__(self, api_key: str):
        """Initialize the generator with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)
        self.app_id_counter = 1
        self.used_app_ids = set()
    
    def generate_app_id(self) -> str:
        """Generate a unique application ID (format: 00001-1)."""
        base_id = f"{self.app_id_counter:05d}"
        
        # Check for duplicates and add suffix if needed
        suffix = 1
        app_id = f"{base_id}-{suffix}"
        
        while app_id in self.used_app_ids:
            suffix += 1
            app_id = f"{base_id}-{suffix}"
        
        self.used_app_ids.add(app_id)
        
        # Only increment base counter when moving to new base number
        if suffix == 1:
            self.app_id_counter += 1
        
        return app_id
    
    def generate_application_date(self, job_posted_date: str) -> str:
        """
        Generate application date that is equal to or after job posted date.
        """
        posted = datetime.strptime(job_posted_date, "%Y-%m-%d")
        today = datetime.now()
        
        # Application must be between job posted date and today
        max_days = (today - posted).days
        if max_days < 0:
            max_days = 0
        
        # Random days after posting (weighted towards earlier)
        days_after = int(random.triangular(0, max_days, max_days * 0.3))
        application_date = posted + timedelta(days=days_after)
        
        return application_date.strftime("%Y-%m-%d")
    
    def generate_status(self) -> str:
        """Generate application status with realistic distribution."""
        return random.choices(
            list(self.STATUS_WEIGHTS.keys()),
            weights=list(self.STATUS_WEIGHTS.values()),
            k=1
        )[0]
    
    def generate_fast_track(self, status: str) -> str:
        """
        Generate fast track status.
        Can only be 'yes' if status is 'accepted', and only 10% chance.
        """
        if status == "accepted":
            # 10% chance of fast track for accepted candidates
            return "yes" if random.random() < 0.10 else "no"
        return "no"
    
    def generate_application_with_ai(self, candidate: Dict, job: Dict) -> Dict:
        """Generate an application/resume using AI based on candidate and job."""
        
        username = candidate.get('username', 'unknown')
        candidate_name = f"{candidate.get('firstname', '')} {candidate.get('lastname', '')}"
        skills = candidate.get('skills', [])
        experience_years = candidate.get('experience_years', 0)
        education = candidate.get('education', '')
        bio = candidate.get('bio', '')
        
        job_title = job.get('job_title', 'Position')
        company_name = job.get('company_name', 'Company')
        requirements = job.get('requirements', [])
        job_posted_date = job.get('posted_date', datetime.now().strftime("%Y-%m-%d"))
        
        prompt = f"""Generate a job application/resume description for {candidate_name} applying to {company_name}.

Candidate Profile:
- Name: {candidate_name}
- Skills: {', '.join(skills[:7])}
- Experience: {experience_years} years
- Education: {education}
- Bio: {bio}

Job Details:
- Position: {job_title}
- Company: {company_name}
- Requirements: {', '.join(requirements[:5])}

Create a professional application description that:
- Highlights how the candidate's skills match the job requirements
- Mentions relevant experience and projects
- Shows enthusiasm for the role at {company_name}
- Is 3-4 sentences long
- Sounds like a cover letter excerpt or resume summary

Return ONLY valid JSON with one field: "description"
No markdown formatting or code blocks."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates realistic job application descriptions. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            ai_data = json.loads(content)
            description = ai_data.get("description", "")
            
        except Exception as e:
            print(f"⚠️  Error generating application with AI: {e}")
            # Fallback description
            description = f"Experienced {job_title} with {experience_years} years in {', '.join(skills[:3])}. {bio[:100]}"
        
        # Generate status and other fields
        status = self.generate_status()
        fast_track = self.generate_fast_track(status)
        application_date = self.generate_application_date(job_posted_date)
        
        # Build complete application
        application = {
            "username": username,
            "app_id": self.generate_app_id(),
            "application_date": application_date,
            "status": status,
            "fast_track": fast_track,
            "description": description,
            "job_id": job.get('job_id'),
            "job_title": job_title,
            "company_name": company_name,
            "candidate_name": candidate_name
        }
        
        return application


def fetch_candidates_from_db(db_url: str, db_name: str) -> List[Dict]:
    """Fetch candidates from MongoDB."""
    try:
        client = MongoClient(db_url, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        candidates = list(db['Candidates'].find())
        client.close()
        
        print(f"✅ Fetched {len(candidates)} candidates from database")
        return candidates
        
    except Exception as e:
        print(f"❌ Error fetching candidates: {e}")
        return []


def fetch_jobs_from_db(db_url: str, db_name: str) -> List[Dict]:
    """Fetch jobs from MongoDB."""
    try:
        client = MongoClient(db_url, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        jobs = list(db['Jobs'].find())
        client.close()
        
        print(f"✅ Fetched {len(jobs)} jobs from database")
        return jobs
        
    except Exception as e:
        print(f"❌ Error fetching jobs: {e}")
        return []


def display_application(app: Dict, index: Optional[int] = None) -> None:
    """Display an application in a formatted way."""
    header = f"\n{'='*70}\n"
    if index is not None:
        header += f"APPLICATION #{index + 1}\n{'='*70}\n"
    else:
        header += f"APPLICATION\n{'='*70}\n"
    
    print(header)
    print(f"👤 Candidate:        {app['candidate_name']} (@{app['username']})")
    print(f"🆔 App ID:           {app['app_id']}")
    print(f"💼 Position:         {app['job_title']}")
    print(f"🏢 Company:          {app['company_name']}")
    print(f"📅 Applied:          {app['application_date']}")
    print(f"📊 Status:           {app['status'].upper()}")
    print(f"⚡ Fast Track:       {app['fast_track'].upper()}")
    print(f"📋 Description:      {app['description'][:80]}...")
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


def save_applications_to_json(applications: List[Dict], filename: str = "generated_applications.json") -> None:
    """Save accepted applications to a JSON file."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    # Load existing applications if file exists
    existing_apps = []
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                existing_apps = json.load(f)
        except:
            existing_apps = []
    
    # Append new applications
    existing_apps.extend(applications)
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(existing_apps, f, indent=2)
    
    print(f"\n✅ Saved {len(applications)} application(s) to {filename}")
    print(f"📊 Total applications in file: {len(existing_apps)}")


def save_applications_to_mongodb(applications: List[Dict], db_url: str, db_name: str, collection_name: str = "Applications") -> bool:
    """Save accepted applications to MongoDB."""
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
        
        # Insert applications
        if len(applications) == 1:
            result = collection.insert_one(applications[0])
            print(f"✅ Inserted 1 application into MongoDB")
            print(f"   Document ID: {result.inserted_id}")
        else:
            result = collection.insert_many(applications)
            print(f"✅ Inserted {len(result.inserted_ids)} applications into MongoDB")
            print(f"   Document IDs: {result.inserted_ids[:3]}{'...' if len(result.inserted_ids) > 3 else ''}")
        
        # Get total count
        total_count = collection.count_documents({})
        print(f"📊 Total applications in MongoDB collection: {total_count}")
        
        # Show status breakdown
        print(f"\n📈 Status Distribution:")
        for status in ["pending", "reviewed", "rejected", "accepted"]:
            count = collection.count_documents({"status": status})
            print(f"   {status.capitalize():10}: {count}")
        
        # Show fast track count
        fast_track_count = collection.count_documents({"fast_track": "yes"})
        print(f"   Fast Track: {fast_track_count}")
        
        client.close()
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("   Please check your database URL and ensure MongoDB is running.")
        return False
    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")
        return False


def save_applications(applications: List[Dict], db_url: Optional[str] = None, db_name: Optional[str] = None) -> None:
    """Save accepted applications to both JSON file and MongoDB (if configured)."""
    # Always save to JSON as backup
    save_applications_to_json(applications)
    
    # Save to MongoDB if database URL is provided
    if db_url and db_name:
        mongodb_success = save_applications_to_mongodb(applications, db_url, db_name)
        if not mongodb_success:
            print("⚠️  Applications were saved to JSON file but not to MongoDB.")
    else:
        print("ℹ️  MongoDB not configured - only saved to JSON file.")


def main():
    """Main CLI interface."""
    print("\n" + "="*70)
    print("📝  TalentNest Application Generator  📝")
    print("="*70)
    
    # Load environment variables
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    load_dotenv(env_path)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n❌ Error: OPENAI_API_KEY not found in .env file")
        print(f"Please add your OpenAI API key to: {env_path}")
        return
    
    # Load database configuration
    db_url = os.getenv('project_db_url')
    db_name = os.getenv('project_db_name')
    
    if not db_url or not db_name:
        print("\n❌ Error: Database configuration not found in .env file")
        print("Please ensure project_db_url and project_db_name are set")
        return
    
    print(f"✅ MongoDB configured: {db_name}")
    
    # Fetch candidates and jobs from database
    print("\n🔄 Fetching data from database...")
    candidates = fetch_candidates_from_db(db_url, db_name)
    jobs = fetch_jobs_from_db(db_url, db_name)
    
    if not candidates:
        print("\n❌ No candidates found in database!")
        print("Please run candidate_generator.py first to create candidates.")
        return
    
    if not jobs:
        print("\n❌ No jobs found in database!")
        print("Please run job_generator.py first to create jobs.")
        return
    
    # Initialize generator
    generator = ApplicationGenerator(api_key)
    
    print(f"\n📊 Available data:")
    print(f"   - {len(candidates)} candidates")
    print(f"   - {len(jobs)} jobs")
    print(f"   - Max possible applications: {len(candidates) * len(jobs)}")
    
    print("\n📝 How many applications would you like to generate?")
    print("   (Each application represents a candidate applying to a job)")
    print("   Tip: Generate 2-5 applications per candidate for realism")
    
    user_input = input("\n👉 Number of applications: ").strip()
    
    if user_input.lower() in ['q', 'quit', 'exit']:
        print("\n👋 Goodbye!")
        return
    
    try:
        num_applications = int(user_input)
        if num_applications <= 0:
            print("❌ Please enter a positive number")
            return
        
        # Generate applications by pairing candidates with jobs
        print(f"\n🔄 Generating {num_applications} application(s)...")
        
        applications = []
        for i in range(num_applications):
            # Randomly select a candidate and job
            candidate = random.choice(candidates)
            job = random.choice(jobs)
            
            print(f"\n⏳ Generating application {i+1}/{num_applications}...")
            print(f"   {candidate.get('firstname')} {candidate.get('lastname')} → {job.get('job_title')}")
            
            application = generator.generate_application_with_ai(candidate, job)
            applications.append(application)
        
        # Display summary statistics
        print("\n" + "="*70)
        print("GENERATION SUMMARY")
        print("="*70)
        
        status_counts = {}
        for status in generator.STATUSES:
            count = sum(1 for app in applications if app['status'] == status)
            status_counts[status] = count
            percentage = (count / len(applications)) * 100
            print(f"{status.capitalize():12}: {count:3} ({percentage:5.1f}%)")
        
        fast_track_count = sum(1 for app in applications if app['fast_track'] == 'yes')
        print(f"Fast Track  : {fast_track_count:3} ({(fast_track_count/len(applications))*100:5.1f}%)")
        
        # Display all applications and get individual approval
        accepted_applications = []
        
        print("\n" + "="*70)
        print("REVIEW GENERATED APPLICATIONS")
        print("="*70)
        
        # Option to accept/reject all
        print("\nWould you like to:")
        print("1. Review each application individually")
        print("2. Accept all applications")
        print("3. Reject all applications")
        
        choice = input("\n👉 Enter choice (1/2/3): ").strip()
        
        if choice == '2':
            accepted_applications = applications
            print(f"\n✅ Accepted all {len(applications)} applications!")
        elif choice == '3':
            print(f"\n❌ Rejected all {len(applications)} applications!")
        else:
            # Review individually
            for i, application in enumerate(applications):
                display_application(application, i)
                if get_yes_no_input("\n✅ Accept this application?"):
                    accepted_applications.append(application)
                    print("   ✓ Application accepted!")
                else:
                    print("   ✗ Application rejected!")
        
        # Save accepted applications
        if accepted_applications:
            save_applications(accepted_applications, db_url, db_name)
        else:
            print("\n⚠️  No applications were accepted.")
    
    except ValueError:
        print("❌ Please enter a valid number")
        return
    
    print("\n" + "="*70)
    print("Thank you for using TalentNest Application Generator! 📝")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

