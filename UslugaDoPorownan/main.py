"""Usługa API do porównywania dokumentów."""
import logging
import asyncio
import uuid
from pathlib import Path
from typing import List
from datetime import datetime

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from models import (
    UploadResponse, ProcessRequest, ProcessResponse, ProcessingStatus,
    FullDocumentResult, ModifiedSentencesResult, AddedSentencesResult,
    DeletedSentencesResult, ModifiedSentence, AddedSentence, DeletedSentence
)
from extractor import DocumentExtractor
from comparator import DocumentComparator
from storage import storage
from pdf_converter import PDFConverter
from pdf_converter.config import DEFAULT_CONFIG as PDF_CONFIG
from pdf_converter.post_processor import PostProcessor


# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Inicjalizacja FastAPI
app = FastAPI(
    title="Usługa Porównywania Dokumentów",
    description="API do porównywania dokumentów DOCX z zachowaniem struktury i znaczników zmian",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Katalogi
UPLOADS_DIR = Path("uploads")
REPORTS_DIR = Path("output/reports")


@app.on_event("startup")
async def startup():
    """Inicjalizacja przy starcie aplikacji."""
    logger.info("Uruchamianie usługi porównywania dokumentów")

    # Utworzenie katalogów
    UPLOADS_DIR.mkdir(exist_ok=True)
    logger.info(f"Katalog uploads: {UPLOADS_DIR.absolute()}")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Katalog reports: {REPORTS_DIR.absolute()}")

    logger.info("Usługa gotowa do działania")


# Montowanie statycznych plików dla raportów HTML
app.mount("/reports", StaticFiles(directory=str(REPORTS_DIR)), name="reports")


@app.get("/")
async def root():
    """Endpoint główny."""
    return {
        "service": "Usługa Porównywania Dokumentów",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "upload": "POST /api/documents/upload",
            "process": "POST /api/process",
            "status": "GET /api/status/{process_id}",
            "full": "GET /api/result/{process_id}/full",
            "modified": "GET /api/result/{process_id}/modified",
            "added": "GET /api/result/{process_id}/added",
            "deleted": "GET /api/result/{process_id}/deleted",
            "generate_report": "GET /api/report/{process_id}/generate"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    stats = storage.get_statistics()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "statistics": stats
    }


@app.post("/api/documents/upload", response_model=UploadResponse)
async def upload_documents(
    old_document: UploadFile = File(...),
    new_document: UploadFile = File(...)
):
    """
    Załaduj parę dokumentów do porównania.

    Obsługuje formaty: DOCX, PDF (automatyczna konwersja)

    Args:
        old_document: Stary dokument (DOCX lub PDF)
        new_document: Nowy dokument (DOCX lub PDF)

    Returns:
        UploadResponse z document_pair_id
    """
    try:
        # Walidacja plików - akceptuj .docx i .pdf
        allowed_extensions = {'.docx', '.pdf'}

        old_ext = Path(old_document.filename).suffix.lower()
        new_ext = Path(new_document.filename).suffix.lower()

        if old_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Stary dokument musi być w formacie DOCX lub PDF (otrzymano: {old_ext})"
            )

        if new_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Nowy dokument musi być w formacie DOCX lub PDF (otrzymano: {new_ext})"
            )

        # Generuj ID
        document_pair_id = str(uuid.uuid4())

        # Zapisz pliki tymczasowo
        old_temp_path = UPLOADS_DIR / f"{document_pair_id}_old_temp{old_ext}"
        new_temp_path = UPLOADS_DIR / f"{document_pair_id}_new_temp{new_ext}"

        with open(old_temp_path, "wb") as f:
            content = await old_document.read()
            f.write(content)

        with open(new_temp_path, "wb") as f:
            content = await new_document.read()
            f.write(content)

        # Konwertuj PDF→DOCX jeśli potrzeba
        old_path = UPLOADS_DIR / f"{document_pair_id}_old.docx"
        new_path = UPLOADS_DIR / f"{document_pair_id}_new.docx"

        conversion_messages = []

        if old_ext == '.pdf':
            logger.info(f"Konwersja starego dokumentu PDF→DOCX: {old_document.filename}")
            converter = PDFConverter(PDF_CONFIG)
            result = await asyncio.to_thread(
                converter.convert,
                old_temp_path,
                old_path
            )

            if not result.success:
                raise HTTPException(
                    status_code=500,
                    detail=f"Błąd konwersji starego dokumentu PDF: {result.error}"
                )

            conversion_messages.append(
                f"Stary dokument PDF skonwertowany (metoda: {result.method}, "
                f"jakość: {result.quality_score:.2f})"
            )

            # Usuń tymczasowy PDF
            old_temp_path.unlink()
        else:
            # Jeśli to DOCX, po prostu przenieś
            old_temp_path.rename(old_path)

        if new_ext == '.pdf':
            logger.info(f"Konwersja nowego dokumentu PDF→DOCX: {new_document.filename}")
            converter = PDFConverter(PDF_CONFIG)
            result = await asyncio.to_thread(
                converter.convert,
                new_temp_path,
                new_path
            )

            if not result.success:
                raise HTTPException(
                    status_code=500,
                    detail=f"Błąd konwersji nowego dokumentu PDF: {result.error}"
                )

            conversion_messages.append(
                f"Nowy dokument PDF skonwertowany (metoda: {result.method}, "
                f"jakość: {result.quality_score:.2f})"
            )

            # Usuń tymczasowy PDF
            new_temp_path.unlink()
        else:
            # Jeśli to DOCX, po prostu przenieś
            new_temp_path.rename(new_path)

        # Zapisz w storage
        storage.store_document_pair(
            document_pair_id,
            str(old_path),
            str(new_path)
        )

        # Komunikat
        message = f"Dokumenty zostały załadowane: {old_document.filename}, {new_document.filename}"
        if conversion_messages:
            message += "\\n" + "\\n".join(conversion_messages)

        logger.info(f"Załadowano dokumenty: {document_pair_id}")
        if conversion_messages:
            for msg in conversion_messages:
                logger.info(f"  {msg}")

        return UploadResponse(
            document_pair_id=document_pair_id,
            status="uploaded",
            message=message
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Błąd podczas ładowania dokumentów: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas ładowania dokumentów: {str(e)}"
        )



