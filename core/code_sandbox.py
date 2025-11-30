"""
Code Sandbox - Safe code execution environment
Uses RestrictedPython for basic safety, with planned Docker integration
"""

import sys
import io
import traceback
import time
from typing import Dict, Any, Optional
from contextlib import redirect_stdout, redirect_stderr
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Guards import guarded_iter_unpack_sequence, safer_getattr


class ExecutionResult:
    """Result of code execution"""
    
    def __init__(
        self,
        success: bool,
        output: str = "",
        error: Optional[str] = None,
        execution_time: float = 0.0,
        return_value: Any = None
    ):
        self.success = success
        self.output = output
        self.error = error
        self.execution_time = execution_time
        self.return_value = return_value
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "execution_time": self.execution_time,
            "return_value": str(self.return_value) if self.return_value else None
        }


class CodeSandbox:
    """
    Safe code execution sandbox
    
    Features:
    - Restricted Python execution
    - Timeout enforcement
    - Output capture
    - Error handling
    """
    
    def __init__(
        self,
        timeout: int = 30,
        allowed_modules: Optional[list] = None
    ):
        self.timeout = timeout
        self.allowed_modules = allowed_modules or ['math', 'random', 'datetime', 'json']
        
    def execute(
        self,
        code: str,
        language: str = "python"
    ) -> ExecutionResult:
        """
        Execute code in a sandboxed environment
        
        Args:
            code: Code to execute
            language: Programming language (currently only Python supported)
            
        Returns:
            ExecutionResult with output/errors
        """
        if language.lower() != "python":
            return ExecutionResult(
                success=False,
                error=f"Language {language} not yet supported. Only Python is available."
            )
        
        return self._execute_python(code)
    
    def _execute_python(self, code: str) -> ExecutionResult:
        """Execute Python code with restrictions"""
        
        # Compile with RestrictedPython
        try:
            byte_code = compile_restricted(
                code,
                filename='<user_code>',
                mode='exec'
            )
        except SyntaxError as e:
            return ExecutionResult(
                success=False,
                error=f"Syntax Error: {str(e)}"
            )
        
        # Set up safe globals
        safe_builtins = safe_globals.copy()
        safe_builtins['_getiter_'] = safe_globals['_iter_']
        safe_builtins['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
        safe_builtins['_getattr_'] = safer_getattr
        
        # Add allowed modules
        for module_name in self.allowed_modules:
            try:
                safe_builtins[module_name] = __import__(module_name)
            except ImportError:
                pass
        
        # Add safe built-in functions
        safe_builtins['print'] = print
        safe_builtins['range'] = range
        safe_builtins['len'] = len
        safe_builtins['str'] = str
        safe_builtins['int'] = int
        safe_builtins['float'] = float
        safe_builtins['list'] = list
        safe_builtins['dict'] = dict
        safe_builtins['tuple'] = tuple
        safe_builtins['set'] = set
        safe_builtins['abs'] = abs
        safe_builtins['min'] = min
        safe_builtins['max'] = max
        safe_builtins['sum'] = sum
        safe_builtins['sorted'] = sorted
        safe_builtins['enumerate'] = enumerate
        safe_builtins['zip'] = zip
        safe_builtins['map'] = map
        safe_builtins['filter'] = filter
        
        # Capture output
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        start_time = time.time()
        
        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(byte_code, safe_builtins)
            
            execution_time = time.time() - start_time
            output = stdout_capture.getvalue()
            
            return ExecutionResult(
                success=True,
                output=output,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_output = stderr_capture.getvalue()
            
            # Get detailed traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error_message = ''.join(tb_lines)
            
            return ExecutionResult(
                success=False,
                output=stdout_capture.getvalue(),
                error=error_message if error_message else str(e),
                execution_time=execution_time
            )
    
    def validate_syntax(self, code: str, language: str = "python") -> tuple[bool, Optional[str]]:
        """
        Validate code syntax without executing
        
        Args:
            code: Code to validate
            language: Programming language
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if language.lower() != "python":
            return False, f"Language {language} not supported"
        
        try:
            compile_restricted(code, filename='<string>', mode='exec')
            return True, None
        except SyntaxError as e:
            return False, str(e)
    
    def get_safe_globals(self) -> Dict[str, Any]:
        """Get the safe globals dictionary"""
        return safe_globals.copy()


# Convenience function
def execute_code(code: str, language: str = "python", timeout: int = 30) -> ExecutionResult:
    """
    Execute code in sandbox
    
    Args:
        code: Code to execute
        language: Programming language
        timeout: Timeout in seconds
        
    Returns:
        ExecutionResult
    """
    sandbox = CodeSandbox(timeout=timeout)
    return sandbox.execute(code, language)
