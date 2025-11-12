"""
Test script for Interview Scheduling API endpoints
"""
import asyncio
import httpx
from datetime import datetime, timedelta

# API Base URL
BASE_URL = "http://localhost:8000/api/v1"

# Test credentials (you'll need to create these users first)
EMPLOYER_EMAIL = "employer@test.com"
EMPLOYER_PASSWORD = "testpassword123"

JOBSEEKER_EMAIL = "jobseeker@test.com"
JOBSEEKER_PASSWORD = "testpassword123"

# Global variables to store tokens and IDs
employer_token = None
jobseeker_token = None
test_job_id = None
test_application_id = None
test_interview_id = None


async def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


async def print_result(status: str, message: str, data=None):
    """Print test result"""
    symbol = "✅" if status == "success" else "❌" if status == "error" else "ℹ️"
    print(f"{symbol} {message}")
    if data:
        print(f"   Data: {data}")


async def register_user(email: str, password: str, role: str, first_name: str, last_name: str):
    """Register a new user"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/auth/register",
                json={
                    "email": email,
                    "password": password,
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": role
                }
            )
            if response.status_code == 200 or response.status_code == 201:
                await print_result("success", f"Registered {role}: {email}")
                return True
            elif response.status_code == 400:
                await print_result("info", f"User {email} already exists")
                return True
            else:
                await print_result("error", f"Failed to register {email}: {response.text}")
                return False
        except Exception as e:
            await print_result("error", f"Error registering {email}: {str(e)}")
            return False


async def login(email: str, password: str):
    """Login and get access token"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/auth/login",
                json={
                    "email": email,
                    "password": password
                }
            )
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                user = data.get("user", {})
                await print_result("success", f"Logged in as {email}", 
                                 f"Role: {user.get('role')}, ID: {user.get('id')}")
                return token
            else:
                await print_result("error", f"Failed to login {email}: {response.text}")
                return None
        except Exception as e:
            await print_result("error", f"Error logging in {email}: {str(e)}")
            return None


async def get_or_create_company(token: str):
    """Get employer's company or create one directly in MongoDB"""
    from motor.motor_asyncio import AsyncIOMotorClient
    from bson import ObjectId
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    async with httpx.AsyncClient() as client:
        try:
            # First, get the current user's profile
            response = await client.get(
                f"{BASE_URL}/users/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                user_data = response.json()
                company_id = user_data.get("company_id")
                user_id = user_data.get("id")
                
                if company_id:
                    await print_result("info", f"Employer already has company", f"Company ID: {company_id}")
                    return company_id
                
                # Create company directly in MongoDB
                mongodb_uri = os.getenv("MONGODB_URI")
                database_name = os.getenv("DATABASE_NAME", "TalentNest")
                
                mongo_client = AsyncIOMotorClient(mongodb_uri)
                db = mongo_client[database_name]
                
                # Create company
                company_doc = {
                    "_id": ObjectId(),
                    "name": "Test Tech Company",
                    "website": "https://testtech.com",
                    "industry": "Technology",
                    "company_size": "50-200",
                    "description": "A test company for interview testing",
                    "location": "San Francisco, CA",
                    "logo_url": None,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                await db.companies.insert_one(company_doc)
                company_id = str(company_doc["_id"])
                
                # Update user's company_id
                await db.users.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"company_id": company_id}}
                )
                
                mongo_client.close()
                
                await print_result("success", f"Created test company", f"Company ID: {company_id}")
                return company_id
            else:
                await print_result("error", f"Failed to get user profile: {response.text}")
                return None
            
        except Exception as e:
            await print_result("error", f"Error getting/creating company: {str(e)}")
            return None


