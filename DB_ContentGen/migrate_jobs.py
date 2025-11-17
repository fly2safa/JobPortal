#!/usr/bin/env python3
"""
MongoDB Job Schema Migration Script
Migrates existing job documents from old schema to new backend-compatible schema.
"""

import os
import re
from datetime import datetime
from typing import Dict, Optional, List
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

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

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI') or os.getenv('project_db_url')
DATABASE_NAME = os.getenv('DATABASE_NAME') or os.getenv('project_db_name') or 'jobportal'

# Mapping dictionaries
EMPLOYMENT_TYPE_MAP = {
    "Full-Time": "full_time",
    "Part-Time": "part_time",
    "Contract": "contract",
    "Internship": "internship",
    "Temporary": "temporary",
    # Add variations
    "full-time": "full_time",
    "part-time": "part_time",
}

EXPERIENCE_LEVEL_MAP = {
    "junior": "junior",
    "mid": "mid",
    "mid-level": "mid",
    "senior": "senior",
    "lead": "lead",
    "principal": "executive",
    "executive": "executive",
}


def parse_salary_range(salary_range: str) -> tuple[Optional[float], Optional[float]]:
    """
    Parse salary range string like '$150,000 - $220,000' into (min, max) tuple.
    Returns (None, None) if parsing fails.
    """
    try:
        # Remove '$' and ',' characters
        cleaned = salary_range.replace('$', '').replace(',', '')
        
        # Split on '-' or 'to'
        if '-' in cleaned:
            parts = cleaned.split('-')
        elif 'to' in cleaned.lower():
            parts = cleaned.lower().split('to')
        else:
            return None, None
        
        if len(parts) == 2:
            min_salary = float(parts[0].strip())
            max_salary = float(parts[1].strip())
            return min_salary, max_salary
    except (ValueError, AttributeError):
        pass
    
    return None, None


def determine_experience_level(job_title: str, requirements: List[str] = None) -> str:
    """
    Determine experience level from job title or requirements.
    """
    title_lower = job_title.lower() if job_title else ""
    
    # Check title keywords
    if any(word in title_lower for word in ["principal", "staff", "distinguished"]):
        return "executive"
    elif any(word in title_lower for word in ["lead", "head of", "director"]):
        return "lead"
    elif any(word in title_lower for word in ["senior", "sr.", "sr "]):
        return "senior"
    elif any(word in title_lower for word in ["junior", "jr.", "jr "]):
        return "junior"
    elif any(word in title_lower for word in ["entry", "associate", "trainee"]):
        return "entry"
    
    # Check requirements for years of experience
    if requirements:
        req_text = " ".join(requirements).lower()
        if "8+" in req_text or "10+" in req_text or "12+" in req_text:
            return "lead"
        elif "5+" in req_text or "6+" in req_text or "7+" in req_text:
            return "senior"
        elif "3+" in req_text or "4+" in req_text:
            return "mid"
        elif "1+" in req_text or "2+" in req_text:
            return "junior"
    
    return "mid"  # Default


