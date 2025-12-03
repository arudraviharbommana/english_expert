# backend/improving.py
"""
Advanced sentence improvement module with synonym replacement, clarity enhancements,
and stylistic improvements based on target audience.
"""

import re
from typing import List, Dict, Tuple

# Synonym and replacement dictionaries for different styles
CLARITY_IMPROVEMENTS = {
    "use": "utilize",
    "get": "obtain",
    "put": "place",
    "make": "create",
    "go": "proceed",
    "come": "arrive",
    "see": "observe",
    "think": "consider",
    "know": "understand",
    "want": "desire",
    "like": "appreciate",
    "help": "assist",
    "start": "commence",
    "end": "conclude",
    "stop": "cease",
    "try": "attempt",
    "find": "discover",
    "give": "provide",
    "take": "acquire",
    "show": "demonstrate",
    "ask": "inquire",
    "say": "state",
    "tell": "inform",
    "do": "perform",
    "happen": "occur",
}

PROFESSIONAL_SYNONYMS = {
    "good": "satisfactory",
    "bad": "unsatisfactory",
    "nice": "favorable",
    "really": "considerably",
    "very": "highly",
    "big": "substantial",
    "small": "minimal",
    "fast": "expeditious",
    "slow": "gradual",
    "easy": "straightforward",
    "hard": "challenging",
    "many": "numerous",
    "few": "limited",
    "lot": "considerable amount",
    "thing": "matter",
    "stuff": "material",
    "guy": "individual",
    "girl": "individual",
    "kid": "child",
    "old": "senior",
}

CASUAL_SIMPLIFICATION = {
    "utilize": "use",
    "obtain": "get",
    "place": "put",
    "create": "make",
    "proceed": "go",
    "commence": "start",
    "conclude": "end",
    "cease": "stop",
    "attempt": "try",
    "discover": "find",
    "provide": "give",
    "acquire": "take",
    "demonstrate": "show",
    "inquire": "ask",
    "state": "say",
    "inform": "tell",
    "perform": "do",
    "occur": "happen",
}

PASSIVE_TO_ACTIVE = {
    r"(\w+)\s+is\s+being\s+(\w+)ed?\s+by\s+(\w+)": r"\3 \2s \1",
    r"(\w+)\s+was\s+(\w+)ed?\s+by\s+(\w+)": r"\3 \2ed \1",
}


