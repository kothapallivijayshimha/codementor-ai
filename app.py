"""
CodeMentor AI - Streamlit Application
Modern, aesthetic UI with interactive quizzes and rich examples
"""

import streamlit as st
import os
import re
from dotenv import load_dotenv

from core.llm_service import create_llm_service
from core.code_sandbox import CodeSandbox
from core.memory import Memory, UserProfile
from agents.orchestrator import Orchestrator, AgentType

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CodeMentor AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern, aesthetic CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #64748b;
        margin-top: -1rem;
        margin-bottom: 2rem;
    }
    
    .agent-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 2rem;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .tutor-badge { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white; 
    }
    .debug-badge { 
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
        color: white; 
    }
    .assessment-badge { 
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
        color: white; 
    }
    .motivation-badge { 
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
        color: white; 
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 0.75rem;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    }
    
    .quiz-option {
        padding: 1rem;
        border-radius: 0.75rem;
        border: 2px solid #e2e8f0;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        background: white;
    }
    
    .quiz-option:hover {
        border-color: #667eea;
        background: #f8f9ff;
        transform: translateX(4px);
    }
    
    .code-example {
        background: #1e293b;
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
        font-family: 'Fira Code', monospace;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .example-section {
        background: linear-gradient(135deg, #f8f9ff 0%, #fff 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .stRadio > label {
        font-weight: 600;
        color: #1e293b;
        font-size: 1.1rem;
    }
    
    .stRadio > div {
        gap: 0.75rem;
    }
    
    .stRadio > div > label {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        border: 2px solid #e2e8f0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stRadio > div > label:hover {
        border-color: #667eea;
        background: #f8f9ff;
        transform: translateX(4px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if "memory" not in st.session_state:
        st.session_state.memory = Memory()
    
    if "llm_service" not in st.session_state:
        st.session_state.llm_service = create_llm_service()
    
    if "code_sandbox" not in st.session_state:
        st.session_state.code_sandbox = CodeSandbox()
    
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = Orchestrator(
            st.session_state.llm_service,
            st.session_state.memory,
            st.session_state.code_sandbox
        )
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "setup_complete" not in st.session_state:
        st.session_state.setup_complete = False
    
    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = None


def render_agent_badge(agent_type: str) -> str:
    """Render agent badge HTML"""
    badges = {
        "tutor": ("👨‍🏫", "Tutor", "tutor-badge"),
        "debug": ("🔧", "Debug", "debug-badge"),
        "assessment": ("📝", "Assessment", "assessment-badge"),
        "motivation": ("🌟", "Motivation", "motivation-badge"),
    }
    
    if agent_type.lower() in badges:
        icon, name, css_class = badges[agent_type.lower()]
        return f'<span class="agent-badge {css_class}">{icon} {name}</span>'
    return ""


def parse_quiz_response(response: str):
    """Parse quiz response to extract questions and options"""
    questions = []
    
    # robust regex to find questions with options
    # Matches: "1. Question?" or "Question 1: Question?" followed by A) ... B) ...
    pattern = r'(?:Question \d+[:.]|\d+\.)\s*(.+?)\n\s*(?:A\)|A\.|- A)\s*(.+?)\n\s*(?:B\)|B\.|- B)\s*(.+?)\n\s*(?:C\)|C\.|- C)\s*(.+?)\n\s*(?:D\)|D\.|- D)\s*(.+?)(?:\n\n|\Z)'
    
    matches = re.findall(pattern, response, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        question_text = match[0].strip()
        options = [opt.strip() for opt in match[1:5]]
        questions.append({
            "question": question_text,
            "options": options
        })
    
    return questions


def render_interactive_quiz(response: str, key_prefix: str = "quiz"):
    """Render quiz with interactive radio buttons"""
    questions = parse_quiz_response(response)
    
    if questions:
        st.markdown("### 📝 Interactive Quiz")
        
        for idx, q in enumerate(questions):
            st.markdown(f"#### Question {idx + 1}")
            st.markdown(f"**{q['question']}**")
            
            # Create radio buttons with unique keys
            answer = st.radio(
                f"Select your answer:",
                options=q['options'],
                key=f"{key_prefix}_q{idx}",
                label_visibility="collapsed"
            )
            
            if st.button(f"Submit Answer", key=f"{key_prefix}_submit_q{idx}"):
                st.success(f"✅ You selected: {answer}")
                st.info("💡 Great! The AI will provide feedback on your answer.")
            
            st.markdown("---")
    else:
        # Fallback: display as regular text
        st.warning("⚠️ Could not parse interactive quiz. Showing raw text:")
        st.markdown(response)
    
    # Debug: Show raw response
    with st.expander("� View Raw AI Response (Debug)"):
        st.text(response)


def setup_user_profile():
    """Setup user profile on first run"""
    st.markdown(f'<h1 class="main-header">🧠 Welcome to CodeMentor AI</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">Let\'s personalize your learning experience! 🚀</p>', unsafe_allow_html=True)
    
    with st.form("user_setup"):
        st.markdown("### 👤 Tell us about yourself")
        
        name = st.text_input("What's your name?", placeholder="Enter your name")
        
        st.markdown("### 🎯 Learning Preferences")
        
        learning_style = st.selectbox(
            "What's your preferred learning style?",
            ["Visual (diagrams, examples)", "Auditory (explanations, discussions)", "Kinesthetic (hands-on practice)"]
        )
        
        pace = st.select_slider(
            "Preferred learning pace:",
            options=["Very Slow", "Slow", "Moderate", "Fast", "Very Fast"],
            value="Moderate"
        )
        
        st.markdown("### ♿ Accessibility")
        
        accessibility_needs = st.multiselect(
            "Do you have any accessibility preferences?",
            ["Dyslexia-friendly mode", "ADHD-friendly (shorter sessions)", "Screen reader support", "None"]
        )
        
        st.markdown("### 💻 Programming Experience")
        
        experience = st.radio(
            "Current programming level:",
            ["Complete Beginner", "Some Experience", "Intermediate", "Advanced"]
        )
        
        interests = st.text_area(
            "What topics are you interested in?",
            placeholder="e.g., Python basics, web development, data science..."
        )
        
        submitted = st.form_submit_button("🚀 Start Learning!", use_container_width=True)
        
        if submitted:
            if not name:
                st.error("Please enter your name!")
                return
            
            # Create user profile
            profile = UserProfile(
                user_id=name.lower().replace(" ", "_"),
                name=name,
                learning_style=learning_style.split(" ")[0].lower(),
                pace_preference=pace.lower().replace(" ", "_"),
                accessibility_needs=accessibility_needs,
                current_language="python"
            )
            
            st.session_state.memory.set_user_profile(profile)
            st.session_state.setup_complete = True
            st.success(f"✅ Welcome aboard, {name}! Let's start learning!")
            st.rerun()


def render_sidebar():
    """Render sidebar with controls and stats"""
    with st.sidebar:
        st.markdown("### 🎮 Quick Actions")
        
        # Agent mode selector
        agent_mode = st.selectbox(
            "Agent Mode:",
            ["auto", "tutor", "debug", "assessment", "motivation"],
            format_func=lambda x: {
                "auto": "🤖 Auto (Smart Routing)",
                "tutor": "👨‍🏫 Tutor",
                "debug": "🔧 Debug",
                "assessment": "📝 Assessment",
                "motivation": "🌟 Motivation"
            }[x]
        )
        st.session_state.agent_mode = agent_mode
        
        st.markdown("---")
        
        # Quick action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📚 Explain", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Explain a programming concept"
                })
                st.rerun()
        
        with col2:
            if st.button("🔧 Debug", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Help me debug my code"
                })
                st.rerun()
        
        col3, col4 = st.columns(2)
        
        with col3:
            if st.button("📝 Quiz", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Give me a quiz on Python basics"
                })
                st.rerun()
        
        with col4:
            if st.button("📊 Progress", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Show my learning progress"
                })
                st.rerun()
        
        st.markdown("---")
        
        # User stats
        profile = st.session_state.memory.get_user_profile()
        
        st.markdown("### 📊 Your Stats")
        
        # Display metrics
        try:
            total_messages = len(st.session_state.messages)
            st.metric("Messages", total_messages)
            
            if hasattr(profile, 'skill_levels') and profile.skill_levels:
                st.metric("Skill Level", list(profile.skill_levels.values())[0].replace("_", " ").title())
            
            if hasattr(profile, 'learning_style') and profile.learning_style:
                st.metric("Learning Style", profile.learning_style.title())
        except:
            st.info("Stats will appear as you learn!")
        
        st.markdown("---")
        
        # Settings
        with st.expander("⚙️ Settings"):
            if st.button("🔄 Reset Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
            
            if st.button("👤 Edit Profile", use_container_width=True):
                st.session_state.setup_complete = False
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown(
            '<div style="text-align: center; color: #64748b; font-size: 0.8rem;">'
            'Built with ❤️ for neurodivergent learners'
            '</div>',
            unsafe_allow_html=True
        )


def main():
    """Main application with modern UI"""
    initialize_session_state()
    
    if not st.session_state.setup_complete:
        setup_user_profile()
        return
    
    profile = st.session_state.memory.get_user_profile()
    
    # Safely get display name with multiple fallbacks
    try:
        display_name = profile.name if hasattr(profile, 'name') and profile.name else profile.user_id
    except:
        display_name = getattr(profile, 'user_id', 'Learner')
    
    st.markdown(f'<h1 class="main-header">🧠 CodeMentor AI</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">Welcome back, <strong>{display_name}</strong>! Ready to learn? 🚀</p>', unsafe_allow_html=True)
    
    render_sidebar()
    
    st.markdown("---")
    
    # Display chat messages
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "agent" in message:
                st.markdown(render_agent_badge(message["agent"]), unsafe_allow_html=True)
            
            # Check if it's a quiz based on agent type or content
            is_quiz = (
                message.get("agent") == "assessment" or 
                "quiz" in message.get("content", "").lower() or
                "Question 1" in message.get("content", "")
            )
            
            if message["role"] == "assistant" and is_quiz:
                render_interactive_quiz(message["content"], key_prefix=f"hist_{i}")
            else:
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("💬 Ask me anything about programming..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                agent_mode = st.session_state.get("agent_mode", "auto")
                
                # Enhanced prompts for better responses
                if "quiz" in prompt.lower() or agent_mode == "assessment":
                    enhanced_prompt = f"{prompt}\n\nIMPORTANT: Format each question EXACTLY like this:\nQuestion 1: [Question text]\nA) [Option A]\nB) [Option B]\nC) [Option C]\nD) [Option D]"
                    response = st.session_state.orchestrator.create_quiz(enhanced_prompt)
                    agent_type = "assessment"
                elif "explain" in prompt.lower() or agent_mode == "tutor":
                    enhanced_prompt = f"{prompt}\n\nPlease include:\n1. Clear explanation\n2. At least 2 practical examples with code\n3. Common use cases"
                    response = st.session_state.orchestrator.explain_concept(enhanced_prompt)
                    agent_type = "tutor"
                elif agent_mode == "debug":
                    response = st.session_state.orchestrator.debug_code(prompt)
                    agent_type = "debug"
                elif agent_mode == "motivation":
                    response = st.session_state.orchestrator.get_progress_update()
                    agent_type = "motivation"
                else:
                    response = st.session_state.orchestrator.chat(prompt)
                    agent_type = "tutor"
                
                st.markdown(render_agent_badge(agent_type), unsafe_allow_html=True)
                
                # Render quiz or regular response
                if agent_type == "assessment":
                    render_interactive_quiz(response, key_prefix="new")
                else:
                    st.markdown(response)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "agent": agent_type
                })


if __name__ == "__main__":
    has_gemini = bool(os.getenv("GOOGLE_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    
    if not (has_gemini or has_openai or has_anthropic):
        st.error("⚠️ No API keys found!")
        st.info("🆓 **Get a FREE Google Gemini API key!**")
        st.markdown("[Get API Key →](https://makersuite.google.com/app/apikey)")
    else:
        if has_gemini:
            st.success("✅ Using Google Gemini (FREE tier)")
        main()
