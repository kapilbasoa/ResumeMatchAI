import re

def extract_experience_by_domain(text):
    domains = ['machine learning', 'data science', 'nlp', 'cloud', 'deep learning', 'computer vision']
    experience = {}

    for domain in domains:
        pattern = re.compile(r'(\d+(?:\.\d+)?(?:\s+)?(?:years|months))\s+(?:experience\s+in|on)\s+' + re.escape(domain), re.IGNORECASE)
        matches = pattern.findall(text)
        
        total_months = 0
        for match in matches:
            value, unit = re.findall(r'(\d+(?:\.\d+)?)\s*(years|months)', match)[0]
            months = float(value) * 12 if 'year' in unit else float(value)
            total_months += months

        if total_months > 0:
            experience[domain] = round(total_months / 12, 2)

    return experience
