# docs/RULES.md
# Grammar Correction Rules Documentation

This document details each grammar rule implemented in the NLP Expert System.

---

## Rule 1: Informal → Formal Replacements

**File**: `backend/rule_engine.py` - `apply_informal_replacements()`

**Purpose**: Convert informal/colloquial expressions to formal alternatives.

**Replacements**:
| Informal | Formal |
|----------|--------|
| gonna | going to |
| wanna | want to |
| gotta | have to |
| kinda | kind of |
| ain't | is not |
| im | i am |

**Example**:
```
Input:  "I'm gonna go to the store."
Output: "I am going to go to the store."
Log:    {"name": "Informal -> Formal", "before": "I'm gonna", "after": "I am going to"}
```

**Limitations**:
- Uses regex word boundaries (case-insensitive)
- Limited set of common contractions
- Doesn't preserve capitalization context perfectly

---

## Rule 2: Wordy Phrase Simplification

**File**: `backend/rule_engine.py` - `apply_wordy_simplification()`

**Purpose**: Replace verbose phrases with concise alternatives.

**Replacements**:
| Verbose Phrase | Simplified |
|----------------|-----------|
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| for the purpose of | to |

**Example**:
```
Input:  "I went to the shop in order to buy groceries."
Output: "I went to the shop to buy groceries."
Log:    {"name": "Wordy phrase simplification", "reason": "Shorten verbose phrases"}
```

**Limitations**:
- Fixed phrase list only
- Doesn't handle variations or synonyms
- May fail with punctuation

---

## Rule 3: Spelling Corrections

**File**: `backend/rule_engine.py` - `apply_spelling_corrections()`

**Purpose**: Detect and correct misspelled words using fuzzy matching.

**Algorithm**:
1. Tokenize with spaCy
2. Check each token: if alphabetic AND not in vocabulary
3. Use `difflib.get_close_matches()` with cutoff 0.78
4. Replace if match found

**Example**:
```
Input:  "He dont know where the market is."
Output: "He don't know where the market is."
Log:    {"name": "Spelling correction", "reason": "Fuzzy match for 'dont'", "before": "dont", "after": "don't"}
```

**Cutoff Score**: 0.78
- Higher = stricter matching (fewer false corrections)
- Lower = more aggressive (more typo catching)

**Limitations**:
- Relies on spaCy vocabulary (not comprehensive)
- No support for proper nouns or domain-specific terms
- May suggest wrong corrections if word is very misspelled

---

## Rule 4: Subject-Verb Agreement

**File**: `backend/rule_engine.py` - `apply_subject_verb_agreement()`

**Purpose**: Ensure verbs match their subjects in person and number.

**Rule Logic**:
```
IF subject is 3rd person singular (he/she/it/this/that)
   AND verb is in base form (lemma == token)
   AND verb doesn't end with 's'
THEN add 's' to verb
```

**Patterns Detected**:
- "He go" → "He goes"
- "She do" → "She does"
- "It happen" → "It happens"
- "This work" → "This works"

**Example**:
```
Input:  "She go to school every day."
Output: "She goes to school every day."
Log:    {
    "name": "Subject-Verb agreement",
    "reason": "Subject 'She' needs 3rd person singular verb",
    "before": "go",
    "after": "goes"
}
```

**Limitations**:
- **VERY NAIVE**: Only handles simple "-s" addition
- Doesn't handle irregular verbs (be/do/have conjugations)
- Doesn't handle complex subjects (compound, relative clauses)
- spaCy dependency parsing must correctly identify subject/verb relations

---

## Rule 5: Tense Consistency

**File**: `backend/rule_engine.py` - `apply_tense_consistency()`

**Purpose**: Ensure tense consistency when time markers are present.

**Rule Logic**:
```
IF sentence contains time marker (yesterday/ago/last/earlier)
   AND verb is in base form (lemma == token)
   AND verb doesn't end with 'ed'
THEN add 'ed' to verb (convert to past)
```

**Time Markers**: yesterday, ago, last, earlier

**Example**:
```
Input:  "Yesterday I go to the store and buy groceries."
Output: "Yesterday I goed to the store and buyed groceries."
Log:    [
    {"name": "Past Tense conversion", "reason": "Time marker present", "before": "go", "after": "goed"},
    {"name": "Past Tense conversion", "reason": "Time marker present", "before": "buy", "after": "buyed"}
]
```

**Limitations**:
- **EXTREMELY NAIVE**: Only appends "ed" (produces wrong forms!)
- Doesn't handle irregular verbs (go→went, buy→bought)
- No proper morphological analysis
- Creates grammatically incorrect output for irregular verbs

---

## Rule 6: Question Word Order Restructuring

**File**: `backend/rule_engine.py` - `restructure_question_order()`

**Purpose**: Fix question word order in indirect questions and subordinate clauses.

**Rule Logic**:
Uses regex to detect embedded questions with inversion:
```
(where|when|what|why|how) (is|are|was|were) (...)
```
Restructures to normal word order.

