# backend/fuzzy_corrector.py
"""
Advanced fuzzy matching and phonetic-based spelling correction.
Uses multiple strategies for detecting and correcting misspellings.
"""

from difflib import SequenceMatcher, get_close_matches
from typing import List, Tuple, Dict
import re

# Common typing mistakes and corrections
COMMON_TYPOS = {
    "teh": "the",
    "wich": "which",
    "recieve": "receive",
    "occured": "occurred",
    "seperate": "separate",
    "definately": "definitely",
    "ocassion": "occasion",
    "neccessary": "necessary",
    "goverment": "government",
    "enviroment": "environment",
    "calender": "calendar",
    "restaurent": "restaurant",
    "occassion": "occasion",
    "adress": "address",
    "exellent": "excellent",
    "existance": "existence",
    "diferent": "different",
    "untill": "until",
    "alot": "a lot",
    "thier": "their",
    "reccommend": "recommend",
    "sucess": "success",
    "wich": "which",
    "becuase": "because",
}

# Common phonetic mistakes (homophone corrections for context)
PHONETIC_MISTAKES = {
    "to": ["too", "two"],
    "their": ["there", "they're"],
    "your": ["you're"],
    "its": ["it's"],
    "weather": ["whether"],
    "where": ["wear", "ware"],
    "would": ["wood"],
    "right": ["write", "rite"],
    "know": ["no"],
    "new": ["knew", "gnu"],
    "break": ["brake"],
    "see": ["sea"],
}

# Context-free common mistakes
CONTEXT_MISTAKES = {
    r'\bur\b': 'your',
    r'\bu\b': 'you',
    r'\br\b': 'are',
    r'\bb4\b': 'before',
    r'\bthru\b': 'through',
    r'\bgr8\b': 'great',
}


class FuzzyCorrector:
    """Advanced spelling correction using multiple strategies."""
    
    def __init__(self, dictionary_words: set = None):
        """
        Initialize fuzzy corrector.
        
        Args:
            dictionary_words: Set of valid English words (optional)
        """
        self.dictionary = dictionary_words or set()
        self.typo_map = COMMON_TYPOS
        self.phonetic_map = PHONETIC_MISTAKES
        self.context_map = CONTEXT_MISTAKES
    
    def correction_priority(self, word: str, candidates: List[str]) -> str:
        """
        Select best correction candidate based on multiple heuristics.
        
        Heuristics (in order of priority):
        1. Exact match in dictionary
        2. Common typo map
        3. Length similarity
        4. Edit distance + phonetic similarity
        """
        word_lower = word.lower()
        
        # 1. Direct typo lookup
        if word_lower in self.typo_map:
            return self.typo_map[word_lower]
        
        # 2. Dictionary match
        if word_lower in self.dictionary:
            return word_lower
        
        # 3. Filter candidates by word length similarity
        word_len = len(word)
        length_candidates = [c for c in candidates if abs(len(c) - word_len) <= 2]
        
        if not length_candidates:
            length_candidates = candidates
        
        # 4. Score remaining candidates
        if length_candidates:
            best = max(
                length_candidates,
                key=lambda c: SequenceMatcher(None, word_lower, c.lower()).ratio()
            )
            return best
        
        return word
    
    def correct_word(self, word: str, threshold: float = 0.75) -> Tuple[str, bool]:
        """
        Correct a single word with high confidence.
        
        Returns:
            (corrected_word, was_corrected)
        """
        word_lower = word.lower()
        
        # 1. Try direct typo map
        if word_lower in self.typo_map:
            return self.typo_map[word_lower], True
        
        # 2. Try context-free replacements
        for pattern, replacement in self.context_map.items():
            if re.match(pattern, word_lower):
                return replacement, True
        
        # 3. Try fuzzy matching
        candidates = get_close_matches(word_lower, self.dictionary, n=3, cutoff=threshold)
        
        if candidates:
            best = self.correction_priority(word, candidates)
            if best.lower() != word_lower:
                return best, True
        
        return word, False
    
    def correct_text(self, text: str, confidence: float = 0.75) -> Tuple[str, List[Dict]]:
        """
        Correct entire text, tracking all corrections.
        
        Args:
            text: Input text to correct
            confidence: Minimum confidence for suggesting correction (0-1)
        
        Returns:
            (corrected_text, list of corrections)
        """
        words = text.split()
        corrected_words = []
        corrections = []
        
        for word in words:
            # Separate punctuation from word
            match = re.match(r'^([^\w]*)(\w+)([^\w]*)$', word, re.UNICODE)
            if not match:
                corrected_words.append(word)
                continue
            
            prefix, actual_word, suffix = match.groups()
            corrected, was_corrected = self.correct_word(actual_word, threshold=confidence)
            
            if was_corrected and corrected.lower() != actual_word.lower():
                corrected_words.append(prefix + corrected + suffix)
                corrections.append({
                    "original": actual_word,
                    "corrected": corrected,
                    "type": "spelling",
                    "confidence": 0.9 if actual_word.lower() in self.typo_map else 0.75
                })
            else:
                corrected_words.append(word)
        
        return ' '.join(corrected_words), corrections
    
    def suggest_corrections(self, word: str, max_suggestions: int = 5) -> List[Tuple[str, float]]:
        """
        Suggest multiple corrections with confidence scores.
        
        Returns:
            List of (correction, confidence_score) tuples
        """
        word_lower = word.lower()
        
        # Direct typo match
        if word_lower in self.typo_map:
            return [(self.typo_map[word_lower], 1.0)]
        
        # Fuzzy matches
        candidates = get_close_matches(word_lower, self.dictionary, n=max_suggestions, cutoff=0.6)
        
        # Score each candidate
        scored = []
        for candidate in candidates:
            similarity = SequenceMatcher(None, word_lower, candidate.lower()).ratio()
            scored.append((candidate, similarity))
        
        # Sort by score
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:max_suggestions]
    
    def batch_correct(self, texts: List[str], confidence: float = 0.75) -> List[Dict]:
        """
        Correct multiple texts efficiently.
        
        Returns:
            List of correction results
        """
        results = []
        for text in texts:
            corrected, corrections = self.correct_text(text, confidence)
            results.append({
                "original": text,
                "corrected": corrected,
                "corrections_count": len(corrections),
                "corrections": corrections
            })
        return results


