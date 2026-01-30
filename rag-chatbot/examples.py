"""
Example Script: Complete RAG Chatbot Workflow
Run this script to see the complete end-to-end workflow
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from main import initialize_rag_system
from evaluation.evaluator import run_comprehensive_evaluation
from training.data_preparation import DataPreparator, ModelVersionManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_basic_chat():
    """Example 1: Basic chat interaction"""
    print("\n" + "="*60)
    print("Example 1: Basic Chat Interaction")
    print("="*60 + "\n")
    
    # Initialize chatbot
    chatbot = initialize_rag_system()
    
    # Ask questions
    questions = [
        "What is artificial intelligence?",
        "What are the types of machine learning?",
        "Tell me about Python programming"
    ]
    
    for question in questions:
        print(f"\n📝 Question: {question}")
        response = chatbot.chat(question)
        print(f"🤖 Answer: {response['response'][:200]}...")
        print(f"📚 Sources: {len(response.get('source_documents', []))} documents")


def example_evaluation():
    """Example 2: Run comprehensive evaluation"""
    print("\n" + "="*60)
    print("Example 2: Comprehensive Evaluation")
    print("="*60 + "\n")
    
    # Initialize chatbot
    chatbot = initialize_rag_system()
    
    # Define test queries
    test_queries = [
        "What is artificial intelligence?",
        "Explain the different types of machine learning",
        "What are the applications of AI in healthcare?",
        "What is deep learning?",
        "Tell me about Python's best practices"
    ]
    
    # Optional ground truths
    ground_truths = [
        "AI is the simulation of human intelligence processes by machines",
        "The main types of machine learning are supervised, unsupervised, and reinforcement learning",
        "AI applications in healthcare include disease diagnosis, drug discovery, and personalized treatment",
        "Deep learning is a subset of machine learning that uses neural networks with multiple layers",
        "Python best practices include writing clean code, using virtual environments, and writing tests"
    ]
    
    print("🔍 Running evaluation with Azure AI Evaluation SDK...")
    
    # Run evaluation
    results = run_comprehensive_evaluation(
        chatbot=chatbot,
        test_queries=test_queries,
        ground_truths=ground_truths,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    print("\n✅ Evaluation Complete!")
    print(f"📊 Results saved to: evaluation/results")
    
    # Display metrics
    if 'metrics' in results:
        print("\n📈 Aggregate Metrics:")
        for metric_name, value in results['metrics'].items():
            print(f"   {metric_name}: {value}")


def example_guardrails():
    """Example 3: Test guardrails system"""
    print("\n" + "="*60)
    print("Example 3: Guardrails Testing")
    print("="*60 + "\n")
    
    # Initialize chatbot with guardrails
    chatbot = initialize_rag_system()
    
    # Test cases
    test_cases = [
        {
            "query": "What is machine learning?",
            "description": "Normal query"
        },
        {
            "query": "My email is test@example.com and my phone is 123-456-7890",
            "description": "Query with PII"
        },
        {
            "query": "x" * 3000,  # Very long query
            "description": "Excessively long query"
        }
    ]
    
    for test in test_cases:
        print(f"\n📝 Testing: {test['description']}")
        print(f"Query: {test['query'][:100]}...")
        
        response = chatbot.chat(test['query'])
        
        if response.get('blocked'):
            print("🚫 Response blocked by guardrails")
            print(f"Reason: {response.get('guardrails_violations', [{}])[0]}")
        else:
            print(f"✅ Response allowed")
            if response.get('guardrails_warnings'):
                print(f"⚠️  Warnings: {len(response['guardrails_warnings'])}")


def example_data_preparation():
    """Example 4: Prepare training data"""
    print("\n" + "="*60)
    print("Example 4: Training Data Preparation")
    print("="*60 + "\n")
    
    # Initialize data preparator
    preparator = DataPreparator()
    
    # Sample documents
    sample_docs = [
        "Artificial Intelligence is the simulation of human intelligence by machines.",
        "Machine Learning is a subset of AI that learns from data.",
        "Deep Learning uses neural networks with multiple layers."
    ]
    
    print("📝 Creating Q&A pairs from documents...")
    qa_path = preparator.create_qa_pairs_from_documents(
        documents=sample_docs,
        output_file="example_qa_data.jsonl"
    )
    print(f"✅ Q&A pairs saved to: {qa_path}")
    
    # Note: In production, you would use an LLM to generate meaningful Q&A pairs


def example_version_management():
    """Example 5: Model version management"""
    print("\n" + "="*60)
    print("Example 5: Model Version Management")
    print("="*60 + "\n")
    
    # Initialize version manager
    version_manager = ModelVersionManager()
    
    # Register versions
    print("📝 Registering model versions...")
    
    version_manager.register_version(
        version_name="v1.0-baseline",
        model_id="gpt-4o-mini",
        description="Baseline model",
        metrics={
            "groundedness": 4.2,
            "relevance": 4.0,
            "coherence": 4.5
        }
    )
    
    version_manager.register_version(
        version_name="v1.1-improved",
        model_id="gpt-4o-mini",
        description="Improved with better prompts",
        metrics={
            "groundedness": 4.5,
            "relevance": 4.3,
            "coherence": 4.6
        }
    )
    
    # List versions
    print("\n📋 Registered Versions:")
    for version in version_manager.list_versions():
        print(f"\n  Version: {version['version_name']}")
        print(f"  Model: {version['model_id']}")
        print(f"  Description: {version['description']}")
        print(f"  Metrics: {version['metrics']}")
    
    # Compare versions
    print("\n📊 Comparing v1.0 vs v1.1:")
    comparison = version_manager.compare_versions("v1.0-baseline", "v1.1-improved")
    for metric, values in comparison['metrics_comparison'].items():
        print(f"  {metric}:")
        print(f"    v1.0: {values['v1.0-baseline']}")
        print(f"    v1.1: {values['v1.1-improved']}")
        print(f"    Difference: {values['difference']:+.2f}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("RAG Chatbot - Complete Examples")
    print("="*60)
    
    try:
        # Run examples
        example_basic_chat()
        example_guardrails()
        example_data_preparation()
        example_version_management()
        
        # Note: Evaluation example requires API calls and takes longer
        # Uncomment to run:
        # example_evaluation()
        
        print("\n" + "="*60)
        print("✅ All Examples Completed Successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
