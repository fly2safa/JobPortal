#!/usr/bin/env python3
"""
TalentNest Employer Generator

This script generates fictitious employers for the TalentNest job portal.
It uses OpenAI to create realistic employer profiles based on user input.
"""

import os
import json
import random
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


class EmployerGenerator:
    """Generates employer profiles using OpenAI."""
    
    # Funny company name components
    ADJECTIVES = [
        "Quantum", "Digital", "Mega", "Super", "Ultra", "Hyper", "Cyber", "Meta",
        "Turbo", "Ninja", "Rocket", "Cloud", "Smart", "Micro", "Macro", "Neo",
        "Alpha", "Beta", "Gamma", "Delta", "Omega", "Prime", "Elite", "Rapid",
        "Swift", "Nimble", "Agile", "Dynamic", "Epic", "Stellar", "Cosmic", "Atomic"
    ]
    
    NOUNS = [
        "Llama", "Penguin", "Unicorn", "Dragon", "Phoenix", "Ninja", "Robot",
        "Wizard", "Pirates", "Pandas", "Koalas", "Narwhals", "Octopus", "Squirrel",
        "Tiger", "Wolf", "Eagle", "Falcon", "Shark", "Dolphin", "Bear", "Lion",
        "Fox", "Raven", "Hawk", "Owl", "Lynx", "Jaguar", "Cheetah", "Panther"
    ]
    
    SUFFIXES = [
        "Inc", "Corp", "LLC", "Ltd", "Systems", "Solutions", "Technologies",
        "Innovations", "Ventures", "Labs", "Studios", "Enterprises",
        "Group", "Partners", "Associates", "Digital", "Interactive", "Global",
        "Dynamics", "Strategies", "Services", "Consulting", "Industries", "Works"
    ]
    
    INDUSTRIES = [
        "Technology", "Healthcare", "Finance", "E-commerce", "Education",
        "Manufacturing", "Retail", "Consulting", "Media & Entertainment",
        "Real Estate", "Transportation", "Telecommunications", "Energy",
        "Hospitality", "Agriculture", "Construction", "Automotive"
    ]
    
    EMPLOYEE_SIZES = [
        "1-10", "11-50", "51-200", "201-500", "501-1000",
        "1001-5000", "5001-10000", "10000+"
    ]
    
    # Weighted distribution for more realistic size variety
    EMPLOYEE_SIZE_WEIGHTS = [0.25, 0.30, 0.20, 0.12, 0.08, 0.03, 0.015, 0.005]
    
    COMPANY_MATURITY = [
        "Startup", "Early Stage", "Growth Stage", "Established", 
        "Mature", "Enterprise", "Legacy", "Industry Leader"
    ]
    
    # Years corresponding to maturity stages
    MATURITY_YEARS = {
        "Startup": "0-2 years",
        "Early Stage": "2-4 years",
        "Growth Stage": "4-8 years",
        "Established": "8-15 years",
        "Mature": "15-25 years",
        "Enterprise": "25-40 years",
        "Legacy": "40-75 years",
        "Industry Leader": "75+ years"
    }
    
    US_CITIES = [
        ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"),
        ("Houston", "TX"), ("Phoenix", "AZ"), ("Philadelphia", "PA"),
        ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"),
        ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"),
        ("San Francisco", "CA"), ("Columbus", "OH"), ("Charlotte", "NC"),
        ("Indianapolis", "IN"), ("Seattle", "WA"), ("Denver", "CO"),
        ("Boston", "MA"), ("Portland", "OR"), ("Atlanta", "GA"),
        ("Miami", "FL"), ("Detroit", "MI"), ("Nashville", "TN"),
        ("Baltimore", "MD"), ("Minneapolis", "MN"), ("Tampa", "FL"),
        ("Raleigh", "NC"), ("Pittsburgh", "PA"), ("Las Vegas", "NV")
    ]
    
    def __init__(self, api_key: str):
        """Initialize the generator with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)
        self.used_company_names = set()
    
    def generate_funny_company_name(self) -> str:
        """Generate a funny/creative company name."""
        while True:
            pattern = random.choice([1, 2, 3])
            
            if pattern == 1:
                # Adjective + Noun + Suffix
                name = f"{random.choice(self.ADJECTIVES)} {random.choice(self.NOUNS)} {random.choice(self.SUFFIXES)}"
            elif pattern == 2:
                # Noun + Suffix
                name = f"{random.choice(self.NOUNS)} {random.choice(self.SUFFIXES)}"
            else:
                # Adjective + Noun
                name = f"{random.choice(self.ADJECTIVES)}{random.choice(self.NOUNS)}"
            
            if name not in self.used_company_names:
                self.used_company_names.add(name)
                return name
    
    def generate_password(self) -> str:
        """Generate a random plaintext password."""
        words = ["Company", "Business", "Corp", "Hire", "Jobs", "Team", "Work", "Best"]
        numbers = random.randint(100, 999)
        special = random.choice(["!", "@", "#", "$"])
        return f"{random.choice(words)}{numbers}{special}"
    
    def generate_location(self) -> Dict[str, str]:
        """Generate a random US city and state."""
        city, state = random.choice(self.US_CITIES)
        return {"city": city, "state": state}
    
    def generate_employee_size(self) -> str:
        """Generate employee size with weighted distribution (more small companies)."""
        return random.choices(self.EMPLOYEE_SIZES, weights=self.EMPLOYEE_SIZE_WEIGHTS, k=1)[0]
    
    def generate_company_maturity(self, employee_size: str = None) -> Dict[str, str]:
        """
        Generate company maturity/age with correlation to size.
        Larger companies tend to be more mature.
        """
        if employee_size:
            size_index = self.EMPLOYEE_SIZES.index(employee_size)
            # Bias maturity towards later stages for larger companies
            if size_index >= 6:  # 5001+
                maturity_options = self.COMPANY_MATURITY[4:]  # Mature to Industry Leader
            elif size_index >= 4:  # 501+
                maturity_options = self.COMPANY_MATURITY[3:6]  # Established to Enterprise
            elif size_index >= 2:  # 51+
                maturity_options = self.COMPANY_MATURITY[2:5]  # Growth Stage to Mature
            else:  # 1-50
                maturity_options = self.COMPANY_MATURITY[0:4]  # Startup to Established
            
            maturity = random.choice(maturity_options)
        else:
            maturity = random.choice(self.COMPANY_MATURITY)
        
        return {
            "maturity": maturity,
            "years_in_business": self.MATURITY_YEARS[maturity]
        }
    
    def generate_employer_with_ai(self, description: str, company_name: str = None) -> Dict:
        """Generate an employer profile using OpenAI based on description."""
        # Create a unique seed for variety
        random_seed = random.randint(1000, 9999)
        
        # Pre-generate a company name if not provided
        if not company_name:
            company_name = self.generate_funny_company_name()
        
        prompt = f"""Generate a realistic employer/company profile.

