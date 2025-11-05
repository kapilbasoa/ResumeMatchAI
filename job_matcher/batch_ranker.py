from .explainable_matcher import calculate_fit_score

def rank_candidates(resume_texts, job_description):
    scores = []
    for name, text in resume_texts:
        score = calculate_fit_score(text, job_description)
        scores.append((name, score))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:3]  # Top 3 candidates
