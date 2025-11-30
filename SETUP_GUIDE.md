# 🚀 CodeMentor AI - Your Personal Setup Guide

## ✅ STEP 1: Get FREE API Key (YOU'RE HERE!)

### What You're Doing:
Getting a 100% FREE Google Gemini API key (no credit card needed!)

### Instructions:
1. Go to: https://makersuite.google.com/app/apikey (already open in your browser!)
2. Click "Create API key"
3. Click "Create API key in new project"
4. COPY the key (looks like: AIzaSy...)
5. Save it somewhere safe (we'll use it in Step 2)

### ✅ When Done:
☐ I have my API key copied

---

## STEP 2: Setup the .env File (NEXT)

### What You're Doing:
Telling CodeMentor AI to use your FREE API key

### Instructions:
1. Open Terminal
2. Navigate to project:
   ```bash
   cd /Users/krishnavardhan/projects/codementor-ai
   ```
3. Create .env file from template:
   ```bash
   cp .env.example .env
   ```
4. Open .env in your editor:
   ```bash
   nano .env
   ```
   (or use VS Code: `code .env`)
   
5. Edit the file - change this line:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   To:
   ```
   GOOGLE_API_KEY=AIzaSy...your-actual-key...
   ```
   
6. Save and close (in nano: Ctrl+X, then Y, then Enter)

### ✅ When Done:
☐ .env file created
☐ My API key is in the file
☐ File saved

---

## STEP 3: Install Dependencies

### What You're Doing:
Installing all the Python packages CodeMentor AI needs

### Instructions:
1. Make sure you're in the project directory:
   ```bash
   cd /Users/krishnavardhan/projects/codementor-ai
   ```

2. OPTION A - Automated (Recommended):
   ```bash
   ./setup.sh
   ```

3. OPTION B - Manual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### What's Happening:
- Creating a virtual environment (isolated Python space)
- Installing: Streamlit, Google Gemini SDK, RestrictedPython, etc.
- Takes 1-2 minutes

### ✅ When Done:
☐ Virtual environment created (venv/ folder exists)
☐ All packages installed (no error messages)
☐ You see "Successfully installed..." messages

---

## STEP 4: Test Gemini Connection

### What You're Doing:
Making sure your FREE API key works before running the full app

### Instructions:
1. Make sure venv is activated:
   ```bash
   source venv/bin/activate
   ```
   (You should see `(venv)` in your terminal prompt)

2. Run the test script:
   ```bash
   python test_gemini.py
   ```

### What You Should See:
```
✅ API Key found: AIzaSy...
✅ google-generativeai package installed
✅ API configured successfully
✅ Model loaded: gemini-1.5-flash
💬 Sending test prompt...
✅ Response received: Hello from Gemini!
🎉 SUCCESS! Gemini API is working correctly!
```

### If You See Errors:
- "API Key not found" → Go back to Step 2, check .env file
- "Package not installed" → Go back to Step 3, run setup again
- "Invalid API key" → Go back to Step 1, get a new key

### ✅ When Done:
☐ Test passed (saw "SUCCESS!" message)
☐ Gemini is responding

---

## STEP 5: Run CodeMentor AI!

### What You're Doing:
Launching the web app - your AI programming tutor!

### Instructions:
1. Make sure venv is active:
   ```bash
   source venv/bin/activate
   ```

2. Run the app:
   ```bash
   streamlit run app.py
   ```

3. Your browser will automatically open to: http://localhost:8501

### What You'll See:
1. **First time**: Setup screen asking for your name and preferences
   - Enter your name
   - Choose learning style (visual/auditory/kinesthetic)
   - Select learning pace
   - Add any accessibility needs
   - Click "Start Learning!"

2. **After setup**: The main chat interface
   - Chat with the AI tutor
   - Quick action buttons (Explain, Debug, Quiz, Progress)
   - Your learning stats in sidebar

### ✅ When Done:
☐ App is running at localhost:8501
☐ Completed the setup form
☐ Seeing the main chat interface

---

## STEP 6: Try It Out!

### What You're Doing:
Testing the different AI agents

### Try These:
1. **Ask a question** (Tutor Agent):
   ```
   Explain what a Python list is
   ```

2. **Debug some code** (Debug Agent):
   ```
   My code has an error:
   def greet(name):
       print(f"Hello {name}!)
   ```

3. **Take a quiz** (Assessment Agent):
   ```
   Give me a quiz on Python basics
   ```

4. **Check progress** (Motivation Agent):
   ```
   Show me my progress
   ```

### ✅ When Done:
☐ Tried all 4 agents
☐ Got responses from AI
☐ Understanding how it works!

---

## UNDERSTANDING THE SYSTEM

### What's Happening Behind the Scenes:

1. **You type a message** → Streamlit app receives it
2. **Orchestrator analyzes** → Determines which agent to use
3. **Agent processes** → Uses your query + user profile
4. **Calls Gemini API** → Gets AI response (FREE!)
5. **Formats response** → Shows it to you nicely
6. **Saves to memory** → Tracks your learning progress

### The 5 Agents:
- **Tutor** 👨‍🏫 - Explains concepts (adaptive to your style)
- **Debugger** 🔧 - Helps fix code errors
- **Assessor** 📝 - Creates quizzes, evaluates code
- **Motivator** 🌟 - Keeps you encouraged
- **Orchestrator** 🎯 - Routes to the right agent

### Your Data:
- Stored locally in memory
- Progress tracked (skill levels, success rates)
- Gets better as you use it more

---

## TROUBLESHOOTING

### "GOOGLE_API_KEY not found"
→ Check .env file exists and has your key
→ Make sure venv is activated
→ Restart the app

### "Module not found: streamlit"
→ Run: `pip install -r requirements.txt`
→ Make sure venv is activated

### "Rate limit exceeded"
→ Wait 1 minute (free tier: 60 requests/min)
→ Don't spam messages too fast

### App won't start
→ Check: `python --version` (need 3.10+)
→ Delete venv and recreate: `rm -rf venv && ./setup.sh`

---

## NEXT STEPS

After you have it running:

1. **Explore Features**
   - Try different questions
   - Submit code for debugging
   - Take quizzes
   - Check your progress

2. **Customize**
   - Edit your profile (name, learning style)
   - Try different agent modes (sidebar)
   - Reset chat if needed

3. **Learn Something!**
   - Pick a topic (Python, JavaScript, etc.)
   - Ask for explanations
   - Practice with code
   - Track your progress

4. **For Kaggle Submission**
   - Review notebooks/demo.ipynb
   - Test all features
   - Take screenshots
   - Submit!

---

## QUICK REFERENCE

```bash
# Start the app
cd /Users/krishnavardhan/projects/codementor-ai
source venv/bin/activate
streamlit run app.py

# Test Gemini
python test_gemini.py

# Run tests
python test_basic.py

# Stop the app
# Press Ctrl+C in terminal
```

---

## YOU'RE READY! 🚀

Follow the steps above in order. After each step, you can:
- ✅ Check it off
- Test it
- Move to next step

**Current Step: Get your API key!**

Once you have it, come back and we'll do Step 2 together!
