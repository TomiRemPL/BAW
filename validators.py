"""File validation utilities for document comparison."""
import logging
from pathlib import Path
from typing import Tuple
import zipfile

from exceptions import (
    FileValidationError,
    InvalidDocumentFormatError,
    CorruptedDocumentError,
    FileTooLargeError,
    EmptyDocumentError
)


logger = logging.getLogger(__name__)


# Constants
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
MIN_FILE_SIZE = 100  # 100 bytes
ALLOWED_EXTENSIONS = ['.docx']


class FileValidator:
    """Validates document files before processing."""

    @staticmethod
    def validate_file(file_path: str) -> Tuple[bool, str]:
        """
        Comprehensive file validation.

        Args:
            file_path: Path to the file to validate

        Returns:
            Tuple of (is_valid, error_message)

        Raises:
            FileValidationError: If validation fails
        """
        path = Path(file_path)

        try:
            # Check if file exists
            if not path.exists():
                raise FileValidationError(f"Plik nie istnieje: {file_path}")

            # Check if it's a file (not a directory)
            if not path.is_file():
                raise FileValidationError(f"Ścieżka nie wskazuje na plik: {file_path}")

            # Check file extension
            FileValidator._validate_extension(path)

            # Check file size
            FileValidator._validate_file_size(path)

            # Check if file is readable
            FileValidator._validate_readable(path)

            # Check DOCX structure
            FileValidator._validate_docx_structure(path)

            logger.info(f"Walidacja pliku pomyślna: {file_path}")
            return True, ""

        except FileValidationError as e:
            logger.error(f"Walidacja pliku nie powiodła się: {e}")
            raise

        except Exception as e:
            logger.error(f"Nieoczekiwany błąd podczas walidacji: {e}", exc_info=True)
            raise FileValidationError(f"Błąd walidacji: {e}")

    @staticmethod
    def _validate_extension(path: Path) -> None:
        """Validate file extension."""
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            raise InvalidDocumentFormatError(
                f"Nieprawidłowe rozszerzenie pliku: {path.suffix}. "
                f"Dozwolone rozszerzenia: {', '.join(ALLOWED_EXTENSIONS)}"
            )

    @staticmethod
    def _validate_file_size(path: Path) -> None:
        """Validate file size."""
        size = path.stat().st_size

        if size > MAX_FILE_SIZE:
            raise FileTooLargeError(
                f"Plik jest zbyt duży: {size / (1024 * 1024):.2f} MB. "
                f"Maksymalny rozmiar: {MAX_FILE_SIZE / (1024 * 1024):.2f} MB"
            )

        if size < MIN_FILE_SIZE:
            raise EmptyDocumentError(
                f"Plik jest zbyt mały (prawdopodobnie pusty): {size} bajtów"
            )

    @staticmethod
    def _validate_readable(path: Path) -> None:
        """Check if file is readable."""
        try:
            with open(path, 'rb') as f:
                # Try to read first few bytes
                f.read(100)
        except PermissionError:
            raise FileValidationError(f"Brak uprawnień do odczytu pliku: {path}")
        except OSError as e:
            raise FileValidationError(f"Nie można odczytać pliku: {e}")

    @staticmethod
    def _validate_docx_structure(path: Path) -> None:
        """
        Validate DOCX file structure.

        DOCX files are ZIP archives with a specific structure.
        """
        try:
            # Try to open as ZIP
            with zipfile.ZipFile(path, 'r') as docx_zip:
                # Check for essential DOCX components
                namelist = docx_zip.namelist()

                # Essential files that should be present in a valid DOCX
                essential_files = [
                    '[Content_Types].xml',
                    '_rels/.rels'
                ]

                # Check if at least one essential file exists
                has_essential = any(
                    any(f in name for f in essential_files)
                    for name in namelist
                )

                if not has_essential:
                    raise CorruptedDocumentError(
                        "Plik DOCX nie zawiera wymaganych komponentów"
                    )

                # Check if document.xml exists (main document content)
                has_document_xml = any(
                    'document.xml' in name for name in namelist
                )

                if not has_document_xml:
                    raise CorruptedDocumentError(
                        "Plik DOCX nie zawiera głównego dokumentu (document.xml)"
                    )

                # Test if we can extract at least one file
                try:
                    test_file = namelist[0]
                    docx_zip.read(test_file)
                except Exception:
                    raise CorruptedDocumentError(
                        "Nie można wyodrębnić zawartości z pliku DOCX"
                    )

        except zipfile.BadZipFile:
            raise CorruptedDocumentError(
                f"Plik {path.name} nie jest prawidłowym dokumentem DOCX (uszkodzony ZIP)"
            )

        except CorruptedDocumentError:
            raise

        except Exception as e:
            raise CorruptedDocumentError(
                f"Błąd podczas sprawdzania struktury DOCX: {e}"
            )

    @staticmethod
    def validate_pair(old_path: str, new_path: str) -> None:
        """
        Validate a pair of documents.

        Args:
            old_path: Path to old document
            new_path: Path to new document

        Raises:
            FileValidationError: If validation fails for either file
        """
        logger.info(f"Walidacja pary dokumentów: {old_path} <-> {new_path}")

        FileValidator.validate_file(old_path)
        FileValidator.validate_file(new_path)

        logger.info("Walidacja pary dokumentów pomyślna")
