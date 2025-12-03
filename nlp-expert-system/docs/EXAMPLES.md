# docs/EXAMPLES.md
# Usage Examples & Test Cases

## Quick Start Examples

### Example 1: Subject-Verb Agreement

```
Input: "She go to school every day."

Expected output:
- Corrected: "She goes to school every day."
- Improved: "She visits school every day."
- Rules fired:
  1. Subject-Verb agreement: "go" → "goes"
  2. Heuristic rewrite: "go to" → "visit"
```

**cURL Request**:
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"sentence": "She go to school every day.", "mode": "standard"}'
```

---

### Example 2: Informal to Formal + Wordy Simplification

```
Input: "I am gonna go to the shop in order to buy some goods."

Expected output:
- Corrected: "I am going to go to the shop to buy some goods."
- Improved: "I am going to go to the shop to purchase some goods."
- Rules fired:
  1. Informal → Formal: "gonna" → "going to"
  2. Wordy phrase simplification: "in order to" → "to"
  3. Heuristic rewrite: "buy" → "purchase" "goods" → ?
```

**Python Request**:
```python
import requests

url = "http://localhost:8000/process"
payload = {
    "sentence": "I am gonna go to the shop in order to buy some goods.",
    "mode": "professional"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Original:  {result['original']}")
print(f"Corrected: {result['corrected']}")
print(f"Improved:  {result['improved']}")
print(f"\nRules fired: {len(result['rules_fired'])}")
for rule in result['rules_fired']:
    print(f"  - {rule['name']}: '{rule['before']}' → '{rule['after']}'")
```

---

### Example 3: Complex Grammar Issues

```
Input: "He don't knows where is the market."

Expected output:
- Corrected: "He doesn't know where the market is."
- Rules fired:
  1. Spelling correction: "dont" → "don't"
  2. Subject-Verb agreement: "knows" → "know" (?)
  3. Question reordering: "where is the market" → "where the market is"
```

**JavaScript Fetch**:
```javascript
const sentence = "He don't knows where is the market.";

fetch("http://localhost:8000/process", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ sentence, mode: "standard" })
})
.then(res => res.json())
.then(data => {
  console.log("Original:", data.original);
  console.log("Corrected:", data.corrected);
  
  console.log("\nRules applied:");
  data.rules_fired.forEach((rule, i) => {
    console.log(`${i+1}. ${rule.name}`);
    console.log(`   Reason: ${rule.reason}`);
    console.log(`   Before: "${rule.before}"`);
    console.log(`   After: "${rule.after}"`);
  });
});
```

---

### Example 4: Tense Consistency

```
Input: "Yesterday I go to the store and buy some food."

Expected output:
- Corrected: "Yesterday I goed to the store and buyed some food."
  (Note: This is naive - should be "went" and "bought")
- Rules fired:
  1. Tense consistency: "go" → "goed"
  2. Tense consistency: "buy" → "buyed"
```

**Note**: This rule is intentionally naive to demonstrate the limitation!

---

### Example 5: Already Correct Sentence

```
Input: "I want to learn English grammar."

Expected output:
- Corrected: "I want to learn English grammar." (no change)
- Improved: "I desire to learn English grammar." (heuristic rewrite)
- Rules fired: (empty list or minimal)
```

---

## Testing All Modes

```python
import requests

sentence = "I'm gonna buy some good stuff in order to make it better."
modes = ["standard", "simple", "formal", "professional"]

for mode in modes:
    resp = requests.post(
        "http://localhost:8000/process",
        json={"sentence": sentence, "mode": mode}
    )
    result = resp.json()
    print(f"\n=== Mode: {mode.upper()} ===")
    print(f"Improved: {result['improved']}")
```

**Expected output**:
```
=== Mode: STANDARD ===
Improved: I am going to purchase some favorable material to make it better.

=== Mode: SIMPLE ===
Improved: I am going to purchase some material to make it better.

=== Mode: FORMAL ===
Improved: I am going to purchase some favorable material to make it better.

=== Mode: PROFESSIONAL ===
Improved: I am going to purchase some favorable material to make it better.
```

---

## Batch Testing Script

```python
import requests
import json

test_cases = [
    {
        "name": "Subject-Verb Agreement",
        "input": "She go to the gym every day.",
        "expected_rules": ["Subject-Verb agreement"]
    },
    {
        "name": "Informal to Formal",
        "input": "I wanna go to the store to get some stuff.",
        "expected_rules": ["Informal -> Formal"]
    },
    {
        "name": "Spelling Errors",
        "input": "He recieve the letter yesterday.",
        "expected_rules": ["Spelling correction"]
    },
    {
        "name": "Wordy Phrases",
        "input": "In order to succeed, you need to work hard.",
        "expected_rules": ["Wordy phrase simplification"]
    },
    {
        "name": "Question Reordering",
        "input": "Do you know where is the library?",
        "expected_rules": ["Question reordering"]
    },
    {
        "name": "Tense Consistency",
        "input": "Last week I go to Paris and see the Eiffel Tower.",
        "expected_rules": ["Past Tense conversion"]
    },
    {
        "name": "Already Correct",
        "input": "The weather is beautiful today.",
        "expected_rules": []
    },
]

