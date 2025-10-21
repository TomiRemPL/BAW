"""Konfiguracja aplikacji."""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Ustawienia aplikacji."""

    # Autentykacja
    app_password: str = "changeme"
    secret_key: str = "change-this-to-a-very-long-random-string-for-production"

    # API dokumentów
    document_api_url: str = "http://localhost:8001"

    # Aplikacja
    app_port: int = 8000
    production: bool = False

    # Limity bezpieczeństwa
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_extensions: set = {".docx"}
    max_requests_per_minute: int = 20
    session_timeout_minutes: int = 60

    # Katalogi
    upload_dir: Path = Path("uploads")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instancja ustawień
settings = Settings()

# Utworzenie katalogu uploads
settings.upload_dir.mkdir(exist_ok=True)
