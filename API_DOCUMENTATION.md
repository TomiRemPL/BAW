# 📚 Dokumentacja API - UslugaDoPorownan

**Wersja:** 1.1.0
**Port:** 8001
**URL Base:** `http://localhost:8001`
**Format:** JSON
**Ostatnia aktualizacja:** 2025-10-23

---

## 📖 Spis Treści

1. [Podstawowe Informacje](#podstawowe-informacje)
2. [Lista Endpointów](#lista-endpointów)
3. [Przykładowy Workflow](#przykładowy-workflow)
4. [Testowanie w VSCode](#testowanie-w-vscode)
5. [Kody Błędów](#kody-błędów)
6. [Modele Danych](#modele-danych)

---

## 🔗 Podstawowe Informacje

- **URL Base:** `http://localhost:8001`
- **Format:** JSON (application/json)
- **Obsługiwane formaty dokumentów:** DOCX, PDF (automatyczna konwersja)
- **Timeout uploadu:** 120 sekund
- **Storage:** In-memory (dane tracone po restarcie)
- **Przetwarzanie:** Asynchroniczne w tle (FastAPI BackgroundTasks)

---

## 📋 Lista Endpointów

### 1. GET `/` - Informacje o serwisie

Zwraca podstawowe informacje o usłudze i dostępnych endpointach.

**Przykład curl:**
```bash
curl http://localhost:8001/
```

**Przykład HTTP:**
```http
GET http://localhost:8001/
Accept: application/json
```

**Odpowiedź (200 OK):**
```json
{
  "service": "Usługa Porównywania Dokumentów",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "upload": "POST /api/documents/upload",
    "process": "POST /api/process",
    "status": "GET /api/status/{process_id}",
    "full": "GET /api/result/{process_id}/full",
    "modified": "GET /api/result/{process_id}/modified",
    "added": "GET /api/result/{process_id}/added",
    "deleted": "GET /api/result/{process_id}/deleted",
    "generate_report": "GET /api/report/{process_id}/generate"
  }
}
```

---

### 2. GET `/health` - Health Check

Sprawdza stan usługi i zwraca statystyki przetwarzania.

**Przykład curl:**
```bash
curl http://localhost:8001/health
```

**Przykład HTTP:**
```http
GET http://localhost:8001/health
Accept: application/json
```

**Odpowiedź (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T10:30:45.123456",
  "statistics": {
    "total_documents": 10,
    "total_processes": 8,
    "completed_processes": 7,
    "failed_processes": 1
  }
}
```

---

### 3. POST `/api/documents/upload` - Upload dokumentów

Załaduj parę dokumentów (DOCX lub PDF) do porównania. Dokumenty PDF są automatycznie konwertowane do formatu DOCX.

**Parametry (multipart/form-data):**
- `old_document` (file, **required**) - Stary dokument (.docx lub .pdf)
- `new_document` (file, **required**) - Nowy dokument (.docx lub .pdf)

**Ograniczenia:**
- Maksymalny rozmiar: 50MB (konfigurowane w SecureDocCompare)
- Formaty: `.docx`, `.pdf`
- Timeout: 120s

#### Przykład 1: Upload DOCX

**curl:**
```bash
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@stara_wersja/dokument.docx" \
  -F "new_document=@nowa_wersja/dokument.docx"
```

**HTTP:**
```http
POST http://localhost:8001/api/documents/upload
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="old_document"; filename="old.docx"
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document

< ./stara_wersja/dokument.docx
------WebKitFormBoundary
Content-Disposition: form-data; name="new_document"; filename="new.docx"
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document

< ./nowa_wersja/dokument.docx
------WebKitFormBoundary--
```

**Odpowiedź (200 OK):**
```json
{
  "document_pair_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "uploaded",
  "message": "Dokumenty zostały załadowane: old.docx, new.docx"
}
```

#### Przykład 2: Upload PDF (z konwersją)

**curl:**
```bash
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@stara_wersja/dokument.pdf" \
  -F "new_document=@nowa_wersja/dokument.pdf"
```

**HTTP:**
```http
POST http://localhost:8001/api/documents/upload
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="old_document"; filename="old.pdf"
Content-Type: application/pdf

< ./stara_wersja/dokument.pdf
------WebKitFormBoundary
Content-Disposition: form-data; name="new_document"; filename="new.pdf"
Content-Type: application/pdf

< ./nowa_wersja/dokument.pdf
------WebKitFormBoundary--
```

**Odpowiedź (200 OK):**
```json
{
  "document_pair_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "uploaded",
  "message": "Dokumenty zostały załadowane: old.pdf, new.pdf\nStary dokument PDF skonwertowany (metoda: pdfplumber, jakość: 0.79)\nNowy dokument PDF skonwertowany (metoda: pdf2docx, jakość: 0.92)"
}
```

#### Przykład 3: Upload mieszany (DOCX + PDF)

**curl:**
```bash
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@stara_wersja/dokument.docx" \
  -F "new_document=@nowa_wersja/dokument.pdf"
```

**Błędy:**
- `400 Bad Request` - Nieprawidłowy format pliku
- `500 Internal Server Error` - Błąd konwersji PDF

---

### 4. POST `/api/process` - Rozpocznij przetwarzanie

Rozpocznij asynchroniczne porównywanie dokumentów. Zwraca natychmiast `process_id`, które można użyć do sprawdzenia statusu i pobrania wyników.

**Parametry (JSON body):**
```json
{
  "document_pair_id": "string"  // UUID z /api/documents/upload
}
```

**Przykład curl:**
```bash
curl -X POST http://localhost:8001/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "document_pair_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  }'
```

**Przykład HTTP:**
```http
POST http://localhost:8001/api/process
Content-Type: application/json

{
  "document_pair_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Odpowiedź (200 OK):**
```json
{
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "status": "started",
  "message": "Przetwarzanie zostało rozpoczęte"
}
```

**Błędy:**
- `404 Not Found` - Nie znaleziono pary dokumentów o podanym ID
- `500 Internal Server Error` - Błąd podczas rozpoczynania przetwarzania

---

### 5. GET `/api/status/{process_id}` - Status przetwarzania

Sprawdź aktualny status przetwarzania dokumentów. Endpoint do pollingu - wywołuj co 1-2 sekundy aż `status` będzie `"completed"` lub `"error"`.

**Parametry URL:**
- `process_id` (string, **required**) - UUID procesu

**Przykład curl:**
```bash
curl http://localhost:8001/api/status/f1e2d3c4-b5a6-7890-cdef-1234567890ab
```

**Przykład HTTP:**
```http
GET http://localhost:8001/api/status/f1e2d3c4-b5a6-7890-cdef-1234567890ab
Accept: application/json
```

#### Odpowiedź: Status "pending"
```json
{
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "status": "pending",
  "progress": 0,
  "message": "Oczekiwanie na rozpoczęcie przetwarzania",
  "started_at": "2025-10-23T10:30:00",
  "completed_at": null,
  "error": null
}
```

#### Odpowiedź: Status "processing"
```json
{
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "status": "processing",
  "progress": 50,
  "message": "Porównywanie dokumentów",
  "started_at": "2025-10-23T10:30:00",
  "completed_at": null,
  "error": null
}
```

**Etapy przetwarzania:**
- Progress 0-10: Oczekiwanie
- Progress 10-30: Ekstrakcja treści ze starego dokumentu
- Progress 30-50: Ekstrakcja treści z nowego dokumentu
- Progress 50-80: Porównywanie dokumentów
- Progress 80-100: Tworzenie wyników

#### Odpowiedź: Status "completed"
```json
{
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "status": "completed",
  "progress": 100,
  "message": "Przetwarzanie zakończone pomyślnie",
  "started_at": "2025-10-23T10:30:00",
  "completed_at": "2025-10-23T10:30:45",
  "error": null
}
```

#### Odpowiedź: Status "error"
```json
{
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "status": "error",
  "progress": 0,
  "message": "Błąd podczas przetwarzania",
  "started_at": "2025-10-23T10:30:00",
  "completed_at": null,
  "error": "Document extraction failed: Invalid DOCX format"
}
```

**Błędy:**
- `404 Not Found` - Nie znaleziono procesu o podanym ID

---

### 6. GET `/api/result/{process_id}/full` - Pełny wynik

Pobierz pełny dokument ze wszystkimi zmianami (unchanged, modified, added, deleted).

**Wymagania:**
- Status procesu musi być `"completed"`

**Parametry URL:**
- `process_id` (string, **required**) - UUID procesu

**Przykład curl:**
```bash
curl http://localhost:8001/api/result/f1e2d3c4-b5a6-7890-cdef-1234567890ab/full
```

**Przykład HTTP:**
```http
GET http://localhost:8001/api/result/f1e2d3c4-b5a6-7890-cdef-1234567890ab/full
Accept: application/json
```

**Odpowiedź (200 OK):**
```json
{
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "document_pair_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "paragraphs": [
    {
      "index": 0,
      "type": "unchanged",
      "text": "To jest niezmieniony paragraf.",
      "old_text": null,
      "changes": []
    },
    {
      "index": 1,
      "type": "modified",
      "text": "To jest nowy tekst.",
      "old_text": "To jest stary tekst.",
      "changes": [
        {
          "type": "delete",
          "text": "stary",
          "position": 8
        },
        {
          "type": "insert",
          "text": "nowy",
          "position": 8
        }
      ]
    },
    {
      "index": 2,
      "type": "added",
      "text": "To jest całkowicie nowy paragraf.",
      "old_text": null,
      "changes": []
    },
    {
      "index": 3,
      "type": "deleted",
      "text": "Ten paragraf został usunięty.",
      "old_text": null,
      "changes": []
    }
  ],
  "tables": [
    {
      "index": 0,
      "type": "unchanged",
      "rows": [
        ["Kolumna 1", "Kolumna 2"],
        ["Wartość 1", "Wartość 2"]
      ],
      "old_rows": null,
      "changes": []
    }
  ],
  "statistics": {
    "total_paragraphs": 4,
    "unchanged": 1,
    "modified": 1,
    "added": 1,
    "deleted": 1,
    "change_percentage": 75.0
  },
  "generated_at": "2025-10-23T10:30:45.123456"
}
```

**Typy zmian paragrafów:**
- `unchanged` - Paragraf bez zmian
- `modified` - Paragraf zmieniony (zawiera szczegóły w `changes`)
- `added` - Paragraf dodany (nowy)
- `deleted` - Paragraf usunięty

**Błędy:**
- `404 Not Found` - Nie znaleziono wyników dla podanego procesu

---

### 7. GET `/api/result/{process_id}/modified` - Tylko zmodyfikowane

Pobierz tylko zmienione zdania (filtrowanie po stronie API). Wygodne do szybkiego przeglądu zmian.

**Parametry URL:**
- `process_id` (string, **required**) - UUID procesu

**Przykład curl:**
```bash
curl http://localhost:8001/api/result/f1e2d3c4-b5a6-7890-cdef-1234567890ab/modified
```

**Przykład HTTP:**
```http
GET http://localhost:8001/api/result/f1e2d3c4-b5a6-7890-cdef-1234567890ab/modified
Accept: application/json
```

**Odpowiedź (200 OK):**
```json
{
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "document_pair_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "modified_sentences": [
    {
      "paragraph_index": 1,
      "old_text": "To jest stary tekst.",
      "new_text": "To jest nowy tekst.",
      "changes": [
        {
          "type": "delete",
          "text": "stary",
          "position": 8
        },
        {
          "type": "insert",
          "text": "nowy",
          "position": 8
        }
      ]
    },
    {
      "paragraph_index": 5,
      "old_text": "Kwota: 100 PLN",
      "new_text": "Kwota: 200 PLN",
      "changes": [
        {
          "type": "delete",
          "text": "100",
          "position": 7
        },
        {
          "type": "insert",
          "text": "200",
          "position": 7
        }
      ]
    }
  ],
  "total_count": 2,
  "generated_at": "2025-10-23T10:30:45.123456"
}
```

**Błędy:**
- `404 Not Found` - Nie znaleziono wyników

---

### 8. GET `/api/result/{process_id}/added` - Tylko dodane

Pobierz tylko dodane zdania.

**Parametry URL:**
- `process_id` (string, **required**) - UUID procesu

**Przykład curl:**
```bash
curl http://localhost:8001/api/result/f1e2d3c4-b5a6-7890-cdef-1234567890ab/added
```

**Przykład HTTP:**
```http
GET http://localhost:8001/api/result/f1e2d3c4-b5a6-7890-cdef-1234567890ab/added
Accept: application/json
```

**Odpowiedź (200 OK):**
```json
{
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "document_pair_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "added_sentences": [
    {
      "paragraph_index": 2,
      "text": "To jest całkowicie nowy paragraf."
    },
    {
      "paragraph_index": 7,
      "text": "Dodano nową klauzulę prawną."
    }
  ],
  "total_count": 2,
  "generated_at": "2025-10-23T10:30:45.123456"
}
```

**Błędy:**
- `404 Not Found` - Nie znaleziono wyników

---

### 9. GET `/api/result/{process_id}/deleted` - Tylko usunięte

Pobierz tylko usunięte zdania.

**Parametry URL:**
- `process_id` (string, **required**) - UUID procesu

**Przykład curl:**
```bash
curl http://localhost:8001/api/result/f1e2d3c4-b5a6-7890-cdef-1234567890ab/deleted
```

**Przykład HTTP:**
```http
GET http://localhost:8001/api/result/f1e2d3c4-b5a6-7890-cdef-1234567890ab/deleted
Accept: application/json
```

**Odpowiedź (200 OK):**
```json
{
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "document_pair_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "deleted_sentences": [
    {
      "paragraph_index": 3,
      "text": "Ten paragraf został usunięty."
    },
    {
      "paragraph_index": 9,
      "text": "Stara klauzula została usunięta."
    }
  ],
  "total_count": 2,
  "generated_at": "2025-10-23T10:30:45.123456"
}
```

**Błędy:**
- `404 Not Found` - Nie znaleziono wyników

---

### 10. GET `/api/report/{process_id}/generate` - Generuj raport HTML

Generuje statyczny raport HTML z osadzonymi danymi JSON. Raport jest zapisywany na serwerze i dostępny przez URL. Działa w trybie offline (nie wymaga serwera do wyświetlenia).

**Parametry URL:**
- `process_id` (string, **required**) - UUID procesu

**Przykład curl:**
```bash
curl http://localhost:8001/api/report/f1e2d3c4-b5a6-7890-cdef-1234567890ab/generate
```

**Przykład HTTP:**
```http
GET http://localhost:8001/api/report/f1e2d3c4-b5a6-7890-cdef-1234567890ab/generate
Accept: application/json
```

**Odpowiedź (200 OK):**
```json
{
  "success": true,
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "report_url": "/reports/report_f1e2d3c4-b5a6-7890-cdef-1234567890ab_20251023_231438.html",
  "report_filename": "report_f1e2d3c4-b5a6-7890-cdef-1234567890ab_20251023_231438.html",
  "report_path": "C:\\Projects\\BAW\\UslugaDoPorownan\\output\\reports\\report_f1e2d3c4-b5a6-7890-cdef-1234567890ab_20251023_231438.html",
  "generated_at": "2025-10-23T23:14:38.123456",
  "message": "Raport HTML został wygenerowany pomyślnie"
}
```

**Dostęp do raportu:**
```bash
# Lokalnie
curl http://localhost:8001/reports/report_f1e2d3c4-b5a6-7890-cdef-1234567890ab_20251023_231438.html > raport.html

# Produkcyjnie
curl http://217.182.76.146/reports/report_f1e2d3c4-b5a6-7890-cdef-1234567890ab_20251023_231438.html > raport.html
```

**Funkcjonalności raportu HTML:**
- ✅ Pełne dane JSON osadzone w HTML (nie wymaga zewnętrznego ładowania)
- ✅ Auto-display przy otwarciu (nie wymaga akcji użytkownika)
- ✅ Interaktywne filtry (wszystkie/modified/added/deleted/unchanged)
- ✅ Summary box z metrykami
- ✅ Responsive design (desktop/tablet/mobile)
- ✅ Print-ready styles
- ✅ Działa offline (bez serwera, bez internetu)

**Use cases:**
- Archiwizacja wyników jako pojedynczy plik HTML
- Udostępnianie offline (email, pendrive)
- Prezentacje (otwórz plik bezpośrednio w przeglądarce)
- Backup alternatywny do JSON
- Integracja z systemami workflow (N8N, zapier)

**Błędy:**
- `404 Not Found` - Nie znaleziono wyników dla podanego process_id
- `500 Internal Server Error` - Błąd podczas generowania raportu (brak uprawnień zapisu, brak miejsca)

**Uwagi:**
- Raport jest generowany na żądanie (nie automatycznie)
- Pliki są zapisywane w `output/reports/` na serwerze
- Format nazwy: `report_{process_id}_{timestamp}.html`
- Raporty NIE są usuwane automatycznie (wymagane ręczne cleanup)
- Raport ma ~55+ KB (zawiera HTML + CSS + JS + JSON)

**Pełna dokumentacja:** Zobacz [HTML_REPORT_ENDPOINT.md](HTML_REPORT_ENDPOINT.md) dla szczegółów i zaawansowanych przykładów.

---

## 🔄 Przykładowy Workflow

### Scenariusz 1: Porównanie dwóch plików DOCX

```bash
# Krok 1: Sprawdź czy serwis działa
curl http://localhost:8001/health

# Odpowiedź: {"status": "healthy", ...}

# Krok 2: Upload dokumentów
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@stara_wersja/umowa.docx" \
  -F "new_document=@nowa_wersja/umowa.docx"

# Odpowiedź: {"document_pair_id": "a1b2c3d4-...", "status": "uploaded"}
# Zapisz document_pair_id!

# Krok 3: Rozpocznij przetwarzanie
curl -X POST http://localhost:8001/api/process \
  -H "Content-Type: application/json" \
  -d '{"document_pair_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}'

# Odpowiedź: {"process_id": "f1e2d3c4-...", "status": "started"}
# Zapisz process_id!

# Krok 4: Sprawdź status (powtarzaj co 2 sekundy)
curl http://localhost:8001/api/status/f1e2d3c4-b5a6-7890-cdef-1234567890ab

# Odpowiedź (processing): {"status": "processing", "progress": 50, ...}
# Czekaj aż status = "completed"

# Krok 5: Pobierz wyniki JSON
curl http://localhost:8001/api/result/f1e2d3c4-b5a6-7890-cdef-1234567890ab/full > wynik.json
curl http://localhost:8001/api/result/f1e2d3c4-b5a6-7890-cdef-1234567890ab/modified > zmiany.json

# Krok 6 (OPCJONALNIE): Wygeneruj raport HTML
curl http://localhost:8001/api/report/f1e2d3c4-b5a6-7890-cdef-1234567890ab/generate

# Odpowiedź: {"success": true, "report_url": "/reports/report_..._20251023_231438.html"}

# Krok 7 (OPCJONALNIE): Pobierz raport HTML
curl http://localhost:8001/reports/report_f1e2d3c4-b5a6-7890-cdef-1234567890ab_20251023_231438.html > raport.html

# Teraz możesz otworzyć raport.html w przeglądarce (działa offline!)
```

### Scenariusz 2: Porównanie dwóch plików PDF

```bash
# Krok 1: Upload PDF (z automatyczną konwersją)
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@stara_wersja/regulamin.pdf" \
  -F "new_document=@nowa_wersja/regulamin.pdf"

# Odpowiedź zawiera info o konwersji:
# {
#   "document_pair_id": "...",
#   "message": "...\\nStary dokument PDF skonwertowany (metoda: pdf2docx, jakość: 0.92)"
# }

# Następne kroki jak w scenariuszu 1...
```

### Scenariusz 3: Automatyzacja z polling (bash script)

```bash
#!/bin/bash

# Upload
UPLOAD_RESPONSE=$(curl -s -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@old.docx" \
  -F "new_document=@new.docx")

DOC_PAIR_ID=$(echo $UPLOAD_RESPONSE | jq -r '.document_pair_id')
echo "Document Pair ID: $DOC_PAIR_ID"

# Rozpocznij przetwarzanie
PROCESS_RESPONSE=$(curl -s -X POST http://localhost:8001/api/process \
  -H "Content-Type: application/json" \
  -d "{\"document_pair_id\": \"$DOC_PAIR_ID\"}")

PROCESS_ID=$(echo $PROCESS_RESPONSE | jq -r '.process_id')
echo "Process ID: $PROCESS_ID"

# Polling status
while true; do
  STATUS_RESPONSE=$(curl -s http://localhost:8001/api/status/$PROCESS_ID)
  STATUS=$(echo $STATUS_RESPONSE | jq -r '.status')
  PROGRESS=$(echo $STATUS_RESPONSE | jq -r '.progress')

  echo "Status: $STATUS ($PROGRESS%)"

  if [ "$STATUS" = "completed" ]; then
    echo "Przetwarzanie zakończone!"
    break
  elif [ "$STATUS" = "error" ]; then
    echo "Błąd podczas przetwarzania!"
    exit 1
  fi

  sleep 2
done

# Pobierz wyniki JSON
curl -s http://localhost:8001/api/result/$PROCESS_ID/full > result.json
echo "Wyniki JSON zapisane w result.json"

# (OPCJONALNIE) Wygeneruj raport HTML
REPORT_RESPONSE=$(curl -s http://localhost:8001/api/report/$PROCESS_ID/generate)
REPORT_URL=$(echo $REPORT_RESPONSE | jq -r '.report_url')
echo "Raport HTML wygenerowany: $REPORT_URL"

# Pobierz raport HTML
curl -s http://localhost:8001$REPORT_URL > report.html
echo "Raport HTML zapisany w report.html"
echo "Otwórz report.html w przeglądarce aby zobaczyć wyniki!"
```

---

## 🛠️ Testowanie w VSCode

Jeśli używasz **Visual Studio Code**, możesz skorzystać z pliku `test.http`:

### Instalacja

1. Otwórz VSCode
2. Naciśnij `Ctrl+Shift+X` (Extensions)
3. Wyszukaj **"REST Client"** (autor: humao)
4. Kliknij **Install**

### Użycie

1. Otwórz plik `C:\Projects\BAW\test.http`
2. Kliknij **"Send Request"** nad wybranym zapytaniem
3. Zobacz wynik w nowym oknie (po prawej stronie)

### Przykład test.http

```http
### Variables
@backend_url = http://localhost:8001

### Health Check
GET {{backend_url}}/health

### Upload dokumentów
POST {{backend_url}}/api/documents/upload
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="old_document"; filename="old.docx"
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document

< ./stara_wersja/dokument.docx
------WebKitFormBoundary
Content-Disposition: form-data; name="new_document"; filename="new.docx"
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document

< ./nowa_wersja/dokument.docx
------WebKitFormBoundary--
```

**Skrót klawiszowy:** `Ctrl+Alt+R` (wyślij request)

---

## ⚠️ Kody Błędów

| Kod | Status | Znaczenie | Przykład |
|-----|--------|-----------|----------|
| 200 | OK | Sukces | Dokument załadowany |
| 400 | Bad Request | Nieprawidłowe parametry | Zły format pliku, brak wymaganych pól |
| 404 | Not Found | Nie znaleziono zasobu | Nieistniejący process_id lub document_pair_id |
| 500 | Internal Server Error | Błąd serwera | Błąd konwersji PDF, błąd ekstrakcji DOCX |

### Przykłady błędów

**400 Bad Request - Zły format pliku:**
```json
{
  "detail": "Stary dokument musi być w formacie DOCX lub PDF (otrzymano: .txt)"
}
```

**404 Not Found - Nieistniejący proces:**
```json
{
  "detail": "Nie znaleziono procesu: f1e2d3c4-b5a6-7890-cdef-1234567890ab"
}
```

**500 Internal Server Error - Błąd konwersji:**
```json
{
  "detail": "Błąd konwersji starego dokumentu PDF: PDF file is corrupted"
}
```

---

## 📊 Modele Danych

### UploadResponse

```json
{
  "document_pair_id": "string (UUID)",
  "status": "string ('uploaded')",
  "message": "string"
}
```

### ProcessRequest

```json
{
  "document_pair_id": "string (UUID)"
}
```

### ProcessResponse

```json
{
  "process_id": "string (UUID)",
  "status": "string ('started')",
  "message": "string"
}
```

### ProcessingStatus

```json
{
  "process_id": "string (UUID)",
  "status": "string ('pending' | 'processing' | 'completed' | 'error')",
  "progress": "number (0-100)",
  "message": "string",
  "started_at": "string (ISO 8601)",
  "completed_at": "string | null (ISO 8601)",
  "error": "string | null"
}
```

### FullDocumentResult

```json
{
  "process_id": "string (UUID)",
  "document_pair_id": "string (UUID)",
  "paragraphs": [
    {
      "index": "number",
      "type": "string ('unchanged' | 'modified' | 'added' | 'deleted')",
      "text": "string",
      "old_text": "string | null",
      "changes": [
        {
          "type": "string ('insert' | 'delete' | 'equal')",
          "text": "string",
          "position": "number"
        }
      ]
    }
  ],
  "tables": [
    {
      "index": "number",
      "type": "string ('unchanged' | 'modified' | 'added' | 'deleted')",
      "rows": "array",
      "old_rows": "array | null",
      "changes": "array"
    }
  ],
  "statistics": {
    "total_paragraphs": "number",
    "unchanged": "number",
    "modified": "number",
    "added": "number",
    "deleted": "number",
    "change_percentage": "number"
  },
  "generated_at": "string (ISO 8601)"
}
```

### ModifiedSentencesResult

```json
{
  "process_id": "string (UUID)",
  "document_pair_id": "string (UUID)",
  "modified_sentences": [
    {
      "paragraph_index": "number",
      "old_text": "string",
      "new_text": "string",
      "changes": [
        {
          "type": "string ('insert' | 'delete' | 'equal')",
          "text": "string",
          "position": "number"
        }
      ]
    }
  ],
  "total_count": "number",
  "generated_at": "string (ISO 8601)"
}
```

### AddedSentencesResult

```json
{
  "process_id": "string (UUID)",
  "document_pair_id": "string (UUID)",
  "added_sentences": [
    {
      "paragraph_index": "number",
      "text": "string"
    }
  ],
  "total_count": "number",
  "generated_at": "string (ISO 8601)"
}
```

### DeletedSentencesResult

```json
{
  "process_id": "string (UUID)",
  "document_pair_id": "string (UUID)",
  "deleted_sentences": [
    {
      "paragraph_index": "number",
      "text": "string"
    }
  ],
  "total_count": "number",
  "generated_at": "string (ISO 8601)"
}
```

### GenerateReportResponse

```json
{
  "success": "boolean",
  "process_id": "string (UUID)",
  "report_url": "string (relatywny URL: /reports/{filename})",
  "report_filename": "string (report_{process_id}_{timestamp}.html)",
  "report_path": "string (pełna ścieżka na serwerze)",
  "generated_at": "string (ISO 8601)",
  "message": "string"
}
```

**Przykład:**
```json
{
  "success": true,
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "report_url": "/reports/report_f1e2d3c4-b5a6-7890-cdef-1234567890ab_20251023_231438.html",
  "report_filename": "report_f1e2d3c4-b5a6-7890-cdef-1234567890ab_20251023_231438.html",
  "report_path": "C:\\Projects\\BAW\\UslugaDoPorownan\\output\\reports\\report_f1e2d3c4-b5a6-7890-cdef-1234567890ab_20251023_231438.html",
  "generated_at": "2025-10-23T23:14:38.123456",
  "message": "Raport HTML został wygenerowany pomyślnie"
}
```

---

## 🔧 Konfiguracja i Limity

### Limity

- **Max rozmiar pliku:** 50MB (konfigurowane w SecureDocCompare middleware)
- **Timeout uploadu:** 120 sekund
- **Timeout konwersji PDF:** 60 sekund (konfigurowane w PDF_CONFIG)
- **Formaty:** DOCX, PDF
- **Storage:** In-memory (brak persistence)

### Konwersja PDF

System używa dwupoziomowej konwersji PDF→DOCX:

1. **pdf2docx** (primary) - Szybka, ~95% przypadków
   - Jakość: 0.85-0.95
   - Czas: ~5-15s per dokument

2. **pdfplumber** (fallback) - Wolniejsza, skomplikowane dokumenty
   - Jakość: 0.75-0.85
   - Czas: ~15-25s per dokument
   - Uruchamia się gdy:
     - pdf2docx zwróci błąd
     - Jakość < 0.7

### Jakość konwersji

- **0.90-1.0** - Doskonała (wszystkie elementy zachowane)
- **0.80-0.89** - Bardzo dobra (drobne różnice w formatowaniu)
- **0.70-0.79** - Dobra (utrata niektórych stylów, ale treść zachowana)
- **< 0.70** - Słaba (znaczące różnice, trigger fallback)

---

## 📝 Uwagi Implementacyjne

### Asynchroniczne przetwarzanie

API używa FastAPI `BackgroundTasks` do przetwarzania w tle:

1. `POST /api/process` zwraca natychmiast `process_id`
2. Przetwarzanie odbywa się asynchronicznie
3. Status można sprawdzić przez polling `/api/status/{process_id}`
4. Wyniki dostępne po `status = "completed"`

### In-memory Storage

- Wszystkie dane przechowywane w pamięci (brak bazy danych)
- Restart serwisu = utrata wszystkich danych
- Pliki DOCX zapisywane w `uploads/` (nie są czyszczone automatycznie)

### CORS

API akceptuje requesty z dowolnego źródła (`allow_origins=["*"]`). W produkcji zaleca się ograniczenie do konkretnych domen.

### Logowanie

- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Level: INFO
- Output: stdout (console)

---

## 📚 Powiązane Dokumenty

- **[README.md](README.md)** - Główna dokumentacja projektu
- **[HTML_REPORT_ENDPOINT.md](HTML_REPORT_ENDPOINT.md)** - **NOWY!** Szczegółowa dokumentacja endpointu raportów HTML
- **[PROGRESS_LOG.md](PROGRESS_LOG.md)** - Historia rozwoju projektu
- **[DOCS_INDEX.md](DOCS_INDEX.md)** - Indeks całej dokumentacji
- **[test.http](test.http)** - Testy API dla REST Client
- **[UslugaDoPorownan/README.md](UslugaDoPorownan/README.md)** - Dokumentacja modułu backend
- **[pdf_converter/README.md](UslugaDoPorownan/pdf_converter/README.md)** - Dokumentacja konwertera PDF

---

## 📞 Pomoc i Wsparcie

### Dokumentacja online

FastAPI automatycznie generuje interaktywną dokumentację:

- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

### Kontakt

- **Projekt:** BAW - Porównywanie Dokumentów Bankowych
- **Wersja:** 1.0.0
- **Python:** 3.11.9
- **Framework:** FastAPI + Uvicorn

---

**Ostatnia aktualizacja:** 2025-10-23
**Wersja dokumentu:** 1.1.0

## 📝 Changelog

### v1.1.0 (2025-10-23)
- ✅ **Dodano endpoint 10:** `GET /api/report/{process_id}/generate` - Generowanie raportów HTML
- ✅ Zaktualizowano odpowiedź endpointu `/` (dodano `generate_report`)
- ✅ Rozszerzono Scenariusz 1 i 3 o generowanie raportów HTML
- ✅ Dodano model `GenerateReportResponse` do sekcji "Modele Danych"
- ✅ Dodano link do szczegółowej dokumentacji: [HTML_REPORT_ENDPOINT.md](HTML_REPORT_ENDPOINT.md)

### v1.0.0 (2025-10-23)
- 🎉 Pierwsze wydanie dokumentacji API
- 📝 9 endpointów (health, upload, process, status, full, modified, added, deleted)
- 📖 Przykładowe workflow i scenariusze
- 🧪 Instrukcje testowania w VSCode (REST Client)
- 📊 Pełne modele danych (Pydantic)
