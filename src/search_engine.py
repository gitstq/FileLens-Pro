"""Search engine with vector and keyword search capabilities."""

import re
import time
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings as ChromaSettings

from config import settings
from models import (
    Document, SearchResult, SearchRequest, SearchResponse, 
    SearchMode, FileType, IndexStatus
)
from file_parser import FileParser

logger = logging.getLogger(__name__)


class TextChunker:
    """Split text into chunks for indexing."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        if not text:
            return []
        
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            
            # Try to break at sentence or word boundary
            if end < text_len:
                # Look for sentence ending
                for i in range(end, max(start, end - 100), -1):
                    if text[i-1] in '.!?。！？\n':
                        end = i
                        break
                else:
                    # Look for word boundary
                    for i in range(end, max(start, end - 50), -1):
                        if text[i-1].isspace():
                            end = i
                            break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - self.chunk_overlap
            if start >= end:
                start = end
        
        return chunks


class SearchEngine:
    """Main search engine class."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.chunker = TextChunker(settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
        self.model = None
        self.chroma_client = None
        self.collection = None
        self.documents: Dict[str, Document] = {}
        self._load_model()
        self._init_chroma()
    
    def _load_model(self):
        """Load embedding model."""
        try:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def _init_chroma(self):
        """Initialize ChromaDB."""
        try:
            self.chroma_client = chromadb.PersistentClient(
                path=str(settings.CHROMA_DIR),
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            self.collection = self.chroma_client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info("ChromaDB initialized")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def index_file(self, filepath: str) -> Tuple[bool, Optional[str]]:
        """
        Index a single file.
        
        Returns:
            Tuple of (success, error_message)
        """
        path = Path(filepath)
        
        if not FileParser.is_supported(filepath):
            return False, f"Unsupported file format: {path.suffix}"
        
        try:
            # Parse file
            content, error = FileParser.parse_file(filepath)
            if error:
                return False, error
            
            if not content:
                return False, "No content extracted"
            
            # Create document
            stat = path.stat()
            doc_id = str(path.resolve())
            
            document = Document(
                id=doc_id,
                filename=path.name,
                filepath=str(path.resolve()),
                file_type=FileParser.get_file_type(path.suffix),
                extension=path.suffix.lower(),
                size=stat.st_size,
                created_at=datetime.fromtimestamp(stat.st_ctime),
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                content=content[:1000],  # Store preview only
                indexed_at=datetime.now()
            )
            
            # Chunk text
            chunks = self.chunker.chunk_text(content)
            if not chunks:
                return False, "No text chunks generated"
            
            # Generate embeddings
            embeddings = self.model.encode(chunks).tolist()
            
            # Prepare metadata
            chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [
                {
                    "doc_id": doc_id,
                    "filename": document.filename,
                    "filepath": document.filepath,
                    "file_type": document.file_type.value,
                    "extension": document.extension,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                for i in range(len(chunks))
            ]
            
            # Add to ChromaDB
            self.collection.add(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            
            # Store document info
            self.documents[doc_id] = document
            
            logger.info(f"Indexed: {filepath} ({len(chunks)} chunks)")
            return True, None
            
        except Exception as e:
            logger.error(f"Error indexing {filepath}: {e}")
            return False, str(e)
    
    def index_directory(self, directory: str, recursive: bool = True,
                       skip_existing: bool = True) -> Dict[str, Any]:
        """
        Index all files in a directory.
        
        Returns:
            Dict with indexing statistics
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"success": False, "error": f"Directory not found: {directory}"}
        
        pattern = "**/*" if recursive else "*"
        files = []
        
        for path in dir_path.glob(pattern):
            if path.is_file() and FileParser.is_supported(str(path)):
                # Check if already indexed
                if skip_existing:
                    doc_id = str(path.resolve())
                    if doc_id in self.documents:
                        continue
                files.append(path)
        
        indexed = 0
        failed = 0
        errors = []
        
        start_time = time.time()
        
        for i, filepath in enumerate(files):
            success, error = self.index_file(str(filepath))
            if success:
                indexed += 1
            else:
                failed += 1
                errors.append(f"{filepath}: {error}")
            
            if (i + 1) % 10 == 0:
                logger.info(f"Indexed {i + 1}/{len(files)} files...")
        
        duration = time.time() - start_time
        
        return {
            "success": True,
            "indexed_count": indexed,
            "failed_count": failed,
            "total_files": len(files),
            "errors": errors[:10],  # Return first 10 errors
            "duration_seconds": round(duration, 2)
        }
    
    def search(self, request: SearchRequest) -> SearchResponse:
        """Perform search."""
        start_time = time.time()
        
        if request.mode == SearchMode.KEYWORD:
            results = self._keyword_search(request)
        elif request.mode == SearchMode.SEMANTIC:
            results = self._semantic_search(request)
        else:  # HYBRID
            keyword_results = self._keyword_search(request)
            semantic_results = self._semantic_search(request)
            results = self._merge_results(keyword_results, semantic_results, request.max_results)
        
        search_time = (time.time() - start_time) * 1000
        
        return SearchResponse(
            query=request.query,
            mode=request.mode,
            total_results=len(results),
            results=results,
            search_time_ms=round(search_time, 2)
        )
    
    def _keyword_search(self, request: SearchRequest) -> List[SearchResult]:
        """Perform keyword-based search."""
        query_lower = request.query.lower()
        query_terms = query_lower.split()
        
        results = []
        seen_docs = set()
        
        # Get all documents from ChromaDB
        all_chunks = self.collection.get()
        
        if not all_chunks or not all_chunks['documents']:
            return results
        
        for i, chunk in enumerate(all_chunks['documents']):
            metadata = all_chunks['metadatas'][i]
            doc_id = metadata['doc_id']
            
            # Apply filters
            if request.file_types:
                if metadata['file_type'] not in [ft.value for ft in request.file_types]:
                    continue
            
            if request.extensions:
                if metadata['extension'] not in request.extensions:
                    continue
            
            # Calculate keyword score
            chunk_lower = chunk.lower()
            score = 0
            
            # Exact match bonus
            if query_lower in chunk_lower:
                score += 2.0
            
            # Term frequency
            for term in query_terms:
                score += chunk_lower.count(term) * 0.5
            
            if score > 0:
                if doc_id not in seen_docs:
                    seen_docs.add(doc_id)
                    
                    # Get document info
                    doc = self.documents.get(doc_id)
                    if not doc:
                        continue
                    
                    # Find highlights
                    highlights = self._extract_highlights(chunk, query_terms)
                    
                    result = SearchResult(
                        document=doc,
                        score=min(score, 5.0),  # Cap score
                        highlights=highlights,
                        metadata={"search_type": "keyword"}
                    )
                    results.append(result)
                else:
                    # Update score for existing result
                    for r in results:
                        if r.document.id == doc_id:
                            r.score = max(r.score, min(score, 5.0))
                            break
        
        # Sort by score
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:request.max_results]
    
    def _semantic_search(self, request: SearchRequest) -> List[SearchResult]:
        """Perform semantic vector search."""
        # Generate query embedding
        query_embedding = self.model.encode(request.query).tolist()
        
        # Search in ChromaDB
        where_filter = {}
        if request.file_types:
            where_filter["file_type"] = {"$in": [ft.value for ft in request.file_types]}
        if request.extensions:
            where_filter["extension"] = {"$in": request.extensions}
        
        try:
            results_chroma = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(request.max_results * 3, 100),
                where=where_filter if where_filter else None
            )
        except Exception as e:
            logger.error(f"ChromaDB query error: {e}")
            return []
        
        if not results_chroma or not results_chroma['ids'][0]:
            return []
        
        # Group by document
        doc_scores: Dict[str, List[float]] = {}
        doc_chunks: Dict[str, List[str]] = {}
        
        for i, doc_id in enumerate(results_chroma['metadatas'][0]):
            doc_id = doc_id['doc_id']
            distance = results_chroma['distances'][0][i]
            chunk = results_chroma['documents'][0][i]
            
            # Convert distance to similarity score (cosine distance)
            score = 1 - distance
            
            if doc_id not in doc_scores:
                doc_scores[doc_id] = []
                doc_chunks[doc_id] = []
            
            doc_scores[doc_id].append(score)
            doc_chunks[doc_id].append(chunk)
        
        # Build results
        results = []
        for doc_id, scores in doc_scores.items():
            if max(scores) < request.threshold:
                continue
            
            doc = self.documents.get(doc_id)
            if not doc:
                continue
            
            # Use max score
            best_score = max(scores)
            
            # Get best matching chunks as highlights
            highlights = doc_chunks[doc_id][:3]
            
            result = SearchResult(
                document=doc,
                score=best_score,
                highlights=highlights,
                metadata={"search_type": "semantic"}
            )
            results.append(result)
        
        # Sort by score
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:request.max_results]
    
    def _merge_results(self, keyword_results: List[SearchResult],
                      semantic_results: List[SearchResult],
                      max_results: int) -> List[SearchResult]:
        """Merge and rank keyword and semantic search results."""
        # Create score map
        doc_scores: Dict[str, float] = {}
        doc_results: Dict[str, SearchResult] = {}
        
        # Add keyword results
        for r in keyword_results:
            doc_scores[r.document.id] = doc_scores.get(r.document.id, 0) + r.score * 0.4
            if r.document.id not in doc_results:
                doc_results[r.document.id] = r
        
        # Add semantic results
        for r in semantic_results:
            doc_scores[r.document.id] = doc_scores.get(r.document.id, 0) + r.score * 0.6
            if r.document.id not in doc_results:
                doc_results[r.document.id] = r
            else:
                # Merge highlights
                existing = doc_results[r.document.id]
                existing.highlights = list(set(existing.highlights + r.highlights))[:3]
        
        # Update scores and create final list
        results = []
        for doc_id, score in doc_scores.items():
            result = doc_results[doc_id]
            result.score = min(score, 1.0)
            result.metadata["search_type"] = "hybrid"
            results.append(result)
        
        # Sort by score
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:max_results]
    
    def _extract_highlights(self, text: str, query_terms: List[str], 
                           max_length: int = 200) -> List[str]:
        """Extract highlighted snippets from text."""
        highlights = []
        text_lower = text.lower()
        
        for term in query_terms:
            idx = text_lower.find(term)
            if idx != -1:
                start = max(0, idx - 50)
                end = min(len(text), idx + len(term) + 50)
                snippet = text[start:end]
                if start > 0:
                    snippet = "..." + snippet
                if end < len(text):
                    snippet = snippet + "..."
                highlights.append(snippet)
                
                if len(highlights) >= 3:
                    break
        
        if not highlights and text:
            # Return beginning of text
            highlights.append(text[:max_length] + ("..." if len(text) > max_length else ""))
        
        return highlights
    
    def get_stats(self) -> IndexStatus:
        """Get indexing statistics."""
        try:
            count = self.collection.count()
        except:
            count = 0
        
        return IndexStatus(
            total_documents=len(self.documents),
            total_chunks=count,
            last_updated=datetime.now() if self.documents else None,
            is_indexing=False
        )
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from index."""
        try:
            # Delete chunks
            self.collection.delete(where={"doc_id": doc_id})
            
            # Remove from documents dict
            if doc_id in self.documents:
                del self.documents[doc_id]
            
            return True
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            return False
    
    def clear_index(self) -> bool:
        """Clear all indexed data."""
        try:
            self.collection.delete(where={})
            self.documents.clear()
            return True
        except Exception as e:
            logger.error(f"Error clearing index: {e}")
            return False
