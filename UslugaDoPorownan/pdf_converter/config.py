"""
Konfiguracja modułu konwersji PDF.
"""

from typing import Optional
from pydantic import BaseModel, Field


class PDFConverterConfig(BaseModel):
    """Konfiguracja konwertera PDF."""

    # Limity czasowe
    max_conversion_time: int = Field(
        default=60,
        description="Maksymalny czas konwersji w sekundach (dla 50 stron)"
    )

    # Progi jakości
    min_quality_score: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimalny wynik jakości (0.0-1.0) dla pdf2docx przed fallback"
    )

    # Priorytety ekstrakcji
    preserve_tables: bool = Field(
        default=True,
        description="Priorytet zachowania tabel"
    )
    preserve_structure: bool = Field(
        default=True,
        description="Priorytet zachowania struktury tekstu"
    )
    preserve_numbering: bool = Field(
        default=True,
        description="Priorytet zachowania numeracji"
    )
    preserve_formatting: bool = Field(
        default=True,
        description="Priorytet zachowania formatowania"
    )

    # Fallback
    enable_fallback: bool = Field(
        default=True,
        description="Włącz automatyczny fallback do pdfplumber"
    )

    # Post-processing
    enable_post_processing: bool = Field(
        default=True,
        description="Włącz post-processing dla dokumentów prawnych"
    )

    # Debugowanie
    verbose: bool = Field(
        default=False,
        description="Szczegółowe logowanie"
    )

    class Config:
        frozen = True  # Immutable


# Domyślna konfiguracja
DEFAULT_CONFIG = PDFConverterConfig()
