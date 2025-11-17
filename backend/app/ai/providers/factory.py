"""
AI Provider Factory with automatic fallback support.
"""
from typing import Optional
from langchain_core.language_models import BaseLanguageModel
from app.core.config import settings
from app.core.logging import get_logger
from app.ai.providers.base import BaseAIProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.anthropic_provider import AnthropicProvider

logger = get_logger(__name__)


class ProviderError(Exception):
    """Raised when all AI providers fail."""
    pass


class AIProviderFactory:
    """Factory for creating AI providers with automatic fallback."""
    
    @staticmethod
    def _has_api_key(provider: str) -> bool:
        """Check if API key exists for a provider."""
        if provider == "openai":
            return settings.OPENAI_API_KEY is not None and settings.OPENAI_API_KEY != ""
        elif provider == "anthropic":
            return settings.ANTHROPIC_API_KEY is not None and settings.ANTHROPIC_API_KEY != ""
        return False
    
    @staticmethod
    def _create_provider(provider: str) -> BaseAIProvider:
        """
        Create a provider instance.
        
        Args:
            provider: Provider name ("openai" or "anthropic")
            
        Returns:
            BaseAIProvider instance
            
        Raises:
            ValueError: If provider is invalid or API key is missing
        """
        if provider == "openai":
            if not AIProviderFactory._has_api_key("openai"):
                raise ValueError("OpenAI API key not configured")
            return OpenAIProvider(
                api_key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_MODEL
            )
        elif provider == "anthropic":
            if not AIProviderFactory._has_api_key("anthropic"):
                raise ValueError("Anthropic API key not configured")
            return AnthropicProvider(
                api_key=settings.ANTHROPIC_API_KEY,
                model=settings.ANTHROPIC_MODEL
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    @staticmethod
    def _get_fallback_provider(primary: str) -> Optional[str]:
        """
        Get fallback provider name.
        
        Args:
            primary: Primary provider name
            
        Returns:
            Fallback provider name or None
        """
        if not settings.AI_FALLBACK_ENABLED:
            return None
        
        # Determine fallback
        fallback = "anthropic" if primary == "openai" else "openai"
        
        # Check if fallback has API key
        if AIProviderFactory._has_api_key(fallback):
            return fallback
        
        return None
    
    @staticmethod
    def get_llm(**override_kwargs) -> BaseLanguageModel:
        """
        Get LLM with automatic fallback support (Option 1).
        
        This method implements automatic fallback:
        1. Try primary provider (from settings.AI_PROVIDER)
        2. If primary fails and fallback is enabled:
           - Automatically try fallback provider
        3. If both fail, raise ProviderError
        
        Args:
            **override_kwargs: Override default LLM parameters
            
        Returns:
            LangChain BaseLanguageModel instance
            
        Raises:
            ProviderError: If all providers fail
        """
        primary = settings.AI_PROVIDER
        fallback = AIProviderFactory._get_fallback_provider(primary)
        
        # Try primary provider
        try:
            provider = AIProviderFactory._create_provider(primary)
            llm = provider.get_llm(**override_kwargs)
            logger.info(f"✅ Using primary AI provider: {primary} (model: {provider.model})")
            
            if fallback:
                logger.info(f"🔄 Fallback available: {fallback}")
            
            return llm
            
        except Exception as e:
            logger.warning(f"⚠️ Primary provider '{primary}' failed: {e}")
            
            # Try fallback if available
            if fallback:
                try:
                    provider = AIProviderFactory._create_provider(fallback)
                    llm = provider.get_llm(**override_kwargs)
                    logger.warning(f"🔄 Switched to fallback provider: {fallback} (model: {provider.model})")
                    return llm
                    
                except Exception as fallback_error:
                    logger.error(f"❌ Fallback provider '{fallback}' also failed: {fallback_error}")
                    raise ProviderError(
                        f"All AI providers failed. Primary ({primary}): {e}. "
                        f"Fallback ({fallback}): {fallback_error}"
                    )
            else:
                # No fallback available
                logger.error(f"❌ No fallback provider available")
                raise ProviderError(
                    f"Primary AI provider '{primary}' failed and no fallback configured. "
                    f"Error: {e}"
                )
    
    @staticmethod
    def get_provider_info() -> dict:
        """
        Get information about configured providers.
        
        Returns:
            Dictionary with provider configuration info
        """
        return {
            "primary": settings.AI_PROVIDER,
            "fallback_enabled": settings.AI_FALLBACK_ENABLED,
            "openai_configured": AIProviderFactory._has_api_key("openai"),
            "anthropic_configured": AIProviderFactory._has_api_key("anthropic"),
            "fallback_available": AIProviderFactory._get_fallback_provider(settings.AI_PROVIDER) is not None
        }


# Convenience function for backward compatibility
def get_llm(**kwargs) -> BaseLanguageModel:
    """
    Get LLM instance with automatic fallback.
    
    This is the main entry point for getting an LLM throughout the application.
    
    Args:
        **kwargs: Override default LLM parameters
        
    Returns:
        LangChain BaseLanguageModel instance
    """
    return AIProviderFactory.get_llm(**kwargs)

