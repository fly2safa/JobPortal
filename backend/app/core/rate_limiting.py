"""
Rate limiting utilities for FastAPI endpoints.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Create a global limiter instance
# Routes will use this limiter, and main.py will attach it to app.state
limiter = Limiter(key_func=get_remote_address)

# Rate limit strings for different endpoint types
RATE_LIMIT_AUTH = f"{settings.RATE_LIMIT_AUTH_PER_MINUTE}/minute"
RATE_LIMIT_JOB_POSTING = f"{settings.RATE_LIMIT_JOB_POSTING_PER_MINUTE}/minute"
RATE_LIMIT_APPLICATION = f"{settings.RATE_LIMIT_APPLICATION_PER_MINUTE}/minute"
RATE_LIMIT_AI = f"{settings.RATE_LIMIT_AI_PER_MINUTE}/minute"
RATE_LIMIT_DEFAULT = f"{settings.RATE_LIMIT_PER_MINUTE}/minute"

