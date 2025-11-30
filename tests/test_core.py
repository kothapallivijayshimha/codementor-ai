"""
Basic tests for CodeMentor AI components
"""

import pytest
from core.code_sandbox import CodeSandbox, execute_code
from core.memory import Memory, UserProfile, LearningMetric
from datetime import datetime


class TestCodeSandbox:
    """Test code execution sandbox"""
    
    def test_simple_execution(self):
        """Test basic code execution"""
        code = "print('Hello, World!')"
        result = execute_code(code)
        
        assert result.success is True
        assert "Hello, World!" in result.output
    
    def test_syntax_error(self):
        """Test syntax error handling"""
        code = "print('unclosed string"
        result = execute_code(code)
        
        assert result.success is False
        assert result.error is not None
    
    def test_math_operations(self):
        """Test math operations"""
        code = """
import math
result = math.sqrt(16)
print(result)
"""
        result = execute_code(code)
        
        assert result.success is True
        assert "4.0" in result.output
    
    def test_runtime_error(self):
        """Test runtime error handling"""
        code = "x = 1 / 0"
        result = execute_code(code)
        
        assert result.success is False
        assert "ZeroDivisionError" in result.error or "division" in result.error.lower()


class TestMemory:
    """Test memory management"""
    
    def test_add_message(self):
        """Test adding messages"""
        memory = Memory()
        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi there!")
        
        history = memory.get_conversation_history()
        assert len(history) == 2
        assert history[0].content == "Hello"
        assert history[1].role == "assistant"
    
    def test_user_profile(self):
        """Test user profile management"""
        memory = Memory()
        profile = UserProfile(
            user_id="test_user",
            learning_style="visual",
            current_language="python"
        )
        memory.set_user_profile(profile)
        
        retrieved = memory.get_user_profile()
        assert retrieved.user_id == "test_user"
        assert retrieved.learning_style == "visual"
    
    def test_learning_metrics(self):
        """Test learning metrics tracking"""
        memory = Memory()
        
        # Practice a topic successfully
        memory.update_learning_metric("loops", success=True, practice_time=120.0)
        memory.update_learning_metric("loops", success=True, practice_time=90.0)
        memory.update_learning_metric("loops", success=False, practice_time=60.0)
        
        metric = memory.get_learning_metric("loops")
        assert metric is not None
        assert metric.practice_count == 3
        assert 0.6 <= metric.success_rate <= 0.7  # 2/3 success
    
    def test_weak_topics(self):
        """Test identifying weak topics"""
        memory = Memory()
        
        memory.update_learning_metric("topic1", success=True)
        memory.update_learning_metric("topic1", success=True)
        
        memory.update_learning_metric("topic2", success=False)
        memory.update_learning_metric("topic2", success=False)
        
        weak = memory.get_weak_topics(threshold=0.5)
        assert "topic2" in weak


class TestSandboxValidation:
    """Test sandbox validation features"""
    
    def test_syntax_validation(self):
        """Test syntax validation"""
        sandbox = CodeSandbox()
        
        valid_code = "x = 10\nprint(x)"
        is_valid, error = sandbox.validate_syntax(valid_code)
        assert is_valid is True
        assert error is None
        
        invalid_code = "if True print('missing colon')"
        is_valid, error = sandbox.validate_syntax(invalid_code)
        assert is_valid is False
        assert error is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