class SentenceImprover:
    """Improves sentence clarity, style, and professionalism."""
    
    def __init__(self):
        self.clarity_map = CLARITY_IMPROVEMENTS
        self.professional_map = PROFESSIONAL_SYNONYMS
        self.casual_map = CASUAL_SIMPLIFICATION
    
    def improve_clarity(self, text: str) -> Tuple[str, List[Dict]]:
        """Replace vague verbs with more precise ones."""
        improved = text
        changes = []
        
        for vague, precise in self.clarity_map.items():
            pattern = re.compile(r'\b' + vague + r'\b', flags=re.I)
            matches = pattern.finditer(text)
            for match in matches:
                old_text = match.group(0)
                new_text = precise.capitalize() if old_text[0].isupper() else precise
                improved = improved.replace(old_text, new_text, 1)
                changes.append({
                    "type": "clarity",
                    "before": old_text,
                    "after": new_text,
                    "reason": "Replace vague verb with precise alternative"
                })
        
        return improved, changes
    
    def improve_professionalism(self, text: str) -> Tuple[str, List[Dict]]:
        """Apply professional vocabulary substitutions."""
        improved = text
        changes = []
        
        for informal, formal in self.professional_map.items():
            pattern = re.compile(r'\b' + re.escape(informal) + r'\b', flags=re.I)
            matches = pattern.finditer(text)
            for match in matches:
                old_text = match.group(0)
                new_text = formal.capitalize() if old_text[0].isupper() else formal
                improved = improved.replace(old_text, new_text, 1)
                changes.append({
                    "type": "professionalism",
                    "before": old_text,
                    "after": new_text,
                    "reason": "Replace informal with professional vocabulary"
                })
        
        return improved, changes
    
    def simplify_for_casual(self, text: str) -> Tuple[str, List[Dict]]:
        """Simplify overly formal language for casual tone."""
        improved = text
        changes = []
        
        for formal, casual in self.casual_map.items():
            pattern = re.compile(r'\b' + re.escape(formal) + r'\b', flags=re.I)
            matches = pattern.finditer(text)
            for match in matches:
                old_text = match.group(0)
                new_text = casual.capitalize() if old_text[0].isupper() else casual
                improved = improved.replace(old_text, new_text, 1)
                changes.append({
                    "type": "simplification",
                    "before": old_text,
                    "after": new_text,
                    "reason": "Simplify overly formal vocabulary"
                })
        
        return improved, changes
    
    def reduce_redundancy(self, text: str) -> Tuple[str, List[Dict]]:
        """Remove redundant phrases and repetition."""
        changes = []
        improved = text
        
        # Common redundant phrases
        redundant_phrases = [
            (r'absolutely\s+essential', 'essential'),
            (r'final\s+conclusion', 'conclusion'),
            (r'past\s+history', 'history'),
            (r'true\s+fact', 'fact'),
            (r'completely\s+finished', 'finished'),
            (r'exact\s+same', 'same'),
            (r'very\s+unique', 'unique'),
            (r'free\s+gift', 'gift'),
            (r'false\s+pretense', 'pretense'),
        ]
        
        for pattern_str, replacement in redundant_phrases:
            pattern = re.compile(pattern_str, flags=re.I)
            matches = pattern.finditer(improved)
            for match in matches:
                old_text = match.group(0)
                new_text = replacement.capitalize() if old_text[0].isupper() else replacement
                improved = pattern.sub(new_text, improved, count=1)
                changes.append({
                    "type": "redundancy",
                    "before": old_text,
                    "after": new_text,
                    "reason": "Remove redundant phrase"
                })
        
        return improved, changes
    
    def enhance_readability(self, text: str) -> Tuple[str, List[Dict]]:
        """Break up overly long phrases and improve sentence flow."""
        changes = []
        improved = text
        
        # Replace weak constructions
        weak_patterns = [
            (r'there\s+is\s+a\s+(\w+)\s+that', r'The \1 that'),
            (r'it\s+is\s+important\s+to\s+note\s+that', r'Note that'),
            (r'in\s+my\s+opinion', r'I believe'),
            (r'it\s+seems\s+that', r'Apparently'),
            (r'it\s+appears\s+that', r'It appears'),
        ]
        
        for pattern_str, replacement in weak_patterns:
            pattern = re.compile(pattern_str, flags=re.I)
            if pattern.search(improved):
                new_text = pattern.sub(replacement, improved)
                if new_text != improved:
                    changes.append({
                        "type": "readability",
                        "before": pattern.search(improved).group(0),
                        "after": replacement,
                        "reason": "Improve sentence structure and readability"
                    })
                    improved = new_text
        
        return improved, changes


def full_improvement_pipeline(text: str, target_style: str = "neutral") -> Dict:
    """
    Apply comprehensive improvements based on target style.
    
    Args:
        text: Input sentence
        target_style: "professional", "casual", "neutral", "academic"
    
    Returns:
        Dictionary with improvements and changes made
    """
    improver = SentenceImprover()
    current_text = text
    all_changes = []
    
    # Always apply: clarity, redundancy, readability
    improved, changes = improver.improve_clarity(current_text)
    if changes:
        all_changes.extend(changes)
        current_text = improved
    
    improved, changes = improver.reduce_redundancy(current_text)
    if changes:
        all_changes.extend(changes)
        current_text = improved
    
    improved, changes = improver.enhance_readability(current_text)
    if changes:
        all_changes.extend(changes)
        current_text = improved
    
    # Apply style-specific improvements
    if target_style == "professional":
        improved, changes = improver.improve_professionalism(current_text)
        if changes:
            all_changes.extend(changes)
            current_text = improved
    
    elif target_style == "casual":
        improved, changes = improver.simplify_for_casual(current_text)
        if changes:
            all_changes.extend(changes)
            current_text = improved
    
    return {
        "original": text,
        "improved": current_text,
        "changes": all_changes,
        "style": target_style,
        "improvement_count": len(all_changes)
    }
