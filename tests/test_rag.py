"""
Tests for RAG system
"""

import pytest
from src.rag import TaxDocumentRAG


def test_rag_initialization():
    """Test RAG system initialization"""
    rag = TaxDocumentRAG(
        embedding_model="huggingface",
        vector_store_type="chroma",
        chunk_size=500
    )
    
    assert rag is not None
    assert rag.chunk_size == 500
    assert rag.chunk_overlap == 200  # default value


def test_document_ingestion():
    """Test document ingestion"""
    rag = TaxDocumentRAG(embedding_model="huggingface")
    
    documents = [
        "Tax rule 1: Standard deduction for 2024 is $14,600",
        "Tax rule 2: Personal exemption is suspended until 2025"
    ]
    
    num_chunks = rag.ingest_documents(documents)
    
    assert num_chunks > 0


def test_rag_stats():
    """Test getting RAG statistics"""
    rag = TaxDocumentRAG(embedding_model="huggingface")
    
    stats = rag.get_stats()
    
    assert "chunk_size" in stats
    assert "chunk_overlap" in stats
    assert "vector_store_path" in stats
