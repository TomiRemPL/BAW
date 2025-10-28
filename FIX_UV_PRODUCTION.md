# 🔧 Naprawa Środowiska UV na Produkcji

## 🔍 Problem

```
ModuleNotFoundError: No module named 'pdf2docx'
```

Pakiety zainstalowane w globalnym pyenv zamiast w środowisku UV.

---

## ✅ Rozwiązanie (Krok po Kroku)

### Opcja 1: Reinstalacja w UV (ZALECANE)

```bash
# 1. Przejdź do głównego katalogu projektu
cd /home/debian/hack/BAW

# 2. Deaktywuj obecne środowisko (jeśli aktywne)
deactivate

# 3. Usuń stare środowisko UV (jeśli istnieje)
rm -rf .venv

# 4. Utwórz nowe środowisko UV
uv venv

# 5. Aktywuj środowisko UV
source .venv/bin/activate

# 6. Sprawdź ścieżkę Python (powinna być w .venv)
which python
# Powinno pokazać: /home/debian/hack/BAW/.venv/bin/python

# 7. Zainstaluj zależności przez UV
uv pip install -r requirements.txt

# 8. Zweryfikuj instalację
uv pip list | grep pdf2docx

# 9. Test uruchomienia
cd UslugaDoPorownan
python main.py
```

**Oczekiwany wynik:** Backend wystartuje bez błędów ModuleNotFoundError.

---

### Opcja 2: Synchronizacja UV z requirements.txt

Jeśli Opcja 1 nie zadziała:

```bash
cd /home/debian/hack/BAW

# Aktywuj środowisko UV (jeśli nie aktywne)
source .venv/bin/activate

# Synchronizuj wszystkie pakiety
uv pip sync requirements.txt

# Lub instaluj pojedynczo
uv pip install pdf2docx PyMuPDF python-docx fastapi uvicorn pydantic
```

---

### Opcja 3: Użyj uv run (Bez aktywacji venv)

```bash
cd /home/debian/hack/BAW/UslugaDoPorownan

# Uruchom przez UV (automatycznie używa .venv)
uv run uvicorn main:app --host 0.0.0.0 --port 8001
```

**Zaleta:** UV automatycznie znajdzie i użyje właściwego środowiska.

---

## 🔍 Diagnostyka

### Sprawdź które Python jest używane:

```bash
# Aktywuj środowisko
source /home/debian/hack/BAW/.venv/bin/activate

# Sprawdź ścieżkę
which python
echo $VIRTUAL_ENV

# Powinno pokazać:
# /home/debian/hack/BAW/.venv/bin/python
# /home/debian/hack/BAW/.venv
```

### Sprawdź zainstalowane pakiety:

```bash
# W środowisku UV
uv pip list

# Globalnie (pyenv)
pip list
```

Jeśli pakiety są tylko w `pip list` (globalnie), a nie w `uv pip list`, to problem jest potwierdzony.

---

## 🚀 Aktualizacja Skryptów Startowych

### Zaktualizuj start_services.sh

Edytuj plik:
```bash
nano /home/debian/hack/BAW/start_services.sh
```

Zmień linię uruchamiającą backend z:
```bash
$VENV_PYTHON -m uvicorn main:app --host 0.0.0.0 --port 8001
```

Na:
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8001
```

**Pełna zaktualizowana wersja:**

```bash
#!/bin/bash

# Kolory
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_ROOT="/home/debian/hack/BAW"
BACKEND_DIR="$PROJECT_ROOT/UslugaDoPorownan"
FRONTEND_DIR="$PROJECT_ROOT/SecureDocCompare"

echo -e "${GREEN}=== Uruchamianie usług BAW (UV mode) ===${NC}\n"

# Funkcja sprawdzająca czy screen istnieje
screen_exists() {
    screen -list | grep -q "$1"
}

# Funkcja sprawdzająca czy port jest zajęty
port_in_use() {
    ss -tuln | grep -q ":$1 "
}

# 1. Sprawdź czy UV jest zainstalowane
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ UV nie jest zainstalowane!${NC}"
    echo "Zainstaluj: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 2. Backend (port 8001)
echo -e "${YELLOW}📦 Backend (UslugaDoPorownan)...${NC}"

if screen_exists "baw-backend"; then
    echo -e "${YELLOW}⚠️  Screen baw-backend już istnieje${NC}"
else
    if port_in_use 8001; then
        echo -e "${RED}❌ Port 8001 jest zajęty${NC}"
        ss -tlnp | grep 8001
    else
        cd "$BACKEND_DIR"
        screen -dmS baw-backend bash -c "uv run uvicorn main:app --host 0.0.0.0 --port 8001"
        sleep 2
        echo -e "${GREEN}✅ Backend uruchomiony w screen: baw-backend${NC}"
    fi
fi

# 3. Frontend (port 8000)
echo -e "\n${YELLOW}🌐 Frontend (SecureDocCompare)...${NC}"

if screen_exists "baw-frontend"; then
    echo -e "${YELLOW}⚠️  Screen baw-frontend już istnieje${NC}"
