"""
Application configuration using Pydantic settings.
"""
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # MongoDB
    MONGODB_URI: str
    DATABASE_NAME: str = "jobportal"
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI (Optional - for AI features)
    OPENAI_API_KEY: Optional[str] = None
    
    # n8n Workflow Automation (Optional - for AI orchestration)
    N8N_BASE_URL: str = "http://localhost:5678"
    N8N_API_KEY: Optional[str] = None
    N8N_JOB_RECOMMENDATION_WORKFLOW_ID: str = "job-recommendation"
    N8N_CANDIDATE_MATCHING_WORKFLOW_ID: str = "candidate-matching"
    N8N_RESUME_PARSING_WORKFLOW_ID: str = "resume-parsing"
    N8N_EMAIL_NOTIFICATION_WORKFLOW_ID: str = "email-notification"
    
    # SMTP (Optional - for email notifications)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    SMTP_FROM_NAME: str = "JobPortal"
    
    # Application
    APP_NAME: str = "JobPortal"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: str = "pdf,doc,docx"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse allowed file extensions from comma-separated string."""
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]


# Global settings instance
settings = Settings()


