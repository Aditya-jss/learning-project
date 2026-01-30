# RAG Chatbot - System Architecture

## Overview

This document provides a comprehensive overview of the RAG Chatbot system architecture, components, and data flow.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                     (Interactive CLI / API)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GUARDRAILS LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Input Validation                                         │  │
│  │  • Length checks     • PII detection                      │  │
│  │  • Content filtering • Toxicity detection                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       RAG PIPELINE                               │
│  ┌────────────────┐    ┌──────────────┐    ┌─────────────────┐ │
│  │   Document     │    │   Vector     │    │   Retrieval     │ │
│  │   Processing   │───▶│   Store      │───▶│   (Top-K)       │ │
│  │   • Load docs  │    │   (ChromaDB) │    │   Documents     │ │
│  │   • Chunk text │    │   • Embed    │    │                 │ │
│  │   • Add meta   │    │   • Index    │    │                 │ │
│  └────────────────┘    └──────────────┘    └────────┬────────┘ │
│                                                       │          │
│  ┌────────────────────────────────────────────────────┘          │
│  │                                                               │
│  ▼                                                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              LLM (OpenAI / Azure OpenAI)                  │  │
│  │  • Query + Retrieved Context → Prompt                     │  │
│  │  • Generate Response                                       │  │
│  │  • Conversation History (optional)                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  OUTPUT GUARDRAILS                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Length control  • PII redaction                        │  │
│  │  • Safety checks   • Content validation                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSE + SOURCES                            │
│  • Generated Answer                                              │
│  • Source Documents                                              │
│  • Metadata & Citations                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Document Processing Layer
**Purpose**: Load, process, and prepare documents for embedding

**Components**:
- `DocumentProcessor`: Handles multiple file formats (PDF, TXT, DOCX, MD)
- Text splitter: Breaks documents into manageable chunks
- Metadata enrichment: Adds source, filename, and file type

**Key Parameters**:
- `CHUNK_SIZE`: 1000 characters
- `CHUNK_OVERLAP`: 200 characters

### 2. Vector Store Layer
**Purpose**: Create and manage vector embeddings for semantic search

**Components**:
- Embedding Model: `text-embedding-3-small` (OpenAI)
- Vector Database: ChromaDB (persistent storage)
- Similarity Search: Cosine similarity for document retrieval

**Features**:
- Persistent storage
- Incremental updates
- Top-K retrieval

### 3. RAG Chatbot Layer
**Purpose**: Generate contextual responses using retrieved documents

**Components**:
- LLM: GPT-4o-mini (OpenAI) or Azure OpenAI
- Retrieval Chain: LangChain RetrievalQA
- Prompt Engineering: Custom RAG prompt template
- Conversation Memory: Optional history tracking

**Features**:
- Single-turn and multi-turn conversations
- Source document tracking
- Configurable temperature and max tokens

### 4. Guardrails Layer
**Purpose**: Ensure safe and appropriate inputs/outputs

**Input Guardrails**:
- Maximum length enforcement (2000 chars)
- PII detection (email, phone, SSN, credit cards)
- Blocked content patterns
- Toxicity detection

**Output Guardrails**:
- Response length control
- PII redaction
- Content safety validation

**Violation Severity**:
- High: Blocks request/response
- Medium: Logs warning, allows with sanitization
- Low: Informational only

### 5. Evaluation System
**Purpose**: Measure and improve chatbot performance

**Built-in Evaluators** (Azure AI Evaluation SDK):
- **Groundedness**: Context-response alignment (1-5)
- **Relevance**: Query-response alignment (1-5)
- **Retrieval**: Document retrieval quality (1-5)
- **Coherence**: Logical structure (1-5)
- **Fluency**: Grammar and readability (1-5)
- **Similarity**: Ground truth comparison (1-5)

**Custom Evaluators**:
- Answer Length: Appropriate response length
- Context Relevance: Query-context alignment

**Output**:
- Row-level scores
- Aggregate metrics
- Detailed analysis reports

### 6. Training & Fine-tuning Layer
**Purpose**: Improve model performance through training

**Components**:
- Data Preparation: Q&A pair generation
- Fine-tuning Manager: OpenAI fine-tuning API integration
- Version Manager: Track and compare model versions

**Features**:
- Training data generation
- Model fine-tuning pipeline
- Version comparison
- Metrics tracking