async def create_test_job(token: str, company_id: str):
    """Create a test job for interviews"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/jobs",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "company_id": company_id,
                    "title": "Senior Frontend Developer",
                    "description": "We are looking for an experienced frontend developer",
                    "location": "San Francisco, CA",
                    "skills": ["React", "TypeScript", "Next.js"],
                    "job_type": "full_time",
                    "experience_level": "senior",
                    "salary_min": 120000,
                    "salary_max": 180000
                }
            )
            if response.status_code in [200, 201]:
                data = response.json()
                job_id = data.get("id")
                
                # Update job status to 'active' directly in MongoDB
                from motor.motor_asyncio import AsyncIOMotorClient
                from bson import ObjectId
                import os
                from dotenv import load_dotenv
                
                load_dotenv()
                mongodb_uri = os.getenv("MONGODB_URI")
                database_name = os.getenv("DATABASE_NAME", "TalentNest")
                
                mongo_client = AsyncIOMotorClient(mongodb_uri)
                db = mongo_client[database_name]
                
                await db.jobs.update_one(
                    {"_id": ObjectId(job_id)},
                    {"$set": {"status": "active", "posted_date": datetime.utcnow()}}
                )
                
                mongo_client.close()
                
                await print_result("success", f"Created and activated test job", f"Job ID: {job_id}")
                return job_id
            else:
                await print_result("error", f"Failed to create job: {response.text}")
                return None
        except Exception as e:
            await print_result("error", f"Error creating job: {str(e)}")
            return None


async def create_test_application(token: str, job_id: str):
    """Create a test application"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/applications",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "job_id": job_id,
                    "cover_letter": "I am very interested in this position...",
                    "resume_url": "https://example.com/resume.pdf"
                }
            )
            if response.status_code in [200, 201]:
                data = response.json()
                app_id = data.get("id")
                await print_result("success", f"Created test application", f"Application ID: {app_id}")
                return app_id
            else:
                await print_result("error", f"Failed to create application: {response.text}")
                return None
        except Exception as e:
            await print_result("error", f"Error creating application: {str(e)}")
            return None


async def schedule_interview(token: str, job_id: str, application_id: str):
    """Test: Schedule an interview (Employer only)"""
    async with httpx.AsyncClient() as client:
        try:
            # Schedule interview 2 days from now
            interview_time = datetime.utcnow() + timedelta(days=2)
            
            response = await client.post(
                f"{BASE_URL}/interviews",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "job_id": job_id,
                    "application_id": application_id,
                    "scheduled_time": interview_time.isoformat(),
                    "duration_minutes": 60,
                    "interview_type": "video",
                    "meeting_link": "https://meet.google.com/test-meeting",
                    "meeting_instructions": "Please join 5 minutes early",
                    "notes": "Technical interview focusing on React and TypeScript"
                }
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                interview_id = data.get("id")
                await print_result("success", "Scheduled interview", 
                                 f"Interview ID: {interview_id}, Time: {interview_time}")
                return interview_id
            else:
                await print_result("error", f"Failed to schedule interview: {response.text}")
                return None
        except Exception as e:
            await print_result("error", f"Error scheduling interview: {str(e)}")
            return None


async def get_interviews(token: str, role: str):
    """Test: Get list of interviews"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/interviews",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                interviews = data.get("interviews", [])
                total = data.get("total", 0)
                await print_result("success", f"Retrieved interviews for {role}", 
                                 f"Total: {total}, Returned: {len(interviews)}")
                return interviews
            else:
                await print_result("error", f"Failed to get interviews: {response.text}")
                return []
        except Exception as e:
            await print_result("error", f"Error getting interviews: {str(e)}")
            return []


async def get_interview_by_id(token: str, interview_id: str):
    """Test: Get specific interview details"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/interviews/{interview_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                await print_result("success", "Retrieved interview details", 
                                 f"Status: {data.get('status')}, Candidate: {data.get('candidate_name')}")
                return data
            else:
                await print_result("error", f"Failed to get interview: {response.text}")
                return None
        except Exception as e:
            await print_result("error", f"Error getting interview: {str(e)}")
            return None


