"""
Orchestrator - Coordinates all agents and routes requests
"""

from typing import Dict, Any, Optional
from enum import Enum
from core.llm_service import LLMService, Message
from core.memory import Memory
from core.code_sandbox import CodeSandbox
from agents.tutor_agent import TutorAgent
from agents.debug_agent import DebugAgent
from agents.assessment_agent import AssessmentAgent
from agents.motivation_agent import MotivationAgent


class AgentType(str, Enum):
    TUTOR = "tutor"
    DEBUG = "debug"
    ASSESSMENT = "assessment"
    MOTIVATION = "motivation"
    AUTO = "auto"  # Let orchestrator decide


class Orchestrator:
    """
    Orchestrator coordinates multiple agents to provide comprehensive learning support
    
    Routes user requests to appropriate agents based on:
    - Intent detection
    - Context
    - User preferences
    """
    
    def __init__(
        self,
        llm_service: LLMService,
        memory: Memory,
        code_sandbox: Optional[CodeSandbox] = None
    ):
        self.llm_service = llm_service
        self.memory = memory
        self.code_sandbox = code_sandbox or CodeSandbox()
        
        # Initialize all agents
        self.tutor = TutorAgent(llm_service, memory)
        self.debugger = DebugAgent(llm_service, memory, self.code_sandbox)
        self.assessor = AssessmentAgent(llm_service, memory, self.code_sandbox)
        self.motivator = MotivationAgent(llm_service, memory)
        
        self.agents = {
            AgentType.TUTOR: self.tutor,
            AgentType.DEBUG: self.debugger,
            AgentType.ASSESSMENT: self.assessor,
            AgentType.MOTIVATION: self.motivator
        }
    
    def process(
        self,
        user_input: str,
        agent_type: AgentType = AgentType.AUTO,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process user input with appropriate agent(s)
        
        Args:
            user_input: User's message
            agent_type: Which agent to use (AUTO for automatic detection)
            context: Additional context
            
        Returns:
            Response dictionary with agent output and metadata
        """
        # Detect intent if auto mode
        if agent_type == AgentType.AUTO:
            agent_type = self._detect_intent(user_input, context)
        
        # Get the appropriate agent
        agent = self.agents[agent_type]
        
        # Process with the agent
        response = agent.process(user_input, context)
        
        return {
            "response": response,
            "agent": agent_type.value,
            "agent_name": agent.name
        }
    
    def _detect_intent(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentType:
        """
        Detect which agent should handle the request
        
        Args:
            user_input: User's message
            context: Additional context
            
        Returns:
            Detected agent type
        """
        user_lower = user_input.lower()
        
        # Check for code blocks (likely debug or assessment)
        has_code = '```' in user_input or context and context.get('has_code')
        
        # Debug keywords
        debug_keywords = [
            'error', 'bug', 'broken', 'not working', 'wrong output',
            'debug', 'fix', 'mistake', 'traceback', 'exception'
        ]
        if any(keyword in user_lower for keyword in debug_keywords):
            return AgentType.DEBUG
        
        # Assessment keywords
        assessment_keywords = [
            'quiz', 'test', 'exercise', 'practice', 'challenge',
            'evaluate', 'check my', 'review my code', 'assessment'
        ]
        if any(keyword in user_lower for keyword in assessment_keywords):
            return AgentType.ASSESSMENT
        
        # Motivation keywords
        motivation_keywords = [
            'frustrated', 'stuck', 'giving up', 'progress', 'motivation',
            'difficult', 'hard', 'confused', 'don\'t understand', 'help!',
            'yay', 'got it', 'solved', 'figured out'
        ]
        if any(keyword in user_lower for keyword in motivation_keywords):
            return AgentType.MOTIVATION
        
        # Learning/teaching keywords (default to tutor)
        tutor_keywords = [
            'explain', 'what is', 'how do', 'teach me', 'learn',
            'understand', 'why', 'example', 'show me'
        ]
        if any(keyword in user_lower for keyword in tutor_keywords):
            return AgentType.TUTOR
        
        # If code is present but no clear debug intent, might be for assessment
        if has_code:
            return AgentType.DEBUG
        
        # Default to tutor for general questions
        return AgentType.TUTOR
    
    def chat(self, user_input: str) -> str:
        """
        Simple chat interface
        
        Args:
            user_input: User message
            
        Returns:
            Agent response
        """
        result = self.process(user_input)
        return result["response"]
    
    def explain(self, concept: str, detail_level: str = "medium") -> str:
        """Explain a concept using tutor agent"""
        return self.tutor.explain_concept(concept, detail_level)
    
    def debug_code(self, code: str, hint_level: int = 1) -> str:
        """Debug code using debug agent"""
        return self.debugger.analyze_error(code, hint_level=hint_level)
    
    def create_quiz(self, topic: str, difficulty: str = "beginner") -> str:
        """Create quiz using assessment agent"""
        return self.assessor.create_quiz(topic, difficulty)
    
    def explain_concept(self, concept: str, detail_level: str = "medium") -> str:
        """Explain a concept using tutor agent with examples"""
        return self.tutor.process(concept)
    
    def evaluate_code(self, problem: str, code: str) -> Dict[str, Any]:
        """Evaluate code submission"""
        return self.assessor.evaluate_code(problem, code)
    
    def celebrate(self, achievement: str) -> str:
        """Celebrate achievement using motivation agent"""
        return self.motivator.celebrate_achievement(achievement)
    
    def get_progress_update(self) -> str:
        """Get progress update"""
        return self.motivator.provide_progress_update()
    
    def multi_agent_response(
        self,
        user_input: str,
        agent_types: list[AgentType]
    ) -> Dict[str, str]:
        """
        Get responses from multiple agents
        
        Args:
            user_input: User message
            agent_types: List of agents to consult
            
        Returns:
            Dictionary of agent responses
        """
        responses = {}
        for agent_type in agent_types:
            agent = self.agents[agent_type]
            responses[agent_type.value] = agent.process(user_input)
        return responses
    
    def smart_assist(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Intelligent assistance that may involve multiple agents
        
        Args:
            user_input: User's request
            context: Additional context
            
        Returns:
            Comprehensive response with multiple perspectives if needed
        """
        # Primary agent response
        primary_result = self.process(user_input, AgentType.AUTO, context)
        primary_agent = AgentType(primary_result["agent"])
        
        result = {
            "primary_response": primary_result["response"],
            "primary_agent": primary_agent.value,
            "additional_support": {}
        }
        
        # Add motivational support if user seems frustrated
        if primary_agent == AgentType.DEBUG:
            # Debugging can be frustrating, add encouragement
            encouragement = self.motivator.process(
                "I'm working on debugging some code",
                context={"situation": "debugging"}
            )
            result["additional_support"]["encouragement"] = encouragement
        
        # Add assessment suggestion if learning a concept
        if primary_agent == AgentType.TUTOR:
            profile = self.memory.get_user_profile()
            if profile and profile.current_topic:
                # Suggest practice
                practice_hint = "Would you like to practice this with a coding challenge?"
                result["additional_support"]["practice_suggestion"] = practice_hint
        
        return result
