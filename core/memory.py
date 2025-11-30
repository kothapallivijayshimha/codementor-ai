"""
Memory Management - User context, learning history, and knowledge tracking
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
import json


class ConversationMessage(BaseModel):
    """Single message in conversation history"""
    role: str
    content: str
    timestamp: datetime = datetime.now()
    agent_type: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LearningMetric(BaseModel):
    """Track learning progress for a specific topic"""
    topic: str
    skill_level: float  # 0.0 to 1.0
    last_practiced: datetime
    practice_count: int = 0
    success_rate: float = 0.0
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserProfile(BaseModel):
    """User profile with learning preferences and history"""
    user_id: str
    name: Optional[str] = None  # User's display name
    learning_style: str = "balanced"  # visual, auditory, kinesthetic, balanced
    pace_preference: str = "moderate"  # slow, moderate, fast
    current_language: str = "python"
    accessibility_needs: List[str] = []
    topics_completed: List[str] = []
    current_topic: Optional[str] = None
    total_practice_time: float = 0.0
    joined_date: datetime = datetime.now()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Memory:
    """
    Memory management system for CodeMentor AI
    
    Handles:
    - Conversation history
    - User profiles
    - Learning metrics
    - Context retrieval
    """
    
    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self.conversation_history: List[ConversationMessage] = []
        self.user_profile: Optional[UserProfile] = None
        self.learning_metrics: Dict[str, LearningMetric] = {}
        self.session_start = datetime.now()
    
    def add_message(
        self,
        role: str,
        content: str,
        agent_type: Optional[str] = None
    ) -> None:
        """Add a message to conversation history"""
        message = ConversationMessage(
            role=role,
            content=content,
            agent_type=agent_type
        )
        self.conversation_history.append(message)
        
        # Trim history if needed
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def get_conversation_history(
        self,
        last_n: Optional[int] = None
    ) -> List[ConversationMessage]:
        """Get conversation history"""
        if last_n:
            return self.conversation_history[-last_n:]
        return self.conversation_history
    
    def get_context_messages(
        self,
        last_n: int = 10
    ) -> List[Dict[str, str]]:
        """Get recent messages formatted for LLM context"""
        recent = self.conversation_history[-last_n:]
        return [
            {"role": msg.role, "content": msg.content}
            for msg in recent
        ]
    
    def set_user_profile(self, profile: UserProfile) -> None:
        """Set or update user profile"""
        self.user_profile = profile
    
    def get_user_profile(self) -> Optional[UserProfile]:
        """Get user profile"""
        return self.user_profile
    
    def update_learning_metric(
        self,
        topic: str,
        success: bool,
        practice_time: float = 0.0
    ) -> None:
        """
        Update learning metrics for a topic
        
        Args:
            topic: Topic being practiced
            success: Whether the practice was successful
            practice_time: Time spent practicing (seconds)
        """
        if topic not in self.learning_metrics:
            self.learning_metrics[topic] = LearningMetric(
                topic=topic,
                skill_level=0.0,
                last_practiced=datetime.now()
            )
        
        metric = self.learning_metrics[topic]
        metric.practice_count += 1
        metric.last_practiced = datetime.now()
        
        # Update success rate
        current_success = metric.success_rate * (metric.practice_count - 1)
        new_success = current_success + (1.0 if success else 0.0)
        metric.success_rate = new_success / metric.practice_count
        
        # Update skill level based on success rate
        # Simple linear model: skill level approaches success rate
        metric.skill_level = 0.7 * metric.skill_level + 0.3 * metric.success_rate
        
        if self.user_profile:
            self.user_profile.total_practice_time += practice_time
    
    def get_learning_metric(self, topic: str) -> Optional[LearningMetric]:
        """Get learning metrics for a specific topic"""
        return self.learning_metrics.get(topic)
    
    def get_all_metrics(self) -> Dict[str, LearningMetric]:
        """Get all learning metrics"""
        return self.learning_metrics
    
    def get_weak_topics(self, threshold: float = 0.5) -> List[str]:
        """Get topics where user needs more practice"""
        return [
            topic for topic, metric in self.learning_metrics.items()
            if metric.skill_level < threshold
        ]
    
    def get_strong_topics(self, threshold: float = 0.8) -> List[str]:
        """Get topics where user is proficient"""
        return [
            topic for topic, metric in self.learning_metrics.items()
            if metric.skill_level >= threshold
        ]
    
    def clear_conversation(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
    
    def export_session(self) -> Dict[str, Any]:
        """Export current session data"""
        return {
            "session_start": self.session_start.isoformat(),
            "conversation_count": len(self.conversation_history),
            "user_profile": self.user_profile.dict() if self.user_profile else None,
            "learning_metrics": {
                topic: metric.dict()
                for topic, metric in self.learning_metrics.items()
            }
        }
    
    def save_to_json(self, filepath: str) -> None:
        """Save memory state to JSON file"""
        data = {
            "conversation_history": [msg.dict() for msg in self.conversation_history],
            "user_profile": self.user_profile.dict() if self.user_profile else None,
            "learning_metrics": {
                topic: metric.dict()
                for topic, metric in self.learning_metrics.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def load_from_json(self, filepath: str) -> None:
        """Load memory state from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Load conversation history
        self.conversation_history = [
            ConversationMessage(**msg)
            for msg in data.get("conversation_history", [])
        ]
        
        # Load user profile
        if data.get("user_profile"):
            self.user_profile = UserProfile(**data["user_profile"])
        
        # Load learning metrics
        self.learning_metrics = {
            topic: LearningMetric(**metric)
            for topic, metric in data.get("learning_metrics", {}).items()
        }


class MemoryManager:
    """Global memory manager for multiple user sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, Memory] = {}
    
    def get_or_create_session(self, user_id: str) -> Memory:
        """Get existing session or create new one"""
        if user_id not in self.sessions:
            self.sessions[user_id] = Memory()
        return self.sessions[user_id]
    
    def end_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """End a user session and return summary"""
        if user_id in self.sessions:
            session = self.sessions[user_id]
            summary = session.export_session()
            del self.sessions[user_id]
            return summary
        return None
