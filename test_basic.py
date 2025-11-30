"""
Simple test script to verify basic functionality
Run without API keys to test core components
"""

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    try:
        from core.code_sandbox import CodeSandbox, execute_code
        from core.memory import Memory, UserProfile
        print("✅ Core modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False


def test_code_sandbox():
    """Test code sandbox functionality"""
    print("\n🧪 Testing Code Sandbox...")
    try:
        from core.code_sandbox import execute_code
        
        # Test 1: Simple execution
        code = "print('Hello, CodeMentor!')"
        result = execute_code(code)
        assert result.success, "Code execution failed"
        assert "Hello, CodeMentor!" in result.output, "Output mismatch"
        print("✅ Simple execution works")
        
        # Test 2: Math operations
        code = "import math\nprint(math.sqrt(16))"
        result = execute_code(code)
        assert result.success, "Math execution failed"
        assert "4.0" in result.output, "Math output mismatch"
        print("✅ Math operations work")
        
        # Test 3: Error handling
        code = "x = 1 / 0"
        result = execute_code(code)
        assert not result.success, "Should have failed"
        assert result.error is not None, "Error not captured"
        print("✅ Error handling works")
        
        return True
    except Exception as e:
        print(f"❌ Sandbox test error: {e}")
        return False


def test_memory():
    """Test memory management"""
    print("\n🧪 Testing Memory System...")
    try:
        from core.memory import Memory, UserProfile
        
        # Create memory
        memory = Memory()
        
        # Test message storage
        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi there!")
        history = memory.get_conversation_history()
        assert len(history) == 2, "Message storage failed"
        print("✅ Message storage works")
        
        # Test user profile
        profile = UserProfile(
            user_id="test_user",
            learning_style="visual",
            current_language="python"
        )
        memory.set_user_profile(profile)
        retrieved = memory.get_user_profile()
        assert retrieved.user_id == "test_user", "Profile storage failed"
        print("✅ User profile works")
        
        # Test learning metrics
        memory.update_learning_metric("loops", success=True, practice_time=60.0)
        metric = memory.get_learning_metric("loops")
        assert metric is not None, "Metrics failed"
        assert metric.practice_count == 1, "Practice count wrong"
        print("✅ Learning metrics work")
        
        return True
    except Exception as e:
        print(f"❌ Memory test error: {e}")
        return False


def test_file_structure():
    """Test that all required files exist"""
    print("\n🧪 Testing File Structure...")
    import os
    
    required_files = [
        "app.py",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "README.md",
        "QUICKSTART.md",
        "agents/__init__.py",
        "core/__init__.py",
        "core/llm_service.py",
        "core/code_sandbox.py",
        "core/memory.py",
        "agents/tutor_agent.py",
        "agents/debug_agent.py",
        "agents/assessment_agent.py",
        "agents/motivation_agent.py",
        "agents/orchestrator.py"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ Missing: {file}")
            all_exist = False
    
    return all_exist


def main():
    """Run all tests"""
    print("=" * 60)
    print("CodeMentor AI - Basic Functionality Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("File Structure", test_file_structure()))
    results.append(("Code Sandbox", test_code_sandbox()))
    results.append(("Memory System", test_memory()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed!")
        print("\nNext steps:")
        print("1. Set up your .env file with API keys")
        print("2. Run: streamlit run app.py")
        print("3. Check out: notebooks/demo.ipynb")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
