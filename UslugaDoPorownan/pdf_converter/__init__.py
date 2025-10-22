"""
Moduł konwersji PDF→DOCX dla UslugaDoPorownan.

Ten moduł zapewnia dwupoziomowy system konwersji PDF na DOCX:
- pdf2docx (podstawowy, ~95% przypadków)
- pdfplumber (fallback dla skomplikowanych tabel)

Z walidacją jakości i automatycznym fallback.
"""

from .converter import PDFConverter, ConversionResult
from .validators import QualityValidator
from .exceptions import ConversionError, ValidationError

__all__ = [
    "PDFConverter",
    "ConversionResult",
    "QualityValidator",
    "ConversionError",
    "ValidationError",
]

__version__ = "1.0.0"
