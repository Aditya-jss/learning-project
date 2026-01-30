# RAG Chatbot with Redis Session Management - Complete Index

## 📋 Quick Navigation

### For Interview Preparation (START HERE!)

1. **[INTERVIEW_TALKING_POINTS.md](INTERVIEW_TALKING_POINTS.md)** ⭐ **START HERE**
   - 30-second summary of problem & solution
   - Deep dive into root cause
   - Key improvements & metrics
   - Anticipated questions with answers
   - 2-3 minute interview script
   - **Time to read: 5-10 minutes**

2. **[REDIS_BEFORE_AFTER.md](REDIS_BEFORE_AFTER.md)** ⭐ **UNDERSTAND THE PROBLEM**
   - Interview scenario context (AI Infoways case study)
   - BEFORE: Why context was lost
   - AFTER: How Redis solves it
   - Feature comparison matrix
   - Real-world walkthroughs
   - Troubleshooting guide
   - **Time to read: 10-15 minutes**

3. **[ARCHITECTURE_VISUAL.md](ARCHITECTURE_VISUAL.md)** ⭐ **VISUALIZE THE SOLUTION**
   - Before/after architecture diagrams
   - Complete data flow
   - State transitions
   - Storage comparison
   - Scalability diagrams
   - **Time to read: 5-10 minutes**

4. **[demo_redis_before_after.py](demo_redis_before_after.py)** ⭐ **SEE IT IN ACTION**
   - Run this to see both modes compared
   - Shows context loss in BEFORE mode
   - Shows persistence in AFTER mode
   - Interactive demonstration
   - **Time to run: 2-3 minutes**

---

### Understanding the RAG System

5. **[README.md](README.md)** - Complete project overview
   - Features list
   - Architecture overview
   - Getting started
   - Usage guide

6. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup
   - Install dependencies
   - Set up API keys
   - Run first chat
   - Basic troubleshooting

7. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Deep technical dive
   - System components
   - Data flow diagrams
   - Technology choices
   - Extension points

8. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Feature overview
   - Core capabilities
   - Guardrails system
   - Evaluation metrics
   - Training pipeline

---

### Code Files (Implementation)

#### Core RAG System
- **[src/chatbot.py](src/chatbot.py)** - RAG implementation (basic + conversational)
- **[src/document_processor.py](src/document_processor.py)** - Multi-format document loading
- **[src/vector_store.py](src/vector_store.py)** - ChromaDB vector store management
- **[src/tracing.py](src/tracing.py)** - OpenTelemetry tracing setup

#### Redis Session Management (NEW!)
- **[src/redis_session.py](src/redis_session.py)** - RedisSessionManager class (450+ lines)
  - Session creation, loading, persistence
  - Message storage with timestamps
  - History formatting for LLM context
  - Graceful fallback to in-memory
  - **Key Classes**: `RedisSessionManager`, `ChatbotWithRedisSession`, `ConversationMessage`

#### Safety & Evaluation
- **[guardrails/guardrails_manager.py](guardrails/guardrails_manager.py)** - Input/output validation, PII detection
- **[evaluation/evaluator.py](evaluation/evaluator.py)** - Azure AI Evaluation SDK integration

#### Training & Fine-tuning
- **[training/data_preparation.py](training/data_preparation.py)** - Q&A pair creation, data versioning
- **[training/fine_tuning.py](training/fine_tuning.py)** - OpenAI fine-tuning integration

#### Configuration
- **[config/config.py](config/config.py)** - Environment and API key management
- **[.env.example](.env.example)** - Template for environment variables

#### Application Entry Points
- **[main.py](main.py)** - Original CLI app (in-memory only, BEFORE mode)
- **[main_with_redis.py](main_with_redis.py)** - NEW: Updated app with Redis support (AFTER mode)
- **[examples.py](examples.py)** - Usage examples and patterns

#### Testing
- **[tests/test_chatbot.py](tests/test_chatbot.py)** - Unit tests

---

### Sample Data

- **[data/documents/ai_ml_introduction.txt](data/documents/ai_ml_introduction.txt)** - Sample AI/ML document
- **[data/documents/python_guide.txt](data/documents/python_guide.txt)** - Sample Python document

---

### Configuration Files

- **[requirements.txt](requirements.txt)** - Python dependencies (includes redis>=5.0.0)
- **[.gitignore](.gitignore)** - Git ignore rules
- **[setup.sh](setup.sh)** - Automation setup script

---

## 🎯 Reading Paths

### Path 1: Quick Interview Prep (30 minutes)
1. [INTERVIEW_TALKING_POINTS.md](INTERVIEW_TALKING_POINTS.md) (10 min) - Understand talking points
2. [REDIS_BEFORE_AFTER.md](REDIS_BEFORE_AFTER.md) (10 min) - Deep context
3. [demo_redis_before_after.py](demo_redis_before_after.py) (5 min) - See demo
4. Review anticipated questions (5 min)

