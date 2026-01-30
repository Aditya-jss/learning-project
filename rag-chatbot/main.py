"""
Main Application - RAG Chatbot with Guardrails and Evaluation
"""
import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.config import Config
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStoreManager
from src.chatbot import RAGChatbot, ConversationalRAGChatbot
from src.tracing import TracingManager
from guardrails.guardrails_manager import GuardrailsManager, GuardrailsWrapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_rag_system(rebuild_vectorstore: bool = False):
    """
    Initialize the RAG chatbot system
    
    Args:
        rebuild_vectorstore: Whether to rebuild the vector store from documents
    
    Returns:
        Initialized chatbot with guardrails
    """
    logger.info("Initializing RAG Chatbot System...")
    
    # Setup tracing if enabled
    if Config.ENABLE_TRACING:
        logger.info("Setting up tracing...")
        tracing = TracingManager(Config.OTLP_ENDPOINT)
        tracing.setup_tracing()
    
    # Initialize vector store manager
    vector_store_manager = VectorStoreManager(
        persist_directory=Config.VECTOR_STORE_PATH,
        embedding_model=Config.EMBEDDING_MODEL,
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        use_azure=Config.use_azure_openai(),
        azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
        azure_api_key=Config.AZURE_OPENAI_API_KEY,
        azure_deployment=Config.AZURE_EMBEDDING_DEPLOYMENT,
        openai_api_key=Config.OPENAI_API_KEY,
    )
    
    # Load or create vector store
    if rebuild_vectorstore or not Path(Config.VECTOR_STORE_PATH).exists():
        logger.info("Building vector store from documents...")
        
        # Load documents
        doc_processor = DocumentProcessor(Config.DOCUMENTS_DIR)
        documents = doc_processor.load_documents()
        
        if not documents:
            logger.warning("No documents found! Please add documents to the data/documents directory.")
            logger.info("The system will work but won't have any knowledge to retrieve from.")
        
        documents = doc_processor.add_metadata(documents)
        
        # Create vector store
        if documents:
            vector_store_manager.create_vectorstore(documents)
        else:
            logger.warning("Skipping vector store creation - no documents available")
    else:
        logger.info("Loading existing vector store...")
        vector_store_manager.load_vectorstore()
    
    # Get retriever
    retriever = vector_store_manager.get_retriever(top_k=Config.TOP_K_RETRIEVAL)
    
    # Initialize chatbot
    logger.info("Initializing chatbot...")
    chatbot = ConversationalRAGChatbot(
        retriever=retriever,
        model_name=Config.OPENAI_MODEL,
        temperature=Config.TEMPERATURE,
        max_tokens=Config.MAX_TOKENS,
        use_azure=Config.use_azure_openai(),
        azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
        azure_api_key=Config.AZURE_OPENAI_API_KEY,
        azure_deployment=Config.AZURE_OPENAI_DEPLOYMENT,
        openai_api_key=Config.OPENAI_API_KEY,
    )
    
    # Add guardrails if enabled
    if Config.ENABLE_GUARDRAILS:
        logger.info("Enabling guardrails...")
        guardrails = GuardrailsManager(
            max_input_length=Config.MAX_INPUT_LENGTH,
            max_output_length=Config.MAX_OUTPUT_LENGTH,
        )
        chatbot = GuardrailsWrapper(chatbot, guardrails)
    
    logger.info("RAG Chatbot System initialized successfully!")
    return chatbot


def interactive_chat(chatbot):
    """
    Run interactive chat session
    
    Args:
        chatbot: Initialized chatbot instance
    """
    print("\n" + "="*60)
    print("RAG Chatbot - Interactive Mode")
    print("="*60)
    print("\nCommands:")
    print("  - Type your question to chat")
    print("  - 'clear' to clear conversation history")
    print("  - 'quit' or 'exit' to end session")
    print("\n" + "="*60 + "\n")
    
    while True:
        try:
            user_input = input("\n🤔 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'clear':
                if hasattr(chatbot, 'chatbot'):  # GuardrailsWrapper
                    if hasattr(chatbot.chatbot, 'clear_history'):
                        chatbot.chatbot.clear_history()
                elif hasattr(chatbot, 'clear_history'):  # Direct chatbot
                    chatbot.clear_history()
                print("✅ Conversation history cleared")
                continue
            
            # Get response
            response = chatbot.chat(user_input)
            
            # Display response
            print(f"\n🤖 Assistant: {response['response']}")
            
            # Show sources if available
            if response.get('source_documents'):
                print(f"\n📚 Sources: {len(response['source_documents'])} document(s)")
                for i, source in enumerate(response['source_documents'][:3], 1):
                    filename = source['metadata'].get('filename', 'Unknown')
                    print(f"   {i}. {filename}")
            
            # Show guardrails warnings if any
            if response.get('guardrails_warnings'):
                print(f"\n⚠️  Guardrails Warnings: {len(response['guardrails_warnings'])}")
            
            if response.get('blocked'):
                print("\n🚫 Response was blocked by guardrails")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            print(f"\n❌ Error: {e}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RAG Chatbot with Guardrails and Evaluation")
    parser.add_argument(
        '--rebuild',
        action='store_true',
        help='Rebuild vector store from documents'
    )
    parser.add_argument(
        '--query',
        type=str,
        help='Single query mode (non-interactive)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize system
        chatbot = initialize_rag_system(rebuild_vectorstore=args.rebuild)
        
        if args.query:
            # Single query mode
            response = chatbot.chat(args.query)
            print(f"\nQuery: {args.query}")
            print(f"\nResponse: {response['response']}")
            if response.get('source_documents'):
                print(f"\nSources: {len(response['source_documents'])} document(s)")
        else:
            # Interactive mode
            interactive_chat(chatbot)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Fatal Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
