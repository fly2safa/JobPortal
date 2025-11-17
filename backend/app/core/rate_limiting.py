"""
Rate limiting utilities for FastAPI endpoints.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Create a global limiter instance
# Note: slowapi decorators will look for app.state.limiter at runtime
# This limiter instance is attached to app.state in main.py
limiter = Limiter(key_func=get_remote_address, default_limits=[], headers_enabled=True)

# Rate limit strings for different endpoint types
# Format: "number/period" where period can be: second, minute, hour, day
RATE_LIMIT_AUTH = f"{settings.RATE_LIMIT_AUTH_PER_MINUTE}/minute"
RATE_LIMIT_JOB_POSTING = f"{settings.RATE_LIMIT_JOB_POSTING_PER_MINUTE}/minute"
RATE_LIMIT_APPLICATION = f"{settings.RATE_LIMIT_APPLICATION_PER_MINUTE}/minute"
RATE_LIMIT_AI = f"{settings.RATE_LIMIT_AI_PER_MINUTE}/minute"
RATE_LIMIT_DEFAULT = f"{settings.RATE_LIMIT_PER_MINUTE}/minute"

# Debug: Print rate limits on import (for testing)
if settings.RATE_LIMIT_ENABLED:
    print(f"🔒 Rate Limiting Enabled:")
    print(f"   Auth: {RATE_LIMIT_AUTH}")
    print(f"   Job Posting: {RATE_LIMIT_JOB_POSTING}")
    print(f"   Applications: {RATE_LIMIT_APPLICATION}")
    print(f"   AI: {RATE_LIMIT_AI}")

