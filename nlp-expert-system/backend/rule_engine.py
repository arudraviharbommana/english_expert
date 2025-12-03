# backend/rule_engine.py
from nlp_engine import preprocess, INFORMAL_MAP, WORDY_REPLACEMENTS, simple_token_spellcheck
import re

# Simplified rule engine that applies forward-chaining rules.
# Each rule returns a dict with: name, reason, before, after

PRONOUNS_3SG = {"he", "she", "it", "this", "that", "someone", "anyone"}

def apply_informal_replacements(text):
    before = text
    changed = False
    for k, v in INFORMAL_MAP.items():
        pattern = re.compile(r'\b' + re.escape(k) + r'\b', flags=re.I)
        if pattern.search(text):
            text = pattern.sub(v, text)
            changed = True
    return {"name":"Informal -> Formal","reason":"Replace common informal contractions","before":before, "after":text} if changed else None

def apply_wordy_simplification(text):
    before = text
    changed = False
    for k,v in WORDY_REPLACEMENTS.items():
        pattern = re.compile(re.escape(k), flags=re.I)
        if pattern.search(text):
            text = pattern.sub(v, text)
            changed = True
    return {"name":"Wordy phrase simplification","reason":"Shorten verbose phrases","before":before, "after":text} if changed else None

def apply_spelling_corrections(doc):
    checks = simple_token_spellcheck(doc)
    changes = []
    corrected_text = doc.text
    for orig, suggestion, changed in checks:
        if changed and suggestion.lower() != orig.lower():
            # replace only whole-word matches (case-insensitive)
            corrected_text = re.sub(r'\b' + re.escape(orig) + r'\b', suggestion, corrected_text, flags=re.I)
            changes.append({"name":"Spelling correction", "reason":f"Fuzzy match for '{orig}'", "before":orig, "after":suggestion})
    return corrected_text, changes

def apply_subject_verb_agreement(doc):
    """
    Very naive: if subject is third-person singular pronoun and verb is base form, add 's' to verb.
    This is a simplified demonstration rule. Real handling requires morphological analysis.
    """
    sent = doc
    changed = False
    text = sent.text
    details = []
    for token in sent:
        if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
            subj = token.text.lower()
            verb = token.head
            # simple pattern: pronoun in 3rd sing and verb lemma equals token (present)
            if subj in PRONOUNS_3SG:
                # quick check: if verb text equals lemma (likely base) and does not end with 's'
                if verb.text.lower() == verb.lemma_.lower() and not verb.text.lower().endswith("s"):
                    # naive conjugation: add 's' to verb (not handling irregulars)
                    new_verb = verb.text + "s"
                    # replace in text
                    text = replace_token_in_text(text, verb.text, new_verb)
                    changed = True
                    details.append({"name":"Subject-Verb agreement","reason":f"Subject '{token.text}' needs 3rd person singular verb","before":verb.text,"after":new_verb})
    return text, details

def replace_token_in_text(text, old, new):
    # replace whole word, preserve case (simple)
    def repl(match):
        orig = match.group(0)
        if orig[0].isupper():
            return new.capitalize()
        return new
    import re
    return re.sub(r'\b' + re.escape(old) + r'\b', repl, text)

def apply_tense_consistency(doc):
    """
    Simple rule: if time marker found (yesterday/ago/last), make present simple verbs into past by adding 'ed'.
    This is demonstrative only — proper conjugation needs more resources.
    """
    tokens = [t.text.lower() for t in doc]
    time_markers = {"yesterday","ago","last"}
    if not any(t in time_markers for t in tokens):
        return None, []
    text = doc.text
    details = []
    for token in doc:
        if token.pos_ == "VERB":
            before = token.text
            # naive: if lemma == token (present), add 'ed' (very naive)
            if token.text.lower() == token.lemma_.lower() and not token.text.lower().endswith("ed"):
                after = token.text + "ed"
                text = replace_token_in_text(text, before, after)
                details.append({"name":"Past Tense conversion","reason":"Time marker present","before":before,"after":after})
    return text, details

def restructure_question_order(doc):
    """
    Simple fix for embedded questions: '... where is the market' -> '... where the market is'
    We'll look for wh-word followed by copula inversion in subordinate clause.
    """
    text = doc.text
    details = []
    # naive pattern: (where|when|what|why|how) <aux> <...>  (only in middle of sentence)
    pattern = re.compile(r'(\bwhere\b|\bwhen\b|\bwhat\b|\bwhy\b|\bhow\b)\s+(\bis\b|\bare\b|\bwas\b|\bwere\b)\s+([^?.!,]+)', flags=re.I)
    def repl(m):
        wh = m.group(1)
        aux = m.group(2)
        rest = m.group(3).strip()
        # produce "where the market is"
        new = f"{wh} {rest} {aux}"
        details.append({"name":"Question reordering","reason":"Indirect question inversion","before":m.group(0),"after":new})
        return new
    new_text, count = pattern.subn(repl, text)
    return new_text, details

def full_pipeline(text):
    # track rule logs
    logs = []
    doc = preprocess(text)
    current_text = text

    # 1. informal replacements
    r = apply_informal_replacements(current_text)
    if r:
        logs.append(r)
        current_text = r["after"]
        doc = preprocess(current_text)

    # 2. wordy simplifications
    r = apply_wordy_simplification(current_text)
    if r:
        logs.append(r)
        current_text = r["after"]
        doc = preprocess(current_text)

    # 3. spelling
    new_text, changes = apply_spelling_corrections(doc)
    if changes:
        logs.extend(changes)
        current_text = new_text
        doc = preprocess(current_text)

    # 4. subject-verb agreement
    new_text, details = apply_subject_verb_agreement(doc)
    if details:
        logs.extend(details)
        current_text = new_text
        doc = preprocess(current_text)

    # 5. tense consistency
    new_text, details = apply_tense_consistency(doc)
    if details:
        logs.extend(details)
        current_text = new_text
        doc = preprocess(current_text)

    # 6. restructure question order
    new_text, details = restructure_question_order(doc)
    if details:
        logs.extend(details)
        current_text = new_text
        doc = preprocess(current_text)

    # "improved" rewrite passes (optional minor synonyms)
    improved = heuristics_rewrite(current_text)

    response = {
        "original": text,
        "corrected": current_text,
        "improved": improved,
        "rules_fired": logs
    }
    return response

def heuristics_rewrite(text):
    # small set of improvements: replace some words with synonyms for professional tone
    repl = {
        "go to": "visit",
        "went to": "visited",
        "buy": "purchase",
        "get": "obtain",
        "good": "favorable",
        "bad": "unfavorable",
    }
    import re
    out = text
    for k,v in repl.items():
        out = re.sub(r'\b' + re.escape(k) + r'\b', v, out, flags=re.I)
    return out
