# backend/app.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from rule_engine import full_pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NLP Expert System API")

# allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessRequest(BaseModel):
    sentence: str
    mode: str = "standard"   # standard | simple | formal | professional | academic

@app.get("/")
def root():
    return {"message":"NLP Expert System Backend running. POST /process with JSON {sentence, mode}"}

@app.post("/process")
async def process(req: ProcessRequest):
    """
    Returns JSON:
    {
      original, corrected, improved, rules_fired: [{name,reason,before,after}, ...]
    }
    """
    result = full_pipeline(req.sentence)
    # Optionally apply rewrite modes. We'll do a light mode mapping.
    if req.mode and req.mode != "standard":
        # very simple mode handling with replacement heuristics
        if req.mode == "simple":
            # simplify improved -> shorter
            res = result
            res["improved"] = make_simple(res["improved"])
        elif req.mode == "formal":
            res = result
            res["improved"] = make_formal(res["improved"])
        elif req.mode == "professional":
            res = result
            res["improved"] = make_professional(res["improved"])
    return result

@app.get("/rules")
def rules():
    # quick human-readable list of active rule names
    return {
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

# Mode helpers
def make_simple(text):
    # remove some adjectives / simplify
    import re
    text = re.sub(r'\b(favorable|unfavorable|professional)\b', '', text, flags=re.I)
    return ' '.join(text.split())

def make_formal(text):
    return text.replace("gonna", "going to").replace("wanna", "want to")

def make_professional(text):
    return text.replace("good", "satisfactory").replace("bad", "unsatisfactory")
