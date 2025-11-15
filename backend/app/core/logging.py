"""
Structured logging configuration.
"""
import logging
import sys
from typing import Any
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.
        
        Args:
            record: Log record to format
            
        Returns:
            JSON formatted log string
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        return json.dumps(log_data)


def setup_logging(level: str = "INFO") -> None:
    """
    Configure application logging with centralized control.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Convert string level to logging constant first
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create console handler with a filter to enforce the level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    
    # Add a filter to strictly enforce the log level
    class LevelFilter(logging.Filter):
        def __init__(self, level):
            self.level = level
            
        def filter(self, record):
            return record.levelno >= self.level
    
    console_handler.addFilter(LevelFilter(numeric_level))
    
    # Use JSON formatter for production, simple formatter for development
    from app.core.config import settings
    
    if settings.DEBUG:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    else:
        formatter = JSONFormatter()
    
    console_handler.setFormatter(formatter)
    
    # Configure root logger to use the specified level
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)  # Set to user's LOG_LEVEL
    root_logger.addHandler(console_handler)
    
    # =========================================================================
    # CENTRALIZED LOGGING CONTROL - Silence noisy third-party libraries
    # ========================================================================='
    
    # Uvicorn (HTTP server logs) - controlled by UVICORN_LOG_LEVEL
    uvicorn_level = getattr(logging, settings.UVICORN_LOG_LEVEL.upper(), logging.INFO)
    logging.getLogger("uvicorn").setLevel(uvicorn_level)
    logging.getLogger("uvicorn.access").setLevel(uvicorn_level)  # HTTP request logs (200 OK, etc.)
    logging.getLogger("uvicorn.error").setLevel(uvicorn_level)
    
    # FastAPI
    logging.getLogger("fastapi").setLevel(max(numeric_level, logging.WARNING))
    
    # HTTP clients
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    # AI/ML libraries
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("langchain").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    
    # Database
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    
    # Security/Auth
    logging.getLogger("passlib").setLevel(logging.ERROR)  # Silence bcrypt warnings
    
    # Email
    logging.getLogger("aiosmtplib").setLevel(logging.WARNING)
    
    # Other noisy libraries
    logging.getLogger("multipart").setLevel(logging.WARNING)
    logging.getLogger("charset_normalizer").setLevel(logging.WARNING)
    
    # =========================================================================
    # APPLICATION LOGGERS - Respect LOG_LEVEL setting
    # =========================================================================
    # Application loggers will use the configured LOG_LEVEL
    # If LOG_LEVEL=WARNING, only WARNING and above will be shown from app code
    logging.getLogger("app").setLevel(numeric_level)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)







