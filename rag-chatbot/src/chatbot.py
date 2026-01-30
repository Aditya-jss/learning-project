"""
RAG Chatbot Implementation
"""
from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)


class RAGChatbot:
    """RAG-based chatbot implementation"""
    
    def __init__(
        self,
        retriever,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        use_azure: bool = False,
        azure_endpoint: Optional[str] = None,
        azure_api_key: Optional[str] = None,
        azure_deployment: Optional[str] = None,
        openai_api_key: Optional[str] = None,
    ):
        self.retriever = retriever
        
        # Initialize LLM
        if use_azure and azure_endpoint:
            self.llm = AzureChatOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=azure_api_key,
                azure_deployment=azure_deployment,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            self.llm = ChatOpenAI(
                model=model_name,
                api_key=openai_api_key,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        
        # Define RAG prompt template
        self.prompt_template = PromptTemplate(
            template="""You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
Always provide citations to the source documents when possible.

Context:
{context}

Question: {question}

Answer: Let me help you with that.""",
            input_variables=["context", "question"]
        )
        
        # Create RAG chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )
    
    def chat(self, query: str) -> Dict:
        """Process a chat query and return response with sources"""
        try:
            logger.info(f"Processing query: {query[:100]}...")
            
            # Get response from RAG chain
            result = self.qa_chain.invoke({"query": query})
            
            response = {
                "query": query,
                "response": result["result"],
                "source_documents": self._format_sources(result.get("source_documents", []))
            }
            
            logger.info("Query processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "query": query,
                "response": "I apologize, but I encountered an error processing your request.",
                "error": str(e),
                "source_documents": []
            }
    
    def _format_sources(self, documents: List[Document]) -> List[Dict]:
        """Format source documents for response"""
        sources = []
        for i, doc in enumerate(documents, 1):
            source = {
                "content": doc.page_content[:200] + "...",  # Truncate for display
                "metadata": doc.metadata
            }
            sources.append(source)
        return sources
    
    def batch_chat(self, queries: List[str]) -> List[Dict]:
        """Process multiple queries in batch"""
        responses = []
        for query in queries:
            response = self.chat(query)
            responses.append(response)
        return responses


class ConversationalRAGChatbot(RAGChatbot):
    """RAG chatbot with conversation history"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversation_history: List[Dict] = []
    
    def chat(self, query: str, use_history: bool = True) -> Dict:
        """Chat with conversation history"""
        if use_history and self.conversation_history:
            # Append history context to query
            history_context = self._format_history()
            enhanced_query = f"Previous conversation:\n{history_context}\n\nCurrent question: {query}"
        else:
            enhanced_query = query
        
        response = super().chat(enhanced_query)
        
        # Store in history
        self.conversation_history.append({
            "query": query,
            "response": response["response"]
        })
        
        # Keep only last 5 exchanges
        if len(self.conversation_history) > 5:
            self.conversation_history = self.conversation_history[-5:]
        
        return response
    
    def _format_history(self) -> str:
        """Format conversation history"""
        history_lines = []
        for exchange in self.conversation_history[-3:]:  # Last 3 exchanges
            history_lines.append(f"Q: {exchange['query']}")
            history_lines.append(f"A: {exchange['response']}")
        return "\n".join(history_lines)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
