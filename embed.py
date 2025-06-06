print("Running embed.py")
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
print("Loading courses...")
with open('data/courses.json', 'r') as f:
    courses = json.load(f)
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
texts = [f"{c['course code']} - {c['title']}: {c['description']} Instructor: {c['instructor']}" for c in courses]

embeddings = model.encode(texts)
print("Creating embeddings...")
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))
print("Building FAISS index...")
faiss.write_index(index, 'data/course_index.faiss') 
print("Saving metadata...")
with open('data/course_index.json', 'w') as f: 
    json.dump(courses, f)
print("✅ Done! All files saved.")