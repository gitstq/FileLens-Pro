"""Tests for search engine module."""

import os
import sys
import pytest
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from search_engine import TextChunker, SearchEngine


class TestTextChunker:
    """Test cases for TextChunker."""
    
    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        chunker = TextChunker(chunk_size=100, chunk_overlap=20)
        text = "This is a test. " * 50
        chunks = chunker.chunk_text(text)
        
        assert len(chunks) > 0
        assert all(len(chunk) <= 100 for chunk in chunks)
    
    def test_chunk_text_empty(self):
        """Test chunking empty text."""
        chunker = TextChunker()
        chunks = chunker.chunk_text("")
        assert chunks == []
    
    def test_chunk_text_short(self):
        """Test chunking short text."""
        chunker = TextChunker(chunk_size=100)
        text = "Short text."
        chunks = chunker.chunk_text(text)
        
        assert len(chunks) == 1
        assert chunks[0] == text


class TestSearchEngine:
    """Test cases for SearchEngine."""
    
    @pytest.fixture(scope="class")
    def engine(self):
        """Create a search engine instance."""
        # Note: This requires the model to be loaded
        # May be slow for testing
        engine = SearchEngine()
        return engine
    
    def test_singleton(self):
        """Test that SearchEngine is a singleton."""
        engine1 = SearchEngine()
        engine2 = SearchEngine()
        assert engine1 is engine2
    
    def test_index_and_search(self, engine):
        """Test indexing and searching."""
        # Create a test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('Python is a great programming language for data science.')
            temp_path = f.name
        
        try:
            # Index the file
            success, error = engine.index_file(temp_path)
            assert success is True
            assert error is None
            
            # Search
            from models import SearchRequest, SearchMode
            request = SearchRequest(
                query="Python programming",
                mode=SearchMode.SEMANTIC,
                max_results=10
            )
            results = engine.search(request)
            
            assert results.total_results > 0
            assert len(results.results) > 0
            
        finally:
            os.unlink(temp_path)
            engine.delete_document(temp_path)
    
    def test_get_stats(self, engine):
        """Test getting stats."""
        stats = engine.get_stats()
        assert stats is not None
        assert hasattr(stats, 'total_documents')
        assert hasattr(stats, 'total_chunks')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
