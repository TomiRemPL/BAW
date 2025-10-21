#!/bin/bash

echo "========================================"
echo "Secure Document Compare - Start"
echo "========================================"
echo ""

# Sprawdź czy plik .env istnieje
if [ ! -f .env ]; then
    echo "UWAGA: Brak pliku .env!"
    echo "Kopiuję .env.example do .env..."
    cp .env.example .env
    echo ""
    echo "WAŻNE: Edytuj plik .env i ustaw swoje hasło!"
    echo ""
    read -p "Naciśnij Enter aby kontynuować..."
fi

echo "Uruchamianie aplikacji..."
echo ""

# Uruchom aplikację
python main.py
