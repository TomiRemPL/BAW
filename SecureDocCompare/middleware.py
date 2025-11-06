"""Middleware zabezpieczający."""
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Callable
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Dodaje bezpieczne nagłówki HTTP."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Bezpieczne nagłówki
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' cdn.jsdelivr.net cdnjs.cloudflare.com cdn.quilljs.com unpkg.com; "
            "style-src 'self' 'unsafe-inline' cdnjs.cloudflare.com cdn.quilljs.com; "
            "img-src 'self' data:; "
            "font-src 'self' cdnjs.cloudflare.com cdn.quilljs.com data:; "
            "connect-src 'self';"
        )

        # Ukryj informacje o serwerze
        response.headers["Server"] = "SecureDocCompare"

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting - ogranicza liczbę żądań."""

    def __init__(self, app):
        super().__init__(app)
        self._requests: dict[str, list[datetime]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Pobierz IP klienta
        client_ip = request.client.host

        # Wyłącz rate limiting dla statycznych plików
        if request.url.path.startswith("/static/"):
            return await call_next(request)

        # Sprawdź rate limit
        now = datetime.now()
        window = timedelta(minutes=1)

        # Usuń stare requesty
        self._requests[client_ip] = [
            req_time for req_time in self._requests[client_ip]
            if now - req_time < window
        ]

        # Sprawdź limit
        if len(self._requests[client_ip]) >= settings.max_requests_per_minute:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Zbyt wiele żądań. Spróbuj ponownie za chwilę."}
            )

        # Dodaj nowy request
        self._requests[client_ip].append(now)

        return await call_next(request)


class FileValidationMiddleware(BaseHTTPMiddleware):
    """Waliduje uploadowane pliki."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Sprawdź tylko endpointy z uploadem
        if request.url.path == "/api/upload" and request.method == "POST":
            # Sprawdź Content-Length
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > settings.max_file_size:
                return JSONResponse(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    content={"detail": f"Plik zbyt duży. Maksymalny rozmiar: {settings.max_file_size // 1024 // 1024}MB"}
                )

        return await call_next(request)
