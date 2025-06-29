import pandas as pd
import spacy
import re
from rapidfuzz import process, fuzz

# Load dataset
df = pd.read_csv("clinical_notes_dataset.csv")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Abbreviation dictionary
abbrev_map = {
    "pt": "Patient",
    "c/o": "complains of",
    "sob": "shortness of breath",
    "bp↑↑": "blood pressure elevated",
    "hx": "history of",
    "dm": "diabetes mellitus",
    "rx": "prescribed",
    "sev": "severe",
    "abd": "abdominal",
    "poss.": "possible",
    "poss": "possible",
    "cp": "chest pain",
    "w/": "with",
    "htn": "hypertension",
    "uri": "upper respiratory infection",
    "dm pt": "patient with diabetes mellitus",
    "febrile": "has fever",
    "sob at night": "experiences shortness of breath at night",
    "ckd": "chronic kidney disease",
    "hb": "hemoglobin",
    "wbc": "white blood cells",
    "gerd": "gastroesophageal reflux disease"
}

known_abbrs = list(abbrev_map.keys())

# Fuzzy matching fallback
def fuzzy_expand(word):
    match_tuple = process.extractOne(word, known_abbrs, scorer=fuzz.ratio)
    if match_tuple:
        match, score = match_tuple[0], match_tuple[1]
        return abbrev_map[match] if score > 85 else word
    else:
        return word

# Combined refinement
def refine_with_spacy_and_fuzzy(note):
    text = note.lower()
    tokens = re.split(r'[ ,]+', text)
    expanded_tokens = [abbrev_map.get(tok, fuzzy_expand(tok)) for tok in tokens]
    expanded_text = " ".join(expanded_tokens)

    doc = nlp(expanded_text)
    sentences = []
    for sent in doc.sents:
        clean = " ".join([t.text for t in sent if not t.is_punct])
        s = clean.strip().capitalize()
        if not s.endswith("."):
            s += "."
        sentences.append(s)

    return " ".join(sentences)

# Apply the function
df["refined_note_combined"] = df["note"].apply(refine_with_spacy_and_fuzzy)
df.to_csv("refined_clinical_notes_combined.csv", index=False)
print("✅ Combined refinement saved to 'refined_clinical_notes_combined.csv'")