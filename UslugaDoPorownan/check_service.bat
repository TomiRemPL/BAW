@echo off
REM Skrypt do sprawdzania statusu uslugi

curl -s http://localhost:8001/health
if %errorlevel% equ 0 (
    exit /b 0
) else (
    echo {"status":"stopped"}
    exit /b 1
)
