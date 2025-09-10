import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import threading
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import subprocess
import openai
import os
from datetime import datetime
import time

# Configure OpenAI
os.environ["TOKENIZERS_PARALLELISM"] = "false"
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    # Show a friendly message box if running GUI without key
    try:
        tk.Tk().withdraw()
        messagebox.showerror("Missing API Key",
                             "OPENAI_API_KEY is not set. Please export it in your shell (e.g.\nexport OPENAI_API_KEY='sk-...') and relaunch.")
    except Exception:
        pass
    raise SystemExit("OPENAI_API_KEY environment variable is required.")

class BrownCourseAdvisorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.setup_variables()
        self.setup_ui()
        self.setup_advisor()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("🎓 Brown Course Advisor - AI-Powered Academic Guidance")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        self.root.configure(bg='#f8f9fa')
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
    
    def setup_styles(self):
        """Define modern color scheme and styles"""
        self.colors = {
            'primary': '#2c3e50',      # Dark blue-gray
            'secondary': '#3498db',     # Bright blue
            'accent': '#e74c3c',        # Red accent
            'success': '#27ae60',       # Green
            'warning': '#f39c12',       # Orange
            'background': '#f8f9fa',    # Light gray
            'surface': '#ffffff',       # White
            'text_primary': '#2c3e50',  # Dark text
            'text_secondary': '#7f8c8d', # Gray text
            'border': '#bdc3c7',        # Light border
            'hover': '#ecf0f1'          # Light hover
        }
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['secondary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))
        
        style.map('Primary.TButton',
                 background=[('active', '#2980b9'),
                           ('pressed', '#21618c')])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       font=('Segoe UI', 9, 'bold'))
        
        style.configure('Danger.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 9, 'bold'))
    
    def setup_variables(self):
        """Initialize application variables"""
        self.conversation_history = []
        self.is_loading = False
        self.advisor = None
        self.courses = None
        self.index = None
        self.model = None
    
    def setup_ui(self):
        """Create the main user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Main content area
        content_frame = tk.Frame(main_frame, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        # Left panel - Chat area
        self.create_chat_panel(content_frame)
        
        # Right panel - Course info
        self.create_course_panel(content_frame)
        
        # Bottom panel - Input area
        self.create_input_panel(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create the application header"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame,
                              text="🎓 Brown Course Advisor",
                              font=('Segoe UI', 24, 'bold'),
                              fg='white',
                              bg=self.colors['primary'])
        title_label.pack(side='left', padx=20, pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="AI-Powered Academic Guidance",
                                 font=('Segoe UI', 12),
                                 fg='#bdc3c7',
                                 bg=self.colors['primary'])
        subtitle_label.pack(side='left', padx=(10, 0), pady=20)
        
        # Status indicator
        self.status_indicator = tk.Label(header_frame,
                                        text="● Initializing...",
                                        font=('Segoe UI', 10),
                                        fg=self.colors['warning'],
                                        bg=self.colors['primary'])
        self.status_indicator.pack(side='right', padx=20, pady=20)
    
    def create_chat_panel(self, parent):
        """Create the chat conversation panel"""
        # Chat container
        chat_frame = tk.Frame(parent, bg=self.colors['surface'], relief='solid', bd=1)
        chat_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Chat header
        chat_header = tk.Frame(chat_frame, bg=self.colors['primary'], height=50)
        chat_header.pack(fill='x')
        chat_header.pack_propagate(False)
        
        chat_title = tk.Label(chat_header,
                             text="💬 Conversation",
                             font=('Segoe UI', 14, 'bold'),
                             fg='white',
                             bg=self.colors['primary'])
        chat_title.pack(pady=15)
        
        # Chat messages area
        self.chat_display = scrolledtext.ScrolledText(chat_frame,
                                                     wrap=tk.WORD,
                                                     font=('Segoe UI', 10),
                                                     bg=self.colors['surface'],
                                                     fg=self.colors['text_primary'],
                                                     relief='flat',
                                                     state='disabled',
                                                     padx=15,
                                                     pady=10)
        self.chat_display.pack(fill='both', expand=True)
        
        # Configure text tags for styling
        self.chat_display.tag_configure('user', foreground=self.colors['secondary'], font=('Segoe UI', 10, 'bold'))
        self.chat_display.tag_configure('assistant', foreground=self.colors['text_primary'], font=('Segoe UI', 10))
        self.chat_display.tag_configure('timestamp', foreground=self.colors['text_secondary'], font=('Segoe UI', 8))
        self.chat_display.tag_configure('loading', foreground=self.colors['warning'], font=('Segoe UI', 10, 'italic'))
    
    def create_course_panel(self, parent):
        """Create the course information panel"""
        # Course container
        course_frame = tk.Frame(parent, bg=self.colors['surface'], relief='solid', bd=1, width=400)
        course_frame.pack(side='right', fill='y')
        course_frame.pack_propagate(False)
        
        # Course header
        course_header = tk.Frame(course_frame, bg=self.colors['success'], height=50)
        course_header.pack(fill='x')
        course_header.pack_propagate(False)
        
        course_title = tk.Label(course_header,
                               text="📚 Recommended Courses",
                               font=('Segoe UI', 14, 'bold'),
                               fg='white',
                               bg=self.colors['success'])
        course_title.pack(pady=15)
        
        # Course list area
        self.course_display = scrolledtext.ScrolledText(course_frame,
                                                       wrap=tk.WORD,
                                                       font=('Segoe UI', 9),
                                                       bg=self.colors['surface'],
                                                       fg=self.colors['text_primary'],
                                                       relief='flat',
                                                       state='disabled',
                                                       padx=15,
                                                       pady=10)
        self.course_display.pack(fill='both', expand=True)
        
        # Configure text tags for course styling
        self.course_display.tag_configure('course_title', foreground=self.colors['primary'], font=('Segoe UI', 11, 'bold'))
        self.course_display.tag_configure('course_code', foreground=self.colors['secondary'], font=('Segoe UI', 10, 'bold'))
        self.course_display.tag_configure('course_desc', foreground=self.colors['text_primary'], font=('Segoe UI', 9))
        self.course_display.tag_configure('course_prereq', foreground=self.colors['warning'], font=('Segoe UI', 9))
        self.course_display.tag_configure('course_instructor', foreground=self.colors['text_secondary'], font=('Segoe UI', 9, 'italic'))
    
    def create_input_panel(self, parent):
        """Create the input area for user questions"""
        input_frame = tk.Frame(parent, bg=self.colors['background'])
        input_frame.pack(fill='x', pady=(20, 0))
        
        # Input container
        input_container = tk.Frame(input_frame, bg=self.colors['surface'], relief='solid', bd=1)
        input_container.pack(fill='x', padx=0)
        
        # Question input
        self.question_entry = tk.Text(input_container,
                                     height=3,
                                     font=('Segoe UI', 10),
                                     bg=self.colors['surface'],
                                     fg=self.colors['text_primary'],
                                     relief='flat',
                                     wrap=tk.WORD,
                                     padx=15,
                                     pady=10)
        self.question_entry.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Send button
        self.send_button = ttk.Button(input_container,
                                     text="Send\n💬",
                                     command=self.send_question,
                                     style='Primary.TButton')
        self.send_button.pack(side='right', padx=(0, 15), pady=10)
        
        # Bind Enter key to send
        self.question_entry.bind('<Control-Return>', lambda e: self.send_question())
        
        # Placeholder text
        self.question_entry.insert('1.0', "Ask me anything about courses, prerequisites, schedules, or academic planning...")
        self.question_entry.configure(fg=self.colors['text_secondary'])
        self.question_entry.bind('<FocusIn>', self.clear_placeholder)
        self.question_entry.bind('<FocusOut>', self.add_placeholder)
    
    def create_status_bar(self, parent):
        """Create the status bar at the bottom"""
        status_frame = tk.Frame(parent, bg=self.colors['primary'], height=30)
        status_frame.pack(fill='x', pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame,
                                    text="Ready to help with your academic journey! 🚀",
                                    font=('Segoe UI', 9),
                                    fg='white',
                                    bg=self.colors['primary'])
        self.status_label.pack(side='left', padx=20, pady=5)
        
        # Progress bar (hidden by default)
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(side='right', padx=20, pady=5)
        self.progress.pack_forget()
    
    def clear_placeholder(self, event):
        """Clear placeholder text when user focuses on input"""
        if self.question_entry.get('1.0', 'end-1c') == "Ask me anything about courses, prerequisites, schedules, or academic planning...":
            self.question_entry.delete('1.0', 'end')
            self.question_entry.configure(fg=self.colors['text_primary'])
    
    def add_placeholder(self, event):
        """Add placeholder text if input is empty"""
        if not self.question_entry.get('1.0', 'end-1c').strip():
            self.question_entry.insert('1.0', "Ask me anything about courses, prerequisites, schedules, or academic planning...")
            self.question_entry.configure(fg=self.colors['text_secondary'])
    
    def setup_advisor(self):
        """Initialize the course advisor in a separate thread"""
        def init_advisor():
            try:
                self.update_status("Loading course data...", self.colors['warning'])
                
                # Load courses data
                with open('data/courses.json', 'r') as f:
                    self.courses = json.load(f)
                
                # Check if embeddings need to be regenerated
                with open('data/course_index.json', 'r') as f:
                    course_embeddings = json.load(f)
                
                if len(course_embeddings) != len(self.courses):
                    self.update_status("Regenerating embeddings...", self.colors['warning'])
                    subprocess.run(["python3", "embed.py"])
                
                self.update_status("Loading AI model...", self.colors['warning'])
                
                # Load FAISS index and model
                self.index = faiss.read_index('data/course_index.faiss')
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                
                self.update_status("Ready to help! 🎓", self.colors['success'])
                self.add_welcome_message()
                
            except Exception as e:
                self.update_status(f"Error: {str(e)}", self.colors['accent'])
                messagebox.showerror("Initialization Error", f"Failed to initialize the advisor:\n{str(e)}")
        
        # Run initialization in background thread
        threading.Thread(target=init_advisor, daemon=True).start()
    
    def update_status(self, message, color=None):
        """Update the status indicator"""
        if color:
            self.status_indicator.configure(fg=color)
        self.status_indicator.configure(text=f"● {message}")
        self.status_label.configure(text=message)
        self.root.update_idletasks()
    
    def add_welcome_message(self):
        """Add welcome message to chat"""
        welcome_text = """🎓 Welcome to the Brown Course Advisor!

I'm here to help you with:
• Course recommendations and information
• Prerequisites and requirements
• Academic planning and scheduling
• Degree requirements and pathways

Ask me anything about courses, and I'll provide personalized advice based on your interests and academic goals!"""
        
        self.add_message("assistant", welcome_text)
    
    def add_message(self, sender, message, courses=None):
        """Add a message to the chat display"""
        self.chat_display.configure(state='normal')
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert('end', f"[{timestamp}] ", 'timestamp')
        
        # Add sender and message
        if sender == 'user':
            self.chat_display.insert('end', "You: ", 'user')
        else:
            self.chat_display.insert('end', "Advisor: ", 'assistant')
        
        self.chat_display.insert('end', f"{message}\n\n", 'assistant' if sender == 'assistant' else 'user')
        
        # Add course information if provided
        if courses and sender == 'assistant':
            self.display_courses(courses)
        
        self.chat_display.configure(state='disabled')
        self.chat_display.see('end')
    
    def display_courses(self, courses):
        """Display recommended courses in the course panel"""
        self.course_display.configure(state='normal')
        self.course_display.delete('1.0', 'end')
        
        if not courses:
            self.course_display.insert('end', "No courses found for this query.", 'course_desc')
        else:
            for i, course in enumerate(courses[:5], 1):  # Show top 5 courses
                # Course title and code
                self.course_display.insert('end', f"{i}. ", 'course_code')
                self.course_display.insert('end', f"{course.get('title', 'Unknown Title')}\n", 'course_title')
                
                # Course code
                if 'course code' in course:
                    self.course_display.insert('end', f"   Code: {course['course code']}\n", 'course_code')
                
                # Instructor
                if 'instructor' in course:
                    self.course_display.insert('end', f"   Instructor: {course['instructor']}\n", 'course_instructor')
                
                # Prerequisites
                if 'prerequisites' in course and course['prerequisites']:
                    self.course_display.insert('end', f"   Prerequisites: {course['prerequisites']}\n", 'course_prereq')
                
                # Description
                if 'description' in course:
                    desc = course['description'][:200] + "..." if len(course['description']) > 200 else course['description']
                    self.course_display.insert('end', f"   {desc}\n", 'course_desc')
                
                self.course_display.insert('end', "\n" + "─"*50 + "\n\n", 'course_desc')
        
        self.course_display.configure(state='disabled')
    
    def send_question(self):
        """Send user question to the advisor"""
        question = self.question_entry.get('1.0', 'end-1c').strip()
        
        if not question or question == "Ask me anything about courses, prerequisites, schedules, or academic planning...":
            return
        
        if self.is_loading or not self.model:
            return
        
        # Clear input
        self.question_entry.delete('1.0', 'end')
        self.add_placeholder(None)
        
        # Add user message
        self.add_message('user', question)
        
        # Show loading state
        self.set_loading_state(True)
        
        # Process question in background thread
        threading.Thread(target=self.process_question, args=(question,), daemon=True).start()
    
    def process_question(self, question):
        """Process the user's question"""
        try:
            # Encode question
            vector = self.model.encode(question)
            _, indices = self.index.search(np.array([vector]), 3)
            
            # Get relevant courses
            course_list = [self.courses[i] for i in indices[0]]
            
            # Generate advice
            conversation_context = "Previous conversation context: " + " ".join([f"Q: {entry['question']} A: {entry['response'][:100]}..." for entry in self.conversation_history[-2:]])
            advice = self.ask_chat(question, course_list, conversation_context)
            
            # Store in conversation history
            self.conversation_history.append({
                "question": question,
                "response": advice,
                "courses": course_list
            })
            
            # Update UI in main thread
            self.root.after(0, lambda: self.display_response(advice, course_list))
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.root.after(0, lambda: self.display_response(error_msg, []))
        finally:
            self.root.after(0, lambda: self.set_loading_state(False))
    
    def ask_chat(self, question, course_list, conversation_context=""):
        """Generate AI response"""
        prompt = f"""You're an academic advisor at Brown University. Use the course data below to recommend helpful courses. Be smart, kind, and specific.
        
        {conversation_context}
        
        COURSES:
        {json.dumps(course_list, indent=2)}

        QUESTION:
        {question} 
        """
        
        messages = [
            {"role": "system", "content": "You are a helpful Brown University academic advisor. Provide specific, actionable course recommendations based on the student's questions."}
        ]
        
        # Add conversation history for context
        for entry in self.conversation_history[-4:]:
            messages.append({"role": "user", "content": entry["question"]})
            messages.append({"role": "assistant", "content": entry["response"]})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. Please try again."
    
    def display_response(self, response, courses):
        """Display the AI response"""
        self.add_message('assistant', response, courses)
    
    def set_loading_state(self, loading):
        """Set loading state for UI elements"""
        self.is_loading = loading
        
        if loading:
            self.send_button.configure(state='disabled')
            self.progress.pack(side='right', padx=20, pady=5)
            self.progress.start()
            self.update_status("Thinking... 🤔", self.colors['warning'])
        else:
            self.send_button.configure(state='normal')
            self.progress.pack_forget()
            self.progress.stop()
            self.update_status("Ready to help! 🎓", self.colors['success'])
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BrownCourseAdvisorGUI()
    app.run()