# Testing & Examples Guide

## Quick Test Cases

### 1. Subject-Verb Agreement
**Input:** `She go to school every day.`

**Expected Output:**
- Corrected: `She goes to school every day.`
- Rule: Subject-Verb agreement

---

### 2. Informal to Formal Conversion
**Input:** `I'm gonna wanna go to the shop.`

**Expected Output:**
- Corrected: `I'm going to want to go to the shop.`
- Rules: 
  - Informal → Formal (gonna → going to)
  - Informal → Formal (wanna → want to)

---

### 3. Wordy Phrase Simplification
**Input:** `I am gonna go to the shop in order to buy some goods.`

**Expected Output:**
- Corrected: `I am going to go to the shop to buy some goods.`
- Rules:
  - Informal → Formal
  - Wordy phrase simplification (in order to → to)

---

### 4. Question Reordering (Indirect Questions)
**Input:** `He don't knows where is the market.`

**Expected Output:**
- Corrected: `He doesn't know where the market is.`
- Rules:
  - Spelling correction (don't)
  - Subject-Verb agreement (knows → know)
  - Question reordering (where is the market → where the market is)

---

### 5. Tense Consistency with Time Markers
**Input:** `Yesterday I go to the store and buy some food.`

**Expected Output:**
- Corrected: `Yesterday I goed to the store and buyed some food.`
- Rules:
  - Past Tense conversion (go → goed, buy → buyed)
  - *Note: Naive implementation - should be "went" and "bought"*

---

### 6. Multiple Errors Combined
**Input:** `She dont kno where are the keys and y is it so hard to find?`

**Expected Output:**
- Corrected: Multiple corrections applied
- Rules: Multiple rules fired

---

## API Testing with cURL

### Test 1: Basic Correction
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "sentence": "He go to school",
    "mode": "standard"
  }'
```

### Test 2: Professional Mode
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "sentence": "I gonna buy some good stuff",
    "mode": "professional"
  }'
```

### Test 3: Get Available Rules
```bash
curl http://localhost:8000/rules
```

### Test 4: Health Check
```bash
curl http://localhost:8000/
```

---

## Frontend Testing Checklist

- [ ] Open http://localhost:5500/frontend/index.html
- [ ] Textarea loads with sample text
- [ ] Type a sentence with grammar errors
- [ ] Click "Analyze & Improve" button
- [ ] Results display in three sections:
  - [ ] Original text shown
  - [ ] Corrected text shown
  - [ ] Improved text shown
  - [ ] Rules list populated
- [ ] Try different modes (Standard, Simple, Formal, Professional)
- [ ] Press Ctrl+Enter in textarea to analyze
- [ ] Particle animation plays on analysis
- [ ] Results section glows/pulses

---

## Backend Testing with Python

### Test Script
```python
import requests
import json

BACKEND_URL = "http://localhost:8000"

test_sentences = [
    "She go to school every day.",
    "He don't knows where is the market.",
    "I'm gonna go to the shop in order to buy some goods.",
    "Yesterday I go to the store and buy some food.",
]

for sentence in test_sentences:
    print(f"\n{'='*60}")
    print(f"Input: {sentence}")
    print('='*60)
    
    response = requests.post(
        f"{BACKEND_URL}/process",
        json={"sentence": sentence, "mode": "standard"}
    )
    
    data = response.json()
    print(f"Corrected: {data['corrected']}")
    print(f"Improved: {data['improved']}")
    print(f"Rules fired: {len(data['rules_fired'])}")
    
    for rule in data['rules_fired']:
        print(f"  • {rule['name']}: {rule['reason']}")
        print(f"    {rule['before']} → {rule['after']}")
```

---

## Performance Testing

### Load Testing with Apache Bench
```bash
# 100 requests, 10 concurrent
ab -n 100 -c 10 -p test.json -T application/json http://localhost:8000/process
```

### Test JSON file (test.json)
```json
{"sentence": "He go to school.", "mode": "standard"}
```

---

## Known Limitations to Test

1. **Irregular Verbs**: Naive conjugation
   - Input: `Yesterday I go`
   - Current: `Yesterday I goed` (should be: `went`)

2. **Complex Clauses**: Simple heuristics
   - Input: `Although he go, she dont know why.`
   - May not handle all variations

3. **Context Sensitivity**: Limited
   - Homophones (to/too/two) are not context-aware in current version

4. **Spelling**: Fuzzy matching limitations
   - Heavily misspelled words may not match

---

## Debugging Tips

### Enable Verbose Logging
Edit `backend/app.py` and add:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add in process endpoint
logger.debug(f"Processing: {req.sentence}")
logger.debug(f"Fired rules: {result['rules_fired']}")
```

### Browser Console Errors
- Open DevTools (F12)
- Check Console tab for JavaScript errors
- Check Network tab to see API requests/responses

### Backend Errors
```bash
# Run with verbose output
uvicorn app:app --reload --port 8000 --log-level debug
```

---

## Test Coverage Checklist

- [ ] All 6 grammar rules tested individually
- [ ] Multiple rules firing on single sentence
- [ ] Each rewrite mode tested (standard, simple, formal, professional)
- [ ] Empty input handling
- [ ] Very long input (100+ words)
- [ ] Special characters and punctuation
- [ ] Numbers in sentences
- [ ] Mixed case handling
- [ ] CORS requests from frontend
- [ ] Backend restart and recovery