### 7. Observability Layer
**Purpose**: Monitor and debug system behavior

**Components**:
- OpenTelemetry tracing
- LLM call instrumentation
- Performance metrics

**Endpoints**:
- OTLP HTTP: `http://localhost:4318`
- Integration with AI Toolkit trace viewer

## Data Flow

### Query Processing Flow

1. **User submits query** → Interactive CLI or API
2. **Input validation** → Guardrails check length, PII, content
3. **Sanitization** → Remove/redact sensitive information
4. **Document retrieval** → Vector similarity search (Top-K)
5. **Context assembly** → Combine query + retrieved documents
6. **LLM processing** → Generate response with context
7. **Output validation** → Check response safety and quality
8. **Response delivery** → Return answer + source citations

### Evaluation Flow

1. **Test dataset creation** → Query chatbot with test questions
2. **Data formatting** → Convert to JSONL with required fields
3. **Evaluator initialization** → Configure model and evaluators
4. **Batch evaluation** → Run all evaluators via `evaluate()` API
5. **Results aggregation** → Automatic metric computation
6. **Report generation** → Save detailed results

### Training Flow

1. **Data collection** → Gather documents and Q&A pairs
2. **Data preparation** → Format for fine-tuning
3. **File upload** → Send to OpenAI API
4. **Job creation** → Start fine-tuning process
5. **Monitoring** → Track training progress
6. **Version registration** → Save model metadata
7. **Deployment** → Use fine-tuned model in chatbot

## Configuration Management

### Environment Variables

```
# LLM Configuration
OPENAI_API_KEY / AZURE_OPENAI_ENDPOINT
OPENAI_MODEL / AZURE_OPENAI_DEPLOYMENT

# RAG Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=5

# Generation Parameters
TEMPERATURE=0.7
MAX_TOKENS=1000

# Safety Configuration
ENABLE_GUARDRAILS=true
MAX_INPUT_LENGTH=2000

# Observability
ENABLE_TRACING=true
OTLP_ENDPOINT=http://localhost:4318
```

## Integration Points

### External Services
- **OpenAI API**: LLM inference and embeddings
- **Azure OpenAI**: Alternative LLM provider
- **AI Toolkit**: Trace visualization

### Internal Components
- All components communicate through Python imports
- Configuration centralized in `config/config.py`
- Logging via Python logging module

## Performance Considerations

### Optimization Strategies
1. **Vector Store**: Persistent ChromaDB for fast retrieval
2. **Caching**: Reuse embeddings when possible
3. **Batch Processing**: Process multiple queries efficiently
4. **Async Operations**: Future enhancement for concurrency

### Scalability
- Vector store can handle thousands of documents
- LLM calls can be rate-limited as needed
- Horizontal scaling possible via API deployment

## Security & Privacy

### Data Protection
- PII detection and redaction
- No data persistence outside vector store
- Configurable content filtering

### API Key Management
- Environment variable storage
- No hardcoded credentials
- Support for multiple providers

## Extension Points

### Easy Customization
1. **Custom Evaluators**: Add business-specific metrics
2. **Document Loaders**: Support new file formats
3. **LLM Providers**: Add new model integrations
4. **Guardrail Rules**: Customize validation logic

### Future Enhancements
- Web UI interface
- REST API endpoint
- Multi-language support
- Advanced caching layer
- Async processing

## Deployment Options

### Local Development
- CLI interface (current)
- Jupyter notebooks
- VS Code integration

### Production Deployment
- Docker containerization
- API server (FastAPI)
- Cloud deployment (Azure, AWS, GCP)
- Monitoring and logging

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| LLM | OpenAI / Azure OpenAI | Text generation |
| Embeddings | OpenAI Embeddings | Vector representation |
| Vector DB | ChromaDB | Similarity search |
| Framework | LangChain | RAG orchestration |
| Evaluation | Azure AI Evaluation SDK | Performance metrics |
| Guardrails | Custom + Patterns | Safety & validation |
| Tracing | OpenTelemetry | Observability |
| Language | Python 3.8+ | Implementation |

## Conclusion

This RAG chatbot system provides a production-ready foundation for building intelligent, safe, and measurable conversational AI applications. The modular architecture allows for easy customization and extension while maintaining robust safety and evaluation capabilities.
