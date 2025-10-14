"""Configuration module for document comparison application."""
import os
from pathlib import Path


class Config:
    """Application configuration."""

    # Directories
    OLD_VERSION_DIR = "stara_wersja"
    NEW_VERSION_DIR = "nowa_wersja"
    OUTPUT_DIR = "output"

    # API Keys (from environment variables with fallback)
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

    # Processing settings
    MAX_CONCURRENT_COMPARISONS = 1  # Sequential processing for POC
    CHUNK_SIZE_PARAGRAPHS = 50  # For long documents

    # Report settings
    INCLUDE_METADATA = True
    GENERATE_PDF_AUTO = False  # On-demand only

    # AI settings
    LLM_TIMEOUT = 60  # seconds
    MAX_RETRIES = 3
    CLAUDE_MODEL = "claude-sonnet-4-20250514"

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist."""
        for dir_name in [cls.OLD_VERSION_DIR, cls.NEW_VERSION_DIR, cls.OUTPUT_DIR]:
            Path(dir_name).mkdir(exist_ok=True)

    @classmethod
    def has_ai_capability(cls) -> bool:
        """Check if AI analysis is available."""
        return bool(cls.ANTHROPIC_API_KEY or cls.GOOGLE_API_KEY)