def extract_years_from_requirements(requirements: List[str]) -> tuple[int, int]:
    """
    Extract experience years from requirements.
    Returns (min_years, max_years) tuple.
    """
    if not requirements:
        return 0, 0
    
    req_text = " ".join(requirements)
    
    # Look for patterns like "5+ years", "3-5 years", "5 to 8 years"
    patterns = [
        r'(\d+)\+\s*years?',  # "5+ years"
        r'(\d+)\s*-\s*(\d+)\s*years?',  # "3-5 years"
        r'(\d+)\s*to\s*(\d+)\s*years?',  # "3 to 5 years"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, req_text, re.IGNORECASE)
        if matches:
            if isinstance(matches[0], tuple):
                # Range found (e.g., "3-5 years")
                return int(matches[0][0]), int(matches[0][1])
            else:
                # Plus sign found (e.g., "5+ years")
                min_years = int(matches[0])
                return min_years, min_years + 3
    
    # Default based on common ranges
    return 2, 5


def migrate_job_document(job: Dict) -> Dict:
    """
    Transform old job schema to new schema.
    """
    # Parse salary
    salary_min, salary_max = None, None
    if "salary_range" in job:
        salary_min, salary_max = parse_salary_range(job["salary_range"])
    
    # Map employment type
    employment_type = job.get("employment_type", "Full-Time")
    job_type = EMPLOYMENT_TYPE_MAP.get(employment_type, "full_time")
    
    # Determine remote boolean
    remote_str = job.get("remote", "On-site")
    is_remote = remote_str.lower() in ["remote", "fully remote"]
    
    # Determine experience level
    job_title = job.get("job_title", job.get("title", ""))
    requirements = job.get("requirements", [])
    experience_level = determine_experience_level(job_title, requirements)
    
    # Extract experience years
    exp_min, exp_max = extract_years_from_requirements(requirements)
    
    # Convert requirements array to string if needed
    requirements_str = None
    if requirements and isinstance(requirements, list):
        requirements_str = "\n".join(f"• {req}" for req in requirements)
    elif requirements and isinstance(requirements, str):
        requirements_str = requirements
    
    # Parse posted_date
    posted_date = None
    if "posted_date" in job:
        try:
            posted_date = datetime.fromisoformat(job["posted_date"])
        except:
            try:
                # Try parsing YYYY-MM-DD format
                posted_date = datetime.strptime(job["posted_date"], "%Y-%m-%d")
            except:
                posted_date = datetime.utcnow()
    else:
        posted_date = datetime.utcnow()
    
    # Build new schema document
    migrated = {
        # Core fields
        "title": job_title,
        "description": job.get("description", ""),
        "requirements": requirements_str,
        "responsibilities": None,  # Not in old schema
        
        # Skills
        "skills": job.get("skills", []),
        "required_skills": job.get("skills", [])[:5] if "skills" in job else [],
        "preferred_skills": job.get("skills", [])[5:10] if "skills" in job else [],
        
        # Location
        "location": job.get("location", "Remote"),
        "is_remote": is_remote,
        
        # Company/Employer - CRITICAL FIELDS
        "company_id": str(job.get("employer_id", job.get("company_id", "default_company"))),
        "company_name": job.get("company_name", "Unknown Company"),
        "employer_id": str(job.get("employer_id", "default_employer")),
        
        # Salary
        "salary_min": salary_min,
        "salary_max": salary_max,
        "salary_currency": "USD",
        
        # Job details
        "job_type": job_type,
        "experience_level": experience_level,
        "experience_years_min": exp_min,
        "experience_years_max": exp_max,
        
        # Status - CRITICAL FIELD
        "status": "active",  # Set all existing jobs to active
        "posted_date": posted_date,
        "closing_date": None,
        
        # Tracking
        "application_count": len(job.get("app_ids_received", [])),
        "view_count": 0,
        
        # Additional
        "benefits": [],
        "application_instructions": None,
        
        # Metadata
        "created_at": posted_date,
        "updated_at": datetime.utcnow(),
        
        # Keep legacy fields for reference (optional)
        "_legacy_job_id": job.get("job_id"),
        "_legacy_schema": True,
    }
    
    return migrated


def migrate_database(dry_run: bool = True):
    """
    Main migration function.
    
    Args:
        dry_run: If True, only show what would be changed without making changes
    """
    if not MONGODB_URI:
        print("❌ Error: MONGODB_URI not found in environment variables")
        print("   Set MONGODB_URI or project_db_url in .env file")
        return
    
    if not DATABASE_NAME:
        print("❌ Error: DATABASE_NAME not found in environment variables")
        print("   Set DATABASE_NAME or project_db_name in .env file")
        return
    
    print("\n" + "="*70)
    print("🔄 MongoDB Job Schema Migration")
    print("="*70)
    print(f"Database: {DATABASE_NAME}")
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'LIVE (will modify data)'}")
    print("="*70 + "\n")
    
    try:
        # Connect to MongoDB
        print("📡 Connecting to MongoDB...")
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ Connected successfully!\n")
        
        # Get database and collection
        db = client[DATABASE_NAME]
        jobs_collection = db["jobs"]  # Backend expects lowercase "jobs"
        
        # Also check for "Jobs" (capital J) collection
        jobs_collection_alt = db["Jobs"]
        
        # Count documents in both collections
        count_lowercase = jobs_collection.count_documents({})
        count_uppercase = jobs_collection_alt.count_documents({})
        
        print(f"📊 Found {count_lowercase} documents in 'jobs' collection")
        print(f"📊 Found {count_uppercase} documents in 'Jobs' collection")
        
        # Determine which collection to migrate
        if count_uppercase > 0 and count_lowercase == 0:
            print(f"\n⚠️  Jobs are in 'Jobs' collection (capital J)")
            print(f"   Backend expects 'jobs' collection (lowercase)")
            source_collection = jobs_collection_alt
            target_collection = jobs_collection
            will_rename = True
        elif count_lowercase > 0:
            print(f"\n✓ Using existing 'jobs' collection")
            source_collection = jobs_collection
            target_collection = jobs_collection
            will_rename = False
        else:
            print("\n❌ No jobs found in database!")
            return
        
        # Check if jobs need migration (look for old schema fields)
        sample_job = source_collection.find_one({})
        if not sample_job:
            print("❌ No jobs found to migrate")
            return
        
        needs_migration = (
            "job_title" in sample_job or
            "salary_range" in sample_job or
            "status" not in sample_job
        )
        
        if not needs_migration:
            print("\n✅ Jobs already appear to be in new schema format!")
            print("   No migration needed.")
            return
        
        print(f"\n🔍 Sample job (old schema):")
        print(f"   Title: {sample_job.get('job_title', sample_job.get('title', 'N/A'))}")
        print(f"   Has 'status' field: {'status' in sample_job}")
        print(f"   Has 'job_title' field: {'job_title' in sample_job}")
        print(f"   Has 'salary_range' field: {'salary_range' in sample_job}")
        
        # Get all jobs
        total_jobs = source_collection.count_documents({})
        print(f"\n📋 Preparing to migrate {total_jobs} job(s)...")
        
        if dry_run:
            print("\n🔬 DRY RUN - Showing migration preview for first 3 jobs:\n")
        
        migrated_count = 0
        error_count = 0
        
        # Process each job
        for idx, job in enumerate(source_collection.find({}), 1):
            try:
                # Migrate the document
                migrated_job = migrate_job_document(job)
                
                # Show preview for first few jobs in dry run
                if dry_run and idx <= 3:
                    print(f"Job {idx}:")
                    print(f"  OLD: job_title='{job.get('job_title', 'N/A')}'")
                    print(f"  NEW: title='{migrated_job['title']}'")
                    print(f"  NEW: status='{migrated_job['status']}'")
                    print(f"  NEW: job_type='{migrated_job['job_type']}'")
                    print(f"  NEW: is_remote={migrated_job['is_remote']}")
                    if migrated_job['salary_min']:
                        print(f"  NEW: salary=${migrated_job['salary_min']:,.0f}-${migrated_job['salary_max']:,.0f}")
                    print()
                
                # If not dry run, update the document
                if not dry_run:
                    # Get the job ID
                    job_id = job.get('_id')
                    
                    if will_rename:
                        # Insert into new 'jobs' collection
                        migrated_job['_id'] = job_id
                        target_collection.insert_one(migrated_job)
                    else:
                        # Update in place
                        target_collection.replace_one(
                            {'_id': job_id},
                            migrated_job,
                            upsert=True
                        )
                    
                    migrated_count += 1
                    
                    if migrated_count % 10 == 0:
                        print(f"   Migrated {migrated_count}/{total_jobs} jobs...")
                
            except Exception as e:
                error_count += 1
                print(f"   ⚠️  Error migrating job {idx}: {str(e)}")
        
        # Summary
        print("\n" + "="*70)
        if dry_run:
            print("🔬 DRY RUN COMPLETE")
            print(f"   Would migrate {total_jobs} job(s)")
            print(f"   Run with --execute to apply changes")
        else:
            print("✅ MIGRATION COMPLETE")
            print(f"   Migrated: {migrated_count} job(s)")
            if error_count > 0:
                print(f"   Errors: {error_count}")
            
            # If we renamed the collection, optionally remove old one
            if will_rename:
                print(f"\n⚠️  Old 'Jobs' collection still exists")
                print(f"   You can manually drop it after verifying the migration:")
                print(f"   db.Jobs.drop()")
        
        print("="*70 + "\n")
        
        client.close()
        
    except ConnectionFailure as e:
        print(f"❌ Failed to connect to MongoDB: {str(e)}")
    except Exception as e:
        print(f"❌ Migration error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        response = input("\n⚠️  This will modify your database. Continue? (yes/no): ")
        if response.lower() == "yes":
            dry_run = False
        else:
            print("Cancelled.")
            sys.exit(0)
    
    migrate_database(dry_run=dry_run)

