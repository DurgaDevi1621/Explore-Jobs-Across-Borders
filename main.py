from flask import Flask, request, jsonify
import re

app = Flask(_name_)

# Sample job listings (in real app, fetch from external APIs)
job_listings = [
    {"id": 1, "title": "Python Developer", "skills": ["python", "django", "rest"]},
    {"id": 2, "title": "Frontend Engineer", "skills": ["javascript", "react", "css"]},
    {"id": 3, "title": "Data Scientist", "skills": ["python", "machine learning", "nlp"]},
    {"id": 4, "title": "DevOps Engineer", "skills": ["aws", "docker", "kubernetes"]},
]

# Simple list of keywords to detect skills
skill_keywords = ["python", "django", "rest", "javascript", "react", "css",
                  "machine learning", "nlp", "aws", "docker", "kubernetes"]

def extract_skills(text):
    text = text.lower()
    found_skills = set()
    for skill in skill_keywords:
        # Simple substring match - can be improved with NLP
        if skill in text:
            found_skills.add(skill)
    return list(found_skills)

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Read file text (for simplicity, assuming text file or small PDF converted to text)
    text = file.read().decode('utf-8', errors='ignore')

    # Extract skills
    skills = extract_skills(text)
    if not skills:
        return jsonify({"message": "No matching skills found in resume."}), 200

    # Match jobs by checking if job requires any skill found in resume
    matched_jobs = []
    for job in job_listings:
        if any(skill in job['skills'] for skill in skills):
            matched_jobs.append(job)

    return jsonify({
        "extracted_skills": skills,
        "matched_jobs": matched_jobs
    })

if _name_ == '_main_':
    app.run(debug=True)
