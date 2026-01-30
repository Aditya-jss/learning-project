# RAG Chatbot with Guardrails and Evaluation

A complete end-to-end Retrieval-Augmented Generation (RAG) chatbot implementation with comprehensive guardrails, evaluation metrics, training capabilities, and observability.

## 🎯 Features

- **RAG Implementation**: Full RAG pipeline using LangChain and ChromaDB
- **Multiple LLM Support**: OpenAI and Azure OpenAI integration
- **Guardrails System**: Input/output validation, content filtering, PII detection
- **Comprehensive Evaluation**: Azure AI Evaluation SDK with RAG-specific metrics
- **Fine-tuning Support**: Model training and version management
- **Observability**: OpenTelemetry tracing integration
- **Conversational Memory**: Context-aware multi-turn conversations

## 📁 Project Structure

```
rag-chatbot/
├── config/
│   └── config.py              # Configuration management
├── src/
│   ├── document_processor.py  # Document loading and processing
│   ├── vector_store.py        # Vector store management
│   ├── chatbot.py            # RAG chatbot implementation
│   └── tracing.py            # OpenTelemetry tracing setup
├── guardrails/
│   └── guardrails_manager.py # Input/output validation and safety
├── evaluation/
│   ├── evaluator.py          # Comprehensive evaluation system
│   └── results/              # Evaluation results output
├── training/
│   ├── data_preparation.py   # Training data preparation
│   ├── fine_tuning.py        # Model fine-tuning
│   ├── data/                 # Training datasets
│   └── versions/             # Model version management
├── data/
│   ├── documents/            # Source documents for RAG
│   └── vectorstore/          # ChromaDB vector store
├── main.py                   # Main application entry point
├── requirements.txt          # Python dependencies
└── .env.example             # Environment variables template
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd rag-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```bash
# For OpenAI
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# OR for Azure OpenAI
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_API_KEY=your_azure_openai_key
# AZURE_OPENAI_DEPLOYMENT=your_deployment_name
```

### 3. Add Documents

Add your documents to the `data/documents/` directory. Supported formats:
- Text files (`.txt`)
- PDF files (`.pdf`)
- Word documents (`.docx`)
- Markdown files (`.md`)

Sample documents are already included to get you started!

### 4. Run the Chatbot

```bash
# Interactive mode
python main.py

# Single query mode
python main.py --query "What is machine learning?"

# Rebuild vector store from documents
python main.py --rebuild
```

## 📊 Evaluation

### Running Evaluation

```python
from main import initialize_rag_system
from evaluation.evaluator import run_comprehensive_evaluation
import os

# Initialize chatbot
chatbot = initialize_rag_system()

# Define test queries
test_queries = [
    "What is artificial intelligence?",
    "Explain deep learning",
    "What are the applications of AI in healthcare?"
]

# Optional: Add ground truth answers
ground_truths = [
    "AI is the simulation of human intelligence by machines...",
    "Deep learning uses neural networks with multiple layers...",
    "AI in healthcare includes disease diagnosis, drug discovery..."
]

