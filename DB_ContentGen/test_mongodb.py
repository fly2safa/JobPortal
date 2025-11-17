#!/usr/bin/env python3
"""
Test MongoDB Connection

Quick script to test if MongoDB credentials are working.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Load environment variables
load_dotenv()

db_url = os.getenv('project_db_url')
db_name = os.getenv('project_db_name')

print("="*60)
print("MongoDB Connection Test")
print("="*60)

if not db_url or not db_name:
    print("\n❌ Error: Database credentials not found in .env file")
    print("\nPlease ensure your .env file contains:")
    print("  project_db_url=your_mongodb_connection_string")
    print("  project_db_name=your_database_name")
    exit(1)

print(f"\n📋 Database Name: {db_name}")
print(f"🔗 Connection URL: {db_url[:20]}...{db_url[-10:] if len(db_url) > 30 else db_url}")

try:
    print("\n🔄 Attempting to connect to MongoDB...")
    client = MongoClient(db_url, serverSelectionTimeoutMS=5000)
    
    # Test the connection
    client.admin.command('ping')
    print("✅ Connection successful!")
    
    # Get database
    db = client[db_name]
    
    # List collections
    collections = db.list_collection_names()
    print(f"\n📚 Collections in '{db_name}':")
    if collections:
        for col in collections:
            count = db[col].count_documents({})
            print(f"   - {col}: {count} documents")
    else:
        print("   (No collections yet)")
    
    # Check candidates collection specifically
    if 'candidates' in collections:
        candidates_col = db['candidates']
        count = candidates_col.count_documents({})
        print(f"\n👥 Candidates collection: {count} total candidates")
        
        if count > 0:
            print("\n📄 Sample candidate (latest):")
            sample = candidates_col.find_one(sort=[('_id', -1)])
            if sample:
                print(f"   Name: {sample.get('firstname', 'N/A')} {sample.get('lastname', 'N/A')}")
                print(f"   Username: {sample.get('username', 'N/A')}")
                print(f"   Email: {sample.get('email', 'N/A')}")
    
    client.close()
    print("\n" + "="*60)
    print("✅ MongoDB is configured correctly!")
    print("="*60)
    
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"\n❌ Connection failed: {e}")
    print("\nPossible issues:")
    print("  1. MongoDB server is not running")
    print("  2. Connection URL is incorrect")
    print("  3. Network/firewall blocking connection")
    print("  4. Authentication credentials are wrong")
    
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")

print()

