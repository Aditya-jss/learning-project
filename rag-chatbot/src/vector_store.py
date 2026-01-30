"""
Vector Store Management Module
"""
from typing import List, Optional
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import logging

logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Manage vector store operations"""
    
    def __init__(
        self,
        persist_directory: str,
        embedding_model: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        use_azure: bool = False,
        azure_endpoint: Optional[str] = None,
        azure_api_key: Optional[str] = None,
        azure_deployment: Optional[str] = None,
        openai_api_key: Optional[str] = None,
    ):
        self.persist_directory = persist_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize embeddings
        if use_azure and azure_endpoint:
            self.embeddings = AzureOpenAIEmbeddings(
                azure_endpoint=azure_endpoint,
                api_key=azure_api_key,
                azure_deployment=azure_deployment,
            )
        else:
            self.embeddings = OpenAIEmbeddings(
                model=embedding_model,
                api_key=openai_api_key,
            )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        
        self.vectorstore = None
    
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """Create vector store from documents"""
        if not documents:
            raise ValueError("No documents provided to create vector store")
        
        # Split documents into chunks
        logger.info(f"Splitting {len(documents)} documents into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        
        # Create vector store
        logger.info("Creating vector store with embeddings...")
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
        )
        
        logger.info(f"Vector store created with {len(chunks)} chunks")
        return self.vectorstore
    
    def load_vectorstore(self) -> Chroma:
        """Load existing vector store"""
        logger.info("Loading existing vector store...")
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
        )
        return self.vectorstore
    
    def get_retriever(self, top_k: int = 5):
        """Get retriever from vector store"""
        if self.vectorstore is None:
            try:
                self.load_vectorstore()
            except Exception as e:
                logger.error(f"Failed to load vector store: {e}")
                raise
        
        return self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": top_k}
        )
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Perform similarity search"""
        if self.vectorstore is None:
            self.load_vectorstore()
        
        return self.vectorstore.similarity_search(query, k=k)
    
    def delete_vectorstore(self) -> None:
        """Delete the vector store"""
        if self.vectorstore is not None:
            self.vectorstore.delete_collection()
            self.vectorstore = None
            logger.info("Vector store deleted")
