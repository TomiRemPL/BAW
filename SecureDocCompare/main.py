"""Bezpieczny frontend do porównywania dokumentów."""
import logging
from pathlib import Path
from typing import Optional
import httpx

from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from auth import (
    session_manager, verify_password, get_session_id, require_auth
)
from middleware import (
    SecurityHeadersMiddleware, RateLimitMiddleware, FileValidationMiddleware
)


# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Inicjalizacja FastAPI
app = FastAPI(
    title="Secure Document Compare",
    description="Bezpieczny interfejs do porównywania dokumentów",
    version="1.0.0",
    docs_url=None if settings.production else "/docs",
    redoc_url=None if settings.production else "/redoc"
)


# Middleware zabezpieczający
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(FileValidationMiddleware)


# Statyczne pliki i templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    """Inicjalizacja przy starcie."""
    logger.info("Uruchamianie Secure Document Compare")
    logger.info(f"Port: {settings.app_port}")
    logger.info(f"API URL: {settings.document_api_url}")
    logger.info(f"Tryb produkcyjny: {settings.production}")


@app.on_event("shutdown")
async def shutdown():
    """Czyszczenie przy zamknięciu."""
    logger.info("Zamykanie aplikacji")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Strona główna - przekierowanie lub dashboard."""
    session_id = get_session_id(request)

    if session_manager.validate_session(session_id):
        # Zalogowany - pokaż dashboard
        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request}
        )
    else:
        # Niezalogowany - pokaż login
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": None}
        )


@app.post("/api/login")
async def login(
    request: Request,
    password: str = Form(...)
):
    """Endpoint logowania."""
    if verify_password(password):
        # Utwórz sesję
        session_id = session_manager.create_session()

        # Przekieruj na dashboard
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=settings.production,
            samesite="strict",
            max_age=settings.session_timeout_minutes * 60
        )

        logger.info("Pomyślne logowanie")
        return response
    else:
        logger.warning("Nieudana próba logowania")
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Nieprawidłowe hasło"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )


@app.post("/api/logout")
async def logout(request: Request):
    """Wylogowanie."""
    session_id = get_session_id(request)
    if session_id:
        session_manager.destroy_session(session_id)

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("session_id")

    logger.info("Wylogowanie")
    return response


@app.post("/api/upload")
async def upload_documents(
    request: Request,
    old_document: UploadFile = File(...),
    new_document: UploadFile = File(...),
    _auth: None = Depends(require_auth)
):
    """
    Upload dokumentów do porównania.
    Wymaga autentykacji.
    """
    try:
        # Walidacja nazw plików (akceptujemy DOCX i PDF)
        allowed_extensions = ('.docx', '.pdf')

        if not old_document.filename.lower().endswith(allowed_extensions):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stary dokument musi być w formacie DOCX lub PDF"
            )

        if not new_document.filename.lower().endswith(allowed_extensions):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nowy dokument musi być w formacie DOCX lub PDF"
            )

        # Walidacja rozmiaru
        old_content = await old_document.read()
        if len(old_content) > settings.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Stary dokument jest zbyt duży. Max: {settings.max_file_size // 1024 // 1024}MB"
            )

        new_content = await new_document.read()
        if len(new_content) > settings.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Nowy dokument jest zbyt duży. Max: {settings.max_file_size // 1024 // 1024}MB"
            )

        # Wyślij do API dokumentów
        # Timeout 120s - konwersja PDF może trwać długo (2 duże pliki ~45-50s)
        async with httpx.AsyncClient(timeout=120.0) as client:
            files = {
                'old_document': (old_document.filename, old_content, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
                'new_document': (new_document.filename, new_content, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            }

            response = await client.post(
                f"{settings.document_api_url}/api/documents/upload",
                files=files
            )

            if response.status_code != 200:
                logger.error(f"Błąd API: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Błąd API: {response.text}"
                )

            result = response.json()
            logger.info(f"Upload OK: {result.get('document_pair_id')}")

            return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Błąd podczas uploadu: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas przetwarzania: {str(e)}"
        )


@app.post("/api/process/{document_pair_id}")
async def process_documents(
    document_pair_id: str,
    _auth: None = Depends(require_auth)
):
    """
    Rozpocznij porównywanie dokumentów.
    Wymaga autentykacji.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.document_api_url}/api/process",
                json={"document_pair_id": document_pair_id}
            )

            if response.status_code != 200:
                logger.error(f"Błąd API: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Błąd API: {response.text}"
                )

            result = response.json()
            logger.info(f"Proces rozpoczęty: {result.get('process_id')}")

            return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Błąd podczas rozpoczynania procesu: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd: {str(e)}"
        )