### Path 2: Technical Deep Dive (1-2 hours)
1. [README.md](README.md) - Project overview
2. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
3. [ARCHITECTURE_VISUAL.md](ARCHITECTURE_VISUAL.md) - Visual architecture
4. [src/redis_session.py](src/redis_session.py) - Study implementation
5. [main_with_redis.py](main_with_redis.py) - Study integration

### Path 3: Full Learning (3-4 hours)
1. Complete Path 2
2. [src/chatbot.py](src/chatbot.py) - Base RAG implementation
3. [src/document_processor.py](src/document_processor.py) - Document handling
4. [guardrails/guardrails_manager.py](guardrails/guardrails_manager.py) - Safety layer
5. [evaluation/evaluator.py](evaluation/evaluator.py) - Evaluation metrics
6. [training/fine_tuning.py](training/fine_tuning.py) - Training pipeline

### Path 4: Get It Running (1 hour)
1. [QUICKSTART.md](QUICKSTART.md) - Setup instructions
2. Install dependencies: `pip install -r requirements.txt`
3. Set up `.env` file with API keys
4. Run BEFORE mode: `python main.py`
5. Run AFTER mode with Redis: `python main_with_redis.py --redis`

---

## 🚀 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Set up Redis locally
brew install redis  # macOS
redis-server        # Start Redis

# In another terminal:

# Try BEFORE mode (in-memory only)
python main.py

# Try AFTER mode (with Redis)
python main_with_redis.py --redis

# Run interactive demo
python demo_redis_before_after.py

# Run with specific query
python main_with_redis.py --redis --query "What is machine learning?"

