# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based document comparison POC application designed to compare banking documents in DOCX format. The application is a standalone web application with a FastAPI backend and responsive HTML frontend, running entirely locally without external databases or message brokers.

## Development Commands

### Setup and Running
```bash
# Install dependencies and run the application
uv run uvicorn main:app --reload
```

### Project Structure
The application follows this directory layout:
- `main.py` - FastAPI application entry point
- `processors/` - Core document processing logic (extractor, comparator, analyzer)
- `report_generator/` - HTML and PDF report generation
- `templates/` - Jinja2 templates for web interface
- `static/` - CSS and JavaScript files
- `nowa_wersja/` - Input directory for new document versions
- `stara_wersja/` - Input directory for old document versions
- `output/` - Generated reports and logs

## Architecture

### Core Components

**Document Processing Pipeline:**
1. **DocumentExtractor** (`processors/extractor.py`) - Extracts content from DOCX files using docx2python, returning structured data including text, paragraphs, tables, comments, and metadata
2. **DocumentComparator** (`processors/comparator.py`) - Performs diff operations using fast_diff_match_patch at paragraph and word level, with special handling for tables and metadata
3. **AIAnalyzer** (`processors/analyzer.py`) - Optional AI-powered analysis using Claude (claude-sonnet-4-20250514) with fallback to Gemini, classifies changes by severity and compliance impact

**Report Generation:**
- **HTMLReportGenerator** (`report_generator/html_generator.py`) - Generates three types of views: Dashboard, Comparison Report, and Summary
- **PDFGenerator** (`report_generator/pdf_generator.py`) - Converts HTML reports to PDF using WeasyPrint

### API Endpoints

- `GET /` - Dashboard interface
- `GET /api/documents` - Lists document pairs from input directories
- `POST /api/compare` - Starts comparison (basic or advanced mode), returns comparison_id
- `GET /api/compare/{comparison_id}/status` - Polls comparison status
- `GET /report/{comparison_id}` - View HTML report
- `GET /api/download/{comparison_id}` - Download PDF report
- `GET /api/summary` - Aggregated view of all comparisons

### Analysis Modes

**Basic Mode:** Pure diff-based comparison without AI, works without API keys

**Advanced Mode:** Includes AI analysis with:
- Severity classification (MINOR/MODERATE/MAJOR)
- Compliance checking for DORA, KYC, and AML regulations
- Requires ANTHROPIC_API_KEY environment variable

### Configuration

API keys are loaded from environment variables:
- `ANTHROPIC_API_KEY` - Primary AI provider (Claude)
- `GOOGLE_API_KEY` - Fallback AI provider (Gemini)

The application gracefully degrades if no API keys are available.

### Design System

Color scheme for banking context:
- Primary background: #F2F2F2 (light gray)
- Accent colors: #009597 (duck blue), #70A300 (dark green), #ED1B2F (banking red)
- Text: #595959 (dark gray)
- Table borders: #A6A6A6 (medium gray)

## Key Implementation Requirements

- Use type hints for all functions
- Document all classes and methods with docstrings
- Use Pydantic models for all data structures
- Use async/await for I/O operations
- Log to both console (colored) and file (`output/app.log` with rotation)
- Handle errors gracefully with user-friendly messages
- Process comparison requests sequentially (MAX_CONCURRENT_COMPARISONS = 1)
