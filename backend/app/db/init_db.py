"""
MongoDB database initialization using Beanie ODM.
"""
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# MongoDB client instance
mongodb_client: AsyncIOMotorClient = None


async def connect_to_mongo():
    """Connect to MongoDB and initialize Beanie."""
    global mongodb_client
    
    try:
        logger.info(f"Connecting to MongoDB at {settings.DATABASE_NAME}...")
        
        # Create MongoDB client
        mongodb_client = AsyncIOMotorClient(settings.MONGODB_URI)
        
        # Get database
        database = mongodb_client[settings.DATABASE_NAME]
        
        # Import all models
        from app.models.user import User
        from app.models.company import Company
        
        # Initialize Beanie with document models
        await init_beanie(
            database=database,
            document_models=[
                User,
                Company,
            ]
        )
        
        logger.info("Successfully connected to MongoDB and initialized Beanie")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection."""
    global mongodb_client
    
    if mongodb_client:
        logger.info("Closing MongoDB connection...")
        mongodb_client.close()
        logger.info("MongoDB connection closed")


async def get_database():
    """Get database instance."""
    return mongodb_client[settings.DATABASE_NAME]




