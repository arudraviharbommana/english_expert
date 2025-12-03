# docs/ARCHITECTURE.md
# NLP Expert System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Three.js)                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ index.html  │ main.js (Three.js)  │ styles.css        │ │
│  │ - Textarea  │ - Particle system   │ - Dark theme      │ │
│  │ - Result    │ - Animations        │ - Glassmorphism   │ │
│  │   display   │ - Fetch API         │                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                    HTTP (port 5500)                          │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ JSON POST/GET
                           │
┌─────────────────────────────────────────────────────────────┐
│               Backend (FastAPI, port 8000)                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  app.py                                               │ │
│  │  ├── POST /process                                   │ │
│  │  ├── GET /rules                                      │ │
│  │  └── GET /                                           │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                   │
│                           │                                   │
│  ┌────────────────────────▼──────────────────────────────┐ │
│  │ rule_engine.py                                       │ │
│  │ full_pipeline(text) → {corrected, rules_fired}      │ │
│  └──────────┬──────────┬──────────┬──────────┬──────────┘ │
│             │          │          │          │             │
│  ┌──────────▼──┐ ┌─────▼──┐ ┌────▼───┐ ┌───▼────┐         │
│  │ Informal->  │ │ Wordy  │ │Spelling│ │Subject │         │
│  │ Formal      │ │Simplify│ │Correct │ │-Verb   │         │
│  │ (FORMAL_MAP)│ │(WORDY) │ │(fuzzy) │ │ Agree  │         │
│  └─────────────┘ └────────┘ └────────┘ └────────┘         │
│                                                              │
│  ┌──────────┐  ┌────────────┐  ┌──────────────┐            │
│  │ Tense    │  │ Question   │  │ Heuristics   │            │
│  │ Consisten│  │ Reordering │  │ Rewrite      │            │
│  │ (naive)  │  │            │  │              │            │
│  └──────────┘  └────────────┘  └──────────────┘            │
│                           │                                   │
│  ┌────────────────────────▼──────────────────────────────┐ │
│  │ nlp_engine.py                                        │ │
│  │ ├── preprocess(text) → spaCy Doc                    │ │
│  │ ├── fuzzy_spell(word) → (corrected, flag)          │ │
│  │ └── simple_token_spellcheck(doc)                   │ │
│  └────────────────────────────────────────────────────┘ │
│                           │                                   │
│  ┌────────────────────────▼──────────────────────────────┐ │
│  │ spaCy (en_core_web_sm)                              │ │
│  │ - Tokenization, POS tagging                         │ │
│  │ - Dependency parsing                               │ │
│  │ - Named Entity Recognition                         │ │
│  │ - Vocabulary (spell-check fallback)                │ │
│  └────────────────────────────────────────────────────┘ │
│                                                              │
│ Optional Modules:                                            │
│  ├── improving.py → SentenceImprover class                │
│  │   (clarity, professionalism, redundancy)                │
│  └── fuzzy_corrector.py → FuzzyCorrector class            │
│      (advanced spelling, homophone detection)              │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### User Request Flow

```
1. User types sentence in textarea
   └─> frontend/main.js: inputSentence.value

2. User clicks "Analyze & Improve" or presses Ctrl+Enter
   └─> analyze() function triggered

3. fetch() POST to backend /process
   └─> {"sentence": "...", "mode": "standard"}

4. Backend processes in rule_engine.full_pipeline()
   ├─> Apply informal replacements
   ├─> Apply wordy simplification
   ├─> Apply spelling corrections
   ├─> Apply subject-verb agreement
   ├─> Apply tense consistency
   ├─> Apply question reordering
   └─> Return {original, corrected, improved, rules_fired}

5. Frontend receives JSON response
   └─> showResults(data)
       ├─> Display original
       ├─> Display corrected
       ├─> Display improved
       └─> List all rules_fired with before/after

6. Animation triggered
   └─> flashParticles() brightens Three.js background
```

---

## Module Responsibilities

### app.py (FastAPI Server)
- **Responsibility**: HTTP API endpoint handling
- **Functions**:
  - `/process`: Main grammar correction endpoint
  - `/rules`: Returns list of available rules
  - `/`: Health check
- **Dependencies**: FastAPI, CORS middleware, rule_engine

### rule_engine.py (Grammar Rules)
- **Responsibility**: Rule-based text correction logic
- **Key Function**: `full_pipeline(text)` - orchestrates all rules
- **Rules**:
  1. Informal → Formal
  2. Wordy → Simplified
  3. Spelling corrections
  4. Subject-Verb agreement
  5. Tense consistency
  6. Question reordering
  7. Heuristic rewrites
