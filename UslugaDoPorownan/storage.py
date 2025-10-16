"""Moduł zarządzania pamięcią dla dokumentów i wyników porównań."""
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path

from models import (
    ProcessingStatus, FullDocumentResult, ModifiedSentencesResult,
    AddedSentencesResult, DeletedSentencesResult
)


logger = logging.getLogger(__name__)


class InMemoryStorage:
    """Przechowywanie danych w pamięci."""

    def __init__(self):
        """Inicjalizacja storage."""
        # Przechowywanie załadowanych dokumentów
        # document_pair_id -> (old_path, new_path)
        self.documents: Dict[str, Tuple[str, str]] = {}

        # Przechowywanie statusów przetwarzania
        # process_id -> ProcessingStatus
        self.processing_status: Dict[str, ProcessingStatus] = {}

        # Przechowywanie wyników
        # process_id -> FullDocumentResult
        self.results: Dict[str, FullDocumentResult] = {}

        # Mapowanie process_id -> document_pair_id
        self.process_to_document: Dict[str, str] = {}

        logger.info("Inicjalizacja in-memory storage")

    def store_document_pair(
        self,
        document_pair_id: str,
        old_path: str,
        new_path: str
    ) -> None:
        """
        Zapisz parę dokumentów.

        Args:
            document_pair_id: ID pary dokumentów
            old_path: Ścieżka do starego dokumentu
            new_path: Ścieżka do nowego dokumentu
        """
        self.documents[document_pair_id] = (old_path, new_path)
        logger.info(f"Zapisano parę dokumentów: {document_pair_id}")

    def get_document_pair(
        self,
        document_pair_id: str
    ) -> Optional[Tuple[str, str]]:
        """
        Pobierz parę dokumentów.

        Args:
            document_pair_id: ID pary dokumentów

        Returns:
            Tuple (old_path, new_path) lub None
        """
        return self.documents.get(document_pair_id)

    def store_processing_status(
        self,
        process_id: str,
        status: ProcessingStatus
    ) -> None:
        """
        Zapisz status przetwarzania.

        Args:
            process_id: ID procesu
            status: Status przetwarzania
        """
        self.processing_status[process_id] = status
        logger.debug(f"Zaktualizowano status {process_id}: {status.status}")

    def get_processing_status(
        self,
        process_id: str
    ) -> Optional[ProcessingStatus]:
        """
        Pobierz status przetwarzania.

        Args:
            process_id: ID procesu

        Returns:
            ProcessingStatus lub None
        """
        return self.processing_status.get(process_id)

    def store_result(
        self,
        process_id: str,
        result: FullDocumentResult
    ) -> None:
        """
        Zapisz wynik porównania.

        Args:
            process_id: ID procesu
            result: Pełny wynik porównania
        """
        self.results[process_id] = result
        logger.info(f"Zapisano wynik porównania: {process_id}")

    def get_result(
        self,
        process_id: str
    ) -> Optional[FullDocumentResult]:
        """
        Pobierz wynik porównania.

        Args:
            process_id: ID procesu

        Returns:
            FullDocumentResult lub None
        """
        return self.results.get(process_id)

    def link_process_to_document(
        self,
        process_id: str,
        document_pair_id: str
    ) -> None:
        """
        Połącz proces z parą dokumentów.

        Args:
            process_id: ID procesu
            document_pair_id: ID pary dokumentów
        """
        self.process_to_document[process_id] = document_pair_id
        logger.debug(f"Połączono proces {process_id} z dokumentem {document_pair_id}")

    def get_document_pair_for_process(
        self,
        process_id: str
    ) -> Optional[str]:
        """
        Pobierz ID pary dokumentów dla procesu.

        Args:
            process_id: ID procesu

        Returns:
            document_pair_id lub None
        """
        return self.process_to_document.get(process_id)

    def cleanup_old_files(self, max_age_hours: int = 24) -> None:
        """
        Usuń stare pliki z katalogu uploads.

        Args:
            max_age_hours: Maksymalny wiek plików w godzinach
        """
        uploads_dir = Path("uploads")
        if not uploads_dir.exists():
            return

        now = datetime.now()

        for file_path in uploads_dir.glob("*.docx"):
            file_age = now - datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_age.total_seconds() > max_age_hours * 3600:
                try:
                    file_path.unlink()
                    logger.info(f"Usunięto stary plik: {file_path.name}")
                except Exception as e:
                    logger.error(f"Błąd podczas usuwania pliku {file_path.name}: {e}")

    def get_statistics(self) -> Dict[str, int]:
        """
        Pobierz statystyki storage.

        Returns:
            Słownik ze statystykami
        """
        return {
            "total_documents": len(self.documents),
            "total_processes": len(self.processing_status),
            "completed_processes": len([
                s for s in self.processing_status.values()
                if s.status == "completed"
            ]),
            "processing_count": len([
                s for s in self.processing_status.values()
                if s.status == "processing"
            ]),
            "error_count": len([
                s for s in self.processing_status.values()
                if s.status == "error"
            ]),
            "cached_results": len(self.results)
        }


# Globalna instancja storage
storage = InMemoryStorage()
