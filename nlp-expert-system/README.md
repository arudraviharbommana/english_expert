# NLP Expert System

A complete AI-powered English grammar correction and improvement system with a 3D web interface. Features a FastAPI backend with rule-based NLP engine and a Three.js-powered interactive frontend.

## Features

- **Rule-Based Grammar Correction**: Detects and fixes common grammatical errors:
  - Informal to formal conversions (gonna → going to)
  - Wordy phrase simplification (in order to → to)
  - Spelling corrections using fuzzy matching
  - Subject-verb agreement
  - Tense consistency
  - Question word order restructuring

- **Multiple Rewrite Modes**: Standard, Simple, Formal, Professional

- **Debug Information**: Detailed rule logs showing exactly what changed and why

- **Interactive 3D UI**: Three.js particle background with real-time analysis results

## Quick Setup

### 1. Install Backend Dependencies

```bash
cd nlp-expert-system
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install fastapi uvicorn spacy python-multipart
python -m spacy download en_core_web_sm
```

### 2. Run Backend Server

```bash
cd backend
uvicorn app:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### 3. Serve Frontend

In a new terminal from the project root:

```bash
python -m http.server 5500
```

Then open `http://localhost:5500/frontend/index.html` in your browser.

## API Endpoints

### POST `/process`

Analyzes and corrects a sentence.

**Request:**
```json
{
  "sentence": "He don't knows where is the market.",
  "mode": "standard"
}
```

**Response:**
```json
{
  "original": "He don't knows where is the market.",
  "corrected": "He doesn't know where the market is.",
  "improved": "He does not know where the market is.",
  "rules_fired": [
    {
      "name": "Spelling correction",
      "reason": "Fuzzy match for 'dont'",
      "before": "dont",
      "after": "doesn't"
    },
    {
      "name": "Subject-Verb agreement",
      "reason": "Subject 'He' needs 3rd person singular verb",
      "before": "knows",
      "after": "know"
    },
    {
      "name": "Question reordering",
      "reason": "Indirect question inversion",
      "before": "where is the market",
      "after": "where the market is"
    }
  ]
}
```

### GET `/rules`

Returns list of all available grammar rules.

### GET `/`

Returns service health status.

## Example Test Cases

Try these sentences to test the system:

1. **Subject-Verb Agreement**
   ```
   She go to school every day.
   ```

2. **Informal to Formal + Wordy Phrases**
   ```
   I am gonna go to the shop in order to buy some goods.
   ```

3. **Question Reordering**
   ```
   He don't knows where is the market.
   ```

4. **Tense Consistency** (with time markers)
   ```
   Yesterday I go to the store and buy some food.
   ```

## Project Structure

```
nlp-expert-system/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── nlp_engine.py          # NLP preprocessing & spell-check
│   ├── rule_engine.py         # Grammar rules & correction logic
│   ├── improving.py           # (Optional) Enhanced corrections
│   ├── fuzzy_corrector.py     # (Optional) Advanced fuzzy matching
│   └── models/                # (Optional) ML models
├── frontend/
│   ├── index.html             # Main UI
│   ├── main.js                # Three.js scene & interactions
│   ├── styles.css             # Styling
│   ├── ui.js                  # UI module
│   └── scene.js               # Scene module
├── docs/
└── README.md
```

## Technology Stack

- **Backend**: Python, FastAPI, spaCy
- **Frontend**: Three.js, HTML5, Vanilla JavaScript
- **NLP**: spaCy (en_core_web_sm), difflib

## Limitations & Notes

- Rule implementations are **demonstrative** and intentionally simple
- Spelling uses fuzzy matching against spaCy vocabulary (lightweight approach)
- Subject-verb and tense rules are heuristic and don't handle irregular verbs or complex clauses
- For production use, consider:
  - Integrating morphological library (pattern, inflect)
  - ML-based grammar correction models
  - Unit tests for rule coverage
  - More sophisticated dependency parsing

## Future Enhancements

- Interactive per-word highlights showing transformations
- Authentication & rate-limiting for API
- Advanced morphological conjugation
- ML-based sequence-to-sequence corrections
- Real-time suggestion refinement
- Multiple language support

## Development

To add new rules, edit `backend/rule_engine.py` and add them to the `full_pipeline()` function.

## License

MIT

