# Quick Start Guide

Welcome to CodeMentor AI! This guide will get you up and running in 5 minutes.

## Prerequisites

- Python 3.10 or higher
- An OpenAI API key OR Anthropic API key
- Internet connection

## Installation Steps

### 1. Get the Code

```bash
cd /Users/krishnavardhan/projects/codementor-ai
```

### 2. Set Up Environment

#### Option A: Automated Setup (Recommended)
```bash
./setup.sh
```

#### Option B: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file from the example:
```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```bash
# For OpenAI
OPENAI_API_KEY=sk-...your-key-here...
LLM_PROVIDER=openai

# OR for Anthropic
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
LLM_PROVIDER=anthropic
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## First Time Use

1. **Profile Setup**: On first launch, you'll set up your learning profile
   - Enter your name
   - Choose your learning style (visual, auditory, kinesthetic)
   - Set your pace preference
   - Add any accessibility needs

2. **Start Learning**: 
   - Ask questions like "Explain Python lists"
   - Submit code for debugging
   - Request a quiz on any topic
   - Check your progress

## Example Interactions

### Learning
```
You: Explain what a function is in Python
```

### Debugging
```
You: My code has an error:
```python
def add_numbers(a, b):
    return a + b

result = add_numbers(5)
print(result)
```
```

### Assessment
```
You: Give me a quiz on Python loops
```

### Progress
```
You: Show me my progress
```

## Features to Try

- 🎯 **Quick Actions** (in sidebar):
  - Explain Concept
  - Debug Code
  - Take Quiz
  - My Progress

- 🤖 **Agent Modes**:
  - Auto (AI chooses best agent)
  - Tutor (explanations)
  - Debug (error fixing)
  - Assessment (quizzes)
  - Motivation (encouragement)

- 📊 **Progress Tracking**:
  - View learning stats in sidebar
  - See topics practiced
  - Track time spent

## Testing

Run the test suite:
```bash
pytest tests/test_core.py -v
```

## Running the Demo Notebook

```bash
jupyter notebook notebooks/demo.ipynb
```

## Troubleshooting

### "No module named 'openai'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "API key not found"
- Check that `.env` file exists
- Verify API key is correctly set
- Restart the application

### "Module not found" errors
```bash
# Make sure you're in the project directory
cd /Users/krishnavardhan/projects/codementor-ai

# Reinstall dependencies
pip install -r requirements.txt
```

## Getting Help

- Check the main [README.md](README.md)
- Review example code in `data/examples/`
- Run tests to verify setup

## What's Next?

1. Complete the onboarding flow
2. Try asking different types of questions
3. Submit code for debugging
4. Take a quiz to test your knowledge
5. Check your progress regularly

Happy learning! 🚀