**Pattern Match**:
```regex
(\bwhere\b|\bwhen\b|\bwhat\b|\bwhy\b|\bhow\b)
\s+
(\bis\b|\bare\b|\bwas\b|\bwere\b)
\s+
([^?.!,]+)
```

**Transformation**:
```
"where is the market" → "where the market is"
"when was he born" → "when he was born"
```

**Example**:
```
Input:  "He don't know where is the market."
Output: "He don't know where the market is."
Log:    {
    "name": "Question reordering",
    "reason": "Indirect question inversion",
    "before": "where is the market",
    "after": "where the market is"
}
```

**Limitations**:
- Only handles copula verbs (be)
- Doesn't handle other aux verbs (do/have/will/etc)
- Regex-based: may miss context
- Can cause issues with intentional questions

---

## Rule 7: Heuristic Rewrites (Synonyms)

**File**: `backend/rule_engine.py` - `heuristics_rewrite()`

**Purpose**: Apply professional vocabulary substitutions for improved writing.

**Replacements**:
| Original | Professional |
|----------|--------------|
| go to | visit |
| went to | visited |
| buy | purchase |
| get | obtain |
| good | favorable |
| bad | unfavorable |

**Example**:
```
Input:  "I go to the market to buy good products."
Output: "I visit the market to purchase favorable products."
```

**Limitations**:
- No context awareness (may be inappropriate)
- Limited vocabulary set
- No word sense disambiguation

---

## Pipeline Execution Order

Rules are applied **sequentially** in this order:

```
1. Informal → Formal
   ↓ (Update text, re-parse)
2. Wordy Simplification
   ↓ (Update text, re-parse)
3. Spelling Corrections
   ↓ (Update text, re-parse)
4. Subject-Verb Agreement
   ↓ (Update text, re-parse)
5. Tense Consistency
   ↓ (Update text, re-parse)
6. Question Reordering
   ↓ (Update text, re-parse)
7. Heuristic Rewrites (synonyms)
```

**Why Sequential?** Each rule's output becomes the next rule's input. This allows:
- Rules to build on each other
- Improved accuracy (corrections get checked by later rules)
- Cleaner detection (fewer overlapping patterns)

---

## Complete Example Walkthrough

**Input**: `"He don't knows where is the market."`

### Step 1: Informal → Formal
- Pattern `don't` not found (it's written as "don")
- **No change**

### Step 2: Wordy Simplification
- No wordy phrases found
- **No change**

### Step 3: Spelling Corrections
- Tokens: ["He", "don't", "knows", "where", "is", "the", "market"]
- Wait, actual input has "dont" without apostrophe: ["He", "dont", "knows", ...]
- "dont" not in vocabulary → fuzzy match → "don't" (similarity 0.89)
- **Change**: "dont" → "don't"
- Text now: `"He don't knows where is the market."`

### Step 4: Subject-Verb Agreement
- spaCy parses
- Finds subject "He" (3rd person singular) + verb "knows"
- But "knows" already has 's'... wait, but "knows" with "don't" is wrong
- Actually, the rule looks for base form verbs
- "knows" lemma is "know", but text is "knows" - doesn't match the rule condition
- Also, there's "don't" which might interfere with parsing
- **Depends on spaCy's parsing** - likely no change or complex behavior

### Step 5: Tense Consistency
- No time markers (yesterday/ago/last/earlier)
- **No change**

### Step 6: Question Reordering
- Pattern: `where is the market` matches!
- "where" (wh-word) + "is" (copula) + "the market"
- Restructure: `where the market is`
- Text now: `"He don't knows where the market is."`

### Step 7: Heuristic Rewrites
- "market" not in replacements
- **No change**

**Final Output**: 
- Original: `"He don't knows where is the market."`
- Corrected: `"He don't knows where the market is."`
- Rules fired: [Spelling correction, Question reordering]

**Note**: This example shows limitations - "don't knows" is still grammatically wrong because the rule engine is simplified!

---

## Testing Rules

### Test Sentences

```python
test_cases = [
    # Rule 1: Informal → Formal
    ("I'm gonna go shopping", "Informal to Formal"),
    
    # Rule 2: Wordy Simplification
    ("I went to the shop in order to buy milk", "Wordy phrases"),
    
    # Rule 3: Spelling
    ("He dont know", "Spelling correction"),
    
    # Rule 4: Subject-Verb Agreement
    ("She go to school", "Subject-Verb agreement"),
    
    # Rule 5: Tense Consistency
    ("Yesterday I go to the store", "Tense consistency"),
    
    # Rule 6: Question Reordering
    ("I wonder what is the answer", "Question reordering"),
    
    # Rule 7: Heuristic Rewrite
    ("I want to get good products", "Heuristic rewrite"),
]
```

---

## Future Improvements

1. **Replace naive conjugation** with `pattern` or `inflect` library
2. **Add more rules**:
   - Article correction (a/an/the)
   - Preposition correction (in/on/at)
   - Capitalization fixes
   - Punctuation rules
3. **Context-aware rules** using more sophisticated parsing
4. **Machine learning** for complex grammatical errors
5. **Multi-language support**
