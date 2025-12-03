# DEVELOPMENT.md
# Development Guide

## Project Overview

The NLP Expert System is a complete English grammar correction tool with:
- **Backend**: Python/FastAPI with rule-based NLP engine
- **Frontend**: Three.js 3D UI with real-time analysis
- **Architecture**: Modular, extensible, well-documented

## Getting Started

### 1. Quick Setup

```bash
# Clone repository
cd nlp-expert-system

# Run setup script (Linux/Mac)
chmod +x run.sh
./run.sh

# Or manual setup (Windows/all platforms)
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Run Backend

```bash
cd backend
uvicorn app:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 3. Run Frontend

In a separate terminal:
```bash
cd nlp-expert-system
python -m http.server 5500
```

Open: `http://localhost:5500/frontend/index.html`

---

## Project Structure

```
nlp-expert-system/
├── backend/                          # Python FastAPI backend
│   ├── __init__.py                   # Package marker
│   ├── app.py                        # FastAPI server & endpoints
│   ├── nlp_engine.py                 # Core NLP with spaCy
│   ├── rule_engine.py                # Grammar correction rules
│   ├── improving.py                  # Advanced improvements
│   ├── fuzzy_corrector.py            # Spelling & fuzzy matching
│   ├── requirements.txt              # Python dependencies
│   └── models/
│       └── README.md                 # ML models directory (future)
│
├── frontend/                         # Web UI
│   ├── index.html                    # Main HTML
│   ├── main.js                       # Three.js + API logic
│   ├── styles.css                    # Dark theme styling
│   ├── ui.js                         # UI module placeholder
│   └── scene.js                      # Scene module placeholder
│
├── docs/                             # Documentation
│   ├── API.md                        # API endpoint reference
│   ├── RULES.md                      # Grammar rules guide
│   ├── ARCHITECTURE.md               # System design & flow
│   └── EXAMPLES.md                   # Usage examples
│
├── README.md                         # Project overview
├── .gitignore                        # Git ignore rules
└── run.sh                            # Quick start script
```

---

## Development Workflow

### Adding a New Rule

1. **Create rule function** in `backend/rule_engine.py`:

```python
def apply_my_new_rule(text):
    """
    Applies new grammar correction.
    
    Args:
        text: Input text
    
    Returns:
        dict with name, reason, before, after OR None if no change
    """
    before = text
    # ... logic ...
    changed = text != before
    
    return {
        "name": "My Rule Name",
        "reason": "Why this rule applies",
        "before": original_text,
        "after": text
    } if changed else None
```

2. **Add to pipeline** in `full_pipeline()`:

```python
def full_pipeline(text):
    logs = []
    doc = preprocess(text)
    current_text = text

    # ... existing rules ...

    # Add your new rule
    r = apply_my_new_rule(current_text)
    if r:
        logs.append(r)
        current_text = r["after"]
        doc = preprocess(current_text)

    # ... rest of pipeline ...
    return response
```

3. **Test** with example:

```python
from rule_engine import full_pipeline

result = full_pipeline("Your test sentence here")
print(result['rules_fired'])
```

### Adding Frontend Features

1. **Modify** `frontend/main.js` or create new module
2. **Test** with `http://localhost:5500/frontend/index.html`
3. **Update** related files (HTML, CSS)

Example - Add result sound effect:
```javascript
// In frontend/main.js analyze() function
function playSuccessSound() {
  const audio = new Audio('data:audio/wav;base64,...');
  audio.play();
}
```

### Testing

#### Manual Testing

```python
# Test individual rule
from rule_engine import apply_informal_replacements
result = apply_informal_replacements("I'm gonna go")
print(result)

# Test full pipeline
from rule_engine import full_pipeline
result = full_pipeline("He don't know where is the market")
print(json.dumps(result, indent=2))
```

#### Automated Testing

```python
# Create backend/test_rules.py
import pytest
from rule_engine import full_pipeline

def test_informal_to_formal():
    result = full_pipeline("I'm gonna go")
    assert "going to" in result['corrected']

def test_empty_input():
    result = full_pipeline("")
    assert result['original'] == ""

if __name__ == "__main__":
    pytest.main([__file__])
```

Run: `pytest backend/test_rules.py`

---

## Code Style Guidelines

### Python

