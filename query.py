import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import subprocess
import openai

openai.api_key = ""
with open('data/courses.json', 'r') as f:
    courses = json.load(f)

with open('data/course_index.json', 'r') as f:
    course_embeddings = json.load(f)

if len(course_embeddings) != len(courses):
    print("Reembedding courses...")
    subprocess.run(["python", "embed.py"])
    print("Reembedding done.")


index = faiss.read_index('data/course_index.faiss')
model = SentenceTransformer('all-MiniLM-L6-v2')

def askChat(question, course):
    prompt = f"""You're an academic advisor at Brown. Use the course data below to recommend helpful courses. Be smart, kind, and specific.
    COURSES :
    {json.dumps(course, indent=2)}

    QUESTION:
    {question} 
    """
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages = [
                                                {"role": "system", "content": "You are a helpful Brown University academic advisor."},
                                                {"role": "user", "content": prompt}
                                            ],
                                            temperature=0.7,
                                            max_tokens = 500
    )
    return response['choices'][0]['message']['content']

#This is not working yet becuase keys are not in the data set
def display_info(course, question):
    question = question.lower()
    output = f"{course['title']}"

    if "prerequisite" in question or "requirement" in question:
        prereq = course["prerequisites"]
        output += f"\n Prerequisites: {prereq}"

    elif "semester" in question or "offered" in question or "when" in question:
        sem = course.get("semester", "Not listed")
        output += f"\n Offered: {sem}"

    else:
        # This the default if no key word is hit
        output += f"\n  Description: {course['description']}"

    print(output)
##############################

def ask_question(question: str, k = 1):
    vector = model.encode(question)
    _, indices = index.search(np.array([vector]), k)
    print('Top 3 courses: \n')
    courseList = [courses[i] for i in indices[0]]
    advice = askChat(question, courseList)
    print("\n" + advice)
    
asking = input("Ask a question about courses: \n")
ask_question(asking)