# Run evaluation
results = run_comprehensive_evaluation(
    chatbot=chatbot,
    test_queries=test_queries,
    ground_truths=ground_truths,  # Optional
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

print(f"Evaluation Results: {results['metrics']}")
```

### Evaluation Metrics

The system evaluates your RAG chatbot on:

**RAG-Specific Metrics:**
- **Groundedness**: How well responses are supported by context
- **Relevance**: Alignment with user queries
- **Retrieval Quality**: Effectiveness of document retrieval

**Quality Metrics:**
- **Coherence**: Logical flow and structure
- **Fluency**: Grammar and readability
- **Similarity**: Match with ground truth (if provided)

**Custom Metrics:**
- **Answer Length**: Appropriate response length
- **Context Relevance**: Query-context alignment

## 🛡️ Guardrails

The system includes comprehensive guardrails:

### Input Validation
- Length limits
- Blocked content patterns
- PII detection (email, phone, SSN, credit cards)
- Toxic content filtering

### Output Validation
- Response length control
- PII redaction
- Safety checks

### Usage

Guardrails are automatically applied when `ENABLE_GUARDRAILS=true` in `.env`:

```python
# Guardrails automatically applied
response = chatbot.chat("Your query here")

if response.get('blocked'):
    print("Response blocked by guardrails")
if response.get('guardrails_warnings'):
    print(f"Warnings: {response['guardrails_warnings']}")
```

## 🎓 Training & Fine-tuning

### Prepare Training Data

```python
from training.data_preparation import DataPreparator, ModelVersionManager

# Initialize preparator
preparator = DataPreparator()

# Create Q&A pairs from documents
qa_data_path = preparator.create_qa_pairs_from_documents(
    documents=your_documents,
    output_file="qa_training_data.jsonl"
)

# Prepare for fine-tuning
fine_tuning_data = preparator.prepare_fine_tuning_data(
    qa_pairs=qa_pairs,
    output_file="fine_tuning_data.jsonl"
)
```

### Fine-tune Model

```python
from training.fine_tuning import run_fine_tuning_pipeline
import os

# Run fine-tuning
result = run_fine_tuning_pipeline(
    training_file_path="./training/data/fine_tuning_data.jsonl",
    base_model="gpt-4o-mini-2024-07-18",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    wait_for_completion=True
)

print(f"Fine-tuned model: {result['fine_tuned_model']}")
```

### Manage Model Versions

```python
from training.data_preparation import ModelVersionManager

version_manager = ModelVersionManager()

# Register new version
version_manager.register_version(
    version_name="v1.0",
    model_id="ft:gpt-4o-mini:...",
    description="First fine-tuned version",
    metrics={"groundedness": 4.5, "relevance": 4.2}
)

# Set as current version
version_manager.set_current_version("v1.0")

# List all versions
versions = version_manager.list_versions()
```

## 📈 Observability & Tracing

### Enable Tracing

1. Ensure AI Toolkit is installed in VS Code
2. Set `ENABLE_TRACING=true` in `.env`
3. The system will automatically send traces to `http://localhost:4318`

### View Traces

Traces are sent to AI Toolkit's trace viewer in VS Code, allowing you to:
- Monitor LLM calls
- Track latency
- Debug issues
- Analyze performance

## 🔧 Advanced Usage

### Custom Evaluators

Create custom evaluators for specific needs:

```python
class CustomEvaluator:
    def __init__(self):
        pass
    
    def __call__(self, *, response: str, **kwargs):
        # Your evaluation logic
        score = calculate_score(response)
        return {"custom_score": score}
```

### Batch Processing

```python
queries = ["Query 1", "Query 2", "Query 3"]
responses = chatbot.batch_chat(queries)
```

### Clear Conversation History

```python
if hasattr(chatbot, 'clear_history'):
    chatbot.clear_history()
```

## 📚 API Reference

### RAGChatbot

```python
RAGChatbot(
    retriever,                    # LangChain retriever
    model_name="gpt-4o-mini",    # Model name
    temperature=0.7,              # Response creativity
    max_tokens=1000,              # Max response length
    use_azure=False,              # Use Azure OpenAI
    azure_endpoint=None,          # Azure endpoint
    azure_api_key=None,           # Azure API key
    azure_deployment=None,        # Azure deployment
    openai_api_key=None           # OpenAI API key
)
```

### GuardrailsManager

```python
GuardrailsManager(
    max_input_length=2000,        # Max input chars
    max_output_length=2000,       # Max output chars
    enable_content_filter=True,   # Filter blocked content
    enable_pii_detection=True     # Detect PII
)
```

### RAGEvaluator

```python
RAGEvaluator(
    use_azure=False,              # Use Azure OpenAI
    azure_endpoint=None,          # Azure endpoint
    azure_api_key=None,           # Azure API key
    azure_deployment=None,        # Azure deployment
    openai_api_key=None,          # OpenAI API key
    openai_model="gpt-4o-mini"   # Model for evaluation
)
```

## 🧪 Testing

Run tests to ensure everything works:

```bash
pytest tests/
```

## 📝 Example Queries

Try these queries with the sample documents:

- "What is artificial intelligence?"
- "Explain the different types of machine learning"
- "What are some applications of AI?"
- "Tell me about Python programming"
- "What are the best practices for Python development?"
- "Explain deep learning and neural networks"

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open-source and available under the MIT License.

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Azure AI Evaluation SDK](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/evaluate-sdk)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 💡 Tips

1. **Start with sample documents**: Test the system with provided documents first
2. **Monitor traces**: Use AI Toolkit trace viewer to debug issues
3. **Tune parameters**: Adjust `CHUNK_SIZE`, `TOP_K_RETRIEVAL`, and `TEMPERATURE` for better results
4. **Regular evaluation**: Run evaluations after making changes
5. **Version control**: Use git to track your model versions and configurations

## 🆘 Troubleshooting

### Vector Store Issues
- Delete `data/vectorstore/` and run with `--rebuild` flag

### API Key Errors
- Verify `.env` file has correct API keys
- Check if keys are properly exported

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment

### Tracing Not Working
- Ensure AI Toolkit extension is installed in VS Code
- Check if OTLP endpoint is accessible

## 🎉 Getting Started Example

```python
# Complete example
from main import initialize_rag_system

# Initialize the system
chatbot = initialize_rag_system(rebuild_vectorstore=True)

# Ask a question
response = chatbot.chat("What is machine learning?")

# View response
print(f"Answer: {response['response']}")
print(f"Sources: {len(response['source_documents'])} documents")

# Run evaluation
from evaluation.evaluator import run_comprehensive_evaluation
import os

results = run_comprehensive_evaluation(
    chatbot=chatbot,
    test_queries=["What is AI?", "Explain deep learning"],
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

print(f"Evaluation complete! Metrics: {results['metrics']}")
```

---

**Built with ❤️ using LangChain, ChromaDB, Azure AI Evaluation SDK, and OpenAI**
