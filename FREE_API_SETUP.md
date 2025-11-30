# 🆓 FREE API Setup Guide - Google Gemini

## Why Gemini?

**CodeMentor AI now supports Google Gemini's FREE tier!**

- ✅ **Completely FREE** - No credit card required
- ✅ **Generous limits** - 60 requests per minute
- ✅ **High quality** - Gemini 1.5 Flash is very capable
- ✅ **Easy setup** - Get your key in 2 minutes

---

## 🚀 Quick Setup (2 Minutes)

### Step 1: Get Your FREE API Key

1. Visit **[Google AI Studio](https://makersuite.google.com/app/apikey)**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Click **"Create API key in new project"** (or select existing project)
5. **Copy the key** - it looks like: `AIzaSy...`

![Get API Key](https://ai.google.dev/static/tutorials/images/get_api_key.png)

### Step 2: Add Key to Your Project

Open or create `.env` file in the project root:

```bash
cd /Users/krishnavardhan/projects/codementor-ai
cp .env.example .env
nano .env  # or use your favorite editor
```

Add your key:

```bash
# 🆓 FREE Google Gemini API
GOOGLE_API_KEY=AIzaSy...your-key-here...
LLM_PROVIDER=gemini
MODEL_NAME=gemini-1.5-flash
```

### Step 3: Install Dependencies

```bash
./setup.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Run the App!

```bash
streamlit run app.py
```

That's it! 🎉

---

## 📊 Gemini Free Tier Limits

### What You Get (FREE)
- **60 requests per minute**
- **1,500 requests per day**
- **1 million tokens per month**
- **No credit card required**
- **No expiration** (as of Nov 2024)

### Perfect For
- ✅ Learning and development
- ✅ Personal projects
- ✅ Educational use
- ✅ Prototyping
- ✅ Small-scale applications

---

## 🆚 Comparing LLM Options

| Feature | Gemini (FREE) | OpenAI GPT-4 | Anthropic Claude |
|---------|---------------|--------------|------------------|
| **Cost** | 🆓 FREE | 💰 $0.01/1k tokens | 💰 $3/million tokens |
| **Quality** | ⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐⭐⭐ Best |
| **Speed** | ⚡ Very Fast | ⚡ Fast | ⚡ Fast |
| **Limits** | 60 req/min | Pay as you go | Pay as you go |
| **Setup** | ✅ Easy | ✅ Easy | ✅ Easy |
| **Best For** | Learning, personal | Production | Production |

**Recommendation**: Start with Gemini FREE tier, upgrade later if needed!

---

## 🔧 Switching Between APIs

You can easily switch between different AI providers by changing your `.env` file:

### Use FREE Gemini
```bash
GOOGLE_API_KEY=your_gemini_key
LLM_PROVIDER=gemini
MODEL_NAME=gemini-1.5-flash
```

### Use OpenAI (Paid)
```bash
OPENAI_API_KEY=sk-your_openai_key
LLM_PROVIDER=openai
MODEL_NAME=gpt-4-turbo-preview
```

### Use Anthropic (Paid)
```bash
ANTHROPIC_API_KEY=sk-ant-your_claude_key
LLM_PROVIDER=anthropic
MODEL_NAME=claude-3-sonnet-20240229
```

Just restart the app after changing!

---

## 🎯 Gemini Models Available

### Gemini 1.5 Flash (Recommended - FREE)
- **Best for**: CodeMentor AI, fast responses
- **Speed**: Very fast
- **Quality**: Excellent for teaching
- **Model ID**: `gemini-1.5-flash`

### Gemini 1.5 Pro (Also FREE)
- **Best for**: Complex reasoning
- **Speed**: Fast
- **Quality**: Highest quality
- **Model ID**: `gemini-1.5-pro`
- **Note**: Slower but more capable

To switch models, update `.env`:
```bash
MODEL_NAME=gemini-1.5-pro
```

---

## 🛡️ Rate Limit Best Practices

### Free Tier Limits
- 60 requests/minute
- 1,500 requests/day

### Tips to Stay Within Limits
1. **Don't spam** - Wait for responses before sending new questions
2. **Use efficiently** - Ask clear, specific questions
3. **Cache responses** - The app already does this in memory
4. **Be patient** - Quality responses take a few seconds

### If You Hit Limits
- Wait 1 minute (rate limit resets)
- Check your [API usage dashboard](https://aistudio.google.com/)
- Consider upgrading if needed (but free tier is usually enough!)

---

## ❓ Troubleshooting

### "GOOGLE_API_KEY not found"
- Check `.env` file exists
- Verify key is on the line: `GOOGLE_API_KEY=AIza...`
- Make sure `LLM_PROVIDER=gemini`
- Restart the app

### "API key invalid"
- Check you copied the complete key
- Verify no extra spaces
- Make sure key is from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Try creating a new key

### "Rate limit exceeded"
- Wait 60 seconds
- You're using it too frequently
- Check usage at [AI Studio](https://aistudio.google.com/)

### Import errors
```bash
# Make sure you installed dependencies
pip install google-generativeai
# Or reinstall all
pip install -r requirements.txt
```

---

## 💡 Pro Tips

### 1. Multiple API Keys
Keep backup keys for different providers:

```bash
# FREE option (primary)
GOOGLE_API_KEY=your_gemini_key
LLM_PROVIDER=gemini

# Fallback options (commented out)
# OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_claude_key
```

### 2. Monitor Usage
Check your usage at [Google AI Studio](https://aistudio.google.com/):
- See requests per day
- Monitor quota
- View API call history

### 3. Optimize Prompts
- Be specific in questions
- Use clear language
- Avoid overly long conversations
- Reset chat if needed (clears context)

---

## 🎓 For Educators & Students

### Why Gemini is Perfect for Education

1. **No Cost Barrier** - Anyone can use it
2. **No Credit Card** - Great for students
3. **Generous Limits** - Enough for learning
4. **Quality AI** - Comparable to paid options
5. **Easy Setup** - 2 minutes to start

### Classroom Use
- Each student can get their own free key
- No institutional billing required
- Perfect for coding bootcamps
- Great for self-paced learning

---

## 📚 Resources

- **Get API Key**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Documentation**: [Gemini API Docs](https://ai.google.dev/docs)
- **Pricing**: [Free tier details](https://ai.google.dev/pricing)
- **Tutorials**: [Google AI Tutorials](https://ai.google.dev/tutorials)

---

## 🎯 Next Steps

1. ✅ Get your FREE Gemini API key
2. ✅ Add it to `.env`
3. ✅ Install dependencies
4. ✅ Run `streamlit run app.py`
5. ✅ Start learning!

---

## 🤝 Making Education Accessible

By supporting Google Gemini's free tier, CodeMentor AI truly lives up to its "Agents for Good" mission:

- ✅ **Accessible** - Anyone can use it without cost
- ✅ **Inclusive** - No financial barrier to entry
- ✅ **Educational** - Supports learning for all
- ✅ **Open** - Free and open-source software

**Now anyone, anywhere can have a personal AI programming tutor!**

---

**Questions?** Check the main [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)

**Ready to start?** Get your [FREE API key](https://makersuite.google.com/app/apikey) now! 🚀