@app.post("/api/process", response_model=ProcessResponse)
async def start_processing(
    request: ProcessRequest,
    background_tasks: BackgroundTasks
):
    """
    Rozpocznij przetwarzanie (porównywanie) dokumentów.

    Args:
        request: ProcessRequest z document_pair_id

    Returns:
        ProcessResponse z process_id
    """
    try:
        # Sprawdź czy para dokumentów istnieje
        doc_pair = storage.get_document_pair(request.document_pair_id)
        if not doc_pair:
            raise HTTPException(
                status_code=404,
                detail=f"Nie znaleziono pary dokumentów: {request.document_pair_id}"
            )

        # Generuj process ID
        process_id = str(uuid.uuid4())

        # Połącz proces z dokumentem
        storage.link_process_to_document(process_id, request.document_pair_id)

        # Utworzenie statusu
        status = ProcessingStatus(
            process_id=process_id,
            status="pending",
            progress=0,
            message="Oczekiwanie na rozpoczęcie przetwarzania",
            started_at=datetime.now()
        )
        storage.store_processing_status(process_id, status)

        # Uruchom przetwarzanie w tle
        background_tasks.add_task(
            process_documents,
            process_id,
            request.document_pair_id,
            doc_pair[0],
            doc_pair[1]
        )

        logger.info(f"Rozpoczęto przetwarzanie: {process_id}")

        return ProcessResponse(
            process_id=process_id,
            status="started",
            message="Przetwarzanie zostało rozpoczęte"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Błąd podczas rozpoczynania przetwarzania: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas rozpoczynania przetwarzania: {str(e)}"
        )


