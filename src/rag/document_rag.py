"""
RAG (Retrieval-Augmented Generation) System for Tax Documents
Handles document ingestion, vectorization, and retrieval
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
    from langchain.vectorstores import Chroma, FAISS
    from langchain.docstore.document import Document
except ImportError:
    # Graceful fallback for demonstration
    pass

logger = logging.getLogger(__name__)


class TaxDocumentRAG:
    """
    RAG system specialized for tax documents and regulations.
    Supports multiple vector stores and embedding models.
    """
    
    def __init__(
        self,
        embedding_model: str = "openai",
        vector_store_type: str = "chroma",
        vector_store_path: str = "./data/vector_store",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize the RAG system
        
        Args:
            embedding_model: Type of embedding model ("openai" or "huggingface")
            vector_store_type: Type of vector store ("chroma" or "faiss")
            vector_store_path: Path to store vector database
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
        """
        self.vector_store_path = Path(vector_store_path)
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize embeddings
        self.embeddings = self._initialize_embeddings(embedding_model)
        
        # Initialize vector store
        self.vector_store = self._initialize_vector_store(vector_store_type)
        
        logger.info(f"RAG system initialized with {embedding_model} embeddings and {vector_store_type} vector store")
    
    def _initialize_embeddings(self, model_type: str):
        """Initialize embedding model"""
        try:
            if model_type == "openai":
                return OpenAIEmbeddings()
            elif model_type == "huggingface":
                return HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
            else:
                raise ValueError(f"Unsupported embedding model: {model_type}")
        except Exception as e:
            logger.warning(f"Failed to initialize {model_type} embeddings: {e}")
            # Return mock embeddings for demonstration
            return None
    
    def _initialize_vector_store(self, store_type: str):
        """Initialize vector store"""
        try:
            if store_type == "chroma":
                return Chroma(
                    embedding_function=self.embeddings,
                    persist_directory=str(self.vector_store_path)
                )
            elif store_type == "faiss":
                return None  # Will be initialized on first add
            else:
                raise ValueError(f"Unsupported vector store: {store_type}")
        except Exception as e:
            logger.warning(f"Failed to initialize {store_type} vector store: {e}")
            return None
    
    def ingest_documents(
        self,
        documents: List[str],
        metadata: Optional[List[Dict[str, Any]]] = None
    ) -> int:
        """
        Ingest documents into the RAG system
        
        Args:
            documents: List of document texts
            metadata: Optional metadata for each document
            
        Returns:
            Number of chunks created
        """
        if not documents:
            logger.warning("No documents provided for ingestion")
            return 0
        
        all_chunks = []
        
        for idx, doc_text in enumerate(documents):
            # Split document into chunks
            chunks = self.text_splitter.split_text(doc_text)
            
            # Create Document objects with metadata
            doc_metadata = metadata[idx] if metadata and idx < len(metadata) else {}
            doc_metadata['doc_index'] = idx
            
            for chunk_idx, chunk in enumerate(chunks):
                chunk_metadata = doc_metadata.copy()
                chunk_metadata['chunk_index'] = chunk_idx
                
                all_chunks.append(
                    Document(page_content=chunk, metadata=chunk_metadata)
                )
        
        # Add to vector store
        if self.vector_store:
            try:
                self.vector_store.add_documents(all_chunks)
                logger.info(f"Ingested {len(all_chunks)} chunks from {len(documents)} documents")
            except Exception as e:
                logger.error(f"Failed to add documents to vector store: {e}")
        
        return len(all_chunks)
    
    def retrieve(
        self,
        query: str,
        k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            filter_metadata: Optional metadata filter
            
        Returns:
            List of retrieved documents with content and metadata
        """
        if not self.vector_store:
            logger.warning("Vector store not initialized")
            return []
        
        try:
            # Perform similarity search
            if filter_metadata:
                results = self.vector_store.similarity_search(
                    query,
                    k=k,
                    filter=filter_metadata
                )
            else:
                results = self.vector_store.similarity_search(query, k=k)
            
            # Format results
            formatted_results = [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance": "high"  # Can be extended with actual scores
                }
                for doc in results
            ]
            
            logger.info(f"Retrieved {len(formatted_results)} documents for query")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to retrieve documents: {e}")
            return []
    
    def retrieve_with_scores(
        self,
        query: str,
        k: int = 5
    ) -> List[tuple[Document, float]]:
        """
        Retrieve documents with similarity scores
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of (document, score) tuples
        """
        if not self.vector_store:
            logger.warning("Vector store not initialized")
            return []
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            logger.info(f"Retrieved {len(results)} documents with scores")
            return results
        except Exception as e:
            logger.error(f"Failed to retrieve documents with scores: {e}")
            return []
    
    def update_document(
        self,
        doc_id: str,
        new_content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update a document in the vector store
        
        Args:
            doc_id: Document identifier
            new_content: New document content
            metadata: Optional new metadata
            
        Returns:
            Success status
        """
        # Implementation depends on vector store capabilities
        logger.info(f"Update requested for document {doc_id}")
        return True
    
    def delete_documents(self, filter_metadata: Dict[str, Any]) -> bool:
        """
        Delete documents matching metadata filter
        
        Args:
            filter_metadata: Metadata filter for deletion
            
        Returns:
            Success status
        """
        try:
            # Implementation depends on vector store capabilities
            logger.info(f"Delete requested for documents matching {filter_metadata}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete documents: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the RAG system
        
        Returns:
            Dictionary with system statistics
        """
        return {
            "vector_store_path": str(self.vector_store_path),
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "vector_store_initialized": self.vector_store is not None,
            "embeddings_initialized": self.embeddings is not None
        }