Description: {description}
Company Name: {company_name}
Variation seed: {random_seed}

CRITICAL RULES:
1. The company name is "{company_name}" - use this EXACT name in the description
2. Do NOT create job portal, recruiting, or hiring platform companies
3. Create companies in DIVERSE industries: Technology (software/SaaS/AI), Healthcare (medical devices/biotech), 
   Finance (fintech/banking), E-commerce (online retail), Manufacturing (hardware/products), 
   Consulting (business services), Media & Entertainment (streaming/gaming), Real Estate, etc.
4. Do NOT use words like: Job, Hire, Recruit, Talent, Career, Employment in the company description

Provide ONLY a JSON response with the following fields:
- company_description: A brief 2-3 sentence description of what "{company_name}" does. Must use the company name "{company_name}" in the description.
- industry: The primary industry (choose from: "Technology", "Healthcare", "Finance", "E-commerce", "Education", "Manufacturing", "Retail", "Consulting", "Media & Entertainment", "Real Estate", "Transportation", "Telecommunications", "Energy", "Hospitality", "Agriculture", "Construction", "Automotive")

Return ONLY valid JSON, no markdown formatting or code blocks.

NOTE: Employee size and company maturity will be auto-generated based on realistic distributions."""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates diverse, realistic company profiles. Always respond with valid JSON only. Create companies in VARIED industries - avoid job portals or recruiting companies."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.85,  # Balanced temperature for consistency
                    max_tokens=400
                )
                
                content = response.choices[0].message.content.strip()
                
                # Remove markdown code blocks if present
                if content.startswith("```"):
                    content = content.split("```")[1]
                    if content.startswith("json"):
                        content = content[4:]
                    content = content.strip()
                
                ai_data = json.loads(content)
                
                # Get location
                location = self.generate_location()
                
                # Generate employee size with weighted distribution
                employee_size = self.generate_employee_size()
                
                # Generate company maturity correlated with size
                maturity_data = self.generate_company_maturity(employee_size)
                
                # Verify the description mentions the company name
                description = ai_data.get("company_description", "")
                if company_name.split()[0] not in description:
                    # If the AI didn't use the company name, add it
                    description = f"{company_name} is a leading company. " + description
                
                # Build complete employer profile
                employer = {
                    "company_name": company_name,
                    "password": self.generate_password(),
                    "company_description": description,
                    "industry": ai_data.get("industry", random.choice(self.INDUSTRIES)),
                    "employee_size": employee_size,
                    "company_maturity": maturity_data['maturity'],
                    "years_in_business": maturity_data['years_in_business'],
                    "location": f"{location['city']}, {location['state']}",
                    "city": location['city'],
                    "state": location['state']
                }
                
                return employer
                
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"⚠️  Error generating employer with AI after {max_retries} attempts: {e}")
                    print("Falling back to basic profile...")
                    return self._generate_fallback_employer(description, company_name)
                # Otherwise, retry
    
    def _generate_fallback_employer(self, description: str, company_name: str = None) -> Dict:
        """Generate a basic employer profile without AI."""
        if not company_name:
            company_name = self.generate_funny_company_name()
            
        location = self.generate_location()
        employee_size = self.generate_employee_size()
        maturity_data = self.generate_company_maturity(employee_size)
        
        return {
            "company_name": company_name,
            "password": self.generate_password(),
            "company_description": f"{company_name} is an innovative company. {description or 'We offer exciting opportunities.'}",
            "industry": random.choice(self.INDUSTRIES),
            "employee_size": employee_size,
            "company_maturity": maturity_data['maturity'],
            "years_in_business": maturity_data['years_in_business'],
            "location": f"{location['city']}, {location['state']}",
            "city": location['city'],
            "state": location['state']
        }


def display_employer(employer: Dict, index: Optional[int] = None) -> None:
    """Display an employer profile in a formatted way."""
    header = f"\n{'='*60}\n"
    if index is not None:
        header += f"EMPLOYER #{index + 1}\n{'='*60}\n"
    else:
        header += f"EMPLOYER PROFILE\n{'='*60}\n"
    
    print(header)
    print(f"🏢 Company Name:     {employer['company_name']}")
    print(f"🔑 Password:         {employer['password']}")
    print(f"📋 Description:      {employer['company_description']}")
    print(f"🏭 Industry:         {employer['industry']}")
    print(f"👥 Employee Size:    {employer['employee_size']}")
    print(f"🎂 Company Stage:    {employer['company_maturity']} ({employer['years_in_business']})")
    print(f"📍 Location:         {employer['location']}")
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


def save_employers_to_json(employers: List[Dict], filename: str = "generated_employers.json") -> None:
    """Save accepted employers to a JSON file."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    # Load existing employers if file exists
    existing_employers = []
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                existing_employers = json.load(f)
        except:
            existing_employers = []
    
    # Append new employers
    existing_employers.extend(employers)
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(existing_employers, f, indent=2)
    
    print(f"\n✅ Saved {len(employers)} employer(s) to {filename}")
    print(f"📊 Total employers in file: {len(existing_employers)}")


