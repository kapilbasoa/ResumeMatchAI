from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    return text
 
def extract_core_sections(text):
    skills = re.findall(r'(Skills|SKILLS|Technical Skills)(.*?)Education', text, re.DOTALL)
    projects = re.findall(r'(Projects|PROJECTS)(.*?)Certifications', text, re.DOTALL)

    skills_text = skills[0][1] if skills else ""
    projects_text = projects[0][1] if projects else ""

    return skills_text, projects_text

def calculate_fit_score(resume_text, job_description):
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    skills_text, projects_text = extract_core_sections(resume_text)

    weighted_resume = (skills_text + ' ') * 2 + (projects_text + ' ') * 2 + resume_text

    embeddings = model.encode([weighted_resume, job_description])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
    return round(float(similarity[0][0]) * 100, 2)