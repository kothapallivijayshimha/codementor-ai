"""
Debug Agent - Helps identify and fix code errors
"""

from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from core.llm_service import LLMService, Message
from core.memory import Memory
from core.code_sandbox import CodeSandbox, ExecutionResult


class DebugAgent(BaseAgent):
    """
    Debug Agent specializes in:
    - Identifying code errors
    - Providing helpful debugging hints
    - Teaching debugging strategies
    - Explaining error messages
    """
    
    SYSTEM_PROMPT = """You are a patient debugging expert helping learners understand and fix their code errors.

Your approach:
1. **Identify the Error**: Clearly state what went wrong
2. **Explain Why**: Help them understand the root cause
3. **Guide, Don't Solve**: Give hints rather than complete solutions
4. **Teach Debugging**: Show them how to debug similar issues
5. **Encourage**: Remind them that errors are part of learning

When analyzing errors:
- Point out the specific line or section with the issue
- Explain the error message in simple terms
- Provide a hint for the fix
- If they're stuck, offer progressively more specific hints
- Only give the complete solution if they explicitly ask after trying

Common error types to help with:
- Syntax errors (missing colons, parentheses, etc.)
- Name errors (undefined variables)
- Type errors (wrong data types in operations)
- Logic errors (code runs but gives wrong results)
- Runtime errors (division by zero, index out of range, etc.)

Remember:
- Making mistakes is how we learn
- Every programmer debugs code daily
- Errors are messages trying to help us
- The best debugging skill is reading error messages carefully"""
    
    def __init__(
        self,
        llm_service: LLMService,
        memory: Memory,
        code_sandbox: Optional[CodeSandbox] = None
    ):
        super().__init__(
            name="Debugger",
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
        Process debugging request
        
        Args:
            user_input: User's code or error description
            context: Additional context (code, error message, etc.)
            
        Returns:
            Debugging guidance
        """
        # Build messages with context
        messages = self._build_messages(user_input, include_history=True, history_count=3)
        
        # Generate response
        response = self.llm_service.generate(
            messages=messages,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.5,  # Lower temperature for more focused debugging
            max_tokens=1200
        )
        
        # Store in memory
        self.memory.add_message("user", user_input, agent_type="debug")
        self.memory.add_message("assistant", response, agent_type="debug")
        
        return response
    
    def analyze_error(
        self,
        code: str,
        error_message: Optional[str] = None,
        hint_level: int = 1
    ) -> str:
        """
        Analyze code error and provide guidance
        
        Args:
            code: The problematic code
            error_message: Error message if available
            hint_level: 1=subtle hint, 2=specific hint, 3=solution
            
        Returns:
            Debugging guidance
        """
        # Try to execute the code to get the error if not provided
        if not error_message:
            result = self.code_sandbox.execute(code)
            if not result.success:
                error_message = result.error
        
        # Build debugging prompt
        prompt = f"Help me debug this code:\n\n```python\n{code}\n```\n"
        
        if error_message:
            prompt += f"\nError message:\n{error_message}\n"
        
        if hint_level == 1:
            prompt += "\nGive me a subtle hint about what might be wrong."
        elif hint_level == 2:
            prompt += "\nI'm still stuck. Can you give me a more specific hint?"
        elif hint_level == 3:
            prompt += "\nI need help. Can you show me how to fix it?"
        
        return self.process(prompt)
    
    def explain_error(self, error_message: str) -> str:
        """
        Explain what an error message means
        
        Args:
            error_message: The error message to explain
            
        Returns:
            Simple explanation
        """
        prompt = f"Explain this error message in simple terms:\n{error_message}"
        return self.process(prompt)
    
    def suggest_debugging_strategy(self, problem_description: str) -> str:
        """
        Suggest debugging approach for a problem
        
        Args:
            problem_description: Description of the issue
            
        Returns:
            Debugging strategy suggestions
        """
        prompt = f"My code has this problem: {problem_description}\n\n"
        prompt += "What debugging strategies should I use to find the issue?"
        return self.process(prompt)
    
    def validate_and_debug(self, code: str) -> Dict[str, Any]:
        """
        Validate code and provide debugging info if needed
        
        Args:
            code: Code to validate
            
        Returns:
            Dictionary with validation results and debugging info
        """
        result = self.code_sandbox.execute(code)
        
        response = {
            "is_valid": result.success,
            "output": result.output,
            "error": result.error,
            "execution_time": result.execution_time
        }
        
        if not result.success:
            # Get debugging help
            debug_help = self.analyze_error(code, result.error, hint_level=1)
            response["debug_hint"] = debug_help
        
        return response
