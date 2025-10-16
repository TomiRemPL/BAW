@echo off
REM Skrypt do uruchamiania Uslugi Porownywania Dokumentow

echo [INFO] Sprawdzanie czy usluga juz dziala...
curl -s http://localhost:8001/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Usluga juz dziala na porcie 8001
    exit /b 0
)

echo [INFO] Uruchamianie uslugi...
cd /d "%~dp0"

REM Uruchom w tle
start /B python -m uvicorn main:app --host 0.0.0.0 --port 8001

REM Czekaj 5 sekund na start
timeout /t 5 /nobreak >nul

REM Sprawdź czy działa
curl -s http://localhost:8001/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Usluga uruchomiona pomyslnie na http://localhost:8001
    exit /b 0
) else (
    echo [ERROR] Nie udalo sie uruchomic uslugi
    exit /b 1
)
