"""Custom exceptions for document comparison application."""


class DocumentComparisonError(Exception):
    """Base exception for document comparison errors."""
    pass


class FileValidationError(DocumentComparisonError):
    """Raised when file validation fails."""
    pass


class DocumentExtractionError(DocumentComparisonError):
    """Raised when document extraction fails."""
    pass


class ComparisonProcessError(DocumentComparisonError):
    """Raised when document comparison process fails."""
    pass


class ReportGenerationError(DocumentComparisonError):
    """Raised when report generation fails."""
    pass


class AIAnalysisError(DocumentComparisonError):
    """Raised when AI analysis fails."""
    pass


class InvalidDocumentFormatError(FileValidationError):
    """Raised when document format is invalid."""
    pass


class CorruptedDocumentError(FileValidationError):
    """Raised when document is corrupted or unreadable."""
    pass


class FileTooLargeError(FileValidationError):
    """Raised when file exceeds maximum allowed size."""
    pass


class EmptyDocumentError(FileValidationError):
    """Raised when document has no content."""
    pass
