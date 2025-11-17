#!/usr/bin/env python3
"""
TalentNest Job Candidate Generator

This script generates fictitious job candidates for the TalentNest job portal.
It uses OpenAI to create realistic candidate profiles based on user input.
"""

import os
import json
import random
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


class CandidateGenerator:
    """Generates job candidate profiles using OpenAI."""
    
    def __init__(self, api_key: str):
        """Initialize the generator with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)
        self.used_usernames = set()
        self.used_emails = set()
        self.used_github = set()
    
    def generate_username(self, firstname: str, lastname: str, skills: List[str] = None) -> str:
        """
        Generate a unique username based on the candidate's name or skills.
        
        Patterns:
        - firstname.lastname
        - firstname_lastname
        - firstnamelastname
        - first_initial + lastname
        - firstname + skill
        - lastname + numbers
        """
        firstname_clean = firstname.lower().replace(" ", "")
        lastname_clean = lastname.lower().replace(" ", "")
        
        # Try different username patterns
        patterns = [
            f"{firstname_clean}.{lastname_clean}",
            f"{firstname_clean}_{lastname_clean}",
            f"{firstname_clean}{lastname_clean}",
            f"{firstname_clean[0]}{lastname_clean}",
            f"{firstname_clean}_{lastname_clean[0]}",
            f"{lastname_clean}{firstname_clean[0]}",
        ]
        
        # Add skill-based patterns if skills provided
        if skills and len(skills) > 0:
            skill_clean = skills[0].lower().replace(" ", "").replace(".", "").replace("#", "sharp")
            patterns.extend([
                f"{firstname_clean}_{skill_clean[:6]}",
                f"{skill_clean[:6]}_{lastname_clean}",
                f"{firstname_clean}{skill_clean[:4]}",
            ])
        
        # Try each pattern
        for pattern in patterns:
            if pattern not in self.used_usernames:
                self.used_usernames.add(pattern)
                return pattern
        
        # If all patterns taken, add random numbers
        base = f"{firstname_clean}_{lastname_clean}"
        while True:
            username = f"{base}{random.randint(10, 99)}"
            if username not in self.used_usernames:
                self.used_usernames.add(username)
                return username
    
    def generate_password(self) -> str:
        """Generate a random plaintext password."""
        words = ["Tech", "Job", "Portal", "Talent", "Nest", "Code", "Hire", "Work"]
        numbers = random.randint(100, 999)
        special = random.choice(["!", "@", "#", "$"])
        return f"{random.choice(words)}{numbers}{special}"
    
    def generate_phone(self) -> str:
        """Generate a 555 phone number (7 digits)."""
        return f"555-{random.randint(1000, 9999)}"
    
    def generate_email(self) -> str:
        """Generate a unique email with format: numbers@revpro.com"""
        while True:
            numbers = random.randint(1000000000, 9999999999)  # 10 digit number
            email = f"{numbers}@revpro.com"
            if email not in self.used_emails:
                self.used_emails.add(email)
                return email
    
    def generate_github(self) -> str:
        """Generate a unique GitHub account (github.com/10numbers)."""
        while True:
            numbers = random.randint(1000000000, 9999999999)  # 10 digit number
            github = f"github.com/{numbers}"
            if github not in self.used_github:
                self.used_github.add(github)
                return github
    
    def generate_candidate_with_ai(self, description: str) -> Dict:
        """Generate a candidate profile using OpenAI based on description."""
        prompt = f"""Generate a realistic job candidate profile for a fictitious job portal called TalentNest.
        
Description: {description}

Provide ONLY a JSON response with the following fields:
- firstname: First name
- lastname: Last name
- application: Brief description of the role/position they're seeking (e.g., "Software Engineer", "Data Analyst", "UX Designer")
- skills: List of 3-5 relevant technical skills
- experience_years: Number of years of experience (0-20)
- education: Highest degree (e.g., "Bachelor's in Computer Science", "Master's in Data Science")
- bio: A brief 2-3 sentence professional bio