@app.get("/api/status/{process_id}")
async def get_status(
    process_id: str,
    _auth: None = Depends(require_auth)
):
    """
    Sprawdź status przetwarzania.
    Wymaga autentykacji.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{settings.document_api_url}/api/status/{process_id}"
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Błąd API: {response.text}"
                )

            return JSONResponse(content=response.json())

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Błąd podczas pobierania statusu: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd: {str(e)}"
        )


@app.get("/api/result/{process_id}/full")
async def get_full_result(
    process_id: str,
    _auth: None = Depends(require_auth)
):
    """
    Pobierz pełny wynik porównania.
    Wymaga autentykacji.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{settings.document_api_url}/api/result/{process_id}/full"
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Błąd API: {response.text}"
                )

            return JSONResponse(content=response.json())

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Błąd podczas pobierania wyniku: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd: {str(e)}"
        )


@app.get("/api/result/{process_id}/modified")
async def get_modified(
    process_id: str,
    _auth: None = Depends(require_auth)
):
    """Pobierz tylko zmodyfikowane zdania."""
    return await _proxy_result(process_id, "modified")


@app.get("/api/result/{process_id}/added")
async def get_added(
    process_id: str,
    _auth: None = Depends(require_auth)
):
    """Pobierz tylko dodane zdania."""
    return await _proxy_result(process_id, "added")


@app.get("/api/result/{process_id}/deleted")
async def get_deleted(
    process_id: str,
    _auth: None = Depends(require_auth)
):
    """Pobierz tylko usunięte zdania."""
    return await _proxy_result(process_id, "deleted")


async def _proxy_result(process_id: str, result_type: str):
    """Helper do proxy wyników."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{settings.document_api_url}/api/result/{process_id}/{result_type}"
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Błąd API: {response.text}"
                )

            return JSONResponse(content=response.json())

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Błąd podczas pobierania {result_type}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd: {str(e)}"
        )


@app.get("/health")
async def health():
    """Health check."""
    return {
        "status": "healthy",
        "service": "Secure Document Compare",
        "backend_api": settings.document_api_url
    }


# ============================================================================
# Endpointy dla systemu podsumowań (integracja n8n)
# ============================================================================


@app.get("/summary/{process_id}", response_class=HTMLResponse)
async def summary_editor_page(request: Request, process_id: str):
    """
    Strona edytora podsumowania.

    NIE wymaga autentykacji - dostęp przez link z process_id (dla n8n workflow).

    Args:
        request: Request object
        process_id: ID procesu

    Returns:
        HTML strona edytora
    """
    return templates.TemplateResponse(
        "summary_editor.html",
        {"request": request, "process_id": process_id}
    )


@app.get("/api/summary/{process_id}")
async def get_summary_proxy(process_id: str):
    """
    Pobierz podsumowanie (proxy do backend).

    NIE wymaga autentykacji - dla n8n workflow.

    Args:
        process_id: ID procesu

    Returns:
        JSON z podsumowaniem
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{settings.document_api_url}/api/summary/{process_id}"
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Błąd API: {response.text}"
                )

            return JSONResponse(content=response.json())

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Błąd podczas pobierania podsumowania: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd: {str(e)}"
        )


@app.get("/api/summary/{process_id}/status")
async def get_summary_status_proxy(process_id: str):
    """
    Pobierz status podsumowania (proxy do backend).

    NIE wymaga autentykacji - dla n8n workflow.

    Args:
        process_id: ID procesu

    Returns:
        JSON ze statusem
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{settings.document_api_url}/api/summary/{process_id}/status"
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Błąd API: {response.text}"
                )

            return JSONResponse(content=response.json())

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Błąd podczas pobierania statusu podsumowania: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd: {str(e)}"
        )


@app.put("/api/summary/{process_id}")
async def update_summary_proxy(
    process_id: str,
    request: Request
):
    """
    Aktualizuj podsumowanie (proxy do backend).

    NIE wymaga autentykacji - dla n8n workflow.

    Args:
        process_id: ID procesu
        request: Request z danymi do aktualizacji

    Returns:
        JSON ze zaktualizowanym podsumowaniem
    """
    try:
        body = await request.json()

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.put(
                f"{settings.document_api_url}/api/summary/{process_id}",
                json=body
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Błąd API: {response.text}"
                )

            logger.info(f"Zaktualizowano podsumowanie: {process_id}")
            return JSONResponse(content=response.json())

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Błąd podczas aktualizacji podsumowania: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd: {str(e)}"
        )


@app.post("/api/summary/{process_id}/approve")
async def approve_summary_proxy(
    process_id: str,
    request: Request
):
    """
    Zatwierdź/odrzuć podsumowanie (proxy do backend).

    NIE wymaga autentykacji - dla n8n workflow.

    Args:
        process_id: ID procesu
        request: Request z danymi zatwierdzenia

    Returns:
        JSON ze zaktualizowanym podsumowaniem
    """
    try:
        body = await request.json()

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.document_api_url}/api/summary/{process_id}/approve",
                json=body
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Błąd API: {response.text}"
                )

            logger.info(f"Zatwierdzono/odrzucono podsumowanie: {process_id}")
            return JSONResponse(content=response.json())

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Błąd podczas zatwierdzania podsumowania: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.app_port,
        reload=not settings.production,
        log_level="info"
    )
