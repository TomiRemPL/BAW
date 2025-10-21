@echo off
echo ========================================
echo Secure Document Compare - Start
echo ========================================
echo.

REM Sprawdź czy plik .env istnieje
if not exist .env (
    echo UWAGA: Brak pliku .env!
    echo Kopiuję .env.example do .env...
    copy .env.example .env
    echo.
    echo WAZNE: Edytuj plik .env i ustaw swoje haslo!
    echo.
    pause
)

echo Uruchamianie aplikacji...
echo.

REM Uruchom aplikację
python main.py

pause
