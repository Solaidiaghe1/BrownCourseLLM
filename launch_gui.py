#!/usr/bin/env python3
"""
Brown Course Advisor GUI Launcher
A beautiful, user-friendly interface for the Brown Course Advisor
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'sentence_transformers',
        'faiss',
        'openai',
        'numpy',
        'tkinter'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'faiss':
                import faiss
            elif package == 'tkinter':
                import tkinter
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    return True

def main():
    """Main launcher function"""
    print("🎓 Brown Course Advisor GUI Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('data/courses.json'):
        print("❌ Error: courses.json not found!")
        print("   Please run this script from the OurLLM directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to install dependencies. Please install manually:")
        print("   pip install -r requirements.txt")
        return
    
    # Launch the GUI
    print("🚀 Launching Brown Course Advisor GUI...")
    try:
        from gui_app import BrownCourseAdvisorGUI
        app = BrownCourseAdvisorGUI()
        app.run()
    except Exception as e:
        print(f"❌ Failed to launch GUI: {e}")
        print("   Please check that all dependencies are installed correctly.")

if __name__ == "__main__":
    main()