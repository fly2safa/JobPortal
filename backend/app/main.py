"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.db.init_db import connect_to_mongo, close_mongo_connection
from app.api.v1.routes import auth, jobs, applications, users, resumes, assistant, interviews, recommendations

# Setup logging from settings
setup_logging(level=settings.LOG_LEVEL)
logger = get_logger(__name__)

# ANSI color codes for console output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Connect to MongoDB
    await connect_to_mongo()
    
    # Initialize AI recommendation system
    try:
        from app.services.recommendation_service import recommendation_service
        from app.ai.rag.embeddings import embeddings_handler
        
        if embeddings_handler.is_available:
            logger.info("Initializing AI recommendation system...")
            await recommendation_service.initialize_vector_store()
            vector_count = recommendation_service.vector_store.size()
            logger.info(f"AI recommendation system initialized with {vector_count} jobs")
        else:
            logger.warning("OpenAI API key not configured - AI recommendations will use fallback mode")
    except Exception as e:
        logger.error(f"Failed to initialize recommendation system: {str(e)}")
        logger.warning("Recommendation system will initialize on first use")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    print(f"\n{Colors.YELLOW}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}🛑 Shutting down application...{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    logger.info("Shutting down application...")
    await close_mongo_connection()
    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Application shutdown complete{Colors.RESET}\n")
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A secure, scalable job portal platform connecting job seekers and employers",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(applications.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(resumes.router, prefix="/api/v1")
app.include_router(assistant.router, prefix="/api/v1")
app.include_router(interviews.router, prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")


# Health check endpoints
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status information
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/")
async def root():
    """
    Root endpoint.
    
    Returns:
        Welcome message and API information
    """
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


