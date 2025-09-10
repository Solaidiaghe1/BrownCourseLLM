# Brown Course Advisor - Usage Guide

## 🎨 GUI Version (Recommended)

### Quick Start with Beautiful GUI

1. **Install Dependencies:**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

2. **Launch the GUI:**
   ```bash
   python3 launch_gui.py
   ```
   Or directly:
   ```bash
   python3 gui_app.py
   ```

### GUI Features
- **🎨 Modern Design**: Beautiful, professional interface with Brown University colors
- **💬 Chat Interface**: Natural conversation flow with message bubbles
- **📚 Course Cards**: Rich display of recommended courses with details
- **⚡ Real-time Updates**: Live status indicators and progress bars
- **🔄 Follow-up Questions**: Seamless conversation without restarting
- **📱 Responsive Layout**: Adapts to different window sizes
- **🎯 Smart Input**: Auto-complete and placeholder text

## 💻 Command Line Version

### Quick Start (Terminal)

1. **Install Dependencies:**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

2. **Run the Advisor:**
   ```bash
   python3 query.py
   ```

## What's New & Improved

### 🚀 **Performance Improvements:**
- **Faster startup**: Models and data are loaded only once at startup
- **No more reloading**: The AI model and course index stay in memory between questions
- **Instant responses**: After the first question, subsequent questions are much faster

### 💬 **Interactive Session:**
- **Follow-up questions**: Ask as many questions as you want without restarting
- **Conversation memory**: The AI remembers your previous questions for better context
- **Easy exit**: Type 'quit', 'exit', 'bye', or 'q' to end the session
- **Better prompts**: Clear instructions and helpful emojis for better user experience

### 🎯 **Enhanced Features:**
- **Context-aware responses**: The AI considers your conversation history
- **Better error handling**: Graceful handling of network issues and errors
- **Improved course display**: Better formatting and more relevant course information
- **Multiple exit options**: Various ways to end the session

## Example Usage

```
🎓 Welcome to the Brown Course Advisor!
Ask me anything about courses, prerequisites, schedules, or academic planning.

❓ Ask a question about courses (or 'quit' to exit): What computer science courses are available?

🤔 Thinking...

============================================================
🎯 AI Advisor Advice (Triple A)
============================================================
Based on your interest in computer science courses, here are some excellent options...

📚 Relevant Courses Found:

1. 📖 CS 101 - Introduction to Computer Science
   Description: An introduction to computer science...

2. 📖 CS 142 - Data Structures and Algorithms
   Prerequisites: CS 101 or equivalent
   Description: Advanced programming concepts...

============================================================
💡 You can ask follow-up questions or type 'quit' to exit.

❓ Ask a question about courses (or 'quit' to exit): What are the prerequisites for CS 142?
```

## Tips for Best Results

1. **Be specific**: Ask detailed questions about courses, prerequisites, or schedules
2. **Use follow-ups**: Build on previous questions for more detailed advice
3. **Ask about prerequisites**: The system can provide specific prerequisite information
4. **Inquire about scheduling**: Ask when courses are offered or about semester availability

## Troubleshooting

- If you get import errors, make sure all dependencies are installed: `pip install -r requirements.txt`
- If the AI model takes time to load initially, this is normal - subsequent questions will be much faster
- If you encounter API errors, check your OpenAI API key in the code