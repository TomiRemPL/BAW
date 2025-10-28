@echo off
REM Start Services - Batch Script
REM Uruchamia UslugaDoPorownan (port 8001) i SecureDocCompare (port 8000)

echo ========================================
echo   BAW - Document Compare Services
echo ========================================
echo.

REM Sprawdź czy środowisko wirtualne istnieje
if not exist ".venv\Scripts\activate.bat" (
    echo BLAD: Nie znaleziono srodowiska wirtualnego!
    echo Utworz srodowisko: python -m venv .venv
    echo Zainstaluj zaleznosci: pip install -r requirements.txt
    pause
    exit /b 1
)

echo [1/4] Sprawdzanie srodowiska...
call .venv\Scripts\activate.bat

python --version
echo.

echo [2/4] Uruchamianie UslugaDoPorownan (Backend - Port 8001)...
echo Otwieranie nowego okna terminala...

start "BAW Backend (Port 8001)" cmd /k "cd /d %CD% && .venv\Scripts\activate.bat && cd UslugaDoPorownan && echo ======================================== && echo   Backend API (UslugaDoPorownan) && echo   Port: 8001 && echo ======================================== && echo. && echo Uruchamianie serwera... && echo. && uvicorn main:app --host 0.0.0.0 --port 8001 --reload"

echo Backend uruchomiony w nowym oknie
echo Czekam 3 sekundy...
timeout /t 3 /nobreak >nul
echo.

echo [3/4] Uruchamianie SecureDocCompare (Frontend - Port 8000)...
echo Otwieranie nowego okna terminala...

start "BAW Frontend (Port 8000)" cmd /k "cd /d %CD% && .venv\Scripts\activate.bat && cd SecureDocCompare && echo ======================================== && echo   Frontend (SecureDocCompare) && echo   Port: 8000 && echo ======================================== && echo. && echo Uruchamianie serwera... && echo. && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo Frontend uruchomiony w nowym oknie
echo Czekam 3 sekundy...
timeout /t 3 /nobreak >nul
echo.

echo [4/4] Serwisy uruchomione!
echo.
echo ========================================
echo   Serwisy uruchomione!
echo ========================================
echo.
echo Backend API:  http://localhost:8001
echo API Docs:     http://localhost:8001/docs
echo.
echo Frontend:     http://localhost:8000
echo.
echo Aby zatrzymic serwisy:
echo   - Zamknij okna terminali z serwerami
echo   - Lub uzyj stop_services.bat
echo.
echo Logi widoczne w osobnych oknach terminali
echo.

set /p OPEN_BROWSER="Otworzyc przegladarke? (t/n): "
if /i "%OPEN_BROWSER%"=="t" (
    start http://localhost:8000
)

echo.
echo Nacisnij dowolny klawisz aby zamknac to okno...
pause >nul
