# Quick Start Guide

## Getting Started in 5 Minutes

### Step 1: Install Dependencies (1 minute)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure API Key (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_key_here
```

### Step 3: Run the Chatbot (3 minutes)

```bash
# Start interactive chat
python main.py
```

That's it! The system includes sample documents and is ready to answer questions.

## Try These Queries

- "What is artificial intelligence?"
- "Explain machine learning types"
- "Tell me about Python programming"
- "What are neural networks?"

## Next Steps

### Run Evaluation

```python
python examples.py  # Runs all examples including evaluation
```

### Add Your Own Documents

1. Place documents in `data/documents/`
2. Supported: `.txt`, `.pdf`, `.docx`, `.md`
3. Rebuild vector store: `python main.py --rebuild`

### Enable Tracing

1. Install AI Toolkit extension in VS Code
2. Set `ENABLE_TRACING=true` in `.env`
3. Traces appear automatically in AI Toolkit

## Common Commands

```bash
# Interactive chat
python main.py

# Single query
python main.py --query "What is AI?"

# Rebuild vector store
python main.py --rebuild

# Run examples
python examples.py

# Run tests
pytest tests/
```

## Architecture Overview

```
User Query
    ↓
[Guardrails] → Input Validation
    ↓
[Retriever] → Vector Store → Top K Documents
    ↓
[LLM] → RAG Prompt with Context
    ↓
[Guardrails] → Output Validation
    ↓
Response + Sources
```

## Evaluation Metrics Explained

**Groundedness** (1-5): Are responses based on the provided context?
**Relevance** (1-5): Do responses address the user's question?
**Coherence** (1-5): Are responses logically structured?
**Fluency** (1-5): Is the language grammatically correct?
**Retrieval** (1-5): How well does the system find relevant documents?

## Troubleshooting

**Problem**: No documents found
**Solution**: Add documents to `data/documents/` and run `python main.py --rebuild`

**Problem**: API key error
**Solution**: Check `.env` file has valid `OPENAI_API_KEY`

**Problem**: Import errors
**Solution**: Activate venv and run `pip install -r requirements.txt`

## Configuration Tips

### For Better Retrieval
- Increase `TOP_K_RETRIEVAL` (default: 5)
- Decrease `CHUNK_SIZE` for more granular context

### For Creative Responses
- Increase `TEMPERATURE` (0.7-1.0)

### For Factual Responses
- Decrease `TEMPERATURE` (0.0-0.3)

## File Structure Quick Reference

```
main.py                 # Main entry point
examples.py            # Example usage scripts
config/config.py       # Configuration
src/chatbot.py         # RAG implementation
evaluation/evaluator.py # Evaluation system
guardrails/            # Safety checks
training/              # Fine-tuning scripts
data/documents/        # Your documents here
```

## Resources

- Full documentation: See `README.md`
- Examples: Run `python examples.py`
- Tests: Run `pytest tests/`

## Support

For issues or questions:
1. Check `README.md` for detailed documentation
2. Review example scripts in `examples.py`
3. Check troubleshooting section above

---

Happy chatting! 🤖