BASE_URL = "http://localhost:8000"

print("Testing NLP Expert System\n")
print("=" * 70)

passed = 0
failed = 0

for test in test_cases:
    response = requests.post(
        f"{BASE_URL}/process",
        json={"sentence": test["input"], "mode": "standard"}
    )
    
    result = response.json()
    rules_fired = [r["name"] for r in result.get("rules_fired", [])]
    
    # Check if expected rules were fired
    all_found = all(rule in rules_fired for rule in test["expected_rules"])
    
    status = "✓ PASS" if all_found else "✗ FAIL"
    if all_found:
        passed += 1
    else:
        failed += 1
    
    print(f"\n{status}: {test['name']}")
    print(f"Input: {test['input']}")
    print(f"Output: {result['corrected']}")
    print(f"Expected rules: {test['expected_rules']}")
    print(f"Fired rules: {rules_fired}")

print("\n" + "=" * 70)
print(f"Results: {passed} passed, {failed} failed")
```

---

## Frontend Usage

Open `http://localhost:5500/frontend/index.html` and:

1. **Type or paste** a sentence in the textarea
2. **Select a mode** (Standard, Simple, Formal, Professional)
3. **Click "Analyze & Improve"** or press **Ctrl+Enter**
4. **View results**:
   - Original sentence
   - Corrected version
   - Improved/rewritten version
   - Detailed rule logs

### Example Workflow

1. Input: `"He dont knows where is the market."`
2. Mode: `Standard`
3. Click Analyze
4. Results show:
   - Original: "He dont knows where is the market."
   - Corrected: "He doesn't know where the market is."
   - Improved: "He doesn't know where the market is." (no further improvements)
   - Rules: 3 rules fired (spelling, question reordering, etc.)

---

## Performance Testing

### Time Complexity Test

```python
import requests
import time

sentences = [
    "I go.",  # short
    "I am gonna go to the shop in order to buy some goods.",  # medium
    "Yesterday I went to the market and I did buy many things because I wanted to prepare for the party that is happening next week.",  # long
]

for sent in sentences:
    start = time.time()
    resp = requests.post(
        "http://localhost:8000/process",
        json={"sentence": sent, "mode": "standard"}
    )
    elapsed = time.time() - start
    
    print(f"Length: {len(sent):3d} chars | Time: {elapsed*1000:6.2f}ms")
```

**Expected output** (typical):
```
Length:   6 chars | Time:  120.45ms
Length:  68 chars | Time:  145.32ms
Length: 180 chars | Time:  185.67ms
```

---

## Error Handling Examples

### Empty Input

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"sentence": "", "mode": "standard"}'
```

**Response**: May process or show empty, depending on implementation

### Invalid Mode

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"sentence": "Hello world", "mode": "invalid_mode"}'
```

**Response**: Currently no validation, but could return error

### Non-English Text

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"sentence": "Bonjour le monde", "mode": "standard"}'
```

**Response**: Will likely fail gracefully or return unchanged

---

## Integration Examples

### With Your Own Frontend

```javascript
const analyzeText = async (text) => {
  const response = await fetch("http://localhost:8000/process", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sentence: text,
      mode: "professional"
    })
  });
  
  const data = await response.json();
  return data.corrected;
};

// Usage
const corrected = await analyzeText("She go to school");
console.log(corrected); // "She goes to school"
```

### With React

```jsx
import { useState } from "react";

function TextCorrector() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sentence: input, mode: "standard" })
      });
      const data = await response.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <textarea value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>
      
      {result && (
        <div>
          <p>Corrected: {result.corrected}</p>
          <ul>
            {result.rules_fired.map((rule, i) => (
              <li key={i}>{rule.name}: {rule.before} → {rule.after}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default TextCorrector;
```

---

## Debugging Tips

### Enable Verbose Logging

Add to `backend/app.py`:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/process")
async def process(req: ProcessRequest):
    logger.info(f"Processing: {req.sentence}")
    result = full_pipeline(req.sentence)
    logger.info(f"Rules fired: {len(result['rules_fired'])}")
    return result
```

### Test Individual Rules

```python
from rule_engine import (
    apply_informal_replacements,
    apply_wordy_simplification,
    apply_spelling_corrections,
    preprocess
)

text = "I'm gonna go in order to buy stuff"

# Test Rule 1
r1 = apply_informal_replacements(text)
print(f"After informal: {r1['after'] if r1 else 'no change'}")

# Test Rule 2
r2 = apply_wordy_simplification(text)
print(f"After wordy: {r2['after'] if r2 else 'no change'}")
```