def save_employers_to_mongodb(employers: List[Dict], db_url: str, db_name: str, collection_name: str = "Employers") -> bool:
    """Save accepted employers to MongoDB."""
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
        
        # Insert employers
        if len(employers) == 1:
            result = collection.insert_one(employers[0])
            print(f"✅ Inserted 1 employer into MongoDB")
            print(f"   Document ID: {result.inserted_id}")
        else:
            result = collection.insert_many(employers)
            print(f"✅ Inserted {len(result.inserted_ids)} employers into MongoDB")
            print(f"   Document IDs: {result.inserted_ids[:3]}{'...' if len(result.inserted_ids) > 3 else ''}")
        
        # Get total count
        total_count = collection.count_documents({})
        print(f"📊 Total employers in MongoDB collection: {total_count}")
        
        client.close()
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("   Please check your database URL and ensure MongoDB is running.")
        return False
    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")
        return False


def save_employers(employers: List[Dict], db_url: Optional[str] = None, db_name: Optional[str] = None) -> None:
    """Save accepted employers to both JSON file and MongoDB (if configured)."""
    # Always save to JSON as backup
    save_employers_to_json(employers)
    
    # Save to MongoDB if database URL is provided
    if db_url and db_name:
        mongodb_success = save_employers_to_mongodb(employers, db_url, db_name)
        if not mongodb_success:
            print("⚠️  Employers were saved to JSON file but not to MongoDB.")
    else:
        print("ℹ️  MongoDB not configured - only saved to JSON file.")


