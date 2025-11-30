"""
Base Agent Class - Foundation for all specialized agents
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from core.llm_service import LLMService, Message
from core.memory import Memory


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system
    """
    
    def __init__(
        self,
        name: str,
        llm_service: LLMService,
        memory: Memory,
        system_prompt: str = ""
    ):
        self.name = name
        self.llm_service = llm_service
        self.memory = memory
        self.system_prompt = system_prompt
    
    @abstractmethod
    def process(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process user input and return response
        
        Args:
            user_input: User's message
            context: Additional context information
            
        Returns:
            Agent's response
        """
        pass
    
    def _build_messages(
        self,
        user_input: str,
        include_history: bool = True,
        history_count: int = 5
    ) -> List[Message]:
        """
        Build message list for LLM including history
        
        Args:
            user_input: Current user input
            include_history: Whether to include conversation history
            history_count: Number of historical messages to include
            
        Returns:
            List of Message objects
        """
        messages = []
        
        if include_history:
            history = self.memory.get_conversation_history(last_n=history_count * 2)
            for msg in history:
                messages.append(Message(role=msg.role, content=msg.content))
        
        messages.append(Message(role="user", content=user_input))
        return messages
    
    def _generate_response(
        self,
        messages: List[Message],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response using LLM
        
        Args:
            messages: Conversation messages
            temperature: Temperature for generation
            max_tokens: Maximum tokens
            
        Returns:
            Generated response
        """
        return self.llm_service.generate(
            messages=messages,
            system_prompt=self.system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def get_user_context(self) -> Dict[str, Any]:
        """Get relevant user context from memory"""
        context = {}
        
        profile = self.memory.get_user_profile()
        if profile:
            context['learning_style'] = profile.learning_style
            context['pace'] = profile.pace_preference
            context['current_language'] = profile.current_language
            context['accessibility_needs'] = profile.accessibility_needs
            context['current_topic'] = profile.current_topic
        
        # Get learning metrics
        weak_topics = self.memory.get_weak_topics()
        strong_topics = self.memory.get_strong_topics()
        
        context['weak_topics'] = weak_topics
        context['strong_topics'] = strong_topics
        
        return context
