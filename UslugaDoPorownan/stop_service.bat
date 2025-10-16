@echo off
REM Skrypt do zatrzymywania Uslugi Porownywania Dokumentow

echo [INFO] Zatrzymywanie uslugi...

REM Znajdz proces Python z uvicorn na porcie 8001
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001 ^| findstr LISTENING') do (
    echo [INFO] Znaleziono proces: %%a
    taskkill /F /PID %%a >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Usluga zatrzymana
        exit /b 0
    )
)

echo [INFO] Usluga nie byla uruchomiona
exit /b 0