Return ONLY valid JSON, no markdown formatting or code blocks."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates realistic job candidate profiles. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            ai_data = json.loads(content)
            
            # Extract name and skills first to generate username
            firstname = ai_data.get("firstname", "John")
            lastname = ai_data.get("lastname", "Doe")
            skills = ai_data.get("skills", [])
            
            # Build complete candidate profile
            candidate = {
                "firstname": firstname,
                "lastname": lastname,
                "username": self.generate_username(firstname, lastname, skills),
                "password": self.generate_password(),
                "application": ai_data.get("application", "General Position"),
                "phone_number": self.generate_phone(),
                "email": self.generate_email(),
                "github_account": self.generate_github(),
                "skills": skills,
                "experience_years": ai_data.get("experience_years", 0),
                "education": ai_data.get("education", "Bachelor's Degree"),
                "bio": ai_data.get("bio", ""),
                "apps_submitted": [],
                "interview_status": None,
                "jobs_bookmarked": []
            }
            
            return candidate
            
        except Exception as e:
            print(f"⚠️  Error generating candidate with AI: {e}")
            print("Falling back to basic profile...")
            return self._generate_fallback_candidate(description)
    
    def _generate_fallback_candidate(self, description: str) -> Dict:
        """Generate a basic candidate profile without AI."""
        first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Quinn"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        
        firstname = random.choice(first_names)
        lastname = random.choice(last_names)
        skills = ["Python", "JavaScript", "SQL"]
        
        return {
            "firstname": firstname,
            "lastname": lastname,
            "username": self.generate_username(firstname, lastname, skills),
            "password": self.generate_password(),
            "application": description or "General Position",
            "phone_number": self.generate_phone(),
            "email": self.generate_email(),
            "github_account": self.generate_github(),
            "skills": skills,
            "experience_years": random.randint(0, 10),
            "education": "Bachelor's Degree",
            "bio": "Experienced professional seeking new opportunities.",
            "apps_submitted": [],
            "interview_status": None,
            "jobs_bookmarked": []
        }


def display_candidate(candidate: Dict, index: Optional[int] = None) -> None:
    """Display a candidate profile in a formatted way."""
    header = f"\n{'='*60}\n"
    if index is not None:
        header += f"CANDIDATE #{index + 1}\n{'='*60}\n"
    else:
        header += f"CANDIDATE PROFILE\n{'='*60}\n"
    
    print(header)
    print(f"📋 Name:             {candidate['firstname']} {candidate['lastname']}")
    print(f"👤 Username:         {candidate['username']}")
    print(f"🔑 Password:         {candidate['password']}")
    print(f"💼 Application:      {candidate['application']}")
    print(f"📞 Phone:            {candidate['phone_number']}")
    print(f"📧 Email:            {candidate['email']}")
    print(f"💻 GitHub:           {candidate['github_account']}")
    
    if candidate.get('skills'):
        print(f"🛠️  Skills:           {', '.join(candidate['skills'])}")
    if candidate.get('experience_years') is not None:
        print(f"📊 Experience:       {candidate['experience_years']} years")
    if candidate.get('education'):
        print(f"🎓 Education:        {candidate['education']}")
    if candidate.get('bio'):
        print(f"📝 Bio:              {candidate['bio']}")
    
    print(f"📄 Apps Submitted:   {candidate['apps_submitted']}")
    print(f"🎤 Interview Status: {candidate['interview_status']}")
    print(f"🔖 Jobs Bookmarked:  {candidate['jobs_bookmarked']}")
    print("=" * 60)


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


