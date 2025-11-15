"""
MongoDB database initialization using Beanie ODM.
"""
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# ANSI color codes for console output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# MongoDB client instance
mongodb_client: AsyncIOMotorClient = None


async def connect_to_mongo():
    """Connect to MongoDB and initialize Beanie."""
    global mongodb_client
    
    try:
        # Print colored connecting message
        print(f"{Colors.CYAN}🔄 Connecting to MongoDB...{Colors.RESET}")
        print(f"{Colors.BLUE}   Database: {Colors.BOLD}{settings.DATABASE_NAME}{Colors.RESET}")
        logger.info(f"Connecting to MongoDB at {settings.DATABASE_NAME}...")
        
        # Create MongoDB client
        mongodb_client = AsyncIOMotorClient(settings.MONGODB_URI)
        
        # Test connection by pinging the server
        await mongodb_client.admin.command('ping')
        
        # Get database
        database = mongodb_client[settings.DATABASE_NAME]
        
        # Import all models
        from app.models.user import User
        from app.models.company import Company
        from app.models.job import Job
        from app.models.application import Application
        from app.models.resume import Resume
        from app.models.conversation import Conversation
        from app.models.interview import Interview
        from app.models.test_session import TestSession
        
        # Initialize Beanie with document models
        await init_beanie(
            database=database,
            document_models=[
                User,
                Company,
                Job,
                Application,
                Resume,
                Conversation,
                Interview,
                TestSession,
            ]
        )
        
        # Print colored success message
        print(f"{Colors.GREEN}{Colors.BOLD}✅ MongoDB Connected Successfully!{Colors.RESET}")
        print(f"{Colors.GREEN}   Database: {settings.DATABASE_NAME}{Colors.RESET}")
        print(f"{Colors.GREEN}   Models: 8 collections initialized{Colors.RESET}")
        logger.info("Successfully connected to MongoDB and initialized Beanie")
        
    except Exception as e:
        # Print colored error message
        print(f"{Colors.RED}{Colors.BOLD}❌ MongoDB Connection Failed!{Colors.RESET}")
        print(f"{Colors.RED}   Error: {str(e)}{Colors.RESET}")
        print(f"{Colors.YELLOW}   Please check:{Colors.RESET}")
        print(f"{Colors.YELLOW}   - MongoDB URI in .env file{Colors.RESET}")
        print(f"{Colors.YELLOW}   - Network connectivity{Colors.RESET}")
        print(f"{Colors.YELLOW}   - Database credentials{Colors.RESET}")
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection."""
    global mongodb_client
    
    if mongodb_client:
        print(f"{Colors.YELLOW}🔄 Closing MongoDB connection...{Colors.RESET}")
        logger.info("Closing MongoDB connection...")
        mongodb_client.close()
        print(f"{Colors.GREEN}✅ MongoDB connection closed{Colors.RESET}")
        logger.info("MongoDB connection closed")


async def get_database():
    """Get database instance."""
    return mongodb_client[settings.DATABASE_NAME]




