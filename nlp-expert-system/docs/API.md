# docs/API.md
# NLP Expert System API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check

**GET** `/`

Returns service status.

**Response:**
```json
{
  "message": "NLP Expert System Backend running. POST /process with JSON {sentence, mode}"
}
```

---

### 2. Process Sentence

**POST** `/process`

Analyzes and corrects an English sentence using the rule-based grammar engine.

**Request Body:**
```json
{
  "sentence": "He don't knows where is the market.",
  "mode": "standard"
}
```

**Parameters:**
- `sentence` (string, required): English sentence to analyze
- `mode` (string, optional): Rewrite style
  - `"standard"`: Default correction
  - `"simple"`: Simplified language
  - `"formal"`: Formal writing style
  - `"professional"`: Professional tone
  - Default: `"standard"`

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

**Status Codes:**
- `200 OK`: Successful processing
- `422 Unprocessable Entity`: Invalid request format
- `500 Internal Server Error`: Server error

---

### 3. Get Available Rules

**GET** `/rules`

Returns list of all grammar correction rules implemented.

**Response:**
```json
{
  "rules": [
    "Informal -> Formal (gonna -> going to ...)",
    "Wordy phrase simplification",
    "Spelling correction (fuzzy)",
    "Subject-Verb agreement (naive)",
    "Tense conversion (naive)",
    "Question reordering (indirect question handling)",
    "Heuristic rewrite (simple synonyms)"
  ]
}
```

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error description"
}
```

### Common Errors

**Empty Sentence:**
```json
{
  "detail": "Sentence cannot be empty"
}
```

**Invalid Mode:**
```json
{
  "detail": "Invalid mode. Choose from: standard, simple, formal, professional"
}
```

---

## Rate Limiting

Currently no rate limiting. For production, consider:
- Implementing token-based rate limiting
- Setting request per minute limits per client
- Adding API key authentication

---

## CORS

CORS is enabled for all origins (`*`). For production, restrict to specific domains:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

---

## Request Examples

### cURL

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"sentence": "He go to school", "mode": "formal"}'
```

### Python Requests

```python
import requests

url = "http://localhost:8000/process"
data = {
    "sentence": "I am gonna go to the shop in order to buy some goods.",
    "mode": "professional"
}

response = requests.post(url, json=data)
result = response.json()

print(f"Original: {result['original']}")
print(f"Corrected: {result['corrected']}")
print(f"Improved: {result['improved']}")

for rule in result['rules_fired']:
    print(f"- {rule['name']}: {rule['before']} → {rule['after']}")
```

### JavaScript Fetch

```javascript
const data = {
  sentence: "She go to school everyday",
  mode: "standard"
};

fetch("http://localhost:8000/process", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(data)
})
.then(r => r.json())
.then(result => {
  console.log("Corrected:", result.corrected);
  console.log("Rules fired:", result.rules_fired.length);
});
```

---

## Response Time

- Average: 100-300ms
- Depends on:
  - Sentence length
  - Number of rules triggered
  - spaCy model complexity

---

## Versioning

Current API Version: 1.0

Future versions may include:
- Batch processing endpoint
- Confidence scores for each correction
- Interactive correction suggestions
- Custom rule loading
