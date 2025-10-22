"""
Wyjątki dla modułu konwersji PDF.
"""


class ConversionError(Exception):
    """Błąd podczas konwersji PDF→DOCX."""
    pass


class ValidationError(Exception):
    """Błąd walidacji jakości konwersji."""
    pass


class TimeoutError(Exception):
    """Przekroczono limit czasu konwersji."""
    pass


class UnsupportedFormatError(Exception):
    """Nieobsługiwany format pliku."""
    pass
