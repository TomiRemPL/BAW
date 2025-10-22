# BAW - Projekt Porównywania Dokumentów Bankowych

Kompleksowy system do porównywania dokumentów bankowych w formacie DOCX składający się z dwóch komponentów:

## 📦 Komponenty Projektu

### 1. **SecureDocCompare** - Bezpieczny Frontend
**Port:** 8000
**Lokalizacja:** `SecureDocCompare/`

Bezpieczny interfejs webowy z:
- 🔐 Systemem logowania (hasło + sesje)
- 📤 Formularzem do uploadu dokumentów
- ⚙️ Interfejsem do uruchamiania analiz
- 📊 Wyświetlaniem wyników w formacie JSON
- 🛡️ 5 warstwami zabezpieczeń (auth, rate limiting, walidacja plików, bezpieczne nagłówki, path safety)

**Szczegóły:** Zobacz `SecureDocCompare/README.md`

### 2. **UslugaDoPorownan** - Backend API
**Port:** 8001
**Lokalizacja:** `UslugaDoPorownan/`

Usługa REST API do przetwarzania dokumentów:
- 📄 Ekstrakcja treści z DOCX i PDF (automatyczna konwersja)
- 🔄 Porównywanie wersji dokumentów
- 📋 Zwracanie wyników w JSON (pełny, zmodyfikowane, dodane, usunięte)
- 💾 Przechowywanie w pamięci
- 🔀 Dwupoziomowy system konwersji PDF→DOCX (pdf2docx + pdfplumber fallback)

**Szczegóły:** Zobacz `UslugaDoPorownan/README.md`

## 🎯 Architektura

```
┌─────────────────────────────────────────────────────┐
│  Użytkownik                                         │
└─────────────────┬───────────────────────────────────┘
                  │ HTTP (przeglądarka)
                  ▼
┌─────────────────────────────────────────────────────┐
│  SecureDocCompare (Frontend) - Port 8000            │
│  - Logowanie                                        │
│  - Upload plików                                    │
│  - Wyświetlanie wyników                             │
└─────────────────┬───────────────────────────────────┘
                  │ HTTP API
                  ▼
┌─────────────────────────────────────────────────────┐
│  UslugaDoPorownan (Backend) - Port 8001             │
│  - Ekstrakcja DOCX                                  │
│  - Porównywanie                                     │
│  - Generowanie JSON                                 │
└─────────────────────────────────────────────────────┘
```

## 🚀 Wymagania

### Windows (Development)
- **Python:** 3.11.9
- **Package Manager:** `uv` lub `pip`
- **System:** Windows 10/11

### Debian/Linux (Production)
- **Python:** 3.11.9 (zainstalowany przez pyenv)
- **OS:** Debian 11+
- **Dostęp:** SSH do serwera

## 📥 Instalacja

### Windows (Development)

```bash
# 1. Sprawdź wersję Pythona
python --version  # Powinno być 3.11.9

# 2. Przejdź do katalogu projektu
cd c:/Projects/BAW

# 3. Stwórz środowisko wirtualne
python -m venv .venv

# 4. Aktywuj środowisko
.venv\Scripts\activate  # Windows CMD
# lub
.\.venv\Scripts\Activate.ps1  # PowerShell

# 5. Zainstaluj zależności
pip install -r requirements.txt

# 6. Gotowe!
```

### Debian/Linux (Production)

**Zobacz szczegółowe instrukcje:** `DEPLOYMENT.md`

Krótka wersja:
```bash
# 1. Zainstaluj pyenv i Python 3.11.9
curl https://pyenv.run | bash
pyenv install 3.11.9
pyenv global 3.11.9

# 2. Stwórz środowisko
cd /home/debian/hack/BAW
python -m venv .venv
source .venv/bin/activate

# 3. Zainstaluj zależności
pip install -r requirements.txt
```

## 🎮 Uruchomienie

### Development (Windows)

**Terminal 1 - Backend:**
```bash
cd c:/Projects/BAW
.venv\Scripts\activate
cd UslugaDoPorownan
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Frontend:**
```bash
cd c:/Projects/BAW
.venv\Scripts\activate
cd SecureDocCompare
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production (Debian)

**Terminal 1 - Backend:**
```bash
cd /home/debian/hack/BAW
source .venv/bin/activate
cd UslugaDoPorownan
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Frontend:**
```bash
cd /home/debian/hack/BAW
source .venv/bin/activate
cd SecureDocCompare
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🌐 Dostęp

Po uruchomieniu obu serwisów:

- **Frontend:** http://localhost:8000
- **Backend API:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs

### Pierwsze logowanie

**Hasło domyślne:** `SecurePassword123!`

⚠️ **WAŻNE:** Zmień hasło w pliku `SecureDocCompare/.env`:
```env
APP_PASSWORD=TwojeNoweSuperbezpieczneHaslo
```

## 📚 Dokumentacja

| Plik | Opis |
|------|------|
| `README.md` | Ten plik - ogólny opis projektu |
| `DEPLOYMENT.md` | Instrukcje wdrożenia na serwer Debian |
| `requirements.txt` | Wszystkie zależności Python |
| `SecureDocCompare/README.md` | Dokumentacja frontendu |
| `SecureDocCompare/QUICK_START.md` | Szybki start frontendu |
| `SecureDocCompare/SECURITY.md` | Opis zabezpieczeń |
| `UslugaDoPorownan/README.md` | Dokumentacja API backendu |
| `UslugaDoPorownan/QUICKSTART.md` | Szybki start backendu |

