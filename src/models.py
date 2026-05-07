"""Pydantic models for FileLens API."""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SearchMode(str, Enum):
    """Search mode options."""
    KEYWORD = "keyword"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"


class FileType(str, Enum):
    """File type categories."""
    DOCUMENT = "document"
    CODE = "code"
    CONFIG = "config"
    OTHER = "other"


class Document(BaseModel):
    """Document model."""
    id: str = Field(..., description="Unique document ID")
    filename: str = Field(..., description="Original filename")
    filepath: str = Field(..., description="Full file path")
    file_type: FileType = Field(..., description="File category")
    extension: str = Field(..., description="File extension")
    size: int = Field(..., description="File size in bytes")
    created_at: datetime = Field(..., description="File creation time")
    modified_at: datetime = Field(..., description="Last modified time")
    content: Optional[str] = Field(None, description="Extracted text content")
    indexed_at: Optional[datetime] = Field(None, description="When indexed")


class SearchResult(BaseModel):
    """Search result model."""
    document: Document = Field(..., description="Document information")
    score: float = Field(..., description="Relevance score")
    highlights: List[str] = Field(default=[], description="Matching text snippets")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")


class SearchRequest(BaseModel):
    """Search request model."""
    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    mode: SearchMode = Field(default=SearchMode.HYBRID, description="Search mode")
    file_types: Optional[List[FileType]] = Field(None, description="Filter by file types")
    extensions: Optional[List[str]] = Field(None, description="Filter by extensions")
    max_results: int = Field(default=20, ge=1, le=100, description="Maximum results")
    threshold: float = Field(default=0.3, ge=0, le=1, description="Minimum relevance score")


class SearchResponse(BaseModel):
    """Search response model."""
    query: str = Field(..., description="Original query")
    mode: SearchMode = Field(..., description="Search mode used")
    total_results: int = Field(..., description="Total matching documents")
    results: List[SearchResult] = Field(..., description="Search results")
    search_time_ms: float = Field(..., description="Search execution time")


class IndexStatus(BaseModel):
    """Indexing status model."""
    total_documents: int = Field(..., description="Total indexed documents")
    total_chunks: int = Field(..., description="Total text chunks")
    last_updated: Optional[datetime] = Field(None, description="Last index update")
    is_indexing: bool = Field(default=False, description="Currently indexing")


class IndexRequest(BaseModel):
    """Index request model."""
    paths: List[str] = Field(..., description="Paths to index")
    recursive: bool = Field(default=True, description="Include subdirectories")
    skip_existing: bool = Field(default=True, description="Skip already indexed files")


class IndexResponse(BaseModel):
    """Index response model."""
    success: bool = Field(..., description="Operation success")
    indexed_count: int = Field(..., description="Number of files indexed")
    failed_count: int = Field(..., description="Number of files failed")
    errors: List[str] = Field(default=[], description="Error messages")
    duration_seconds: float = Field(..., description="Indexing duration")


class FilePreview(BaseModel):
    """File preview model."""
    document: Document = Field(..., description="Document information")
    preview: str = Field(..., description="Preview text content")
    line_count: int = Field(..., description="Total lines in file")
    char_count: int = Field(..., description="Total characters")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="App version")
    uptime_seconds: float = Field(..., description="Service uptime")
    index_status: IndexStatus = Field(..., description="Index status")
