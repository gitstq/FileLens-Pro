"""Configuration management for FileLens."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    # App info
    APP_NAME: str = "FileLens"
    APP_VERSION: str = "1.0.0"
    
    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Data directories
    DATA_DIR: Path = Field(default_factory=lambda: Path.home() / ".filelens")
    UPLOAD_DIR: Path = Field(default_factory=lambda: Path.home() / ".filelens" / "uploads")
    INDEX_DIR: Path = Field(default_factory=lambda: Path.home() / ".filelens" / "index")
    CHROMA_DIR: Path = Field(default_factory=lambda: Path.home() / ".filelens" / "chroma_db")
    
    # Model settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    MAX_RESULTS: int = 50
    
    # Search settings
    DEFAULT_SEARCH_MODE: str = "hybrid"  # keyword, semantic, hybrid
    SIMILARITY_THRESHOLD: float = 0.3
    
    # Supported file extensions
    SUPPORTED_EXTENSIONS: set = {
        # Documents
        ".txt", ".md", ".markdown",
        ".pdf",
        ".doc", ".docx",
        ".ppt", ".pptx",
        ".xls", ".xlsx",
        # Code files
        ".py", ".js", ".ts", ".jsx", ".tsx",
        ".java", ".kt", ".scala",
        ".c", ".cpp", ".h", ".hpp",
        ".go", ".rs",
        ".rb", ".php",
        ".html", ".htm", ".css", ".scss", ".sass",
        ".json", ".xml", ".yaml", ".yml",
        ".sql",
        # Config files
        ".env", ".ini", ".cfg", ".conf",
        ".sh", ".bash", ".zsh", ".ps1",
        ".dockerfile", ".gitignore",
    }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.INDEX_DIR.mkdir(parents=True, exist_ok=True)
        self.CHROMA_DIR.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
