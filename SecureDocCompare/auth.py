"""Moduł autentykacji."""
import secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
import hashlib

from config import settings


class SessionManager:
    """Zarządza sesjami użytkowników."""

    def __init__(self):
        self._sessions: dict[str, datetime] = {}

    def create_session(self) -> str:
        """Tworzy nową sesję."""
        session_id = secrets.token_urlsafe(32)
        self._sessions[session_id] = datetime.now()
        return session_id

    def validate_session(self, session_id: Optional[str]) -> bool:
        """Sprawdza czy sesja jest ważna."""
        if not session_id or session_id not in self._sessions:
            return False

        # Sprawdź czy sesja nie wygasła
        session_time = self._sessions[session_id]
        timeout = timedelta(minutes=settings.session_timeout_minutes)

        if datetime.now() - session_time > timeout:
            # Sesja wygasła
            del self._sessions[session_id]
            return False

        # Odśwież czas sesji
        self._sessions[session_id] = datetime.now()
        return True

    def destroy_session(self, session_id: str):
        """Niszczy sesję."""
        if session_id in self._sessions:
            del self._sessions[session_id]

    def cleanup_old_sessions(self):
        """Usuwa stare sesje."""
        now = datetime.now()
        timeout = timedelta(minutes=settings.session_timeout_minutes)

        expired = [
            sid for sid, stime in self._sessions.items()
            if now - stime > timeout
        ]

        for sid in expired:
            del self._sessions[sid]


# Globalna instancja
session_manager = SessionManager()


def hash_password(password: str) -> str:
    """Hashuje hasło."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str) -> bool:
    """Weryfikuje hasło."""
    hashed = hash_password(password)
    expected = hash_password(settings.app_password)

    # Użyj secrets.compare_digest aby zapobiec timing attacks
    return secrets.compare_digest(hashed, expected)


def get_session_id(request: Request) -> Optional[str]:
    """Pobiera session_id z cookie."""
    return request.cookies.get("session_id")


def require_auth(request: Request):
    """
    Wymaga autentykacji.
    Używane jako dependency w endpointach.
    """
    session_id = get_session_id(request)

    if not session_manager.validate_session(session_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wymagane logowanie"
        )
