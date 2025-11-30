"""
LLM Service - Unified interface for OpenAI, Anthropic, and Google Gemini
"""

import os
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"  # FREE tier available!


class Message(BaseModel):
    role: str
    content: str


class LLMService:
    """Unified LLM service supporting multiple providers"""
    
    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        self.provider = provider or os.getenv("LLM_PROVIDER", "gemini")  # Default to FREE Gemini!
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if self.provider == LLMProvider.OPENAI:
            import openai
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = model or os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
        elif self.provider == LLMProvider.ANTHROPIC:
            import anthropic
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = model or os.getenv("MODEL_NAME", "claude-3-sonnet-20240229")
        elif self.provider == LLMProvider.GEMINI:
            import google.generativeai as genai
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found. Get a free key at: https://makersuite.google.com/app/apikey")
            genai.configure(api_key=api_key)
            self.model = model or os.getenv("MODEL_NAME", "gemini-2.5-flash")  # Free tier model
            self.client = genai.GenerativeModel(self.model)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate a response from the LLM
        
        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Generated text response
        """
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        if self.provider == LLMProvider.OPENAI:
            return self._generate_openai(messages, system_prompt, temp, tokens, **kwargs)
        elif self.provider == LLMProvider.ANTHROPIC:
            return self._generate_anthropic(messages, system_prompt, temp, tokens, **kwargs)
        elif self.provider == LLMProvider.GEMINI:
            return self._generate_gemini(messages, system_prompt, temp, tokens, **kwargs)
    
    def _generate_openai(
        self,
        messages: List[Message],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using OpenAI API"""
        formatted_messages = []
        
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        
        formatted_messages.extend([
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ])
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def _generate_anthropic(
        self,
        messages: List[Message],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using Anthropic API"""
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt if system_prompt else "",
            messages=formatted_messages,
            **kwargs
        )
        
        return response.content[0].text
    
    def _generate_gemini(
        self,
        messages: List[Message],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using Google Gemini API"""
        import google.generativeai as genai
        
        # Configure generation settings
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        
        # Build conversation history for Gemini
        # Gemini expects alternating user/model messages
        chat_history = []
        
        for msg in messages[:-1]:  # All except last message
            if msg.role == "user":
                chat_history.append({
                    "role": "user",
                    "parts": [msg.content]
                })
            elif msg.role == "assistant":
                chat_history.append({
                    "role": "model",
                    "parts": [msg.content]
                })
        
        # Start chat with history
        chat = self.client.start_chat(history=chat_history)
        
        # Prepare the final message
        final_message = messages[-1].content
        
        # Prepend system prompt if provided
        if system_prompt:
            final_message = f"{system_prompt}\n\n{final_message}"
        
        # Generate response
        response = chat.send_message(
            final_message,
            generation_config=generation_config
        )
        
        return response.text
    
    async def agenerate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Async version of generate (placeholder for future implementation)"""
        # For now, just call the sync version
        # TODO: Implement true async calls
        return self.generate(messages, system_prompt, temperature, max_tokens, **kwargs)
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text
        
        Args:
            text: Input text
            
        Returns:
            Estimated token count
        """
        if self.provider == LLMProvider.OPENAI:
            import tiktoken
            try:
                encoding = tiktoken.encoding_for_model(self.model)
            except KeyError:
                encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        elif self.provider == LLMProvider.GEMINI:
            # Gemini has built-in token counting
            try:
                return self.client.count_tokens(text).total_tokens
            except:
                # Fallback estimate
                return len(text) // 4
        else:
            # Rough estimate for Anthropic and others: ~4 chars per token
            return len(text) // 4


# Convenience function
def create_llm_service(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    **kwargs
) -> LLMService:
    """Create and return an LLM service instance"""
    return LLMService(provider=provider, model=model, **kwargs)
