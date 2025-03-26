"""
Module for summarizing text using various LLM providers.
"""

import os
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
import ollama


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        """
        Summarize the given text.
        
        Args:
            text: The text to summarize
            max_length: Optional maximum length for the summary
            
        Returns:
            The summarized text
        """
        pass


class OllamaProvider(LLMProvider):
    """Provider for local Ollama models."""
    
    def __init__(self, model_name: str = "llama3.2"):
        """
        Initialize the Ollama provider.
        
        Args:
            model_name: The name of the Ollama model to use
        """
        self.model_name = model_name
    
    def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        """
        Summarize the given text using a local Ollama model.
        
        Args:
            text: The text to summarize
            max_length: Optional maximum length for the summary
            
        Returns:
            The summarized text
        """
        # Prepare the prompt
        prompt = f"""Please provide a concise summary of the following transcript.
Focus on the main points and key insights.

TRANSCRIPT:
{text}

SUMMARY:"""

        if max_length:
            prompt += f"\n(Please keep the summary under {max_length} words)"
        
        # Generate the summary
        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            options={
                "temperature": 0.3,
                "num_predict": 1000,
            }
        )
        
        return response['response'].strip()


class OpenAIProvider(LLMProvider):
    """Provider for OpenAI models (requires API key)."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        """
        Initialize the OpenAI provider.
        
        Args:
            model_name: The name of the OpenAI model to use
            api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass explicitly.")
        
        # Defer importing to avoid dependency if not using this provider
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("OpenAI package is required for OpenAIProvider. Install with 'poetry add openai'.")
    
    def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        """
        Summarize the given text using OpenAI's API.
        
        Args:
            text: The text to summarize
            max_length: Optional maximum length for the summary
            
        Returns:
            The summarized text
        """
        # Prepare the system message
        system_message = "You are a helpful assistant that summarizes transcripts concisely."
        
        # Prepare the user message
        user_message = f"Please summarize the following transcript:\n\n{text}"
        if max_length:
            user_message += f"\n\nKeep the summary under {max_length} words."
        
        # Generate the summary
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()


class AnthropicProvider(LLMProvider):
    """Provider for Anthropic Claude models (requires API key)."""
    
    def __init__(self, model_name: str = "claude-3-haiku-20240307", api_key: Optional[str] = None):
        """
        Initialize the Anthropic provider.
        
        Args:
            model_name: The name of the Anthropic model to use
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY environment variable)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable or pass explicitly.")
        
        # Defer importing to avoid dependency if not using this provider
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("Anthropic package is required for AnthropicProvider. Install with 'poetry add anthropic'.")
    
    def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        """
        Summarize the given text using Anthropic's API.
        
        Args:
            text: The text to summarize
            max_length: Optional maximum length for the summary
            
        Returns:
            The summarized text
        """
        # Prepare the prompt
        system_message = "Summarize the provided transcript concisely, focusing on key points and insights."
        
        user_message = f"Here is the transcript to summarize:\n\n{text}"
        if max_length:
            user_message += f"\n\nKeep the summary under {max_length} words."
        
        # Generate the summary
        response = self.client.messages.create(
            model=self.model_name,
            system=system_message,
            max_tokens=1000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        return response.content[0].text.strip()


def get_provider(provider_name: str = None, **kwargs) -> LLMProvider:
    """
    Factory function to get the appropriate LLM provider.
    
    Args:
        provider_name: The name of the provider to use (defaults to SUMMARY_PROVIDER env var or 'ollama')
        **kwargs: Additional arguments to pass to the provider constructor
        
    Returns:
        An instance of the requested LLM provider
    """
    provider_name = provider_name or os.getenv("SUMMARY_PROVIDER", "ollama").lower()
    
    if provider_name == "ollama":
        model_name = kwargs.get("model_name") or os.getenv("OLLAMA_MODEL", "llama3.2")
        return OllamaProvider(model_name=model_name)
    
    elif provider_name == "openai":
        model_name = kwargs.get("model_name") or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        api_key = kwargs.get("api_key") or os.getenv("OPENAI_API_KEY")
        return OpenAIProvider(model_name=model_name, api_key=api_key)
    
    elif provider_name == "anthropic":
        model_name = kwargs.get("model_name") or os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
        api_key = kwargs.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
        return AnthropicProvider(model_name=model_name, api_key=api_key)
    
    else:
        raise ValueError(f"Unknown provider: {provider_name}")


def summarize_text(text: str, provider_name: str = None, max_length: Optional[int] = None, **kwargs) -> str:
    """
    Summarize the given text using the specified provider.
    
    Args:
        text: The text to summarize
        provider_name: The name of the provider to use
        max_length: Optional maximum length for the summary
        **kwargs: Additional arguments to pass to the provider
        
    Returns:
        The summarized text
    """
    provider = get_provider(provider_name, **kwargs)
    return provider.summarize(text, max_length)
