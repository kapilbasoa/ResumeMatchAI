import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_info(text):
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\+?\d[\d\s\-]{8,}\d', text)
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    return {
        "Name": names[0] if names else "Not Found",
        "Email": email[0] if email else "Not Found",
        "Phone": phone[0] if phone else "Not Found"
    }