def main():
    """Main CLI interface."""
    print("\n" + "="*60)
    print("🏢  TalentNest Employer Generator  🏢")
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
        print("⚠️  MongoDB not configured - employers will only be saved to JSON file")
    
    # Initialize generator
    generator = EmployerGenerator(api_key)
    
    print("\n📝 Enter a brief description of the employer OR a number of profiles to create:")
    print("   Examples:")
    print("   - 'Tech startup focused on AI and machine learning'")
    print("   - '5' (to generate 5 employers)")
    print("   - 'q' to quit")
    
    user_input = input("\n👉 Your input: ").strip()
    
    if user_input.lower() in ['q', 'quit', 'exit']:
        print("\n👋 Goodbye!")
        return
    
    # Determine if input is a number or description
    try:
        num_employers = int(user_input)
        # Generate multiple employers
        print(f"\n🔄 Generating {num_employers} employer profile(s)...")
        
        employers = []
        for i in range(num_employers):
            print(f"\n⏳ Generating employer {i+1}/{num_employers}...")
            description = f"Innovative company #{i+1}"
            employer = generator.generate_employer_with_ai(description)
            employers.append(employer)
        
        # Display all employers and get individual approval
        accepted_employers = []
        
        print("\n" + "="*60)
        print("REVIEW GENERATED EMPLOYERS")
        print("="*60)
        
        # Option to accept/reject all
        print("\nWould you like to:")
        print("1. Review each employer individually")
        print("2. Accept all employers")
        print("3. Reject all employers")
        
        choice = input("\n👉 Enter choice (1/2/3): ").strip()
        
        if choice == '2':
            accepted_employers = employers
            print(f"\n✅ Accepted all {len(employers)} employers!")
        elif choice == '3':
            print(f"\n❌ Rejected all {len(employers)} employers!")
        else:
            # Review individually
            for i, employer in enumerate(employers):
                display_employer(employer, i)
                if get_yes_no_input("\n✅ Accept this employer?"):
                    accepted_employers.append(employer)
                    print("   ✓ Employer accepted!")
                else:
                    print("   ✗ Employer rejected!")
        
        # Save accepted employers
        if accepted_employers:
            save_employers(accepted_employers, db_url, db_name)
        else:
            print("\n⚠️  No employers were accepted.")
    
    except ValueError:
        # Single employer with description
        description = user_input
        print(f"\n🔄 Generating employer profile...")
        
        employer = generator.generate_employer_with_ai(description)
        display_employer(employer)
        
        if get_yes_no_input("\n✅ Accept this employer?"):
            save_employers([employer], db_url, db_name)
        else:
            print("\n❌ Employer rejected!")
    
    print("\n" + "="*60)
    print("Thank you for using TalentNest Employer Generator! 🏢")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