async def reschedule_interview(token: str, interview_id: str):
    """Test: Reschedule an interview (Employer only)"""
    async with httpx.AsyncClient() as client:
        try:
            # Reschedule to 3 days from now
            new_time = datetime.utcnow() + timedelta(days=3)
            
            response = await client.post(
                f"{BASE_URL}/interviews/{interview_id}/reschedule",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "scheduled_time": new_time.isoformat(),
                    "reason": "Scheduling conflict, need to move to a later date"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                await print_result("success", "Rescheduled interview", 
                                 f"New time: {new_time}, Status: {data.get('status')}")
                return data
            else:
                await print_result("error", f"Failed to reschedule: {response.text}")
                return None
        except Exception as e:
            await print_result("error", f"Error rescheduling: {str(e)}")
            return None


async def cancel_interview(token: str, interview_id: str, role: str):
    """Test: Cancel an interview"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/interviews/{interview_id}/cancel",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "reason": f"Cancelled by {role} for testing purposes"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                await print_result("success", f"Cancelled interview by {role}", 
                                 f"Status: {data.get('status')}")
                return data
            else:
                await print_result("error", f"Failed to cancel: {response.text}")
                return None
        except Exception as e:
            await print_result("error", f"Error cancelling: {str(e)}")
            return None


async def complete_interview(token: str, interview_id: str):
    """Test: Mark interview as completed (Employer only)"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/interviews/{interview_id}/complete",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "feedback": "Great technical skills. Strong React and TypeScript knowledge. Recommended for next round.",
                    "interviewer_notes": "Candidate showed excellent problem-solving abilities."
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                await print_result("success", "Marked interview as completed", 
                                 f"Status: {data.get('status')}")
                return data
            else:
                await print_result("error", f"Failed to complete: {response.text}")
                return None
        except Exception as e:
            await print_result("error", f"Error completing: {str(e)}")
            return None


async def run_tests():
    """Run all interview API tests"""
    global employer_token, jobseeker_token, test_job_id, test_application_id, test_interview_id
    
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║          Interview Scheduling API - Test Suite                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    # Step 1: Setup - Register and Login Users
    await print_section("STEP 1: User Setup")
    await register_user(EMPLOYER_EMAIL, EMPLOYER_PASSWORD, "employer", "Test", "Employer")
    await register_user(JOBSEEKER_EMAIL, JOBSEEKER_PASSWORD, "job_seeker", "Test", "Jobseeker")
    
    employer_token = await login(EMPLOYER_EMAIL, EMPLOYER_PASSWORD)
    jobseeker_token = await login(JOBSEEKER_EMAIL, JOBSEEKER_PASSWORD)
    
    if not employer_token or not jobseeker_token:
        print("\n❌ Failed to authenticate users. Exiting tests.")
        return
    
    # Step 2: Get or Create Company
    await print_section("STEP 2: Get or Create Company")
    company_id = await get_or_create_company(employer_token)
    
    if not company_id:
        print("\n❌ Failed to get company. Exiting tests.")
        return
    
    # Step 3: Create Test Job
    await print_section("STEP 3: Create Test Job")
    test_job_id = await create_test_job(employer_token, company_id)
    
    if not test_job_id:
        print("\n❌ Failed to create test job. Exiting tests.")
        return
    
    # Step 4: Create Test Application
    await print_section("STEP 4: Create Test Application")
    test_application_id = await create_test_application(jobseeker_token, test_job_id)
    
    if not test_application_id:
        print("\n❌ Failed to create test application. Exiting tests.")
        return
    
    # Step 5: Schedule Interview
    await print_section("STEP 5: Schedule Interview (Employer)")
    test_interview_id = await schedule_interview(employer_token, test_job_id, test_application_id)
    
    if not test_interview_id:
        print("\n❌ Failed to schedule interview. Exiting tests.")
        return
    
    # Step 6: Get Interviews (Employer View)
    await print_section("STEP 6: Get Interviews (Employer View)")
    await get_interviews(employer_token, "Employer")
    
    # Step 7: Get Interviews (Job Seeker View)
    await print_section("STEP 7: Get Interviews (Job Seeker View)")
    await get_interviews(jobseeker_token, "Job Seeker")
    
    # Step 8: Get Interview Details
    await print_section("STEP 8: Get Interview Details")
    await get_interview_by_id(employer_token, test_interview_id)
    await get_interview_by_id(jobseeker_token, test_interview_id)
    
    # Step 9: Reschedule Interview
    await print_section("STEP 9: Reschedule Interview (Employer)")
    await reschedule_interview(employer_token, test_interview_id)
    
    # Step 10: Complete Interview (create new interview first)
    await print_section("STEP 10: Complete Interview Test")
    complete_interview_id = await schedule_interview(employer_token, test_job_id, test_application_id)
    if complete_interview_id:
        await complete_interview(employer_token, complete_interview_id)
    
    # Step 11: Cancel Interview
    await print_section("STEP 11: Cancel Interview (Job Seeker)")
    await cancel_interview(jobseeker_token, test_interview_id, "Job Seeker")
    
    # Final Summary
    await print_section("TEST SUMMARY")
    print("✅ All interview API endpoints tested successfully!")
    print(f"   - Employer Token: {employer_token[:20]}...")
    print(f"   - Job Seeker Token: {jobseeker_token[:20]}...")
    print(f"   - Test Job ID: {test_job_id}")
    print(f"   - Test Application ID: {test_application_id}")
    print(f"   - Test Interview ID: {test_interview_id}")
    
    print("\n" + "=" * 70)
    print("  Testing Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    print("\n🚀 Starting Interview API Tests...")
    print("📍 API URL:", BASE_URL)
    print("⏳ Please ensure the backend server is running at localhost:8000\n")
    
    try:
        asyncio.run(run_tests())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running tests: {str(e)}")

