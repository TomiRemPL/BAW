# 📄 Dokumentacja Endpointu Generowania Raportów HTML

**Wersja:** 1.0.0
**Data:** 2025-10-23
**Status:** ✅ Gotowy do użycia w produkcji

---

## 📋 Spis Treści

1. [Przegląd](#przegląd)
2. [Endpoint API](#endpoint-api)
3. [Przykłady użycia](#przykłady-użycia)
4. [Struktura odpowiedzi](#struktura-odpowiedzi)
5. [Funkcjonalności raportu](#funkcjonalności-raportu)
6. [Integracja z workflow](#integracja-z-workflow)
7. [Dostęp do raportów](#dostęp-do-raportów)
8. [Troubleshooting](#troubleshooting)
9. [Zaawansowane użycie](#zaawansowane-użycie)

---

## 🎯 Przegląd

Endpoint `/api/report/{process_id}/generate` umożliwia generowanie statycznych raportów HTML z wynikami porównania dokumentów. Raporty zawierają osadzone dane JSON i działają w trybie offline (bez potrzeby serwera).

### Kluczowe funkcjonalności

- ✅ **Statyczne pliki HTML** - jeden plik zawiera wszystko (HTML + CSS + JS + JSON)
- ✅ **Offline viewing** - działa bez serwera i internetu
- ✅ **Auto-display** - automatyczne wyświetlanie wyników po załadowaniu
- ✅ **Responsive design** - działa na desktopie, tablecie i mobile
- ✅ **Print-ready** - stylizacja dla druku
- ✅ **Wszystkie funkcje viewera** - filtry, summary, hover effects

### Use cases

1. **Archiwizacja wyników** - zapisz raport HTML jako trwałą dokumentację
2. **Udostępnianie offline** - wyślij plik HTML przez email
3. **Prezentacje** - otwórz raport bezpośrednio w przeglądarce
4. **Backup** - alternatywny sposób przechowywania wyników (oprócz JSON)
5. **Integracja z systemami** - automatyczne generowanie raportów w workflow

---

## 🔌 Endpoint API

### GET /api/report/{process_id}/generate

Generuje statyczny raport HTML na podstawie wyników procesu porównywania.

#### Parametry

| Parametr | Typ | Lokalizacja | Wymagany | Opis |
|----------|-----|-------------|----------|------|
| `process_id` | string (UUID) | Path | ✅ Tak | ID procesu porównywania |

#### Request

```http
GET /api/report/{process_id}/generate HTTP/1.1
Host: localhost:8001
```

#### Response - Sukces (200 OK)

```json
{
  "success": true,
  "process_id": "6b36eade-d0c8-43fa-832d-a307bdb09979",
  "report_url": "/reports/report_6b36eade-d0c8-43fa-832d-a307bdb09979_20251023_231438.html",
  "report_filename": "report_6b36eade-d0c8-43fa-832d-a307bdb09979_20251023_231438.html",
  "report_path": "C:\\Projects\\BAW\\UslugaDoPorownan\\output\\reports\\report_6b36eade-d0c8-43fa-832d-a307bdb09979_20251023_231438.html",
  "generated_at": "2025-10-23T23:14:38.123456",
  "message": "Raport HTML został wygenerowany pomyślnie"
}
```

#### Response - Błąd (404 Not Found)

```json
{
  "detail": "Nie znaleziono wyników dla process_id: {process_id}"
}
```

#### Response Fields

| Pole | Typ | Opis |
|------|-----|------|
| `success` | boolean | Czy operacja zakończyła się sukcesem |
| `process_id` | string | ID procesu |
| `report_url` | string | Relatywny URL do raportu (do użycia z API) |
| `report_filename` | string | Nazwa pliku HTML |
| `report_path` | string | Pełna ścieżka do pliku na serwerze |
| `generated_at` | string (ISO 8601) | Timestamp generowania |
| `message` | string | Komunikat tekstowy |

---

## 💻 Przykłady użycia

### cURL

```bash
# Generowanie raportu
curl -X GET http://localhost:8001/api/report/6b36eade-d0c8-43fa-832d-a307bdb09979/generate

# Odpowiedź (json)
{
  "success": true,
  "report_url": "/reports/report_6b36eade-d0c8-43fa-832d-a307bdb09979_20251023_231438.html",
  ...
}

# Dostęp do wygenerowanego raportu
curl http://localhost:8001/reports/report_6b36eade-d0c8-43fa-832d-a307bdb09979_20251023_231438.html
```

### Python + requests

```python
import requests

# Generuj raport
process_id = "6b36eade-d0c8-43fa-832d-a307bdb09979"
response = requests.get(f"http://localhost:8001/api/report/{process_id}/generate")

if response.status_code == 200:
    data = response.json()
    print(f"✅ Raport wygenerowany: {data['report_url']}")

    # Pobierz HTML
    report_url = f"http://localhost:8001{data['report_url']}"
    html_response = requests.get(report_url)

    # Zapisz lokalnie
    with open('raport.html', 'w', encoding='utf-8') as f:
        f.write(html_response.text)
    print("✅ Raport zapisany jako raport.html")
else:
    print(f"❌ Błąd: {response.status_code}")
```

### Python + httpx (async)

```python
import httpx
import asyncio

async def generate_report(process_id: str):
    async with httpx.AsyncClient() as client:
        # Generuj raport
        response = await client.get(
            f"http://localhost:8001/api/report/{process_id}/generate"
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Raport URL: {data['report_url']}")

            # Pobierz HTML
            html_response = await client.get(
                f"http://localhost:8001{data['report_url']}"
            )

            # Zapisz
            with open('raport.html', 'w', encoding='utf-8') as f:
                f.write(html_response.text)

            return data
        else:
            raise Exception(f"Błąd {response.status_code}: {response.text}")

# Użycie
asyncio.run(generate_report("6b36eade-d0c8-43fa-832d-a307bdb09979"))
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');
const fs = require('fs');

async function generateReport(processId) {
    try {
        // Generuj raport
        const response = await axios.get(
            `http://localhost:8001/api/report/${processId}/generate`
        );

        console.log(`✅ Raport wygenerowany: ${response.data.report_url}`);

        // Pobierz HTML
        const reportUrl = `http://localhost:8001${response.data.report_url}`;
        const htmlResponse = await axios.get(reportUrl);

        // Zapisz
        fs.writeFileSync('raport.html', htmlResponse.data, 'utf-8');
        console.log('✅ Raport zapisany jako raport.html');

        return response.data;
    } catch (error) {
        console.error(`❌ Błąd: ${error.message}`);
        throw error;
    }
}

// Użycie
generateReport('6b36eade-d0c8-43fa-832d-a307bdb09979');
```

### REST Client (VSCode)

Dodaj do pliku `test.http`:

```http
### Generowanie raportu HTML
GET http://localhost:8001/api/report/{{process_id}}/generate

### Pobierz wygenerowany raport
GET http://localhost:8001/reports/report_{{process_id}}_{{timestamp}}.html
```

---

## 📦 Struktura odpowiedzi

### Success Response (200 OK)

```typescript
interface GenerateReportResponse {
  success: boolean;              // true
  process_id: string;            // UUID procesu
  report_url: string;            // "/reports/report_{process_id}_{timestamp}.html"
  report_filename: string;       // "report_{process_id}_{timestamp}.html"
  report_path: string;           // Pełna ścieżka na serwerze
  generated_at: string;          // ISO 8601 timestamp
  message: string;               // "Raport HTML został wygenerowany pomyślnie"
}
```

### Error Responses

#### 404 Not Found - Brak wyników

```json
{
  "detail": "Nie znaleziono wyników dla process_id: abc123"
}
```

**Przyczyny:**
- Nieprawidłowy `process_id`
- Proces nie istnieje w storage
- Proces nie został jeszcze zakończony

#### 500 Internal Server Error - Błąd serwera

```json
{
  "detail": "Błąd podczas generowania raportu: {error_message}"
}
```

**Przyczyny:**
- Błąd zapisu pliku (brak uprawnień, brak miejsca)
- Błąd odczytu template HTML
- Błąd serializacji JSON

---

## 🎨 Funkcjonalności raportu

Wygenerowany raport HTML zawiera wszystkie funkcje offline viewera:

### 1. Summary Box

- Metryki: Total Changes, Modified, Added, Deleted
- Gradient w kolorach bankowych
- Procent zmian

### 2. Metadata

- Process ID
- Document Pair ID
- Generated At
- Total Paragraphs
- Pełne statystyki

### 3. Statistics Cards

6 kart z hover effects:
- Total Paragraphs
- Unchanged
- Modified
- Added
- Deleted
- Total Changes

### 4. Filtry interaktywne

- Wszystkie (domyślny)
- Zmodyfikowane
- Dodane
- Usunięte
- Niezmienione

### 5. Lista paragrafów

- Numer paragrafu
- Status (badge kolorowy)
- Stary tekst (jeśli istnieje)
- Nowy tekst (jeśli istnieje)
- Highlight zmian (insert/delete)

### 6. Tabele

- Wyświetlanie zmodyfikowanych tabel
- Highlight zmienionych komórek
- Row/Col index

### 7. Responsive Design

- Desktop (1920x1080+)
- Tablet (768-1919px)
- Mobile (< 768px)

### 8. Print-ready

- Auto-hide controls przy drukowaniu
- Optymalizacja dla A4
- Zachowanie kolorów

---

## 🔄 Integracja z workflow

### Kompletny workflow porównywania dokumentów

```
1. Upload dokumentów
   POST /api/documents/upload
   ↓
2. Rozpocznij porównanie
   POST /api/process
   ↓
3. Polling statusu (loop)
   GET /api/status/{process_id}
   ↓
4. Pobierz wynik JSON
   GET /api/result/{process_id}/full
   ↓
5. ✨ Wygeneruj raport HTML
   GET /api/report/{process_id}/generate
   ↓
6. Udostępnij lub pobierz raport
   GET /reports/{filename}
```

### Przykład - Python workflow

```python
import requests
import time

def complete_workflow(old_doc_path: str, new_doc_path: str):
    """Kompletny workflow z generowaniem raportu HTML."""

    base_url = "http://localhost:8001"

    # 1. Upload dokumentów
    print("1️⃣ Upload dokumentów...")
    with open(old_doc_path, 'rb') as old_f, open(new_doc_path, 'rb') as new_f:
        files = {
            'old_document': old_f,
            'new_document': new_f
        }
        upload_resp = requests.post(f"{base_url}/api/documents/upload", files=files)

    old_id = upload_resp.json()['old_document_id']
    new_id = upload_resp.json()['new_document_id']
    print(f"✅ Dokumenty wgrane: {old_id}, {new_id}")

    # 2. Rozpocznij porównanie
    print("2️⃣ Rozpoczynam porównanie...")
    process_resp = requests.post(
        f"{base_url}/api/process",
        json={'old_doc_id': old_id, 'new_doc_id': new_id}
    )
    process_id = process_resp.json()['process_id']
    print(f"✅ Process ID: {process_id}")

    # 3. Polling statusu
    print("3️⃣ Polling statusu...")
    while True:
        status_resp = requests.get(f"{base_url}/api/status/{process_id}")
        status_data = status_resp.json()

        if status_data['status'] == 'completed':
            print("✅ Porównanie zakończone!")
            break
        elif status_data['status'] == 'failed':
            print(f"❌ Błąd: {status_data['message']}")
            return None

        print(f"⏳ Status: {status_data['progress']}%")
        time.sleep(2)

    # 4. Pobierz wynik JSON
    print("4️⃣ Pobieram wynik JSON...")
    result_resp = requests.get(f"{base_url}/api/result/{process_id}/full")
    result_json = result_resp.json()
    print(f"✅ Wynik: {result_json['statistics']['total_changes']} zmian")

    # 5. ✨ Wygeneruj raport HTML
    print("5️⃣ Generuję raport HTML...")
    report_resp = requests.get(f"{base_url}/api/report/{process_id}/generate")
    report_data = report_resp.json()
    print(f"✅ Raport URL: {report_data['report_url']}")

    # 6. Pobierz raport HTML
    print("6️⃣ Pobieram raport HTML...")
    html_resp = requests.get(f"{base_url}{report_data['report_url']}")

    # Zapisz lokalnie
    local_filename = f"report_{process_id}.html"
    with open(local_filename, 'w', encoding='utf-8') as f:
        f.write(html_resp.text)

    print(f"✅ Raport zapisany jako: {local_filename}")
    print(f"🌐 Online URL: {base_url}{report_data['report_url']}")

    return {
        'process_id': process_id,
        'report_url': report_data['report_url'],
        'local_file': local_filename,
        'statistics': result_json['statistics']
    }

# Użycie
result = complete_workflow('old.docx', 'new.docx')
```

---

## 🌐 Dostęp do raportów

### 1. Przez API (Online)

```bash
# Lokalnie
http://localhost:8001/reports/report_{process_id}_{timestamp}.html

# Produkcyjnie
http://217.182.76.146/reports/report_{process_id}_{timestamp}.html
```

### 2. Bezpośrednio (Offline)

```bash
# Windows
start C:\Projects\BAW\UslugaDoPorownan\output\reports\report_{process_id}_{timestamp}.html

# Linux/Mac
open /path/to/BAW/UslugaDoPorownan/output/reports/report_{process_id}_{timestamp}.html
```

### 3. StaticFiles mount

Raporty są serwowane przez FastAPI StaticFiles:

```python
# UslugaDoPorownan/main.py
from fastapi.staticfiles import StaticFiles

REPORTS_DIR = Path("output/reports")
app.mount("/reports", StaticFiles(directory=str(REPORTS_DIR)), name="reports")
```

### 4. Struktura katalogów

```
UslugaDoPorownan/
└── output/
    └── reports/
        ├── report_6b36eade-d0c8-43fa-832d-a307bdb09979_20251023_231438.html
        ├── report_abc12345-6789-0def-ghij-klmnopqrstuv_20251023_232156.html
        └── ...
```

---

## 🔧 Troubleshooting

### Problem 1: 404 Not Found

**Objaw:**
```json
{"detail": "Nie znaleziono wyników dla process_id: abc123"}
```

**Rozwiązanie:**
1. Sprawdź czy `process_id` jest poprawny
2. Sprawdź status procesu: `GET /api/status/{process_id}`
3. Upewnij się że proces zakończył się sukcesem
4. Sprawdź czy wyniki istnieją: `GET /api/result/{process_id}/full`

### Problem 2: Raport nie ładuje się

**Objaw:** Przeglądarka wyświetla pusty ekran lub błąd

**Rozwiązanie:**
1. Sprawdź czy plik HTML istnieje:
   ```bash
   ls output/reports/report_{process_id}_{timestamp}.html
   ```
2. Sprawdź czy plik zawiera dane:
   ```bash
   wc -l output/reports/report_{process_id}_{timestamp}.html
   # Powinno być > 900 linii
   ```
3. Sprawdź Console w DevTools (F12) przeglądarki
4. Sprawdź logi backendu:
   ```bash
   tail -f output/app.log | grep "generate_html_report"
   ```

### Problem 3: StaticFiles 404

**Objaw:** `http://localhost:8001/reports/{filename}` zwraca 404

**Rozwiązanie:**
1. Sprawdź czy katalog `output/reports/` istnieje:
   ```bash
   mkdir -p output/reports
   ```
2. Sprawdź uprawnienia do katalogu:
   ```bash
   chmod 755 output/reports
   ```
3. Zrestartuj backend:
   ```bash
   pkill -f "uvicorn main:app"
   uvicorn main:app --port 8001
   ```
4. Sprawdź czy StaticFiles jest zamontowany:
   ```bash
   curl http://localhost:8001/openapi.json | grep "/reports"
   ```

### Problem 4: Raport bez danych

**Objaw:** Raport HTML otwiera się ale nie wyświetla danych

**Rozwiązanie:**
1. Sprawdź czy JSON jest osadzony w HTML:
   ```bash
   grep "let fullData = " output/reports/report_{process_id}_{timestamp}.html
   ```
   Powinno pokazać: `let fullData = {` (nie `let fullData = null;`)

2. Sprawdź czy auto-display jest dodany:
   ```bash
   grep "DOMContentLoaded" output/reports/report_{process_id}_{timestamp}.html
   ```

3. Jeśli brak, wygeneruj raport ponownie:
   ```bash
   curl http://localhost:8001/api/report/{process_id}/generate
   ```

### Problem 5: Timeout

**Objaw:** Request timeout po 30-60s

**Rozwiązanie:**
1. Zwiększ timeout w kliencie HTTP:
   ```python
   # Python requests
   response = requests.get(url, timeout=120)

   # Python httpx
   async with httpx.AsyncClient(timeout=120.0) as client:
       response = await client.get(url)
   ```

2. Sprawdź czy proces się nie zawiesił:
   ```bash
   curl http://localhost:8001/api/status/{process_id}
   ```

---

## 🚀 Zaawansowane użycie

### 1. Bulk generation (wiele raportów)

```python
def generate_multiple_reports(process_ids: list[str]) -> list[dict]:
    """Generuj wiele raportów równolegle."""
    import concurrent.futures

    def generate_one(process_id: str) -> dict:
        response = requests.get(
            f"http://localhost:8001/api/report/{process_id}/generate"
        )
        return response.json()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(generate_one, pid) for pid in process_ids]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    return results

# Użycie
process_ids = ["id1", "id2", "id3", "id4", "id5"]
reports = generate_multiple_reports(process_ids)
print(f"✅ Wygenerowano {len(reports)} raportów")
```

### 2. Auto-cleanup (usuwanie starych raportów)

```python
from pathlib import Path
from datetime import datetime, timedelta

def cleanup_old_reports(days_old: int = 7):
    """Usuń raporty starsze niż X dni."""
    reports_dir = Path("output/reports")
    cutoff_time = datetime.now() - timedelta(days=days_old)

    removed = 0
    for report_file in reports_dir.glob("report_*.html"):
        file_time = datetime.fromtimestamp(report_file.stat().st_mtime)

        if file_time < cutoff_time:
            report_file.unlink()
            removed += 1
            print(f"🗑️ Usunięto: {report_file.name}")

    print(f"✅ Usunięto {removed} starych raportów")

# Użycie
cleanup_old_reports(days_old=7)  # Usuń raporty starsze niż 7 dni
```

### 3. Integracja z N8N

Dodaj node do workflow N8N:

```json
{
  "parameters": {
    "url": "http://217.182.76.146/api/report/{{$json[\"process_id\"]}}/generate",
    "method": "GET",
    "options": {
      "timeout": 60000
    }
  },
  "name": "Generate HTML Report",
  "type": "n8n-nodes-base.httpRequest",
  "position": [1200, 400]
}
```

Następnie dodaj node zapisujący do Dropbox:

```json
{
  "parameters": {
    "resource": "file",
    "operation": "upload",
    "path": "/Reports/{{$json[\"report_filename\"]}}",
    "binaryData": true,
    "options": {}
  },
  "name": "Save to Dropbox",
  "type": "n8n-nodes-base.dropbox"
}
```

### 4. Email integration

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def email_report(process_id: str, recipient_email: str):
    """Wygeneruj raport i wyślij przez email."""

    # Wygeneruj raport
    response = requests.get(
        f"http://localhost:8001/api/report/{process_id}/generate"
    )
    report_data = response.json()

    # Pobierz HTML
    html_response = requests.get(
        f"http://localhost:8001{report_data['report_url']}"
    )

    # Przygotuj email
    msg = MIMEMultipart()
    msg['From'] = 'noreply@example.com'
    msg['To'] = recipient_email
    msg['Subject'] = f"Raport porównania dokumentów - {process_id}"

    # Body
    body = f"""
    Witaj,

    Raport porównania dokumentów został wygenerowany.

    Process ID: {process_id}
    Data: {report_data['generated_at']}

    W załączniku znajdziesz interaktywny raport HTML.
    Otwórz go w przeglądarce aby zobaczyć szczegóły.

    Pozdrawiam,
    System BAW
    """
    msg.attach(MIMEText(body, 'plain'))

    # Załącznik HTML
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(html_response.content)
    encoders.encode_base64(attachment)
    attachment.add_header(
        'Content-Disposition',
        f'attachment; filename= {report_data["report_filename"]}'
    )
    msg.attach(attachment)

    # Wyślij
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    server.send_message(msg)
    server.quit()

    print(f"✅ Email wysłany do: {recipient_email}")

# Użycie
email_report(
    process_id="6b36eade-d0c8-43fa-832d-a307bdb09979",
    recipient_email="user@example.com"
)
```

---

## 📚 Powiązane dokumenty

- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Kompletna dokumentacja wszystkich endpointów API
- [UslugaDoPorownan/README.md](UslugaDoPorownan/README.md) - Dokumentacja backendu API
- [N8N_INTEGRATION.md](N8N_INTEGRATION.md) - Integracja z N8N workflow
- [PROGRESS_LOG.md](PROGRESS_LOG.md) - Historia rozwoju projektu

---

## ✅ Podsumowanie

### Zalety endpointu

- ✅ Proste API (GET request)
- ✅ Jeden plik HTML zawiera wszystko
- ✅ Działa offline
- ✅ Responsive i print-ready
- ✅ Łatwa integracja z workflow
- ✅ Automatyczna archiwizacja

### Typowe zastosowania

1. **Archiwizacja** - długoterminowe przechowywanie wyników
2. **Udostępnianie** - wysyłanie raportów przez email
3. **Prezentacje** - pokazywanie wyników offline
4. **Backup** - dodatkowa kopia danych (oprócz JSON)
5. **Automation** - automatyczne generowanie w N8N/CI/CD

### Następne kroki

- Zintegruj endpoint z N8N workflow
- Dodaj automatyczne cleanup starych raportów
- Skonfiguruj email notifications z załącznikiem HTML
- Rozważ archiwizację w cloud storage (S3, Dropbox)

---

**Dokumentacja zakończona:** 2025-10-23
**Autor:** TomiRemPL + Claude Code (Anthropic)
**Wersja:** 1.0.0
**Status:** ✅ Production Ready
