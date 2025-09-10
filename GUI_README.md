# 🎓 Brown Course Advisor - GUI Application

A beautiful, modern desktop application for the Brown Course Advisor with an intuitive user interface and excellent user experience.

## ✨ Features

### 🎨 **Modern Design**
- **Professional UI**: Clean, modern interface with Brown University color scheme
- **Responsive Layout**: Adapts to different window sizes and screen resolutions
- **Beautiful Typography**: Clear, readable fonts with proper hierarchy
- **Intuitive Navigation**: Easy-to-use interface that requires no training

### 💬 **Chat Interface**
- **Natural Conversation**: Chat-like interface for asking questions
- **Message Bubbles**: Clear distinction between user and AI messages
- **Timestamps**: Track when each message was sent
- **Conversation History**: Full chat history with context preservation

### 📚 **Course Display**
- **Rich Course Cards**: Detailed course information with formatting
- **Smart Filtering**: Shows most relevant courses based on your question
- **Prerequisites**: Clear display of course requirements
- **Instructor Info**: Course instructor and scheduling details

### ⚡ **Performance & UX**
- **Fast Loading**: Optimized startup and response times
- **Progress Indicators**: Visual feedback during processing
- **Error Handling**: Graceful error messages and recovery
- **Background Processing**: Non-blocking UI during AI processing

## 🚀 Quick Start

### Option 1: Easy Launch
```bash
python3 launch_gui.py
```

### Option 2: Direct Launch
```bash
python3 gui_app.py
```

## 🎯 How to Use

1. **Launch the Application**: Run the GUI using one of the methods above
2. **Wait for Initialization**: The app will load course data and AI models (first time only)
3. **Ask Questions**: Type your questions in the input area at the bottom
4. **View Recommendations**: See AI advice in the chat and course details on the right
5. **Follow-up Questions**: Ask follow-up questions naturally in the conversation

## 🎨 Interface Overview

### Header
- **Title**: Brown Course Advisor branding
- **Status Indicator**: Shows current system status (loading, ready, error)

### Main Chat Area (Left)
- **Conversation History**: All your questions and AI responses
- **Message Formatting**: Different styles for user vs AI messages
- **Scrollable**: Navigate through long conversations

### Course Panel (Right)
- **Recommended Courses**: Top courses based on your question
- **Course Details**: Title, code, instructor, prerequisites, description
- **Smart Formatting**: Highlighted important information

### Input Area (Bottom)
- **Text Input**: Multi-line input for detailed questions
- **Send Button**: Send your question to the AI
- **Keyboard Shortcut**: Ctrl+Enter to send quickly

### Status Bar (Bottom)
- **Status Messages**: Current system status and helpful tips
- **Progress Bar**: Shows when AI is processing (appears during thinking)

## 🎨 Color Scheme

The application uses a professional color palette inspired by Brown University:

- **Primary**: Dark blue-gray (#2c3e50) - Headers and important text
- **Secondary**: Bright blue (#3498db) - Buttons and highlights
- **Success**: Green (#27ae60) - Course panel and success messages
- **Warning**: Orange (#f39c12) - Loading states and warnings
- **Background**: Light gray (#f8f9fa) - Main background
- **Surface**: White (#ffffff) - Content panels

## 🔧 Technical Details

### Built With
- **Tkinter**: Python's built-in GUI framework
- **Threading**: Background processing for AI responses
- **Modern Styling**: Custom ttk styles and color schemes

### Performance
- **One-time Loading**: Models load only once at startup
- **Memory Efficient**: Optimized for smooth performance
- **Responsive**: Non-blocking UI during processing

### Compatibility
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Python 3.7+**: Compatible with modern Python versions
- **No Additional Dependencies**: Uses only standard libraries for GUI

## 🆘 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Run: `python3 -m pip install -r requirements.txt`

2. **GUI doesn't start**
   - Check Python version: `python3 --version` (needs 3.7+)
   - Try: `python3 launch_gui.py` for automatic dependency checking

3. **Slow performance**
   - First launch takes longer (loading AI models)
   - Subsequent questions are much faster

4. **Window not visible**
   - Check if window is minimized or behind other windows
   - Try Alt+Tab (Windows/Linux) or Cmd+Tab (macOS)

### Getting Help

If you encounter issues:
1. Check the status indicator in the header
2. Look at the status bar for error messages
3. Try restarting the application
4. Check that all dependencies are installed

## 🎉 Enjoy Your Academic Journey!

The Brown Course Advisor GUI is designed to make course planning easy, intuitive, and enjoyable. Ask questions naturally, explore course recommendations, and get the academic guidance you need!