"""Modele danych dla usługi porównywania dokumentów."""
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Odpowiedź po załadowaniu dokumentów."""
    document_pair_id: str
    status: str
    message: str


class ProcessRequest(BaseModel):
    """Żądanie przetwarzania dokumentów."""
    document_pair_id: str


class ProcessResponse(BaseModel):
    """Odpowiedź po rozpoczęciu przetwarzania."""
    process_id: str
    status: str
    message: str


class ProcessingStatus(BaseModel):
    """Status przetwarzania."""
    process_id: str
    status: Literal["pending", "processing", "completed", "error"]
    progress: Optional[int] = None  # 0-100
    message: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class ChangeMarker(BaseModel):
    """Znacznik zmiany w tekście."""
    operation: Literal["delete", "equal", "insert"]
    text: str


class ParagraphResult(BaseModel):
    """Reprezentacja paragrafu w wynikowym dokumencie."""
    index: int
    text: str  # Pełny tekst paragrafu (dla nowego dokumentu)
    type: Literal["unchanged", "modified", "added", "deleted"]
    old_text: Optional[str] = None  # Tylko dla modified i deleted
    changes: Optional[List[ChangeMarker]] = None  # Szczegółowe zmiany dla modified


class TableCellChange(BaseModel):
    """Zmiana w komórce tabeli."""
    table_index: int
    row_index: int
    col_index: int
    old_value: str
    new_value: str
    changes: List[ChangeMarker]


class TableResult(BaseModel):
    """Reprezentacja tabeli w wynikowym dokumencie."""
    index: int
    rows: List[List[str]]
    changes: Optional[List[TableCellChange]] = None


class StatisticsResult(BaseModel):
    """Statystyki porównania."""
    total_paragraphs: int
    unchanged_paragraphs: int
    modified_paragraphs: int
    added_paragraphs: int
    deleted_paragraphs: int
    total_changes: int
    tables_count: int
    modified_cells: int


class FullDocumentResult(BaseModel):
    """Pełny dokument ze znacznikami zmian."""
    process_id: str
    document_pair_id: str
    paragraphs: List[ParagraphResult]
    tables: List[TableResult]
    statistics: StatisticsResult
    generated_at: datetime


class ModifiedSentence(BaseModel):
    """Zmienione zdanie."""
    paragraph_index: int
    old_text: str
    new_text: str
    changes: List[ChangeMarker]


class ModifiedSentencesResult(BaseModel):
    """Tylko zmienione zdania."""
    process_id: str
    document_pair_id: str
    modified_sentences: List[ModifiedSentence]
    total_count: int
    generated_at: datetime


class AddedSentence(BaseModel):
    """Dodane zdanie."""
    paragraph_index: int
    text: str


class AddedSentencesResult(BaseModel):
    """Tylko dodane zdania."""
    process_id: str
    document_pair_id: str
    added_sentences: List[AddedSentence]
    total_count: int
    generated_at: datetime


class DeletedSentence(BaseModel):
    """Usunięte zdanie."""
    paragraph_index: int
    text: str


class DeletedSentencesResult(BaseModel):
    """Tylko usunięte zdania."""
    process_id: str
    document_pair_id: str
    deleted_sentences: List[DeletedSentence]
    total_count: int
    generated_at: datetime
