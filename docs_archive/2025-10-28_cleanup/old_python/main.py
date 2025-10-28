"""Main FastAPI application for document comparison."""
import logging
import asyncio
import uuid
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import Config
from processors import DocumentExtractor, DocumentComparator, AIAnalyzer
from report_generator import HTMLReportGenerator, PDFGenerator
from report_generator.html_generator import DocumentPair, ComparisonReport
from validators import FileValidator
from exceptions import (
    DocumentComparisonError,
    FileValidationError,
    DocumentExtractionError,
    ComparisonProcessError,
    ReportGenerationError
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Document Comparison POC",
    description="Banking document comparison application",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for comparisons
comparisons: Dict[str, Dict] = {}
comparison_results: Dict[str, ComparisonReport] = {}


# Pydantic models for API
class CompareRequest(BaseModel):
    """Request to compare two documents."""
    old_path: str
    new_path: str
    mode: str = "basic"  # "basic" or "advanced"


class CompareResponse(BaseModel):
    """Response from starting a comparison."""
    comparison_id: str
    status: str


class StatusResponse(BaseModel):
    """Response for status check."""
    status: str
    report_url: Optional[str] = None
    error: Optional[str] = None


# Startup event
@app.on_event("startup")
async def startup():
    """Initialize application on startup."""
    logger.info("Starting document comparison application")

    # Ensure directories exist
    Config.ensure_directories()

    # Check API keys
    if Config.has_ai_capability():
        logger.info("AI analysis available")
    else:
        logger.warning("No AI API keys configured - only basic comparison available")

    # Verify directories
    for dir_name in [Config.OLD_VERSION_DIR, Config.NEW_VERSION_DIR, Config.OUTPUT_DIR]:
        dir_path = Path(dir_name)
        if dir_path.exists():
            logger.info(f"Directory OK: {dir_name}")
        else:
            logger.warning(f"Directory created: {dir_name}")

    logger.info("Application startup complete")


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard page."""
    try:
        # Scan for document pairs
        document_pairs = scan_document_pairs()

        # Get current comparison statuses
        comparison_statuses = {
            cid: data["status"]
            for cid, data in comparisons.items()
        }

        # Generate HTML
        generator = HTMLReportGenerator()
        html = generator.generate_dashboard(document_pairs, comparison_statuses)

        return HTMLResponse(content=html)

    except Exception as e:
        logger.error(f"Error rendering dashboard: {e}", exc_info=True)
        return HTMLResponse(
            content=f"<h1>Error</h1><p>{str(e)}</p>",
            status_code=500
        )


@app.get("/api/documents")
async def get_documents():
    """Get list of document pairs."""
    try:
        document_pairs = scan_document_pairs()

        return {
            "pairs": [pair.dict() for pair in document_pairs],
            "total": len(document_pairs)
        }

    except Exception as e:
        logger.error(f"Error getting documents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compare", response_model=CompareResponse)
async def start_comparison(
    request: CompareRequest,
    background_tasks: BackgroundTasks
):
    """Start a document comparison."""
    try:
        # Validate paths
        old_path = Path(request.old_path)
        new_path = Path(request.new_path)

        # Comprehensive file validation
        try:
            FileValidator.validate_pair(str(old_path), str(new_path))
        except FileValidationError as e:
            logger.error(f"File validation failed: {e}")
            raise HTTPException(status_code=400, detail=str(e))

        # Validate mode
        if request.mode not in ["basic", "advanced"]:
            raise HTTPException(status_code=400, detail="Tryb musi być 'basic' lub 'advanced'")

        # Check if AI is required but not available
        if request.mode == "advanced" and not Config.has_ai_capability():
            raise HTTPException(
                status_code=400,
                detail="Tryb zaawansowany wymaga klucza API (ANTHROPIC_API_KEY lub GOOGLE_API_KEY)"
            )

        # Generate comparison ID
        comparison_id = str(uuid.uuid4())

        # Store comparison metadata
        comparisons[comparison_id] = {
            "status": "processing",
            "old_path": str(old_path),
            "new_path": str(new_path),
            "mode": request.mode,
            "started_at": datetime.now().isoformat()
        }

        # Start background task
        background_tasks.add_task(
            perform_comparison,
            comparison_id,
            str(old_path),
            str(new_path),
            request.mode
        )

        logger.info(f"Started comparison {comparison_id} in {request.mode} mode")

        return CompareResponse(
            comparison_id=comparison_id,
            status="started"
        )

    except HTTPException:
        raise
    except FileValidationError as e:
        logger.error(f"File validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error starting comparison: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Błąd podczas rozpoczynania porównania: {str(e)}")


@app.get("/api/compare/{comparison_id}/status", response_model=StatusResponse)
async def get_comparison_status(comparison_id: str):
    """Get status of a comparison."""
    if comparison_id not in comparisons:
        raise HTTPException(status_code=404, detail="Comparison not found")

    comparison = comparisons[comparison_id]
    status = comparison["status"]

    response = StatusResponse(status=status)

    if status == "completed":
        response.report_url = f"/report/{comparison_id}"
    elif status == "error":
        response.error = comparison.get("error", "Unknown error")

    return response


@app.get("/report/{comparison_id}", response_class=HTMLResponse)
async def view_report(comparison_id: str):
    """View a comparison report."""
    if comparison_id not in comparison_results:
        raise HTTPException(status_code=404, detail="Report not found")

    try:
        report_data = comparison_results[comparison_id]

        generator = HTMLReportGenerator()
        html = generator.generate_comparison_report(report_data)

        return HTMLResponse(content=html)

    except Exception as e:
        logger.error(f"Error rendering report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{comparison_id}")
async def download_pdf(comparison_id: str):
    """Download PDF report."""
    if comparison_id not in comparison_results:
        raise HTTPException(status_code=404, detail="Raport nie został znaleziony")

    try:
        report_data = comparison_results[comparison_id]

        # Generate PDF directly from report data
        pdf_gen = PDFGenerator()
        pdf_path = pdf_gen.generate_pdf(
            report_data,
            comparison_id,
            report_data.document_pair.name,
            report_data.document_pair.name
        )

        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=Path(pdf_path).name
        )

    except ReportGenerationError as e:
        logger.error(f"Report generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        logger.error(f"Error generating PDF: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Błąd podczas generowania PDF: {str(e)}")


@app.get("/api/summary", response_class=HTMLResponse)
async def view_summary():
    """View summary of all comparisons."""
    try:
        # Get all completed reports
        reports = [
            report for report in comparison_results.values()
        ]

        if not reports:
            return HTMLResponse(
                content="<h1>No reports available</h1><p>Complete some comparisons first.</p>"
            )

        generator = HTMLReportGenerator()
        html = generator.generate_summary(reports)

        return HTMLResponse(content=html)

    except Exception as e:
        logger.error(f"Error rendering summary: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Helper functions

def scan_document_pairs() -> List[DocumentPair]:
    """Scan directories for document pairs."""
    old_dir = Path(Config.OLD_VERSION_DIR)
    new_dir = Path(Config.NEW_VERSION_DIR)

    pairs = []

    # Get all DOCX files from old directory
    old_files = {f.name: f for f in old_dir.glob("*.docx")}

    # Match with new directory
    for old_name, old_path in old_files.items():
        new_path = new_dir / old_name

        if new_path.exists():
            # Get file stats
            old_stat = old_path.stat()
            new_stat = new_path.stat()

            # Determine status and comparison_id
            status = "pending"
            comparison_id = None
            for cid, comp in comparisons.items():
                if comp["old_path"] == str(old_path) and comp["new_path"] == str(new_path):
                    status = comp["status"]
                    comparison_id = cid
                    break

            pair = DocumentPair(
                name=old_name,
                old_path=str(old_path),
                new_path=str(new_path),
                old_size=old_stat.st_size,
                new_size=new_stat.st_size,
                old_modified=datetime.fromtimestamp(old_stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                new_modified=datetime.fromtimestamp(new_stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                status=status,
                comparison_id=comparison_id
            )
            pairs.append(pair)

    logger.debug(f"Found {len(pairs)} document pairs")
    return pairs


async def perform_comparison(
    comparison_id: str,
    old_path: str,
    new_path: str,
    mode: str
):
    """
    Perform document comparison in background.

    This is the main processing pipeline.
    """
    try:
        logger.info(f"Starting comparison {comparison_id}")

        # Update status
        comparisons[comparison_id]["status"] = "processing"

        # Step 1: Extract documents
        logger.info("Step 1: Extracting documents")
        extractor = DocumentExtractor(verbose=False)

        old_content = await asyncio.to_thread(extractor.extract, old_path)
        new_content = await asyncio.to_thread(extractor.extract, new_path)

        logger.info("Documents extracted successfully")

        # Step 2: Compare documents
        logger.info("Step 2: Comparing documents")
        comparator = DocumentComparator()

        diff_result = await asyncio.to_thread(
            comparator.compare,
            old_content,
            new_content
        )

        table_diff = await asyncio.to_thread(
            comparator.compare_tables,
            old_content.tables,
            new_content.tables
        )

        metadata_diff = await asyncio.to_thread(
            comparator.compare_metadata,
            old_content,
            new_content
        )

        logger.info("Comparison complete")

        # Step 3: AI Analysis (if advanced mode)
        ai_analysis = None
        if mode == "advanced":
            logger.info("Step 3: Running AI analysis")
            analyzer = AIAnalyzer()

            ai_analysis = await asyncio.to_thread(
                analyzer.analyze_advanced,
                diff_result
            )

            logger.info("AI analysis complete")

        # Step 4: Create report
        logger.info("Step 4: Creating report")

        # Get file stats for document pair
        old_stat = Path(old_path).stat()
        new_stat = Path(new_path).stat()

        document_pair = DocumentPair(
            name=Path(old_path).name,
            old_path=old_path,
            new_path=new_path,
            old_size=old_stat.st_size,
            new_size=new_stat.st_size,
            old_modified=datetime.fromtimestamp(old_stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            new_modified=datetime.fromtimestamp(new_stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            status="completed"
        )

        report = ComparisonReport(
            comparison_id=comparison_id,
            document_pair=document_pair,
            old_content=old_content,
            new_content=new_content,
            diff_result=diff_result,
            table_diff=table_diff,
            metadata_diff=metadata_diff,
            ai_analysis=ai_analysis,
            generated_at=datetime.now()
        )

        # Store report
        comparison_results[comparison_id] = report

        # Update status
        comparisons[comparison_id]["status"] = "completed"
        comparisons[comparison_id]["completed_at"] = datetime.now().isoformat()

        logger.info(f"Comparison {comparison_id} completed successfully")

    except FileValidationError as e:
        logger.error(f"File validation error in comparison {comparison_id}: {e}")
        comparisons[comparison_id]["status"] = "error"
        comparisons[comparison_id]["error"] = f"Błąd walidacji pliku: {str(e)}"
        comparisons[comparison_id]["failed_at"] = datetime.now().isoformat()

    except DocumentExtractionError as e:
        logger.error(f"Extraction error in comparison {comparison_id}: {e}")
        comparisons[comparison_id]["status"] = "error"
        comparisons[comparison_id]["error"] = f"Błąd ekstrakcji dokumentu: {str(e)}"
        comparisons[comparison_id]["failed_at"] = datetime.now().isoformat()

    except ComparisonProcessError as e:
        logger.error(f"Comparison error in comparison {comparison_id}: {e}")
        comparisons[comparison_id]["status"] = "error"
        comparisons[comparison_id]["error"] = f"Błąd porównywania: {str(e)}"
        comparisons[comparison_id]["failed_at"] = datetime.now().isoformat()

    except ReportGenerationError as e:
        logger.error(f"Report generation error in comparison {comparison_id}: {e}")
        comparisons[comparison_id]["status"] = "error"
        comparisons[comparison_id]["error"] = f"Błąd generowania raportu: {str(e)}"
        comparisons[comparison_id]["failed_at"] = datetime.now().isoformat()

    except Exception as e:
        logger.error(f"Unexpected error in comparison {comparison_id}: {e}", exc_info=True)
        comparisons[comparison_id]["status"] = "error"
        comparisons[comparison_id]["error"] = f"Nieoczekiwany błąd: {str(e)}"
        comparisons[comparison_id]["failed_at"] = datetime.now().isoformat()


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "ai_available": Config.has_ai_capability(),
        "active_comparisons": len([c for c in comparisons.values() if c["status"] == "processing"]),
        "completed_comparisons": len([c for c in comparisons.values() if c["status"] == "completed"])
    }


# Mount static files AFTER all routes
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
