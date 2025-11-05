from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    return text

def extract_top_keywords(resume_text, job_description, top_n=8):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([resume_text, job_description])
    feature_names = vectorizer.get_feature_names_out()

    resume_vec, jd_vec = tfidf.toarray()

    overlap_indices = np.where((resume_vec > 0) & (jd_vec > 0))[0]
    keywords_with_scores = [(feature_names[i], jd_vec[i] + resume_vec[i]) for i in overlap_indices]
    keywords_with_scores.sort(key=lambda x: x[1], reverse=True)

    top_keywords = [kw for kw, _ in keywords_with_scores[:top_n]]
    return top_keywords

def calculate_fit_score(resume_text, job_description):
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    embeddings = model.encode([resume_text, job_description])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
    return round(float(similarity[0][0]) * 100, 2)
