# CodeMentor-AI: Adaptive Learning for Neurodivergent Coders 🧠

> **Google Capstone Project 2025**

## 🚀 Project Overview
CodeMentor-AI is a multi-agent system designed to make programming education accessible for neurodivergent learners (ADHD, Autism, Dyslexia). Unlike standard tutorials, this system adapts the teaching style, pacing, and feedback to match the user's cognitive needs.

## ✨ Key Features
- **Adaptive Learning Engine:** Real-time adjustment of lesson complexity.
- **Multi-Agent Architecture:** 5 specialized AI agents (Tutor, Quiz, Reviewer, etc.) powered by Google Gemini.
- **GitHub Integration:** Direct code analysis and feedback on user repositories.
- **Neuro-Inclusive UI:** High contrast, screen-reader friendly, and distraction-free mode.

## 🛠️ Tech Stack
- **AI/LLM:** Google Gemini API
- **Backend:** Python / Node.js (Multi-agent orchestration)
- **Frontend:** React.js
- **Integrations:** GitHub API

## 🏗️ System Architecture
The system uses a specialized agentic workflow:
1. **Input Analysis:** User code/query is analyzed for intent.
2. **Agent Dispatch:** The `TutorAgent` or `ReviewAgent` claims the task.
3. **Context Retrieval:** System fetches user learning profile.
4. **Response Generation:** tailored explanation is generated via Gemini.

## 📦 How to Run
