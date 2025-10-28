@echo off
REM Stop Services - Batch Script
REM Zatrzymuje UslugaDoPorownan i SecureDocCompare

echo ========================================
echo   Zatrzymywanie serwisow BAW
echo ========================================
echo.

echo Wyszukiwanie procesow uvicorn...
echo.

REM Znajdź procesy na portach 8000 i 8001
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001.*LISTENING"') do (
    set PID_8001=%%a
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING"') do (
    set PID_8000=%%a
)

if "%PID_8001%"=="" if "%PID_8000%"=="" (
    echo Nie znaleziono uruchomionych serwisow
    echo.
    pause
    exit /b 0
)

if not "%PID_8001%"=="" (
    echo Znaleziono Backend ^(Port 8001^):
    echo   PID: %PID_8001%
    echo.
)

if not "%PID_8000%"=="" (
    echo Znaleziono Frontend ^(Port 8000^):
    echo   PID: %PID_8000%
    echo.
)

set /p CONFIRM="Zatrzymac serwisy? (t/n): "
if /i not "%CONFIRM%"=="t" (
    echo Anulowano
    pause
    exit /b 0
)

echo.
echo Zatrzymywanie procesow...
echo.

if not "%PID_8001%"=="" (
    echo Zatrzymuje Backend (PID %PID_8001%)...
    taskkill /F /PID %PID_8001% >nul 2>&1
    if errorlevel 1 (
        echo   BLAD: Nie udalo sie zatrzymac procesu
    ) else (
        echo   OK
    )
)

if not "%PID_8000%"=="" (
    echo Zatrzymuje Frontend (PID %PID_8000%)...
    taskkill /F /PID %PID_8000% >nul 2>&1
    if errorlevel 1 (
        echo   BLAD: Nie udalo sie zatrzymac procesu
    ) else (
        echo   OK
    )
)

echo.
echo Serwisy zatrzymane
echo.
pause
