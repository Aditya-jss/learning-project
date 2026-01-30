"""
Document Processing and Loading Module
"""
from pathlib import Path
from typing import List
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
)
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process and load documents from various formats"""
    
    def __init__(self, documents_dir: Path):
        self.documents_dir = Path(documents_dir)
        self.loaders = {
            '.txt': TextLoader,
            '.pdf': PyPDFLoader,
            '.docx': Docx2txtLoader,
            '.md': UnstructuredMarkdownLoader,
        }
    
    def load_documents(self) -> List[Document]:
        """Load all supported documents from the documents directory"""
        documents = []
        
        if not self.documents_dir.exists():
            logger.warning(f"Documents directory not found: {self.documents_dir}")
            return documents
        
        for file_path in self.documents_dir.rglob('*'):
            if file_path.is_file():
                try:
                    docs = self._load_single_document(file_path)
                    documents.extend(docs)
                    logger.info(f"Loaded {len(docs)} document(s) from {file_path.name}")
                except Exception as e:
                    logger.error(f"Error loading {file_path.name}: {e}")
        
        logger.info(f"Total documents loaded: {len(documents)}")
        return documents
    
    def _load_single_document(self, file_path: Path) -> List[Document]:
        """Load a single document based on its file extension"""
        suffix = file_path.suffix.lower()
        
        if suffix not in self.loaders:
            logger.warning(f"Unsupported file format: {suffix}")
            return []
        
        loader_class = self.loaders[suffix]
        loader = loader_class(str(file_path))
        
        return loader.load()
    
    def add_metadata(self, documents: List[Document]) -> List[Document]:
        """Add metadata to documents"""
        for doc in documents:
            if 'source' in doc.metadata:
                source_path = Path(doc.metadata['source'])
                doc.metadata['filename'] = source_path.name
                doc.metadata['file_type'] = source_path.suffix
        
        return documents