class ContextualSpellChecker:
    """
    More sophisticated spelling checker that considers context.
    Uses simple heuristics to identify homophone errors.
    """
    
    def __init__(self):
        self.homophone_groups = {
            "to/too/two": ["to", "too", "two"],
            "their/there/they're": ["their", "there", "they're"],
            "your/you're": ["your", "you're"],
            "its/it's": ["its", "it's"],
            "weather/whether": ["weather", "whether"],
            "where/wear/ware": ["where", "wear", "ware"],
            "would/wood": ["would", "wood"],
            "right/write": ["right", "write"],
            "know/no": ["know", "no"],
            "new/knew": ["new", "knew"],
            "break/brake": ["break", "brake"],
            "see/sea": ["see", "sea"],
        }
    
    def check_homophone(self, word: str, context: str) -> str:
        """
        Check if a word should be replaced with a homophone based on context.
        
        Args:
            word: Word to check
            context: Full sentence context
        
        Returns:
            Corrected word or original word
        """
        word_lower = word.lower()
        
        # Find which homophone group this word belongs to
        group = None
        for group_name, homophones in self.homophone_groups.items():
            if word_lower in homophones:
                group = homophones
                break
        
        if not group or len(group) <= 1:
            return word
        
        context_lower = context.lower()
        
        # Simple heuristic: check common word patterns
        if word_lower in ["to", "too", "two"]:
            if "go to" in context_lower or "give to" in context_lower:
                return "to"
            elif "too many" in context_lower or "too much" in context_lower:
                return "too"
            elif "two of" in context_lower or "two years" in context_lower:
                return "two"
        
        elif word_lower in ["their", "there", "they're"]:
            if "their " in context_lower:
                return "their"
            elif "there is" in context_lower or "there are" in context_lower or "there was" in context_lower:
                return "there"
            elif "they are" in context_lower:
                return "they're"
        
        elif word_lower in ["your", "you're"]:
            if "you are" in context_lower:
                return "you're"
            else:
                return "your"
        
        elif word_lower in ["its", "it's"]:
            if "it is" in context_lower or "it has" in context_lower:
                return "it's"
            else:
                return "its"
        
        return word


def quick_spell_check(text: str, common_words: set = None) -> Tuple[str, int]:
    """
    Quick spell check using common typo map only.
    Fast but less comprehensive.
    
    Returns:
        (corrected_text, corrections_made)
    """
    corrected = text
    count = 0
    
    for typo, correct in COMMON_TYPOS.items():
        pattern = re.compile(r'\b' + re.escape(typo) + r'\b', flags=re.I)
        matches = pattern.findall(corrected)
        if matches:
            count += len(matches)
            corrected = pattern.sub(correct, corrected)
    
    # Also apply context mistakes
    for pattern, replacement in CONTEXT_MISTAKES.items():
        if re.search(pattern, corrected):
            corrected = re.sub(pattern, replacement, corrected)
            count += 1
    
    return corrected, count
