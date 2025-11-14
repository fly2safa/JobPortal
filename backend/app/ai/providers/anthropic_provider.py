"""
Anthropic Claude provider implementation.
"""
from typing import Optional
from langchain_anthropic import ChatAnthropic
from langchain.schema import BaseLanguageModel
from app.ai.providers.base import BaseAIProvider
from app.core.logging import get_logger

logger = get_logger(__name__)


class AnthropicProvider(BaseAIProvider):
    """Anthropic Claude AI provider implementation."""
    
    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs
    ):
        """
        Initialize Anthropic provider.
        
        Args:
            api_key: Anthropic API key
            model: Model name (default: claude-3-5-sonnet-20241022)
            temperature: Sampling temperature (default: 0.3)
            max_tokens: Maximum tokens to generate (default: 4096)
            **kwargs: Additional ChatAnthropic parameters
        """
        super().__init__(api_key, model, **kwargs)
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def get_llm(self, **override_kwargs) -> BaseLanguageModel:
        """
        Get ChatAnthropic instance.
        
        Args:
            **override_kwargs: Override default parameters
            
        Returns:
            ChatAnthropic instance
        """
        params = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "anthropic_api_key": self.api_key,
            **self.kwargs,
            **override_kwargs
        }
        
        logger.debug(f"Initializing Anthropic with model: {params['model']}")
        return ChatAnthropic(**params)
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "anthropic"
    
    def __repr__(self) -> str:
        return f"AnthropicProvider(model={self.model}, temperature={self.temperature}, max_tokens={self.max_tokens})"