- **Dependencies**: nlp_engine, regex, spaCy

### nlp_engine.py (NLP Processing)
- **Responsibility**: Core NLP tasks using spaCy
- **Functions**:
  - `preprocess(text)`: Tokenize and parse with spaCy
  - `fuzzy_spell(word)`: Fuzzy spelling suggestion
  - `simple_token_spellcheck(doc)`: Token-level spell checking
- **Dependencies**: spaCy, difflib

### improving.py (Advanced Improvements)
- **Responsibility**: Style-aware sentence improvements
- **Class**: `SentenceImprover`
- **Methods**:
  - `improve_clarity()`: Vague → precise verbs
  - `improve_professionalism()`: Casual → professional vocab
  - `simplify_for_casual()`: Formal → casual simplification
  - `reduce_redundancy()`: Remove redundant phrases
  - `enhance_readability()`: Break weak constructions
- **Function**: `full_improvement_pipeline(text, style)`

### fuzzy_corrector.py (Advanced Spelling)
- **Responsibility**: Advanced spelling and homophone correction
- **Classes**:
  - `FuzzyCorrector`: Multi-strategy spelling correction
  - `ContextualSpellChecker`: Context-aware homophone detection
- **Includes**: Common typo maps, phonetic matching, edit distance

### frontend/main.js (Three.js UI)
- **Responsibility**: Interactive 3D UI and API communication
- **Components**:
  - Three.js scene with particle system
  - Event listeners for button/textarea
  - fetch() API calls to backend
  - Real-time result display
  - Animation effects

---

## Grammar Rule Pipeline

Each rule follows a pattern:

```python
def apply_rule(text_or_doc):
    """
    Before: Original text
    After: Check for pattern
    Match: Apply correction
    Log: Record change with name, reason, before, after
    Return: (corrected_text, list_of_changes)
    """
```

Example: Subject-Verb Agreement Rule
```
Input:  "He go to school"
1. Parse with spaCy
2. Find subject "He" (3rd person singular)
3. Find verb "go" (base form)
4. Rule matches: 3rd person sing + base verb = ERROR
5. Correction: Add 's' → "goes"
6. Log: {"name": "...", "reason": "...", "before": "go", "after": "goes"}
Output: ("He goes to school", [log])
```

---

## Error Handling Strategy

```
User Input
    ├─> Empty check
    ├─> Sanitization (safe strings)
    ├─> spaCy processing
    │   └─> Try/catch if model fails
    └─> Rules application
        └─> Non-fatal errors (skip rule, continue pipeline)

Response:
- Success: Return full correction + rules + improved
- Partial success: Return what was corrected
- Error: Return HTTP error + details
```

---

## Performance Considerations

### Bottlenecks
1. **spaCy model loading** (~300ms on first call)
   - Solution: Load once on startup
2. **Fuzzy matching with large vocabulary** (~50-100ms)
   - Solution: Use cutoff threshold (0.78)
3. **Complex dependency parsing** (~100ms per sentence)
   - Solution: Keep sentences under 50 tokens

### Optimization Tips
- Cache spaCy model in memory
- Use `en_core_web_sm` (smaller, faster)
- Consider `en_core_web_trf` for better accuracy (slower)
- Batch process multiple sentences if needed

---

## Extension Points

### Adding New Rules

1. Create rule function in `rule_engine.py`:
```python
def apply_my_rule(text):
    # ... logic ...
    return {"name": "...", "reason": "...", "before": "...", "after": "..."}, changed
```

2. Add to `full_pipeline()`:
```python
r = apply_my_rule(current_text)
if r:
    logs.append(r)
    current_text = r["after"]
    doc = preprocess(current_text)
```

### Integrating ML Models

```python
from transformers import pipeline

# Load grammar correction model
grammar_corrector = pipeline("text2text-generation", model="grammarly/coedit-base")

def apply_ml_correction(text):
    corrected = grammar_corrector(text, max_length=512)[0]['generated_text']
    return corrected, corrected != text
```

---

## Deployment Considerations

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
COPY backend/ .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

```
BACKEND_PORT=8000
SPACY_MODEL=en_core_web_sm
LOG_LEVEL=INFO
CORS_ORIGINS=*
```

### Scaling

- **Horizontal**: Multiple backend instances behind load balancer
- **Vertical**: Use `en_core_web_trf` for better accuracy
- **Caching**: Cache results for repeated queries
- **Queue**: Use Celery for async processing
