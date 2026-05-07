"""Tests for file parser module."""

import os
import tempfile
import pytest
from pathlib import Path

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from file_parser import FileParser
from models import FileType


class TestFileParser:
    """Test cases for FileParser."""
    
    def test_get_file_type_document(self):
        """Test document file type detection."""
        assert FileParser.get_file_type('.pdf') == FileType.DOCUMENT
        assert FileParser.get_file_type('.docx') == FileType.DOCUMENT
        assert FileParser.get_file_type('.txt') == FileType.DOCUMENT
        assert FileParser.get_file_type('.md') == FileType.DOCUMENT
    
    def test_get_file_type_code(self):
        """Test code file type detection."""
        assert FileParser.get_file_type('.py') == FileType.CODE
        assert FileParser.get_file_type('.js') == FileType.CODE
        assert FileParser.get_file_type('.html') == FileType.CODE
        assert FileParser.get_file_type('.json') == FileType.CODE
    
    def test_get_file_type_config(self):
        """Test config file type detection."""
        assert FileParser.get_file_type('.env') == FileType.CONFIG
        assert FileParser.get_file_type('.ini') == FileType.CONFIG
        assert FileParser.get_file_type('.sh') == FileType.CONFIG
    
    def test_get_file_type_other(self):
        """Test other file type detection."""
        assert FileParser.get_file_type('.unknown') == FileType.OTHER
        assert FileParser.get_file_type('.xyz') == FileType.OTHER
    
    def test_parse_text_file(self):
        """Test parsing a text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('Hello, World!\nThis is a test file.')
            temp_path = f.name
        
        try:
            content, error = FileParser.parse_file(temp_path)
            assert error is None
            assert content is not None
            assert 'Hello, World!' in content
        finally:
            os.unlink(temp_path)
    
    def test_parse_nonexistent_file(self):
        """Test parsing a non-existent file."""
        content, error = FileParser.parse_file('/nonexistent/file.txt')
        assert content is None
        assert error is not None
        assert 'not found' in error.lower()
    
    def test_is_supported(self):
        """Test file support check."""
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
            temp_path = f.name
        
        try:
            assert FileParser.is_supported(temp_path) is True
        finally:
            os.unlink(temp_path)
        
        # Unsupported extension
        with tempfile.NamedTemporaryFile(suffix='.unsupported', delete=False) as f:
            temp_path = f.name
        
        try:
            assert FileParser.is_supported(temp_path) is False
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