def save_candidates_to_json(candidates: List[Dict], filename: str = "generated_candidates.json") -> None:
    """Save accepted candidates to a JSON file."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    # Load existing candidates if file exists
    existing_candidates = []
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                existing_candidates = json.load(f)
        except:
            existing_candidates = []
    
    # Append new candidates
    existing_candidates.extend(candidates)
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(existing_candidates, f, indent=2)
    
    print(f"\n✅ Saved {len(candidates)} candidate(s) to {filename}")
    print(f"📊 Total candidates in file: {len(existing_candidates)}")


def save_candidates_to_mongodb(candidates: List[Dict], db_url: str, db_name: str, collection_name: str = "Candidates") -> bool:
    """Save accepted candidates to MongoDB."""
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
        
        # Insert candidates
        if len(candidates) == 1:
            result = collection.insert_one(candidates[0])
            print(f"✅ Inserted 1 candidate into MongoDB")
            print(f"   Document ID: {result.inserted_id}")
        else:
            result = collection.insert_many(candidates)
            print(f"✅ Inserted {len(result.inserted_ids)} candidates into MongoDB")
            print(f"   Document IDs: {result.inserted_ids[:3]}{'...' if len(result.inserted_ids) > 3 else ''}")
        
        # Get total count
        total_count = collection.count_documents({})
        print(f"📊 Total candidates in MongoDB collection: {total_count}")
        
        client.close()
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("   Please check your database URL and ensure MongoDB is running.")
        return False
    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")
        return False


def save_candidates(candidates: List[Dict], db_url: Optional[str] = None, db_name: Optional[str] = None) -> None:
    """Save accepted candidates to both JSON file and MongoDB (if configured)."""
    # Always save to JSON as backup
    save_candidates_to_json(candidates)
    
    # Save to MongoDB if database URL is provided
    if db_url and db_name:
        mongodb_success = save_candidates_to_mongodb(candidates, db_url, db_name)
        if not mongodb_success:
            print("⚠️  Candidates were saved to JSON file but not to MongoDB.")
    else:
        print("ℹ️  MongoDB not configured - only saved to JSON file.")


def main():
    """Main CLI interface."""
    print("\n" + "="*60)
    print("🌟  TalentNest Job Candidate Generator  🌟")
    print("="*60)
    
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
    
    if db_url and db_name:
        print(f"✅ MongoDB configured: {db_name}")
    else:
        print("⚠️  MongoDB not configured - candidates will only be saved to JSON file")
    
    # Initialize generator
    generator = CandidateGenerator(api_key)
    
    print("\n📝 Enter a brief description of the candidate OR a number of profiles to create:")
    print("   Examples:")
    print("   - 'Senior Python developer with ML experience'")
    print("   - '5' (to generate 5 candidates)")
    print("   - 'q' to quit")
    
    user_input = input("\n👉 Your input: ").strip()
    
    if user_input.lower() in ['q', 'quit', 'exit']:
        print("\n👋 Goodbye!")
        return
    
    # Determine if input is a number or description
    try:
        num_candidates = int(user_input)
        # Generate multiple candidates
        print(f"\n🔄 Generating {num_candidates} candidate profile(s)...")
        
        candidates = []
        for i in range(num_candidates):
            print(f"\n⏳ Generating candidate {i+1}/{num_candidates}...")
            description = f"Professional candidate with diverse skills #{i+1}"
            candidate = generator.generate_candidate_with_ai(description)
            candidates.append(candidate)
        
        # Display all candidates and get individual approval
        accepted_candidates = []
        
        print("\n" + "="*60)
        print("REVIEW GENERATED CANDIDATES")
        print("="*60)
        
        # Option to accept/reject all
        print("\nWould you like to:")
        print("1. Review each candidate individually")
        print("2. Accept all candidates")
        print("3. Reject all candidates")
        
        choice = input("\n👉 Enter choice (1/2/3): ").strip()
        
        if choice == '2':
            accepted_candidates = candidates
            print(f"\n✅ Accepted all {len(candidates)} candidates!")
        elif choice == '3':
            print(f"\n❌ Rejected all {len(candidates)} candidates!")
        else:
            # Review individually
            for i, candidate in enumerate(candidates):
                display_candidate(candidate, i)
                if get_yes_no_input("\n✅ Accept this candidate?"):
                    accepted_candidates.append(candidate)
                    print("   ✓ Candidate accepted!")
                else:
                    print("   ✗ Candidate rejected!")
        
        # Save accepted candidates
        if accepted_candidates:
            save_candidates(accepted_candidates, db_url, db_name)
        else:
            print("\n⚠️  No candidates were accepted.")
    
    except ValueError:
        # Single candidate with description
        description = user_input
        print(f"\n🔄 Generating candidate profile...")
        
        candidate = generator.generate_candidate_with_ai(description)
        display_candidate(candidate)
        
        if get_yes_no_input("\n✅ Accept this candidate?"):
            save_candidates([candidate], db_url, db_name)
        else:
            print("\n❌ Candidate rejected!")
    
    print("\n" + "="*60)
    print("Thank you for using TalentNest Candidate Generator! 🌟")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

