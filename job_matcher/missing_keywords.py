from sklearn.feature_extraction.text import TfidfVectorizer

def find_missing_keywords(resume_text, job_description, top_n=10):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([job_description])
    feature_names = vectorizer.get_feature_names_out()

    jd_keywords = feature_names.tolist()
    resume_words = resume_text.lower().split()

    missing = [word for word in jd_keywords if word not in resume_words]
    return missing[:top_n]
