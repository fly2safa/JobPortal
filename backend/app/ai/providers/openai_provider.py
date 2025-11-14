"""
OpenAI provider implementation.
"""
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.schema import BaseLanguageModel
from app.ai.providers.base import BaseAIProvider
from app.core.logging import get_logger

logger = get_logger(__name__)


class OpenAIProvider(BaseAIProvider):
    """OpenAI AI provider implementation."""
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        temperature: float = 0.3,
        **kwargs
    ):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
            model: Model name (default: gpt-4o)
            temperature: Sampling temperature (default: 0.3)
            **kwargs: Additional ChatOpenAI parameters
        """
        super().__init__(api_key, model, **kwargs)
        self.temperature = temperature
    
    def get_llm(self, **override_kwargs) -> BaseLanguageModel:
        """
        Get ChatOpenAI instance.
        
        Args:
            **override_kwargs: Override default parameters
            
        Returns:
            ChatOpenAI instance
        """
        params = {
            "model": self.model,
            "temperature": self.temperature,
            "openai_api_key": self.api_key,
            **self.kwargs,
            **override_kwargs
        }
        
        logger.debug(f"Initializing OpenAI with model: {params['model']}")
        return ChatOpenAI(**params)
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "openai"
    
    def __repr__(self) -> str:
        return f"OpenAIProvider(model={self.model}, temperature={self.temperature})"