- Use **type hints** where possible
- Follow **PEP 8** (4-space indentation)
- Add **docstrings** to functions and classes
- Use **comments** for complex logic

```python
def apply_rule(text: str) -> Tuple[str, List[Dict]]:
    """
    Applies grammar correction.
    
    Args:
        text: Input sentence
    
    Returns:
        Tuple of (corrected_text, list_of_changes)
    """
    # Implementation
    pass
```

### JavaScript

- Use **const/let**, avoid **var**
- Use **arrow functions** where appropriate
- Add **comments** for non-obvious code
- Keep functions small and focused

```javascript
const analyzeText = async (sentence) => {
  // Fetch and process
  const response = await fetch(endpoint);
  return response.json();
};
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-rule

# Make changes
# ... edit files ...

# Commit
git add .
git commit -m "Add new grammar rule for [specific case]"

# Push and create PR
git push origin feature/new-rule
```

---

## Debugging

### Backend Debugging

**Add logging**:
```python
import logging
logger = logging.getLogger(__name__)

def apply_rule(text):
    logger.debug(f"Applying rule to: {text}")
    # ... logic ...
    logger.info(f"Rule result: {result}")
```

**Run with logging**:
```bash
cd backend
uvicorn app:app --reload --log-level debug
```

**Use debugger (breakpoint)**:
```python
def apply_rule(text):
    breakpoint()  # Execution pauses here
    # ... code ...
```

### Frontend Debugging

1. **Open browser DevTools** (F12)
2. **Console tab** for errors
3. **Network tab** to inspect API calls
4. **Debugger** to step through code

```javascript
// Add debugging
console.log("Processing:", sentence);
fetch(...).then(r => {
  console.log("Response:", r);
  return r.json();
});
```

---

## Performance Optimization

### Backend

```python
# Cache spaCy model
from functools import lru_cache

@lru_cache(maxsize=1)
def get_nlp():
    return spacy.load("en_core_web_sm")

nlp = get_nlp()  # Called once, cached thereafter
```

### Frontend

```javascript
// Debounce API calls
const debounce = (func, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

const debouncedAnalyze = debounce(analyze, 500);
```

---

## Deployment

### Docker

**Create `Dockerfile`** in project root:
```dockerfile
FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY backend/ .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run**:
```bash
docker build -t nlp-expert .
docker run -p 8000:8000 nlp-expert
```

### Cloud Deployment

**Heroku**:
```bash
# Create Procfile
echo "web: cd backend && uvicorn app:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main
```

**AWS/GCP**: Use container services (ECS, Cloud Run)

---

## Future Development

### Short-term

- [ ] Unit tests for all rules
- [ ] Input validation & sanitization
- [ ] Error handling improvements
- [ ] Rate limiting & API keys

### Mid-term

- [ ] ML-based corrections (seq2seq)
- [ ] Advanced verb conjugation (pattern library)
- [ ] Article correction (a/an/the)
- [ ] Preposition correction

### Long-term

- [ ] Multi-language support
- [ ] Real-time collaborative editing
- [ ] Custom rule builder UI
- [ ] ML model fine-tuning interface

---

## Resources

- **spaCy docs**: https://spacy.io
- **FastAPI docs**: https://fastapi.tiangolo.com
- **Three.js docs**: https://threejs.org/docs
- **Python style guide**: https://pep8.org

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/x`)
3. Make changes with tests
4. Commit with clear messages
5. Push and create Pull Request

---

## Troubleshooting

### Backend won't start

```bash
# Check Python version (need 3.9+)
python --version

# Reinstall dependencies
pip install --upgrade -r backend/requirements.txt

# Check if port 8000 is free
lsof -i :8000  # Kill if needed: kill -9 <PID>
```

### Frontend can't reach backend

```javascript
// Check CORS
// In backend/app.py, ensure CORS is enabled
// In frontend/main.js, verify BACKEND URL

const BACKEND = "http://localhost:8000";  // Check this
```

### spaCy model not found

```bash
# Reinstall model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('OK')"
```

---

## Support

For issues or questions:
- Check `docs/` folder for detailed guides
- Review `EXAMPLES.md` for usage patterns
- Check GitHub issues
- Create new issue with details and error logs

---

## License

MIT - See LICENSE file