@app.get("/api/status/{process_id}", response_model=ProcessingStatus)
async def get_status(process_id: str):
    """
    Pobierz status przetwarzania.

    Args:
        process_id: ID procesu

    Returns:
        ProcessingStatus
    """
    status = storage.get_processing_status(process_id)
    if not status:
        raise HTTPException(
            status_code=404,
            detail=f"Nie znaleziono procesu: {process_id}"
        )

    return status


@app.get("/api/result/{process_id}/full", response_model=FullDocumentResult)
async def get_full_result(process_id: str):
    """
    Pobierz pełny dokument ze znacznikami zmian.

    Args:
        process_id: ID procesu

    Returns:
        FullDocumentResult
    """
    result = storage.get_result(process_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Nie znaleziono wyników dla procesu: {process_id}"
        )

    return result


@app.get("/api/result/{process_id}/modified", response_model=ModifiedSentencesResult)
async def get_modified_sentences(process_id: str):
    """
    Pobierz tylko zmienione zdania.

    Args:
        process_id: ID procesu

    Returns:
        ModifiedSentencesResult
    """
    result = storage.get_result(process_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Nie znaleziono wyników dla procesu: {process_id}"
        )

    # Filtruj tylko zmodyfikowane paragrafy
    modified_sentences = [
        ModifiedSentence(
            paragraph_index=p.index,
            old_text=p.old_text,
            new_text=p.text,
            changes=p.changes
        )
        for p in result.paragraphs
        if p.type == "modified"
    ]

    return ModifiedSentencesResult(
        process_id=process_id,
        document_pair_id=result.document_pair_id,
        modified_sentences=modified_sentences,
        total_count=len(modified_sentences),
        generated_at=datetime.now()
    )


@app.get("/api/result/{process_id}/added", response_model=AddedSentencesResult)
async def get_added_sentences(process_id: str):
    """
    Pobierz tylko dodane zdania.

    Args:
        process_id: ID procesu

    Returns:
        AddedSentencesResult
    """
    result = storage.get_result(process_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Nie znaleziono wyników dla procesu: {process_id}"
        )

    # Filtruj tylko dodane paragrafy
    added_sentences = [
        AddedSentence(
            paragraph_index=p.index,
            text=p.text
        )
        for p in result.paragraphs
        if p.type == "added"
    ]

    return AddedSentencesResult(
        process_id=process_id,
        document_pair_id=result.document_pair_id,
        added_sentences=added_sentences,
        total_count=len(added_sentences),
        generated_at=datetime.now()
    )


@app.get("/api/result/{process_id}/deleted", response_model=DeletedSentencesResult)
async def get_deleted_sentences(process_id: str):
    """
    Pobierz tylko usunięte zdania.

    Args:
        process_id: ID procesu

    Returns:
        DeletedSentencesResult
    """
    result = storage.get_result(process_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Nie znaleziono wyników dla procesu: {process_id}"
        )

    # Filtruj tylko usunięte paragrafy
    deleted_sentences = [
        DeletedSentence(
            paragraph_index=p.index,
            text=p.text
        )
        for p in result.paragraphs
        if p.type == "deleted"
    ]

    return DeletedSentencesResult(
        process_id=process_id,
        document_pair_id=result.document_pair_id,
        deleted_sentences=deleted_sentences,
        total_count=len(deleted_sentences),
        generated_at=datetime.now()
    )