## 🔧 Konfiguracja

### SecureDocCompare (.env)

```env
# Hasło dostępu
APP_PASSWORD=TwojeHaslo

# URL do API
DOCUMENT_API_URL=http://localhost:8001

# Port aplikacji
APP_PORT=8000

# Tryb produkcyjny
PRODUCTION=false
```

### Wspólne zależności

Wszystkie zależności są w głównym `requirements.txt`:
- FastAPI, Uvicorn - framework webowy
- Pydantic - walidacja danych
- httpx - HTTP client
- Jinja2 - templating
- docx2python - przetwarzanie DOCX
- fast-diff-match-patch - algorytm diff

## 📁 Struktura Projektu

```
BAW/
├── README.md                    # Ten plik
├── DEPLOYMENT.md                # Instrukcje wdrożenia
├── requirements.txt             # Wspólne zależności
├── .venv/                       # Środowisko wirtualne (wspólne)
├── CLAUDE.md                    # Instrukcje dla Claude Code
│
├── SecureDocCompare/            # Frontend (Port 8000)
│   ├── main.py                  # Aplikacja FastAPI
│   ├── config.py                # Konfiguracja
│   ├── auth.py                  # System autentykacji
│   ├── middleware.py            # Zabezpieczenia
│   ├── templates/               # Szablony HTML
│   ├── static/                  # CSS, JS
│   ├── .env                     # Konfiguracja (NIE commituj!)
│   ├── README.md
│   ├── QUICK_START.md
│   └── SECURITY.md
│
└── UslugaDoPorownan/            # Backend API (Port 8001)
    ├── main.py                  # API FastAPI
    ├── models.py                # Modele danych
    ├── extractor.py             # Ekstrakcja DOCX
    ├── comparator.py            # Algorytm porównywania
    ├── storage.py               # Przechowywanie
    ├── uploads/                 # Uploadowane pliki
    └── README.md
```

## 🧪 Testowanie

### Test API backendu:

```bash
# Health check
curl http://localhost:8001/health

# Upload dokumentów
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@stary.docx" \
  -F "new_document=@nowy.docx"
```

### Test frontendu:

1. Otwórz http://localhost:8000
2. Zaloguj się hasłem
3. Wybierz dwa pliki DOCX
4. Kliknij "Wgraj dokumenty"
5. Kliknij "Rozpocznij analizę"
6. Pobierz wyniki

## 🐛 Rozwiązywanie Problemów

### Port jest zajęty

```bash
# Sprawdź co zajmuje port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux

# Użyj innego portu
uvicorn main:app --port 8002
```

### ModuleNotFoundError

```bash
# Upewnij się że środowisko jest aktywowane
source .venv/bin/activate  # Linux
.venv\Scripts\activate      # Windows

# Zainstaluj ponownie zależności
pip install -r requirements.txt
```

### "Connection refused" do API

Upewnij się, że UslugaDoPorownan (backend) działa na porcie 8001:
```bash
curl http://localhost:8001/health
```

## 🔒 Bezpieczeństwo

### Dla Development
- Użyj silnych haseł w `.env`
- Nie commituj pliku `.env` do git
- HTTPS nie jest wymagane (localhost)

### Dla Production
- ✅ Zmień domyślne hasło
- ✅ Wygeneruj SECRET_KEY
- ✅ Ustaw `PRODUCTION=true`
- ✅ Skonfiguruj HTTPS (nginx + Let's Encrypt)
- ✅ Skonfiguruj firewall
- ✅ Używaj systemd do auto-startu

**Zobacz:** `DEPLOYMENT.md` i `SecureDocCompare/SECURITY.md`

## 📈 Wydajność

- Przetwarzanie sekwencyjne (1 para dokumentów na raz)
- Przechowywanie w pamięci (brak bazy danych)
- Optymalne dla dokumentów do 50 stron
- Szybkość: ~30 sekund na parę dokumentów 50-stron

## 🛠️ Development

### Dodawanie funkcji:
1. Backend: Edytuj `UslugaDoPorownan/main.py` i dodaj endpoint
2. Frontend: Edytuj `SecureDocCompare/main.py` i `templates/`
3. Testuj lokalnie
4. Wdróż na serwer

### Struktura commitów:
```bash
git add .
git commit -m "feat: opis nowej funkcji"
git push
```

## 📞 Wsparcie

- **Dokumentacja:** Pliki `.md` w katalogach projektu
- **Issues:** Zgłaszaj problemy przez GitHub Issues
- **Development:** Używaj Claude Code dla pomocy

## 📄 Licencja

Wewnętrzny projekt - wszystkie prawa zastrzeżone.

## 👥 Autorzy

Projekt stworzony przez TomiRemPL z pomocą Claude Code.

---

**Wersja:** 1.0.0
**Ostatnia aktualizacja:** 2025-10-21
**Python:** 3.11.9
**Status:** ✅ Production Ready
