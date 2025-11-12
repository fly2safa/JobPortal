"""
Quick script to get a company ID from the database
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

async def get_companies():
    """Get companies from database"""
    mongodb_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("DATABASE_NAME", "TalentNest")
    
    client = AsyncIOMotorClient(mongodb_uri)
    db = client[database_name]
    
    # Get first company
    companies = await db.companies.find().limit(5).to_list(5)
    
    if companies:
        print("\n✅ Found companies in database:")
        for i, company in enumerate(companies, 1):
            print(f"\n{i}. Company Name: {company.get('name')}")
            print(f"   Company ID: {company.get('_id')}")
            print(f"   Industry: {company.get('industry', 'N/A')}")
    else:
        print("\n❌ No companies found in database")
        print("   You may need to run the employer_generator.py script first")
    
    client.close()
    
    return companies[0].get('_id') if companies else None

if __name__ == "__main__":
    asyncio.run(get_companies())

