"""
Configuration Manager for RAG Chatbot
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for RAG chatbot"""
    
    # Project Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    DOCUMENTS_DIR = DATA_DIR / "documents"
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", str(DATA_DIR / "vectorstore"))
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Azure OpenAI Configuration (Alternative)
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")
    
    # Embedding Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    AZURE_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
    
    # RAG Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "5"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    
    # Guardrails Configuration
    ENABLE_GUARDRAILS = os.getenv("ENABLE_GUARDRAILS", "true").lower() == "true"
    MAX_INPUT_LENGTH = int(os.getenv("MAX_INPUT_LENGTH", "2000"))
    MAX_OUTPUT_LENGTH = int(os.getenv("MAX_OUTPUT_LENGTH", "2000"))
    
    # Tracing Configuration
    ENABLE_TRACING = os.getenv("ENABLE_TRACING", "true").lower() == "true"
    OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT", "http://localhost:4318")
    
    @classmethod
    def use_azure_openai(cls) -> bool:
        """Check if Azure OpenAI should be used"""
        return bool(cls.AZURE_OPENAI_ENDPOINT and cls.AZURE_OPENAI_API_KEY)
    
    @classmethod
    def validate_config(cls) -> None:
        """Validate that required configuration is present"""
        if cls.use_azure_openai():
            if not cls.AZURE_OPENAI_DEPLOYMENT:
                raise ValueError("AZURE_OPENAI_DEPLOYMENT is required when using Azure OpenAI")
        else:
            if not cls.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required when not using Azure OpenAI")
        
        # Create necessary directories
        cls.DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
        Path(cls.VECTOR_STORE_PATH).mkdir(parents=True, exist_ok=True)


# Validate configuration on import
Config.validate_config()
