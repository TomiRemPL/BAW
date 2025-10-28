@echo off
REM Check Services - Batch Script
REM Sprawdza status UslugaDoPorownan i SecureDocCompare

echo ========================================
echo   Status serwisow BAW
echo ========================================
echo.

echo [1/2] Sprawdzanie portow...
echo.

REM Sprawdź port 8001 (Backend)
netstat -ano | findstr ":8001.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo Backend ^(Port 8001^): ZATRZYMANY
    set BACKEND_RUNNING=0
) else (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001.*LISTENING"') do set PID_8001=%%a
    echo Backend ^(Port 8001^): URUCHOMIONY
    echo   PID: %PID_8001%
    set BACKEND_RUNNING=1
)

echo.

REM Sprawdź port 8000 (Frontend)
netstat -ano | findstr ":8000.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo Frontend ^(Port 8000^): ZATRZYMANY
    set FRONTEND_RUNNING=0
) else (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING"') do set PID_8000=%%a
    echo Frontend ^(Port 8000^): URUCHOMIONY
    echo   PID: %PID_8000%
    set FRONTEND_RUNNING=1
)

echo.
echo [2/2] Sprawdzanie health endpoints...
echo.

REM Sprawdź backend health (jeśli curl jest dostępny)
where curl >nul 2>&1
if errorlevel 1 (
    echo curl nie jest dostepny - pomijam test HTTP
) else (
    if %BACKEND_RUNNING%==1 (
        curl -s http://localhost:8001/health >nul 2>&1
        if errorlevel 1 (
            echo Backend Health: BLAD
        ) else (
            echo Backend Health: OK
        )
    ) else (
        echo Backend Health: NIEDOSTEPNY ^(serwis zatrzymany^)
    )

    echo.

    if %FRONTEND_RUNNING%==1 (
        curl -s http://localhost:8000/health >nul 2>&1
        if errorlevel 1 (
            echo Frontend Health: BLAD
        ) else (
            echo Frontend Health: OK
        )
    ) else (
        echo Frontend Health: NIEDOSTEPNY ^(serwis zatrzymany^)
    )
)

echo.
echo ========================================

REM Podsumowanie
if %BACKEND_RUNNING%==1 if %FRONTEND_RUNNING%==1 (
    echo   Status: WSZYSTKO DZIALA
    echo.
    echo Adresy:
    echo   Backend:  http://localhost:8001
    echo   Docs:     http://localhost:8001/docs
    echo   Frontend: http://localhost:8000
) else if %BACKEND_RUNNING%==1 (
    echo   Status: CZESCIOWO URUCHOMIONE
    echo.
    echo   Frontend jest zatrzymany
    echo   Uruchom: start_services.bat
) else if %FRONTEND_RUNNING%==1 (
    echo   Status: CZESCIOWO URUCHOMIONE
    echo.
    echo   Backend jest zatrzymany
    echo   Uruchom: start_services.bat
) else (
    echo   Status: WSZYSTKO ZATRZYMANE
    echo.
    echo Uruchom serwisy:
    echo   start_services.bat
)

echo ========================================
echo.
pause
