"""
Simple script to test MongoDB connection.
"""
import asyncio
from app.db.init_db import connect_to_mongo, close_mongo_connection
from app.core.logging import setup_logging, get_logger

setup_logging(level="INFO")
logger = get_logger(__name__)


async def test_connection():
    """Test MongoDB connection."""
    try:
        logger.info("Testing MongoDB connection...")
        await connect_to_mongo()
        logger.info("✅ Successfully connected to MongoDB!")
        logger.info("✅ Database connection test PASSED!")
        await close_mongo_connection()
        return True
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_connection())
    if result:
        print("\n✅ MongoDB connection test SUCCESSFUL!")
    else:
        print("\n❌ MongoDB connection test FAILED!")