else
    if port_in_use 8000; then
        echo -e "${RED}❌ Port 8000 jest zajęty${NC}"
        ss -tlnp | grep 8000
    else
        cd "$FRONTEND_DIR"
        screen -dmS baw-frontend bash -c "uv run uvicorn main:app --host 0.0.0.0 --port 8000"
        sleep 2
        echo -e "${GREEN}✅ Frontend uruchomiony w screen: baw-frontend${NC}"
    fi
fi

# 4. Podsumowanie
echo -e "\n${GREEN}=== Status ===${NC}"
screen -list

# 5. Health check
echo -e "\n${GREEN}=== Health Check ===${NC}"
sleep 3

echo -n "Backend (8001): "
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
fi

echo -n "Frontend (8000): "
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
fi

echo -e "\n${YELLOW}Podłącz się do sesji:${NC}"
echo "  screen -r baw-backend   # Backend logs"
echo "  screen -r baw-frontend  # Frontend logs"
echo -e "\n${YELLOW}Odłącz się: Ctrl+A, potem D${NC}"
```

---

## 🔄 Aktualizacja systemd (Opcjonalnie)

Jeśli używasz systemd zamiast screen:

```bash
sudo nano /etc/systemd/system/baw-backend.service
```

Zmień `ExecStart` na:
```ini
ExecStart=/home/debian/.local/bin/uv run uvicorn main:app --host 0.0.0.0 --port 8001
```

**Pełny plik:**
```ini
[Unit]
Description=BAW Backend API (UslugaDoPorownan) - UV mode
After=network.target

[Service]
Type=simple
User=debian
WorkingDirectory=/home/debian/hack/BAW/UslugaDoPorownan
Environment="PATH=/home/debian/.local/bin:/home/debian/.pyenv/shims:/usr/bin:/bin"
ExecStart=/home/debian/.local/bin/uv run uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Podobnie dla frontendu:
```bash
sudo nano /etc/systemd/system/baw-frontend.service
```

```ini
[Unit]
Description=BAW Frontend (SecureDocCompare) - UV mode
After=network.target baw-backend.service

[Service]
Type=simple
User=debian
WorkingDirectory=/home/debian/hack/BAW/SecureDocCompare
Environment="PATH=/home/debian/.local/bin:/home/debian/.pyenv/shims:/usr/bin:/bin"
EnvironmentFile=/home/debian/hack/BAW/SecureDocCompare/.env
ExecStart=/home/debian/.local/bin/uv run uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Przeładuj:
```bash
sudo systemctl daemon-reload
sudo systemctl restart baw-backend baw-frontend
```

---

## ✅ Weryfikacja

```bash
# 1. Sprawdź środowisko UV
cd /home/debian/hack/BAW
source .venv/bin/activate
which python
# Wynik: /home/debian/hack/BAW/.venv/bin/python

# 2. Sprawdź pakiety w UV
uv pip list | grep -E "pdf2docx|fastapi|uvicorn"

# 3. Test importu
cd UslugaDoPorownan
python -c "from pdf_converter import PDFConverter; print('OK')"

# 4. Uruchom backend
uv run uvicorn main:app --host 0.0.0.0 --port 8001

# 5. Test health check (w drugim terminalu)
curl http://localhost:8001/health
```

---

## 🐛 Troubleshooting

### Jeśli nadal nie działa:

**Problem 1: UV nie znalazł .venv**
```bash
# Sprawdź czy .venv istnieje
ls -la /home/debian/hack/BAW/.venv

# Jeśli nie istnieje, utwórz:
cd /home/debian/hack/BAW
uv venv
```

**Problem 2: requirements.txt nie zawiera pdf2docx**
```bash
# Sprawdź plik
cat requirements.txt | grep pdf2docx

# Jeśli nie ma, dodaj:
echo "pdf2docx>=0.5.8" >> requirements.txt
uv pip install -r requirements.txt
```

**Problem 3: Konflikt z pyenv**
```bash
# Tymczasowo wyłącz pyenv
export PATH="/usr/bin:/bin:$PATH"

# Sprawdź Python
which python

# Uruchom przez UV
uv run uvicorn main:app --host 0.0.0.0 --port 8001
```

---

## 📝 Podsumowanie

### Co zostało naprawione:
1. ✅ Środowisko UV prawidłowo skonfigurowane
2. ✅ Pakiety zainstalowane w `.venv` zamiast globalnie
3. ✅ Skrypty startowe używają `uv run`
4. ✅ Backend i Frontend działają przez UV

### Rekomendowane podejście:
- **Development (Windows):** venv z `pip`
- **Production (Debian):** UV z `uv run` lub `uv pip`

### Komendy produkcyjne:
```bash
# Start
cd /home/debian/hack/BAW
./start_services.sh

# Status
./status_services.sh

# Stop
./stop_services.sh

# Restart single service
screen -r baw-backend  # Ctrl+C → up arrow → Enter
```

---

**Data:** 2025-10-28
**Wersja:** 1.0.0
