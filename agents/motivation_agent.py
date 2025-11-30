"""
Motivation Agent - Keeps learners engaged and encouraged
"""

from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from core.llm_service import LLMService
from core.memory import Memory
from datetime import datetime


class MotivationAgent(BaseAgent):
    """
    Motivation Agent specializes in:
    - Keeping learners engaged
    - Providing encouragement
    - Celebrating achievements
    - Helping overcome frustration
    - Setting achievable goals
    """
    
    SYSTEM_PROMPT = """You are an encouraging learning coach focused on motivation and emotional support.

Your mission:
1. **Celebrate Progress**: Acknowledge every achievement, no matter how small
2. **Reframe Setbacks**: Help learners see mistakes as learning opportunities
3. **Build Confidence**: Remind them of their capabilities and progress
4. **Maintain Energy**: Keep the learning experience positive and engaging
5. **Personal Connection**: Show empathy and understanding

When learners are:
- **Frustrated**: Validate their feelings, remind them it's normal, suggest a break or different approach
- **Stuck**: Encourage persistence, break the problem down, celebrate trying
- **Succeeding**: Enthusiastically celebrate, highlight what they did well
- **Losing Interest**: Re-engage with fun facts, real-world applications, or new challenges

Motivational strategies:
- Use specific praise ("Great job handling that edge case!")
- Share relatable experiences ("Even senior developers Google syntax!")
- Break goals into micro-achievements
- Gamify progress with milestones
- Connect learning to their personal goals

ADHD-specific support:
- Quick wins and frequent positive feedback
- Variety and novelty in examples
- Break sessions into 5-10 minute chunks
- Celebrate focus and completion

Remember:
- Growth mindset: abilities can be developed
- Effort and progress matter more than perfection
- Every expert was once a beginner
- You're here to support their journey"""
    
    def __init__(
        self,
        llm_service: LLMService,
        memory: Memory
    ):
        super().__init__(
            name="Motivator",
            llm_service=llm_service,
            memory=memory,
            system_prompt=self.SYSTEM_PROMPT
        )
    
    def process(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process motivation-related interaction
        
        Args:
            user_input: User's message or situation
            context: Additional context
            
        Returns:
            Motivational response
        """
        messages = self._build_messages(user_input, include_history=True, history_count=3)
        
        response = self.llm_service.generate(
            messages=messages,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.8,  # Higher temperature for more varied, engaging responses
            max_tokens=800
        )
        
        self.memory.add_message("user", user_input, agent_type="motivation")
        self.memory.add_message("assistant", response, agent_type="motivation")
        
        return response
    
    def celebrate_achievement(
        self,
        achievement: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Celebrate a learner's achievement
        
        Args:
            achievement: What they accomplished
            context: Additional context about the achievement
            
        Returns:
            Celebratory message
        """
        prompt = f"I just {achievement}!"
        
        if context and context.get('difficulty') == 'hard':
            prompt += " This was really challenging for me."
        
        return self.process(prompt)
    
    def handle_frustration(
        self,
        situation: str,
        attempts: int = 1
    ) -> str:
        """
        Help learner deal with frustration
        
        Args:
            situation: What's causing frustration
            attempts: How many times they've tried
            
        Returns:
            Supportive response
        """
        prompt = f"I'm frustrated. I've tried {attempts} times and {situation}"
        return self.process(prompt)
    
    def suggest_break(self, session_duration: float) -> str:
        """
        Suggest taking a break
        
        Args:
            session_duration: How long they've been working (minutes)
            
        Returns:
            Break suggestion
        """
        prompt = f"I've been working for {session_duration:.0f} minutes. Should I take a break?"
        return self.process(prompt)
    
    def provide_progress_update(self) -> str:
        """
        Provide encouraging progress update based on learning history
        
        Returns:
            Progress summary with encouragement
        """
        context = self.get_user_context()
        profile = self.memory.get_user_profile()
        
        if not profile:
            return "Welcome to your coding journey! Every expert started exactly where you are now. Let's begin! 🚀"
        
        # Calculate session time
        session_time = (datetime.now() - self.memory.session_start).total_seconds() / 60
        
        # Get metrics
        all_metrics = self.memory.get_all_metrics()
        strong_topics = context.get('strong_topics', [])
        
        prompt = f"""I've completed {len(profile.topics_completed)} topics and practiced for {profile.total_practice_time:.1f} minutes total. 

In this session: {session_time:.0f} minutes
Topics I'm strong in: {', '.join(strong_topics) if strong_topics else 'building skills'}
Total practice areas: {len(all_metrics)}

Give me an encouraging progress update!"""
        
        return self.process(prompt)
    
    def set_goal(self, goal: str) -> str:
        """
        Help set an achievable learning goal
        
        Args:
            goal: The goal they want to achieve
            
        Returns:
            Goal-setting guidance
        """
        prompt = f"I want to achieve this goal: {goal}. Help me break it down into achievable steps."
        return self.process(prompt)
    
    def detect_emotion_from_message(self, message: str) -> str:
        """
        Detect emotional state from message and respond appropriately
        
        Args:
            message: User's message
            
        Returns:
            Emotion-aware response
        """
        # Simple keyword detection
        frustration_keywords = ['frustrated', 'stuck', 'confused', 'don\'t understand', 'giving up']
        excitement_keywords = ['got it', 'works', 'solved', 'figured out', 'yay', 'yes!']
        
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in frustration_keywords):
            return self.handle_frustration(message)
        elif any(keyword in message_lower for keyword in excitement_keywords):
            return self.celebrate_achievement(message)
        else:
            return self.process(message)
    
    def provide_fun_fact(self, topic: str) -> str:
        """
        Share an interesting/fun fact about a programming topic
        
        Args:
            topic: Programming topic
            
        Returns:
            Fun fact to re-engage interest
        """
        prompt = f"Share a fun or interesting fact about {topic} to make learning more engaging!"
        return self.process(prompt)
    
    def suggest_next_step(self) -> str:
        """
        Suggest what to learn next based on progress
        
        Returns:
            Suggestion for next learning step
        """
        context = self.get_user_context()
        current = context.get('current_topic', 'programming basics')
        strong = context.get('strong_topics', [])
        
        prompt = f"I've been working on {current}. I'm comfortable with: {', '.join(strong) if strong else 'the basics'}. What should I learn next?"
        return self.process(prompt)
