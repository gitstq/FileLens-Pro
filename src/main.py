"""FastAPI main application for FileLens."""

import time
import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from config import settings
from models import (
    SearchRequest, SearchResponse, IndexRequest, IndexResponse,
    IndexStatus, HealthResponse, FilePreview, Document
)
from search_engine import SearchEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
search_engine: SearchEngine = None
start_time = datetime.now()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    global search_engine
    
    # Startup
    logger.info("Starting FileLens server...")
    search_engine = SearchEngine()
    logger.info("FileLens server started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FileLens server...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="🔍 Local Intelligent File Search Tool - Semantic search for your documents",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API info."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{settings.APP_NAME}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                line-height: 1.6;
            }}
            h1 {{ color: #333; }}
            .info {{ background: #f4f4f4; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            code {{ background: #e0e0e0; padding: 2px 6px; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <h1>🔍 {settings.APP_NAME}</h1>
        <div class="info">
            <p><strong>Version:</strong> {settings.APP_VERSION}</p>
            <p><strong>Status:</strong> ✅ Running</p>
            <p>Local Intelligent File Search Tool with semantic search capabilities.</p>
        </div>
        <h2>API Endpoints</h2>
        <ul>
            <li><code>POST /search</code> - Search documents</li>
            <li><code>POST /index</code> - Index files or directories</li>
            <li><code>GET /stats</code> - Get indexing statistics</li>
            <li><code>GET /health</code> - Health check</li>
            <li><code>GET /docs</code> - API documentation (Swagger UI)</li>
        </ul>
    </body>
    </html>
    """


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Search for documents.
    
    Supports keyword, semantic, and hybrid search modes.
    """
    try:
        results = search_engine.search(request)
        return results
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/index", response_model=IndexResponse)
async def index_files(request: IndexRequest, background_tasks: BackgroundTasks):
    """
    Index files or directories.
    
    This will scan the specified paths and add all supported files to the search index.
    """
    try:
        total_indexed = 0
        total_failed = 0
        all_errors = []
        total_duration = 0
        
        for path in request.paths:
            result = search_engine.index_directory(
                path, 
                recursive=request.recursive,
                skip_existing=request.skip_existing
            )
            
            if result.get("success"):
                total_indexed += result.get("indexed_count", 0)
                total_failed += result.get("failed_count", 0)
                all_errors.extend(result.get("errors", []))
                total_duration += result.get("duration_seconds", 0)
            else:
                all_errors.append(result.get("error", "Unknown error"))
        
        return IndexResponse(
            success=True,
            indexed_count=total_indexed,
            failed_count=total_failed,
            errors=all_errors[:20],  # Limit errors
            duration_seconds=round(total_duration, 2)
        )
        
    except Exception as e:
        logger.error(f"Indexing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=IndexStatus)
async def get_stats():
    """Get indexing statistics."""
    try:
        return search_engine.get_stats()
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    uptime = (datetime.now() - start_time).total_seconds()
    stats = search_engine.get_stats()
    
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        uptime_seconds=round(uptime, 2),
        index_status=stats
    )


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document from the index."""
    try:
        success = search_engine.delete_document(doc_id)
        if success:
            return {"success": True, "message": "Document deleted"}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        logger.error(f"Delete error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/index")
async def clear_index():
    """Clear all indexed data."""
    try:
        success = search_engine.clear_index()
        if success:
            return {"success": True, "message": "Index cleared"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear index")
    except Exception as e:
        logger.error(f"Clear index error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents", response_model=list[Document])
async def list_documents(
    file_type: str = None,
    extension: str = None,
    limit: int = 100,
    offset: int = 0
):
    """List indexed documents with optional filtering."""
    try:
        documents = list(search_engine.documents.values())
        
        # Apply filters
        if file_type:
            documents = [d for d in documents if d.file_type.value == file_type]
        if extension:
            documents = [d for d in documents if d.extension == extension]
        
        # Sort by indexed time (newest first)
        documents.sort(key=lambda x: x.indexed_at or datetime.min, reverse=True)
        
        # Apply pagination
        total = len(documents)
        documents = documents[offset:offset + limit]
        
        return documents
        
    except Exception as e:
        logger.error(f"List documents error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
