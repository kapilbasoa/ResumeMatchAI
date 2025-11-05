from sklearn.feature_extraction.text import TfidfVectorizer

def suggest_enhancements(resume_text, job_description, top_n=10):
    # Extract keywords from JD
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([job_description])
    feature_names = vectorizer.get_feature_names_out()
    jd_keywords = set(feature_names)

    # Resume text words
    resume_words = set(resume_text.lower().split())

    # Find missing keywords
    missing_keywords = list(jd_keywords - resume_words)

    # Suggest enhancement phrases
    suggestions = []
    for word in missing_keywords[:top_n]:
        suggestions.append(f"Consider adding a line highlighting your experience or familiarity with '{word}'.")

    return suggestions
