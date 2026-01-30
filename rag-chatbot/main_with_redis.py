"""
Main Application - RAG Chatbot with Redis Session Management
BEFORE/AFTER demonstration
"""
import os
import sys
import logging
from pathlib import Path
import uuid

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.config import Config
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStoreManager
from src.chatbot import RAGChatbot, ConversationalRAGChatbot
from src.tracing import TracingManager
from src.redis_session import RedisSessionManager, ChatbotWithRedisSession
from guardrails.guardrails_manager import GuardrailsManager, GuardrailsWrapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_rag_system(rebuild_vectorstore: bool = False, use_redis: bool = False):
    """
    Initialize the RAG chatbot system
    
    Args:
        rebuild_vectorstore: Whether to rebuild the vector store from documents
        use_redis: Whether to use Redis for session management
    
    Returns:
        Initialized chatbot (with or without Redis)
    """
    logger.info("="*60)
    logger.info("Initializing RAG Chatbot System...")
    logger.info("="*60)
    
    if use_redis:
        logger.info("🔴 MODE: With Redis Session Management (AFTER)")
    else:
        logger.info("⚪ MODE: In-Memory Only (BEFORE)")
    
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
    
    # Add Redis session management if enabled
    if use_redis:
        logger.info("🔴 Initializing Redis Session Manager...")
        session_manager = RedisSessionManager(
            host="localhost",
            port=6379,
            session_timeout=3600  # 1 hour
        )
        
        if session_manager.is_connected:
            logger.info("✅ Redis connected! Session persistence ENABLED")
            chatbot = ChatbotWithRedisSession(chatbot, session_manager)
        else:
            logger.warning("⚠️ Redis not available. Using in-memory fallback.")
            chatbot = ChatbotWithRedisSession(chatbot, session_manager)
    else:
        logger.info("⚪ In-memory only (session lost on idle)")
    
    logger.info("="*60)
    logger.info("✅ Chatbot initialized successfully!")
    logger.info("="*60 + "\n")
    
    return chatbot, use_redis


def interactive_chat_with_redis(chatbot, use_redis: bool = False):
    """
    Run interactive chat session with optional Redis
    
    Args:
        chatbot: Initialized chatbot instance
        use_redis: Whether Redis is enabled
    """
    print("\n" + "="*70)
    if use_redis:
        print("🔴 RAG Chatbot - Interactive Mode (WITH Redis Session Management)")
        print("="*70)
        print("\n📝 Your session is being saved to Redis!")
        print("   • Idle for 1 hour? Your context is still there!")
        print("   • Restart server? Your conversation persists!")
        print("   • Close terminal? Reopen and continue!")
    else:
        print("⚪ RAG Chatbot - Interactive Mode (IN-MEMORY ONLY)")
        print("="*70)
        print("\n⚠️  WARNING: Session data is NOT persisted")
        print("   • Go idle? Context will be lost!")
        print("   • Restart server? Everything is gone!")
        print("   • Close terminal? Chat history deleted!")
    
    print("\n" + "="*70)
    print("Commands:")
    print("  - Type your question to chat")
    print("  - 'clear' to clear conversation history")
    print("  - 'history' to see conversation history")
    print("  - 'stats' to see session stats (Redis only)")
    print("  - 'quit' or 'exit' to end session")
    print("="*70 + "\n")
    
    user_id = str(uuid.uuid4())[:8]
    print(f"📌 Session ID: {user_id}\n")
    
    while True:
        try:
            user_input = input("\n🤔 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'clear':
                if use_redis and hasattr(chatbot, 'clear_user_session'):
                    chatbot.clear_user_session(user_id)
                    print("✅ Conversation history cleared from Redis")
                elif hasattr(chatbot, 'chatbot') and hasattr(chatbot.chatbot, 'clear_history'):
                    chatbot.chatbot.clear_history()
                    print("✅ In-memory conversation history cleared")
                else:
                    print("✅ Conversation history cleared")
                continue
            
            if user_input.lower() == 'history':
                if use_redis and hasattr(chatbot, 'get_user_history'):
                    history = chatbot.get_user_history(user_id)
                    if history:
                        print(f"\n📚 Conversation History ({len(history)} messages):")
                        for i, msg in enumerate(history, 1):
                            role = "You" if msg['role'] == 'user' else "Bot"
                            preview = msg['content'][:80] + "..." if len(msg['content']) > 80 else msg['content']
                            print(f"  {i}. [{role}] {preview}")
                    else:
                        print("No conversation history yet")
                else:
                    print("History not available in in-memory mode")
                continue
            
            if user_input.lower() == 'stats':
                if use_redis and hasattr(chatbot, 'session_manager'):
                    stats = chatbot.session_manager.get_session_stats()
                    print(f"\n📊 Session Stats:")
                    for key, value in stats.items():
                        print(f"   {key}: {value}")
                else:
                    print("Stats only available with Redis enabled")
                continue
            
            # Get response
            if use_redis and hasattr(chatbot, 'chat'):
                response = chatbot.chat(user_id, user_input)
            else:
                response = chatbot.chat(user_input)
            
            # Display response
            print(f"\n🤖 Assistant: {response['response']}")
            
            # Show Redis-specific info
            if use_redis and response.get('session_persisted'):
                print(f"\n✅ Session persisted in {response.get('backend', 'Unknown')}")
                print(f"📝 Total messages in session: {response.get('conversation_length', 'N/A')}")
            
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
    
    parser = argparse.ArgumentParser(description="RAG Chatbot with Optional Redis Session Management")
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
    parser.add_argument(
        '--redis',
        action='store_true',
        help='Enable Redis session management (AFTER mode)'
    )
    parser.add_argument(
        '--mode',
        choices=['before', 'after', 'auto'],
        default='auto',
        help='Mode: before (in-memory), after (with Redis), auto (detect)'
    )
    
    args = parser.parse_args()
    
    # Determine if Redis should be used
    if args.mode == 'after' or args.redis:
        use_redis = True
    elif args.mode == 'before':
        use_redis = False
    else:  # auto
        use_redis = args.redis
    
    try:
        # Initialize system
        chatbot, use_redis_mode = initialize_rag_system(
            rebuild_vectorstore=args.rebuild,
            use_redis=use_redis
        )
        
        if args.query:
            # Single query mode
            if use_redis_mode:
                user_id = "single_query_user"
                response = chatbot.chat(user_id, args.query)
            else:
                response = chatbot.chat(args.query)
            
            print(f"\nQuery: {args.query}")
            print(f"Response: {response['response']}")
            if response.get('source_documents'):
                print(f"Sources: {len(response['source_documents'])} document(s)")
        else:
            # Interactive mode
            interactive_chat_with_redis(chatbot, use_redis_mode)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Fatal Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
