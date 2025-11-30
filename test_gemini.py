"""
Test Google Gemini API integration
Run this to verify Gemini setup before running the full app
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_basic():
    """Test basic Gemini API functionality"""
    print("🧪 Testing Google Gemini API Integration\n")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        print("\n📝 To fix this:")
        print("1. Visit: https://makersuite.google.com/app/apikey")
        print("2. Create a FREE API key")
        print("3. Add to .env file: GOOGLE_API_KEY=your_key_here")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    print("\n🔄 Testing Gemini API...")
    
    try:
        import google.generativeai as genai
        print("✅ google-generativeai package installed")
    except ImportError:
        print("❌ google-generativeai not installed")
        print("\n📝 To fix this:")
        print("   pip install google-generativeai")
        return False
    
    try:
        # Configure API
        genai.configure(api_key=api_key)
        print("✅ API configured successfully")
        
        # Test simple generation
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Model loaded: gemini-2.5-flash")
        
        print("\n💬 Sending test prompt...")
        response = model.generate_content("Say 'Hello from Gemini!' and nothing else.")
        
        print(f"✅ Response received: {response.text}")
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Gemini API is working correctly!")
        print("\nYou're ready to run CodeMentor AI with FREE Gemini!")
        print("Run: streamlit run app.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing Gemini API: {str(e)}")
        print("\n📝 Troubleshooting:")
        print("1. Check your API key is valid")
        print("2. Visit: https://makersuite.google.com/app/apikey")
        print("3. Try creating a new key")
        print("4. Make sure you have internet connection")
        return False


def test_llm_service():
    """Test LLM service integration"""
    print("\n\n🧪 Testing LLM Service Integration\n")
    print("=" * 60)
    
    try:
        from core.llm_service import create_llm_service, Message
        print("✅ LLM Service imported successfully")
        
        # Create service with Gemini
        llm = create_llm_service(provider="gemini")
        print("✅ LLM Service created with Gemini provider")
        
        # Test generation
        messages = [Message(role="user", content="Say 'CodeMentor AI works!' and nothing else.")]
        print("\n💬 Testing generation...")
        
        response = llm.generate(messages)
        print(f"✅ Response: {response}")
        
        print("\n" + "=" * 60)
        print("🎉 LLM Service integration working!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n" + "🧠" * 30)
    print("   CodeMentor AI - Gemini API Test")
    print("🧠" * 30 + "\n")
    
    # Test 1: Basic Gemini
    result1 = test_gemini_basic()
    
    # Test 2: LLM Service (only if basic test passed)
    if result1:
        result2 = test_llm_service()
    else:
        result2 = False
    
    # Summary
    print("\n\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Gemini API Basic: {'✅ PASS' if result1 else '❌ FAIL'}")
    print(f"LLM Service Integration: {'✅ PASS' if result2 else '❌ FAIL'}")
    
    if result1 and result2:
        print("\n🎉 All tests passed! You're ready to use CodeMentor AI!")
        print("\nNext step:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️ Some tests failed. Please follow the instructions above.")
        print("\nNeed help? Check: FREE_API_SETUP.md")
    
    print("=" * 60)
