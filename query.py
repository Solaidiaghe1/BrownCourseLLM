import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import subprocess
import openai
import os
import sys


os.environ["TOKENIZERS_PARALLELISM"] = "false"
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("❌ OPENAI_API_KEY is not set. Please export your API key, e.g.:\n   export OPENAI_API_KEY='sk-...'")
    sys.exit(1)

class BrownCourseAdvisor:
    def __init__(self):
        """Initialize the advisor with all necessary components loaded once."""
        print("🤖 Initializing Brown Course Advisor...")
        
        # Load courses data
        with open('data/courses.json', 'r') as f:
            self.courses = json.load(f)
        
        # Check if embeddings need to be regenerated
        with open('data/course_index.json', 'r') as f:
            course_embeddings = json.load(f)
        
        if len(course_embeddings) != len(self.courses):
            print("🔄 Reembedding courses...")
            subprocess.run(["python", "embed.py"])
            print("✅ Reembedding done.")
        
        # Load FAISS index and model (only once!)
        print("📚 Loading course index...")
        self.index = faiss.read_index('data/course_index.faiss')
        
        print("🧠 Loading AI model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize conversation history
        self.conversation_history = []
        
        print("✅ Brown Course Advisor ready! Type 'quit', 'exit', or 'bye' to end the session.\n")
>>>>>>> b3ce760 (new gui)
    
    def ask_chat(self, question, course_list, conversation_context=""):
        """Enhanced chat function with conversation context."""
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
        for entry in self.conversation_history[-4:]:  # Keep last 4 exchanges for context
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
    
    def display_info(self, course, question):
        """Display course information based on question keywords."""
        question = question.lower()
        output = f"📖 {course['title']}"

        if "prerequisite" in question or "requirement" in question:
            prereq = course.get("prerequisites", "Not specified")
            output += f"\n   Prerequisites: {prereq}"

        elif "semester" in question or "offered" in question or "when" in question:
            sem = course.get("semester", "Not listed")
            output += f"\n   Offered: {sem}"

        else:
            # This is the default if no keyword is hit
            output += f"\n   Description: {course['description']}"

        return output
    
    def ask_question(self, question: str, k=3):
        """Process a question and return recommendations."""
        try:
            # Encode question
            vector = self.model.encode(question)
            _, indices = self.index.search(np.array([vector]), k)
            
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
            
            return advice, course_list
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error processing your question: {str(e)}"
            return error_msg, []
    
    def run_interactive_session(self):
        """Run the interactive question-answering session."""
        print("🎓 Welcome to the Brown Course Advisor!")
        print("Ask me anything about courses, prerequisites, schedules, or academic planning.\n")
        
        while True:
            try:
                # Get user input
                question = input("❓ Ask a question about courses (or 'quit' to exit): ").strip()
                
                # Check for exit commands
                if question.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\n👋 Thanks for using the Brown Course Advisor! Good luck with your studies!")
                    break
                
                if not question:
                    print("Please enter a question or type 'quit' to exit.")
                    continue
                
                # Process the question
                print("\n🤔 Thinking...")
                advice, courses = self.ask_question(question)
                
                # Display results
                print("\n" + "="*60)
                print("🎯 AI Advisor Advice (Triple A)")
                print("="*60)
                print(advice)
                
                if courses:
                    print("\n📚 Relevant Courses Found:")
                    for i, course in enumerate(courses[:3], 1):
                        print(f"\n{i}. {self.display_info(course, question)}")
                
                print("\n" + "="*60)
                print("💡 You can ask follow-up questions or type 'quit' to exit.\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using the Brown Course Advisor! Good luck with your studies!")
                break
            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {str(e)}")
                print("Please try again or type 'quit' to exit.\n")

# Initialize and run the advisor
advisor = BrownCourseAdvisor()
advisor.run_interactive_session()