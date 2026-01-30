"""
Unit Tests for RAG Chatbot Components
"""
import pytest
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.document_processor import DocumentProcessor
from src.vector_store import VectorStoreManager
from guardrails.guardrails_manager import GuardrailsManager, GuardrailViolation
from evaluation.evaluator import CustomAnswerLengthEvaluator


class TestDocumentProcessor:
    """Test document processing"""
    
    def test_initialization(self, tmp_path):
        processor = DocumentProcessor(tmp_path)
        assert processor.documents_dir == tmp_path
    
    def test_supported_formats(self, tmp_path):
        processor = DocumentProcessor(tmp_path)
        assert '.txt' in processor.loaders
        assert '.pdf' in processor.loaders
        assert '.docx' in processor.loaders


class TestGuardrailsManager:
    """Test guardrails functionality"""
    
    def test_input_length_validation(self):
        guardrails = GuardrailsManager(max_input_length=100)
        
        # Valid input
        result = guardrails.validate_input("Short text")
        assert result["is_valid"] == True
        
        # Invalid input (too long)
        result = guardrails.validate_input("x" * 200)
        assert result["is_valid"] == False
    
    def test_pii_detection(self):
        guardrails = GuardrailsManager(enable_pii_detection=True)
        
        # Input with email
        result = guardrails.validate_input("Contact me at test@example.com")
        violations = result["violations"]
        assert any(v.rule == "pii_detected" for v in violations)
        
        # Input without PII
        result = guardrails.validate_input("What is machine learning?")
        pii_violations = [v for v in result["violations"] if v.rule == "pii_detected"]
        assert len(pii_violations) == 0
    
    def test_sanitization(self):
        guardrails = GuardrailsManager(enable_pii_detection=True)
        text = "My email is test@example.com"
        sanitized = guardrails._sanitize_text(text)
        assert "test@example.com" not in sanitized
        assert "REDACTED" in sanitized


class TestCustomEvaluators:
    """Test custom evaluators"""
    
    def test_answer_length_evaluator(self):
        evaluator = CustomAnswerLengthEvaluator(min_length=10, max_length=100)
        
        # Appropriate length
        result = evaluator(response="This is a good length answer for testing")
        assert result["length_appropriate"] == True
        assert result["length_score"] == 1.0
        
        # Too short
        result = evaluator(response="Short")
        assert result["length_appropriate"] == False
        
        # Too long
        result = evaluator(response="x" * 200)
        assert result["length_appropriate"] == False


@pytest.fixture
def sample_documents():
    """Sample documents for testing"""
    return [
        "Artificial Intelligence is the simulation of human intelligence.",
        "Machine Learning is a subset of AI that learns from data.",
        "Deep Learning uses neural networks."
    ]


def test_guardrails_wrapper_integration():
    """Test guardrails wrapper with mock chatbot"""
    class MockChatbot:
        def chat(self, query):
            return {
                "query": query,
                "response": "This is a test response",
                "source_documents": []
            }
    
    chatbot = MockChatbot()
    guardrails = GuardrailsManager()
    wrapped_chatbot = GuardrailsWrapper(chatbot, guardrails)
    
    # Normal query
    response = wrapped_chatbot.chat("What is AI?")
    assert "blocked" not in response or not response["blocked"]
    
    # Query with PII
    response = wrapped_chatbot.chat("My email is test@example.com")
    assert "REDACTED" in response["query"] or "blocked" in response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
