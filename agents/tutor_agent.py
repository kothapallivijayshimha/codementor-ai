"""
Tutor Agent - Main teaching agent for explaining concepts
"""

from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from core.llm_service import LLMService, Message
from core.memory import Memory


class TutorAgent(BaseAgent):
    """
    Tutor Agent specializes in:
    - Explaining programming concepts
    - Providing examples
    - Breaking down complex topics
    - Adapting to learning styles
    """
    
    SYSTEM_PROMPT = """You are CodeMentor, an expert programming tutor specialized in teaching neurodivergent learners and beginners.

Your teaching approach:
1. **Clarity First**: Use simple, clear language. Avoid jargon unless explaining it.
2. **Visual Learning**: Provide analogies, metaphors, and real-world examples.
3. **Incremental Steps**: Break complex concepts into small, digestible pieces.
4. **Patient & Encouraging**: Celebrate small wins, never make learners feel inadequate.
5. **Adaptive**: Adjust your teaching style based on the learner's preferences.
6. **Hands-On**: ALWAYS include at least 2 practical code examples.

IMPORTANT: When explaining concepts, ALWAYS include:
- A clear, simple explanation
- At least 2 practical code examples with comments
- Real-world use cases
- Common mistakes to avoid

For ADHD learners:
- Keep explanations concise and focused
- Use bullet points and clear structure
- Provide frequent summaries
- Include engaging examples

For dyslexic learners:
- Use clear, simple sentences
- Avoid complex terminology
- Provide visual diagrams when possible
- Use consistent formatting

For autism spectrum learners:
- Be explicit and literal
- Provide clear, step-by-step instructions
- Give concrete examples
- Explain the "why" behind concepts

Always:
- Ask if the explanation makes sense
- Offer to explain in a different way if needed
- Provide code examples when relevant
- Encourage questions"""
    
    def __init__(
        self,
        llm_service: LLMService,
        memory: Memory
    ):
        super().__init__(
            name="Tutor",
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
        Process user's learning request
        
        Args:
            user_input: User's question or request
            context: Additional context (topic, difficulty, etc.)
            
        Returns:
            Teaching response
        """
        # Get user context for personalization
        user_context = self.get_user_context()
        
        # Enhance system prompt with user context
        enhanced_prompt = self._enhance_prompt_with_context(user_context, context)
        
        # Build messages
        messages = self._build_messages(user_input, include_history=True, history_count=5)
        
        # Generate response
        response = self.llm_service.generate(
            messages=messages,
            system_prompt=enhanced_prompt,
            temperature=0.7,
            max_tokens=1500
        )
        
        # Store in memory
        self.memory.add_message("user", user_input, agent_type="tutor")
        self.memory.add_message("assistant", response, agent_type="tutor")
        
        return response
    
    def _enhance_prompt_with_context(
        self,
        user_context: Dict[str, Any],
        request_context: Optional[Dict[str, Any]]
    ) -> str:
        """Enhance system prompt with user-specific context"""
        
        enhanced = self.SYSTEM_PROMPT
        
        # Add learning style guidance
        if user_context.get('learning_style'):
            style = user_context['learning_style']
            if style == 'visual':
                enhanced += "\n\nThis learner is VISUAL - use diagrams, analogies, and visual metaphors."
            elif style == 'auditory':
                enhanced += "\n\nThis learner is AUDITORY - use verbal explanations, talk through concepts."
            elif style == 'kinesthetic':
                enhanced += "\n\nThis learner is KINESTHETIC - provide hands-on exercises and interactive examples."
        
        # Add pace preference
        if user_context.get('pace'):
            pace = user_context['pace']
            if pace == 'slow':
                enhanced += "\n\nTeach at a SLOW pace with extra detail and repetition."
            elif pace == 'fast':
                enhanced += "\n\nThis learner prefers a FASTER pace - be concise but thorough."
        
        # Add accessibility needs
        if user_context.get('accessibility_needs'):
            needs = user_context['accessibility_needs']
            if 'adhd' in needs:
                enhanced += "\n\nLearner has ADHD - keep responses focused and structured."
            if 'dyslexia' in needs:
                enhanced += "\n\nLearner has dyslexia - use simple sentences and clear formatting."
            if 'autism' in needs:
                enhanced += "\n\nLearner is on autism spectrum - be explicit and literal."
        
        # Add current topic context
        if user_context.get('current_topic'):
            enhanced += f"\n\nCurrent topic focus: {user_context['current_topic']}"
        
        # Add weak topics for targeted support
        if user_context.get('weak_topics'):
            weak = ', '.join(user_context['weak_topics'][:3])
            enhanced += f"\n\nTopics needing more practice: {weak}"
        
        return enhanced
    
    def explain_concept(
        self,
        concept: str,
        detail_level: str = "medium"
    ) -> str:
        """
        Explain a specific programming concept
        
        Args:
            concept: The concept to explain
            detail_level: 'simple', 'medium', or 'detailed'
            
        Returns:
            Explanation
        """
        prompt = f"Explain {concept} in programming"
        
        if detail_level == "simple":
            prompt += " in the simplest way possible, as if explaining to a complete beginner."
        elif detail_level == "detailed":
            prompt += " in detail, covering all important aspects and edge cases."
        
        return self.process(prompt)
    
    def provide_example(
        self,
        concept: str,
        language: str = "python"
    ) -> str:
        """
        Provide a code example for a concept
        
        Args:
            concept: The concept to demonstrate
            language: Programming language
            
        Returns:
            Code example with explanation
        """
        prompt = f"Show me a clear code example of {concept} in {language}, with explanatory comments."
        return self.process(prompt)
