#!/usr/bin/env python3
"""
Brown Course Advisor GUI Demo
Demonstrates the key features of the GUI application
"""

import tkinter as tk
from tkinter import messagebox
import webbrowser

def show_demo():
    """Show a demo of the GUI features"""
    root = tk.Tk()
    root.title("🎓 Brown Course Advisor - Feature Demo")
    root.geometry("800x600")
    root.configure(bg='#f8f9fa')
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (800 // 2)
    y = (root.winfo_screenheight() // 2) - (600 // 2)
    root.geometry(f"800x600+{x}+{y}")
    
    # Header
    header = tk.Frame(root, bg='#2c3e50', height=80)
    header.pack(fill='x')
    header.pack_propagate(False)
    
    title = tk.Label(header, text="🎓 Brown Course Advisor GUI", 
                    font=('Segoe UI', 24, 'bold'), fg='white', bg='#2c3e50')
    title.pack(pady=20)
    
    # Content
    content = tk.Frame(root, bg='#f8f9fa')
    content.pack(fill='both', expand=True, padx=40, pady=20)
    
    # Features list
    features = [
        "🎨 Modern, Professional Design",
        "💬 Natural Chat Interface",
        "📚 Rich Course Information Display",
        "⚡ Fast, Responsive Performance",
        "🔄 Seamless Follow-up Questions",
        "📱 Responsive Layout",
        "🎯 Smart Input with Placeholders",
        "⏱️ Real-time Status Updates",
        "🎨 Beautiful Color Scheme",
        "🛡️ Robust Error Handling"
    ]
    
    for i, feature in enumerate(features):
        feature_frame = tk.Frame(content, bg='#ffffff', relief='solid', bd=1)
        feature_frame.pack(fill='x', pady=5)
        
        feature_label = tk.Label(feature_frame, text=feature, 
                               font=('Segoe UI', 12), fg='#2c3e50', bg='#ffffff')
        feature_label.pack(pady=10, padx=20, anchor='w')
    
    # Buttons
    button_frame = tk.Frame(content, bg='#f8f9fa')
    button_frame.pack(fill='x', pady=20)
    
    def launch_gui():
        root.destroy()
        import subprocess
        subprocess.Popen(['python3', 'gui_app.py'])
    
    def launch_cli():
        root.destroy()
        import subprocess
        subprocess.Popen(['python3', 'query.py'])
    
    def show_help():
        messagebox.showinfo("Help", 
                           "Brown Course Advisor GUI\n\n"
                           "Features:\n"
                           "• Beautiful, modern interface\n"
                           "• Natural chat conversation\n"
                           "• Rich course information\n"
                           "• Fast, responsive performance\n\n"
                           "Usage:\n"
                           "1. Type your question in the input area\n"
                           "2. Press Send or Ctrl+Enter\n"
                           "3. View AI response and course recommendations\n"
                           "4. Ask follow-up questions naturally")
    
    launch_btn = tk.Button(button_frame, text="🚀 Launch GUI", 
                          command=launch_gui, font=('Segoe UI', 12, 'bold'),
                          bg='#3498db', fg='white', padx=20, pady=10)
    launch_btn.pack(side='left', padx=10)
    
    cli_btn = tk.Button(button_frame, text="💻 Launch CLI", 
                       command=launch_cli, font=('Segoe UI', 12, 'bold'),
                       bg='#95a5a6', fg='white', padx=20, pady=10)
    cli_btn.pack(side='left', padx=10)
    
    help_btn = tk.Button(button_frame, text="❓ Help", 
                        command=show_help, font=('Segoe UI', 12, 'bold'),
                        bg='#27ae60', fg='white', padx=20, pady=10)
    help_btn.pack(side='left', padx=10)
    
    # Footer
    footer = tk.Frame(root, bg='#2c3e50', height=40)
    footer.pack(fill='x')
    
    footer_text = tk.Label(footer, text="Choose your preferred interface above", 
                          font=('Segoe UI', 10), fg='white', bg='#2c3e50')
    footer_text.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    show_demo()