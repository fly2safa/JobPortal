"""
Integrations module for external services.

This module provides integrations with:
- n8n workflow automation
- Other third-party services
"""
from app.integrations.n8n_client import get_n8n_client, N8nClient

__all__ = ["get_n8n_client", "N8nClient"]


