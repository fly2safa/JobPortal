"""
Test script to verify authentication functionality.
"""
import asyncio
from app.db.init_db import connect_to_mongo, close_mongo_connection
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.core.logging import setup_logging, get_logger

setup_logging(level="INFO")
logger = get_logger(__name__)


async def test_user_creation():
    """Test creating a user in the database."""
    try:
        logger.info("Connecting to MongoDB...")
        await connect_to_mongo()
        logger.info("Connected successfully!")
        
        # Check if test user exists
        test_email = "testuser@example.com"
        existing_user = await User.find_one(User.email == test_email)
        
        if existing_user:
            logger.info(f"Test user already exists: {test_email}")
            logger.info(f"User ID: {existing_user.id}")
        else:
            logger.info("Creating test user...")
            user = User(
                email=test_email,
                hashed_password=get_password_hash("TestPass123"),
                first_name="Test",
                last_name="User",
                role=UserRole.JOB_SEEKER,
            )
            await user.insert()
            logger.info(f"User created successfully! ID: {user.id}")
        
        # Count total users
        user_count = await User.count()
        logger.info(f"Total users in database: {user_count}")
        
        await close_mongo_connection()
        logger.info("Test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(test_user_creation())
    if result:
        print("\n✓ User creation test PASSED!")
    else:
        print("\n✗ User creation test FAILED!")




