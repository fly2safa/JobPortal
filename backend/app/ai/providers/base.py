"""
Base abstract class for AI providers.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain_core.language_models import BaseLanguageModel


class BaseAIProvider(ABC):
    """Abstract base class for AI providers."""
    
    def __init__(self, api_key: str, model: str, **kwargs):
        """
        Initialize the AI provider.
        
        Args:
            api_key: API key for the provider
            model: Model name to use
            **kwargs: Additional provider-specific parameters
        """
        self.api_key = api_key
        self.model = model
        self.kwargs = kwargs
    
    @abstractmethod
    def get_llm(self, **override_kwargs) -> BaseLanguageModel:
        """
        Get the LangChain LLM instance.
        
        Args:
            **override_kwargs: Override default parameters
            
        Returns:
            LangChain BaseLanguageModel instance
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the provider name.
        
        Returns:
            Provider name (e.g., "openai", "anthropic")
        """
        pass
    
    def test_connection(self) -> bool:
        """
        Test if the provider is accessible.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            llm = self.get_llm()
            # Try a simple completion
            llm.invoke("test")
            return True
        except Exception:
            return False

