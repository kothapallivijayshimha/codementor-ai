"""
Assessment Agent - Creates quizzes and evaluates understanding
"""

from typing import Dict, Any, Optional, List
from agents.base_agent import BaseAgent
from core.llm_service import LLMService, Message
from core.memory import Memory
from core.code_sandbox import CodeSandbox
import json
import re


class AssessmentAgent(BaseAgent):
    """
    Assessment Agent specializes in:
    - Creating tailored quizzes and exercises
    - Evaluating code submissions
    - Providing constructive feedback
    - Tracking learning progress
    """
    
    SYSTEM_PROMPT = """You are an assessment expert who creates engaging, educational coding challenges.

Your approach:
1. **Fair Assessment**: Create challenges appropriate to the learner's level
2. **Clear Instructions**: Make requirements crystal clear
3. **Constructive Feedback**: Always highlight what's good AND what can improve
4. **Growth Mindset**: Frame mistakes as learning opportunities
5. **Specific Guidance**: Point out exactly what needs work

When creating assessments:
- Start with the fundamentals before advancing
- Provide clear, unambiguous requirements
- Include examples of expected input/output
- Make questions solvable with the knowledge taught
- Vary question types (multiple choice, code writing, debugging)

When evaluating submissions:
- Acknowledge correct parts first
- Explain mistakes clearly
- Suggest specific improvements
- Provide hints for next attempt if needed
- Celebrate progress and effort

Assessment types:
- **Concept Check**: Quick theoretical questions
- **Code Writing**: Write code to solve a problem
- **Debug Challenge**: Find and fix errors in code
- **Code Review**: Improve working but suboptimal code

Remember:
- Assessment is for learning, not judging
- Partial credit is valuable
- Understanding the "why" matters more than memorization"""
    
    def __init__(
        self,
        llm_service: LLMService,
        memory: Memory,
        code_sandbox: Optional[CodeSandbox] = None
    ):
        super().__init__(
            name="Assessor",
            llm_service=llm_service,
            memory=memory,
            system_prompt=self.SYSTEM_PROMPT
        )
        self.code_sandbox = code_sandbox or CodeSandbox()
    
    def process(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process assessment request
        
        Args:
            user_input: User's request or answer
            context: Additional context
            
        Returns:
            Assessment response
        """
        messages = self._build_messages(user_input, include_history=True, history_count=4)
        
        response = self.llm_service.generate(
            messages=messages,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.6,
            max_tokens=1500
        )
        
        self.memory.add_message("user", user_input, agent_type="assessment")
        self.memory.add_message("assistant", response, agent_type="assessment")
        
        return response
    
    def create_quiz(
        self,
        topic: str,
        difficulty: str = "beginner",
        num_questions: int = 3,
        question_types: Optional[List[str]] = None
    ) -> str:
        """
        Create a quiz on a specific topic
        
        Args:
            topic: Topic to quiz on
            difficulty: 'beginner', 'intermediate', or 'advanced'
            num_questions: Number of questions
            question_types: Types of questions to include
            
        Returns:
            Quiz in formatted text with multiple choice options
        """
        prompt = f"""Create a {difficulty} level multiple choice quiz about {topic} with {num_questions} questions.

IMPORTANT: Format EXACTLY like this for each question:

Question 1: [Your question here]
A) [First option]
B) [Second option]
C) [Third option]
D) [Fourth option]

Question 2: [Your question here]
A) [First option]
B) [Second option]
C) [Third option]
D) [Fourth option]

Make the questions clear, educational, and appropriate for {difficulty} level learners.
Include one correct answer and three plausible distractors for each question."""
        
        return self.process(prompt)
    
    def evaluate_answer(
        self,
        question: str,
        answer: str,
        expected_answer: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a learner's answer
        
        Args:
            question: The original question
            answer: Learner's answer
            expected_answer: Expected/correct answer if available
            
        Returns:
            Evaluation results
        """
        prompt = f"Question: {question}\n\nLearner's Answer: {answer}\n"
        
        if expected_answer:
            prompt += f"\nExpected Answer: {expected_answer}\n"
        
        prompt += "\nPlease evaluate this answer. Provide:\n"
        prompt += "1. What they got right\n"
        prompt += "2. What needs improvement\n"
        prompt += "3. A score out of 10\n"
        prompt += "4. Specific suggestions for improvement"
        
        evaluation = self.process(prompt)
        
        # Try to extract score from response
        score_match = re.search(r'(\d+)/10', evaluation)
        score = int(score_match.group(1)) if score_match else None
        
        return {
            "evaluation": evaluation,
            "score": score,
            "passed": score >= 7 if score else None
        }
    
    def evaluate_code(
        self,
        problem: str,
        code: str,
        test_cases: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate code submission
        
        Args:
            problem: Problem description
            code: Submitted code
            test_cases: Optional test cases with input/expected_output
            
        Returns:
            Evaluation with feedback
        """
        # First, try to execute the code
        execution_result = self.code_sandbox.execute(code)
        
        feedback = {
            "executes": execution_result.success,
            "output": execution_result.output,
            "error": execution_result.error,
            "passed_tests": 0,
            "total_tests": 0
        }
        
        # Run test cases if provided and code executes
        if test_cases and execution_result.success:
            # This is simplified - in production, would need proper test execution
            feedback["total_tests"] = len(test_cases)
            # For now, mark as needing manual review
            feedback["needs_manual_review"] = True
        
        # Get LLM-based code review
        review_prompt = f"""Problem: {problem}

Submitted Code:
```python
{code}
```

Execution Result:
- Success: {execution_result.success}
- Output: {execution_result.output or 'None'}
- Error: {execution_result.error or 'None'}

Please review this code submission:
1. Does it solve the problem?
2. Code quality (readability, style, best practices)
3. Efficiency considerations
4. Specific suggestions for improvement
5. Overall score out of 10"""
        
        code_review = self.process(review_prompt)
        feedback["review"] = code_review
        
        # Extract score
        score_match = re.search(r'(\d+)/10', code_review)
        if score_match:
            feedback["score"] = int(score_match.group(1))
        
        # Update learning metrics
        topic = self.memory.get_user_profile().current_topic if self.memory.get_user_profile() else "general"
        success = feedback.get("score", 0) >= 7
        self.memory.update_learning_metric(
            topic=topic,
            success=success,
            practice_time=execution_result.execution_time
        )
        
        return feedback
    
    def create_practice_problem(
        self,
        topic: str,
        difficulty: str = "beginner"
    ) -> str:
        """
        Create a practice coding problem
        
        Args:
            topic: Topic for the problem
            difficulty: Difficulty level
            
        Returns:
            Problem description
        """
        prompt = f"""Create a {difficulty} level coding problem about {topic}.

Include:
- Clear problem description
- Example input/output
- Any constraints or requirements
- Hints to get started (but don't give away the solution)

Make it practical and engaging!"""
        
        return self.process(prompt)
    
    def generate_personalized_challenge(self) -> str:
        """
        Generate a challenge based on user's learning history
        
        Returns:
            Personalized challenge
        """
        context = self.get_user_context()
        weak_topics = context.get('weak_topics', [])
        current_topic = context.get('current_topic', 'python basics')
        
        if weak_topics:
            focus = weak_topics[0]
            prompt = f"Create a practice problem focusing on {focus}, which this learner needs more practice with."
        else:
            prompt = f"Create a practice problem on {current_topic} to reinforce learning."
        
        return self.create_practice_problem(prompt)
