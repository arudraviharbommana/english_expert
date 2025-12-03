# backend/models/README.md
# Models Directory

This directory is reserved for machine learning models and pre-trained weights.

## Potential Future Models

- **Grammar Correction Model**: Fine-tuned sequence-to-sequence model (e.g., T5, BART)
- **POS Tagging Model**: Custom part-of-speech tagger
- **Named Entity Recognition**: Custom NER model for context-aware corrections
- **Syntax Parsing Model**: Dependency parser improvements
- **Style Classifier**: Classify text by writing style (formal/casual/academic)

## Usage

To add a model:

1. Create a subdirectory with the model name
2. Add model files (weights, vocab, config)
3. Update the backend to load and use the model
4. Document the model in this README

Example structure:
```
models/
├── grammar_seq2seq/
│   ├── model.pt
│   ├── config.json
│   └── README.md
├── style_classifier/
│   ├── weights.pkl
│   └── README.md
└── README.md
```

## Current Models

None (using rule-based system only)

## Notes

- Models should be version-controlled with Git LFS for large files
- Include model cards with performance metrics
- Document training data and methodology
