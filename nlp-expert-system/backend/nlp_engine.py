# backend/nlp_engine.py
import spacy
from difflib import get_close_matches
import re

nlp = spacy.load("en_core_web_sm")

# small dictionary for spell-check fallback
EN_WORDS = set()
try:
    # attempt to populate basic wordset from spaCy vocab
    EN_WORDS = {w.text.lower() for w in nlp.vocab if w.is_lower and w.is_alpha and len(w.text) > 1}
except Exception:
    EN_WORDS = set()

INFORMAL_MAP = {
    "gonna": "going to",
    "wanna": "want to",
    "gotta": "have to",
    "kinda": "kind of",
    "ain't": "is not",
    "im": "i am",
}

WORDY_REPLACEMENTS = {
    "in order to": "to",
    "due to the fact that": "because",
    "at this point in time": "now",
    "for the purpose of": "to",
}

def preprocess(text):
    doc = nlp(text)
    return doc

def fuzzy_spell(word):
    """Return best match from EN_WORDS using difflib"""
    if word.lower() in EN_WORDS:
        return word, False
    matches = get_close_matches(word.lower(), EN_WORDS, n=1, cutoff=0.78)
    if matches:
        return matches[0], True
    # else return original
    return word, False

def simple_token_spellcheck(doc):
    """Return list of (token, suggestion, changed_flag)"""
    results = []
    for token in doc:
        if token.is_alpha and token.lower_ not in EN_WORDS:
            suggestion, changed = fuzzy_spell(token.text)
            results.append((token.text, suggestion, changed))
    return results

def detect_question_order(doc):
    # heuristic: simple check for subordinate clause inversion
    # e.g., "where is the market" in an indirect clause; for now return True if root is copula in subordinate
    return any([tok.tag_ == "WRB" and tok.dep_ == "advmod" for tok in doc])

def to_past_if_time_marker(doc):
    # very naive: if words like yesterday found, convert present verbs to past (returns mapping)
    time_markers = {"yesterday", "ago", "last", "earlier"}
    if any(tok.text.lower() in time_markers for tok in doc):
        verbs = [tok for tok in doc if tok.pos_ == "VERB"]
        return verbs
    return []