# Run in BEFORE mode (for comparison)
python main_with_redis.py --mode before
```

---

## 📊 System Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              RAG CHATBOT SYSTEM                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  USER INTERFACE (CLI)                            │  │
│  │  main.py (BEFORE) or main_with_redis.py (AFTER) │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                   │
│  ┌──────────────────▼──────────────────────────────┐   │
│  │  SESSION MANAGEMENT (NEW!)                      │   │
│  │  src/redis_session.py (Redis + In-Memory)       │   │
│  └──────────────┬────────────────────┬─────────────┘   │
│                 │                    │                 │
│  ┌──────────────▼──┐    ┌────────────▼──────────────┐  │
│  │  RAM Cache      │    │  Redis (Persistent)       │  │
│  │  (Fast)         │    │  (Durable + TTL)          │  │
│  └────────────────┘    └───────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  RAG ENGINE                                      │  │
│  │  src/chatbot.py + src/document_processor.py     │  │
│  │  + src/vector_store.py (ChromaDB)               │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                       │
│  ┌──────────────▼────────────────────────────────┐     │
│  │  SAFETY & EVALUATION                          │     │
│  │  guardrails/ + evaluation/                    │     │
│  │  - PII Detection                              │     │
│  │  - Content Filtering                          │     │
│  │  - Azure AI Evaluation SDK                    │     │
│  └──────────────────────────────────────────────┘     │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  LLM & VECTOR DB                                │  │
│  │  OpenAI/Azure OpenAI API + ChromaDB            │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔑 Key Features

### Core RAG Features
✅ Document loading (PDF, TXT, DOCX, MD)
✅ Vector embedding and semantic search
✅ Conversational memory
✅ Source document attribution
✅ Multi-turn conversations

### Session Management (NEW!)
✅ Redis-based persistence
✅ In-memory fallback (no Redis? No problem!)
✅ Automatic TTL-based cleanup (1 hour default)
✅ Session statistics and monitoring
✅ Graceful degradation

### Safety Features
✅ PII detection (email, phone, SSN, credit cards)
✅ Content filtering
✅ Toxicity detection
✅ Input validation and sanitization

### Evaluation Features
✅ Built-in metrics (Groundedness, Relevance, Retrieval, etc.)
✅ Custom evaluators
✅ Azure AI Evaluation SDK integration
✅ Detailed analysis reports

### Training Features
✅ Q&A pair generation from documents
✅ Fine-tuning data preparation
✅ OpenAI fine-tuning integration
✅ Model version management

---

## 📚 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Core Framework** | Python 3.8+ | Application logic |
| **RAG Engine** | LangChain | Orchestration |
| **LLM** | OpenAI / Azure OpenAI | Text generation |
| **Vector DB** | ChromaDB | Semantic search |
| **Session Manager** | Redis | Persistence |
| **Safety** | Custom PII patterns | Guardrails |
| **Evaluation** | Azure AI SDK | Metrics |
| **Tracing** | OpenTelemetry | Observability |
| **Fine-tuning** | OpenAI API | Model training |
| **Testing** | Pytest | Unit tests |

---

## 🎓 Learning Outcomes

By studying this project, you'll understand:

1. **RAG Architecture**: How to build retrieval-augmented generation systems
2. **Session Management**: Persistent session handling at scale
3. **Distributed Systems**: Multi-server architecture with shared storage
4. **Graceful Degradation**: Fallback mechanisms for reliability
5. **Safety in AI**: Guardrails and PII detection
6. **Evaluation**: How to measure RAG system quality
7. **Fine-tuning**: How to improve models with custom data
8. **Production Design**: Building systems that scale and fail gracefully

---

## ❓ FAQ

### Q: How do I run the demo?
**A**: `python demo_redis_before_after.py` - Shows both BEFORE and AFTER modes in action.

### Q: Do I need Redis to run this?
**A**: No! The system has graceful fallback to in-memory mode if Redis is unavailable.

### Q: How do I prepare for my interview?
**A**: 
1. Read [INTERVIEW_TALKING_POINTS.md](INTERVIEW_TALKING_POINTS.md) (10 min)
2. Read [REDIS_BEFORE_AFTER.md](REDIS_BEFORE_AFTER.md) (15 min)
3. Study [ARCHITECTURE_VISUAL.md](ARCHITECTURE_VISUAL.md) (10 min)
4. Review [src/redis_session.py](src/redis_session.py) (15 min)
5. Practice the 2-3 minute script

### Q: What's the main difference from the original chatbot?
**A**: Added Redis-based persistent session storage so conversations survive server restarts and idle time. Maintains backward compatibility with in-memory fallback.

### Q: Can this scale to production?
**A**: Yes! The Redis architecture enables:
- Horizontal scaling (multiple server instances)
- Session persistence (survive restarts)
- Load balancing (sessions shared across servers)
- Monitoring (session statistics available)

### Q: How do I extend this project?
**A**: See the extension points in [ARCHITECTURE.md](ARCHITECTURE.md):
- Add new document formats
- Implement custom evaluators
- Add authentication
- Build REST API with FastAPI
- Deploy with Docker/Kubernetes

---

## 📞 Support & Questions

For questions about:
- **Interview Preparation**: Read [INTERVIEW_TALKING_POINTS.md](INTERVIEW_TALKING_POINTS.md)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md) and [ARCHITECTURE_VISUAL.md](ARCHITECTURE_VISUAL.md)
- **Redis Implementation**: Study [src/redis_session.py](src/redis_session.py)
- **Getting Started**: Follow [QUICKSTART.md](QUICKSTART.md)
- **Problem/Solution**: Read [REDIS_BEFORE_AFTER.md](REDIS_BEFORE_AFTER.md)

---

## ✅ Files Created/Modified

### New Files (Redis Integration)
- ✅ `src/redis_session.py` (450+ lines) - Redis session manager
- ✅ `main_with_redis.py` (300+ lines) - Updated app with Redis support
- ✅ `REDIS_BEFORE_AFTER.md` (600+ lines) - Complete BEFORE/AFTER analysis
- ✅ `ARCHITECTURE_VISUAL.md` (500+ lines) - Visual architecture diagrams
- ✅ `INTERVIEW_TALKING_POINTS.md` (400+ lines) - Interview preparation guide
- ✅ `demo_redis_before_after.py` (300+ lines) - Interactive demo script
- ✅ `PROJECT_INDEX.md` (this file) - Navigation and overview

### Modified Files
- ✅ `requirements.txt` - Added `redis>=5.0.0`

### Existing Files (Unchanged but Relevant)
- `main.py` - Original CLI (BEFORE mode)
- `src/chatbot.py` - Base RAG implementation
- `src/document_processor.py` - Document loading
- `src/vector_store.py` - Vector store management
- `guardrails/guardrails_manager.py` - Safety features
- `evaluation/evaluator.py` - Evaluation metrics
- `config/config.py` - Configuration management

---

## 🎯 Your Next Steps

### Immediate (Next 30 minutes)
1. Read [INTERVIEW_TALKING_POINTS.md](INTERVIEW_TALKING_POINTS.md)
2. Review [REDIS_BEFORE_AFTER.md](REDIS_BEFORE_AFTER.md)
3. Study the visual diagrams in [ARCHITECTURE_VISUAL.md](ARCHITECTURE_VISUAL.md)

### Before Interview (Next few hours)
1. Run `python demo_redis_before_after.py`
2. Study [src/redis_session.py](src/redis_session.py) code
3. Practice the 2-3 minute interview script
4. Think through anticipated questions

### Optional (For Deep Learning)
1. Set up and run the system locally
2. Try BEFORE vs AFTER modes
3. Study the full architecture
4. Explore extension possibilities

---

**Good luck with your interview! You've got this! 🚀**

Generated: 2025-01-22