@app.get("/api/report/{process_id}/generate")
async def generate_html_report(process_id: str):
    """
    Generuje statyczną stronę HTML z raportem na podstawie wyników procesu.

    Args:
        process_id: ID procesu

    Returns:
        JSON z linkiem do wygenerowanego raportu HTML
    """
    import json

    # Pobierz wynik z storage
    result = storage.get_result(process_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Nie znaleziono wyników dla procesu: {process_id}"
        )

    # Wczytaj template HTML
    template_path = Path(__file__).parent / "report_viewer_offline.html"
    if not template_path.exists():
        raise HTTPException(
            status_code=500,
            detail="Template report_viewer_offline.html nie istnieje"
        )

    with open(template_path, 'r', encoding='utf-8') as f:
        html_template = f.read()

    # Przygotuj dane JSON
    result_dict = result.model_dump(mode='json')
    result_json = json.dumps(result_dict, ensure_ascii=False, indent=2)

    # Osadź dane JSON w HTML (zastąp mechanizm upload danymi)
    # Znajdź miejsce gdzie zdefiniowana jest zmienna fullData i wstaw dane
    html_with_data = html_template.replace(
        'let fullData = null;',
        f'let fullData = {result_json};'
    )

    # Dodaj auto-display przy ładowaniu strony
    html_with_data = html_with_data.replace(
        '</script>',
        '''
        // Auto-display przy ładowaniu strony
        window.addEventListener('DOMContentLoaded', function() {
            if (fullData) {
                document.getElementById('uploadArea').classList.add('hidden');
                document.getElementById('resultsSection').classList.remove('hidden');
                displayResults();
            }
        });
        </script>'''
    )

    # Zapisz do pliku
    reports_dir = Path(__file__).parent / "output" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Nazwa pliku z timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{process_id}_{timestamp}.html"
    report_path = reports_dir / filename

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_with_data)

    logger.info(f"Wygenerowano raport HTML: {report_path}")

    # Zwróć URL do raportu
    # URL względny: /reports/{filename}
    report_url = f"/reports/{filename}"

    return {
        "success": True,
        "process_id": process_id,
        "report_url": report_url,
        "report_filename": filename,
        "report_path": str(report_path),
        "generated_at": datetime.now().isoformat(),
        "message": "Raport HTML został wygenerowany pomyślnie"
    }


# Funkcja pomocnicza do przetwarzania w tle
async def process_documents(
    process_id: str,
    document_pair_id: str,
    old_path: str,
    new_path: str
):
    """
    Przetwarzanie dokumentów w tle.

    Args:
        process_id: ID procesu
        document_pair_id: ID pary dokumentów
        old_path: Ścieżka do starego dokumentu
        new_path: Ścieżka do nowego dokumentu
    """
    try:
        logger.info(f"Rozpoczęcie przetwarzania {process_id}")

        # Aktualizacja statusu
        status = ProcessingStatus(
            process_id=process_id,
            status="processing",
            progress=10,
            message="Ekstrakcja treści ze starego dokumentu",
            started_at=datetime.now()
        )
        storage.store_processing_status(process_id, status)

        # Krok 1: Ekstrakcja
        extractor = DocumentExtractor(verbose=False)
        old_content = await asyncio.to_thread(extractor.extract, old_path)

        status.progress = 30
        status.message = "Ekstrakcja treści z nowego dokumentu"
        storage.store_processing_status(process_id, status)

        new_content = await asyncio.to_thread(extractor.extract, new_path)

        # Krok 2: Porównanie
        status.progress = 50
        status.message = "Porównywanie dokumentów"
        storage.store_processing_status(process_id, status)

        comparator = DocumentComparator()
        paragraphs, tables, statistics = await asyncio.to_thread(
            comparator.compare_documents,
            old_content,
            new_content
        )

        # Krok 3: Utworzenie wyniku
        status.progress = 80
        status.message = "Tworzenie wyników"
        storage.store_processing_status(process_id, status)

        result = FullDocumentResult(
            process_id=process_id,
            document_pair_id=document_pair_id,
            paragraphs=paragraphs,
            tables=tables,
            statistics=statistics,
            generated_at=datetime.now()
        )

        # Zapisz wynik
        storage.store_result(process_id, result)

        # Aktualizacja statusu na zakończony
        status.status = "completed"
        status.progress = 100
        status.message = "Przetwarzanie zakończone pomyślnie"
        status.completed_at = datetime.now()
        storage.store_processing_status(process_id, status)

        logger.info(f"Przetwarzanie zakończone: {process_id}")

    except Exception as e:
        logger.error(f"Błąd podczas przetwarzania {process_id}: {e}", exc_info=True)

        # Aktualizacja statusu na błąd
        status = ProcessingStatus(
            process_id=process_id,
            status="error",
            progress=0,
            message="Błąd podczas przetwarzania",
            error=str(e),
            started_at=datetime.now()
        )
        storage.store_processing_status(process_id, status)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
