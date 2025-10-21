# Secure Document Compare

Bezpieczny interfejs webowy do porównywania dokumentów DOCX z wbudowanymi mechanizmami zabezpieczeń.

## 🔒 Zabezpieczenia

Aplikacja implementuje pięć warstw zabezpieczeń:

1. **Autentykacja** - Prosty system logowania z hasłem
2. **Walidacja plików** - Sprawdzanie typu i rozmiaru plików
3. **Rate limiting** - Ochrona przed atakami DoS
4. **Bezpieczne nagłówki HTTP** - CSP, X-Frame-Options, etc.
5. **Walidacja ścieżek** - Ochrona przed path traversal

## 📋 Wymagania

- Python 3.11+
- Uruchomiona usługa porównywania dokumentów (UslugaDoPorownan) na porcie 8001

## 🚀 Instalacja

1. Sklonuj repozytorium lub skopiuj pliki

2. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

3. Skopiuj i dostosuj konfigurację:
```bash
cp .env.example .env
```

4. Edytuj plik `.env` i ustaw własne wartości:
```env
APP_PASSWORD=TwojeSuperbezpieczneHaslo123!
SECRET_KEY=wygeneruj-tutaj-bardzo-dluga-losowa-sekwencje-znakow
DOCUMENT_API_URL=http://localhost:8001
APP_PORT=8000
```

**WAŻNE:** Koniecznie zmień domyślne hasło i wygeneruj unikalny SECRET_KEY!

## 🎯 Uruchomienie

1. Upewnij się, że usługa UslugaDoPorownan działa na porcie 8001

2. Uruchom aplikację:
```bash
python main.py
```

Lub używając uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3. Otwórz przeglądarkę: http://localhost:8000

## 💻 Użycie

1. **Logowanie** - Wprowadź hasło ustawione w pliku `.env`

2. **Upload dokumentów**
   - Wybierz starą wersję dokumentu (.docx)
   - Wybierz nową wersję dokumentu (.docx)
   - Kliknij "Wgraj dokumenty"

3. **Rozpocznij analizę**
   - Kliknij "Rozpocznij analizę"
   - Obserwuj postęp przetwarzania

4. **Pobierz wyniki**
   - Pełny dokument - kompletny wynik z wszystkimi zmianami
   - Zmodyfikowane - tylko zmienione fragmenty
   - Dodane - tylko nowe fragmenty
   - Usunięte - tylko usunięte fragmenty

5. **Pobierz lub kopiuj**
   - Pobierz wynik jako JSON
   - Skopiuj do schowka

## 🏗️ Architektura

```
SecureDocCompare/
├── main.py              # Główna aplikacja FastAPI
├── config.py            # Konfiguracja
├── auth.py              # System autentykacji
├── middleware.py        # Middleware zabezpieczający
├── templates/
│   ├── login.html       # Strona logowania
│   └── dashboard.html   # Dashboard użytkownika
├── static/
│   ├── css/
│   │   └── style.css    # Style CSS
│   └── js/
│       └── app.js       # JavaScript
├── .env                 # Konfiguracja (nie commituj!)
├── .env.example         # Przykładowa konfiguracja
├── requirements.txt     # Zależności Python
└── README.md           # Ten plik
```

## 🔐 Funkcje bezpieczeństwa

### 1. Autentykacja
- Prosty system logowania z hasłem
- Sesje z automatycznym wygasaniem (domyślnie 60 min)
- Hashowanie haseł (SHA-256)
- Ochrona przed timing attacks

### 2. Walidacja plików
- Tylko pliki .docx
- Limit rozmiaru: 50MB (konfigurowalne)
- Sprawdzanie Content-Type

### 3. Rate Limiting
- Limit: 20 requestów/minutę (konfigurowalne)
- Osobny licznik dla każdego IP
- Automatyczne czyszczenie starych wpisów

### 4. Bezpieczne nagłówki HTTP
- Content-Security-Policy
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection
- Strict-Transport-Security

### 5. Walidacja ścieżek
- Brak bezpośredniego dostępu do systemu plików
- Proxy do API backend
- Walidacja wszystkich parametrów

## 🛠️ Konfiguracja

### Zmienne środowiskowe (.env)

| Zmienna | Opis | Domyślna wartość |
|---------|------|------------------|
| `APP_PASSWORD` | Hasło dostępu | `changeme` |
| `SECRET_KEY` | Klucz sesji | losowy ciąg |
| `DOCUMENT_API_URL` | URL do API dokumentów | `http://localhost:8001` |
| `APP_PORT` | Port aplikacji | `8000` |
| `PRODUCTION` | Tryb produkcyjny | `false` |

### Limity bezpieczeństwa (config.py)

```python
max_file_size = 50 * 1024 * 1024  # 50MB
allowed_extensions = {".docx"}
max_requests_per_minute = 20
session_timeout_minutes = 60
```

## 📊 API Endpoints

| Endpoint | Metoda | Opis | Autentykacja |
|----------|--------|------|--------------|
| `/` | GET | Strona główna (login/dashboard) | Nie |
| `/api/login` | POST | Logowanie | Nie |
| `/api/logout` | POST | Wylogowanie | Tak |
| `/api/upload` | POST | Upload dokumentów | Tak |
| `/api/process/{id}` | POST | Rozpocznij porównanie | Tak |
| `/api/status/{id}` | GET | Status przetwarzania | Tak |
| `/api/result/{id}/full` | GET | Pełny wynik | Tak |
| `/api/result/{id}/modified` | GET | Zmodyfikowane | Tak |
| `/api/result/{id}/added` | GET | Dodane | Tak |
| `/api/result/{id}/deleted` | GET | Usunięte | Tak |
| `/health` | GET | Health check | Nie |

## 🚦 Integracja

Aplikacja komunikuje się z usługą UslugaDoPorownan poprzez HTTP API:

```
Secure Document Compare (port 8000)
          ↓ HTTP
UslugaDoPorownan (port 8001)
```

Wymagane endpointy w UslugaDoPorownan:
- `POST /api/documents/upload`
- `POST /api/process`
- `GET /api/status/{process_id}`
- `GET /api/result/{process_id}/full`
- `GET /api/result/{process_id}/modified`
- `GET /api/result/{process_id}/added`
- `GET /api/result/{process_id}/deleted`

## 🔧 Tryb produkcyjny

W trybie produkcyjnym:

1. Ustaw w `.env`:
```env
PRODUCTION=true
```

2. Wyłącza się dokumentacja API (/docs, /redoc)
3. Włącza się Secure cookies
4. Bardziej restrykcyjne nagłówki

## 📝 Changelog

### v1.0.0 (2025-10-20)
- Inicjalna wersja
- System logowania
- Upload i porównywanie dokumentów
- 5 warstw zabezpieczeń
- Responsywny interfejs

## 📄 Licencja

Wewnętrzny projekt - wszystkie prawa zastrzeżone.

## 🤝 Wsparcie

W razie problemów sprawdź:
1. Czy usługa UslugaDoPorownan działa na porcie 8001
2. Czy plik `.env` jest poprawnie skonfigurowany
3. Czy wszystkie zależności są zainstalowane
4. Logi w konsoli

## ⚠️ Ważne uwagi

- **Nie commituj pliku `.env`** - zawiera wrażliwe dane!
- **Zmień domyślne hasło** przed użyciem w produkcji
- **Wygeneruj unikalny SECRET_KEY** dla każdej instalacji
- Aplikacja jest zaprojektowana dla **lokalnego użytku**
- Dla dostępu przez Internet potrzebne są dodatkowe zabezpieczenia (HTTPS, firewall, etc.)
