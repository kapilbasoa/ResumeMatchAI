import streamlit as st
import fitz
from job_matcher.explainable_matcher import calculate_fit_score, extract_top_keywords
from job_matcher.batch_ranker import rank_candidates
from job_matcher.missing_keywords import find_missing_keywords
from resume_parser.experience_extractor import extract_experience_by_domain
from job_matcher.resume_suggestions import suggest_enhancements
# Set dark page config
st.set_page_config(page_title="Resume Matcher AI", page_icon="📄", layout="wide")
# Enhanced resume suggestions mapping
SUGGESTION_MAP = {
    'python': "Highlight your experience programming with Python for data analysis, automation, or application development.",
    'aws': "Mention your hands-on experience with AWS cloud services and deployments.",
    'machine learning': "Describe your involvement in machine learning projects, models, or algorithm development.",
    'deep learning': "Showcase your work using deep learning frameworks and neural networks.",
    'nlp': "Include projects related to natural language processing or text analytics.",
    'scikit': "Emphasize your skills with scikit-learn for building and evaluating machine learning models.",
    'xgboost': "Highlight experience tuning or deploying XGBoost models for improved predictions.",
    'cloud': "Detail your expertise with cloud platforms and infrastructure management.",
    'data': "Provide examples of your work with data collection, cleaning, and exploratory analysis.",
    'sql': "Include your proficiency with SQL databases and query optimization.",
    # Add other domain-specific suggestions here
}

def suggest_enhancements(resume_text, job_description, top_n=10):
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([job_description])
    jd_keywords = set(vectorizer.get_feature_names_out())

    resume_words = set(resume_text.lower().split())
    missing_keywords = list(jd_keywords - resume_words)

    suggestions = []
    count = 0
    for word in missing_keywords:
        if count >= top_n:
            break
        key = word.lower()
        if key in SUGGESTION_MAP:
            suggestions.append(SUGGESTION_MAP[key])
        else:
            suggestions.append(f"Consider highlighting your experience or familiarity with '{word}'.")
        count += 1
    return suggestions

# Set dark page config
st.set_page_config(page_title="Resume Matcher AI", page_icon="📄", layout="wide")

# Custom CSS for dark theme
st.markdown("""
<style>
body {
    background-color: #0f1117;
    color: #f0f0f0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1, h2, h3 {
    color: #ffffff;
}
.sidebar .sidebar-content {
    background-color: #1f222e;
}
.metric {
    color: #ffffff;
}
.stButton>button {
    color: #ffffff;
    background-color: #262730;
    border: 1px solid #444;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #333645;
}
hr {
    border-top: 1px solid #444;
    margin-top: 16px;
    margin-bottom: 16px;
}
.stTextArea textarea {
    background-color: #1a1f2a !important;
    color: #f0f0f0 !important;
    border: 1.5px solid #33364a !important;
    border-radius: 6px;
    font-size: 16px;
    padding: 8px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("static/logo.png", width=180)
    st.title("Resume Matcher AI")
    st.markdown("A smart AI-powered resume matching system.")
    st.markdown("---")
    st.write("Built by Kapil")

# Title
st.title("📄 AI Resume Matcher Dashboard")
st.markdown("---")

# Resume uploader + JD input in two columns
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_files = st.file_uploader(
        "📤 Upload Resumes (PDF)", 
        type=["pdf"], 
        accept_multiple_files=True
    )

with col2:
    job_description = st.text_area(
        "📑 Paste Job Description", 
        height=200
    )

# Process resumes
if uploaded_files and job_description:
    resume_texts = []
    for file in uploaded_files:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = "".join(page.get_text() for page in doc)
        resume_texts.append((file.name, text))

    st.markdown("---")
    st.subheader("🏆 Top 3 Candidates")

    top_scores = rank_candidates(resume_texts, job_description)
    for name, score in top_scores:
        st.write(f"**{name}** — {score}% match")

    st.markdown("---")
    st.subheader("📈 Resume Insights")

    for name, text in resume_texts:
        with st.container():
            st.markdown(f"### 📋 {name}")

            score = calculate_fit_score(text, job_description)

            # Display progress bar and metric
            st.write("**Fit Score:**")
            st.progress(int(score))
            st.metric(label="Fit Score (%)", value=f"{score}%")

            if score >= 75:
                st.success(f"Excellent Fit: {score}%")
            elif score >= 60:
                st.write(f"Fit Score: {score}%")
            else:
                st.error(f"Low Fit: {score}%")

            top_keywords = extract_top_keywords(text, job_description)
            st.write(f"**Top Keywords:** {', '.join(top_keywords)}")

            missing_keywords = find_missing_keywords(text, job_description)
            st.write(f"**Missing Keywords:** {', '.join(missing_keywords)}")

            exp = extract_experience_by_domain(text)
            if exp:
                st.write("**Experience by Domain (yrs):**")
                st.write(exp)
            else:
                st.write("_No domain-specific experience found._")

            enhancements = suggest_enhancements(text, job_description)
            if enhancements:
                st.markdown("**Resume Improvement Suggestions:**")
                for sugg in enhancements:
                    st.write(f"- {sugg}")
            else:
                st.success("No further suggestions — strong alignment!")
            st.markdown("---")
else:
    st.info("Please upload at least one resume and enter a job description to begin.")