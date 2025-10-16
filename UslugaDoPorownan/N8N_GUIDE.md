# 🔗 Przewodnik Integracji z n8n

## Wprowadzenie

Ten przewodnik pokazuje jak zintegrować Usługę Porównywania Dokumentów z n8n (automatyzacja workflow).

## Wymagania

- Usługa uruchomiona na `http://localhost:8001` (lub innym adresie)
- n8n zainstalowane i działające
- Dokumenty DOCX do porównania

## Podstawowa Konfiguracja

W n8n używamy node'a **HTTP Request** do komunikacji z API.

### 1. Health Check

**Node:** HTTP Request

**Konfiguracja:**
```
Method: GET
URL: http://localhost:8001/health
Authentication: None
```

**Output:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-15T13:00:00",
  "statistics": {
    "total_documents": 5,
    "completed_processes": 3
  }
}
```

---

## 📤 KROK 1: Załadowanie Dokumentów

### Node: HTTP Request - Upload Documents

**Konfiguracja:**
```
Method: POST
URL: http://localhost:8001/api/documents/upload
Authentication: None
Send Binary Data: Yes
```

**Body Parameters:**
```
Type: Multipart Form Data
Parameters:
  - Name: old_document
    Type: Binary File
    Input Binary Field: data (lub nazwa pola z poprzedniego node'a)

  - Name: new_document
    Type: Binary File
    Input Binary Field: data (lub nazwa pola z poprzedniego node'a)
```

**Przykład z Read Binary File:**

1. **Node 1:** Read Binary File
   - File Path: `C:\documents\old_document.docx`
   - Property Name: `old_file`

2. **Node 2:** Read Binary File
   - File Path: `C:\documents\new_document.docx`
   - Property Name: `new_file`

3. **Node 3:** HTTP Request
   - Method: POST
   - URL: http://localhost:8001/api/documents/upload
   - Body Parameters:
     ```
     Multipart Form Data:
       old_document: {{ $binary.old_file }}
       new_document: {{ $binary.new_file }}
     ```

**Response:**
```json
{
  "document_pair_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "uploaded",
  "message": "Dokumenty zostały załadowane: old.docx, new.docx"
}
```

**Zapisz do zmiennej:**
```javascript
{{ $json.document_pair_id }}
```

---

## ⚙️ KROK 2: Rozpoczęcie Przetwarzania

### Node: HTTP Request - Start Processing

**Konfiguracja:**
```
Method: POST
URL: http://localhost:8001/api/process
Authentication: None
Send Body: Yes
Body Content Type: JSON
```

**Body (JSON):**
```json
{
  "document_pair_id": "{{ $('Upload Documents').item.json.document_pair_id }}"
}
```

**Response:**
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "started",
  "message": "Przetwarzanie zostało rozpoczęte"
}
```

**Zapisz do zmiennej:**
```javascript
{{ $json.process_id }}
```

---

## ⏳ KROK 3: Sprawdzenie Statusu

### Node: HTTP Request - Check Status

**Konfiguracja:**
```
Method: GET
URL: http://localhost:8001/api/status/{{ $('Start Processing').item.json.process_id }}
Authentication: None
```

**Response:**
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "completed",
  "progress": 100,
  "message": "Przetwarzanie zakończone pomyślnie",
  "started_at": "2025-10-15T10:00:00",
  "completed_at": "2025-10-15T10:00:30"
}
```

**Statusy:**
- `pending` - Oczekuje na rozpoczęcie
- `processing` - W trakcie przetwarzania
- `completed` - Zakończone ✅
- `error` - Błąd ❌

### Dodaj pętlę oczekiwania (opcjonalne)

Użyj node'a **Wait** i **IF** aby sprawdzać status co kilka sekund:

1. **Node:** HTTP Request (Check Status)
2. **Node:** IF
   - Condition: `{{ $json.status }}` equals `completed`
   - If TRUE: Przejdź do pobierania wyników
   - If FALSE: Przejdź do Wait
3. **Node:** Wait
   - Time: 2 seconds
   - Loop back to: Check Status

---

## 📥 KROK 4: Pobranie Wyników

### 4a. Pełny Dokument ze Znacznikami

**Node:** HTTP Request - Get Full Result

**Konfiguracja:**
```
Method: GET
URL: http://localhost:8001/api/result/{{ $('Start Processing').item.json.process_id }}/full
Authentication: None
```

**Response:**
```json
{
  "process_id": "...",
  "document_pair_id": "...",
  "paragraphs": [
    {
      "index": 0,
      "text": "Nowa treść paragrafu",
      "type": "modified",
      "old_text": "Stara treść paragrafu",
      "changes": [
        {"operation": "equal", "text": "..."},
        {"operation": "delete", "text": "Stara"},
        {"operation": "insert", "text": "Nowa"}
      ]
    }
  ],
  "tables": [...],
  "statistics": {
    "total_paragraphs": 64,
    "unchanged_paragraphs": 52,
    "modified_paragraphs": 12,
    "added_paragraphs": 0,
    "deleted_paragraphs": 0,
    "total_changes": 12
  }
}
```

### 4b. Tylko Zmienione Fragmenty

**Konfiguracja:**
```
Method: GET
URL: http://localhost:8001/api/result/{{ $('Start Processing').item.json.process_id }}/modified
Authentication: None
```

**Response:**
```json
{
  "process_id": "...",
  "modified_sentences": [
    {
      "paragraph_index": 11,
      "old_text": "Chief Risk Officer (CRO)",
      "new_text": "Chief Operating Officer (COO)",
      "changes": [...]
    }
  ],
  "total_count": 12
}
```

### 4c. Tylko Dodane Fragmenty

**Konfiguracja:**
```
Method: GET
URL: http://localhost:8001/api/result/{{ $('Start Processing').item.json.process_id }}/added
```

### 4d. Tylko Usunięte Fragmenty

**Konfiguracja:**
```
Method: GET
URL: http://localhost:8001/api/result/{{ $('Start Processing').item.json.process_id }}/deleted
```

---

## 🔄 Kompletny Workflow n8n

```
┌─────────────────────┐
│ 1. Read Binary File │ (old document)
│    old_document     │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 2. Read Binary File │ (new document)
│    new_document     │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 3. HTTP Request     │
│    Upload Docs      │
│    POST /upload     │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 4. Set Variable     │
│    doc_pair_id      │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 5. HTTP Request     │
│    Start Process    │
│    POST /process    │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 6. Set Variable     │
│    process_id       │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 7. Wait             │
│    3 seconds        │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 8. HTTP Request     │
│    Check Status     │
│    GET /status/{id} │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 9. IF               │◄─────┐
│    status=complete? │      │
└──────┬───┬──────────┘      │
       │   │                 │
    YES│   │NO               │
       │   │                 │
       │   └──►Wait 2sec─────┘
       │
┌──────▼──────────────┐
│ 10. HTTP Request    │
│     Get Full Result │
│     GET /full       │
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 11. HTTP Request    │
│     Get Modified    │
│     GET /modified   │
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 12. Process Results │
│     (Your logic)    │
└─────────────────────┘
```

---

## 📋 Przykładowe Konfiguracje Node'ów

### Node: Set Variable (document_pair_id)

**Type:** Set
**Values:**
```javascript
Name: document_pair_id
Value: {{ $('Upload Documents').item.json.document_pair_id }}
```

### Node: IF (Check if completed)

**Type:** IF
**Conditions:**
```javascript
Value 1: {{ $('Check Status').item.json.status }}
Operation: Equal
Value 2: completed
```

### Node: Wait

**Type:** Wait
**Wait Time:**
```
Resume: After Time Interval
Amount: 2
Unit: Seconds
```

---

## 🔍 Przetwarzanie Wyników w n8n

### Przykład 1: Zliczanie Zmian

**Node:** Code (JavaScript)

```javascript
const fullResult = $input.item.json;
const stats = fullResult.statistics;

// Przygotuj podsumowanie
const summary = {
  total_changes: stats.total_changes,
  modified: stats.modified_paragraphs,
  added: stats.added_paragraphs,
  deleted: stats.deleted_paragraphs,
  severity: stats.total_changes > 10 ? 'HIGH' : 'LOW'
};

return { json: summary };
```

### Przykład 2: Filtrowanie Tylko Istotnych Zmian

**Node:** Code (JavaScript)

```javascript
const modifiedResult = $input.item.json;

// Filtruj tylko duże zmiany (>50 znaków różnicy)
const significantChanges = modifiedResult.modified_sentences.filter(sentence => {
  const oldLen = sentence.old_text.length;
  const newLen = sentence.new_text.length;
  const diff = Math.abs(oldLen - newLen);
  return diff > 50;
});

return {
  json: {
    significant_changes: significantChanges,
    count: significantChanges.length
  }
};
```

### Przykład 3: Wysyłka Email z Podsumowaniem

**Node:** Send Email

```javascript
To: compliance@example.com
Subject: Raport Porównania Dokumentów - {{ $now.format('YYYY-MM-DD') }}
Body:
Porównanie zakończone:

Statystyki:
- Zmodyfikowane paragrafy: {{ $('Get Full Result').item.json.statistics.modified_paragraphs }}
- Dodane paragrafy: {{ $('Get Full Result').item.json.statistics.added_paragraphs }}
- Usunięte paragrafy: {{ $('Get Full Result').item.json.statistics.deleted_paragraphs }}
- Łącznie zmian: {{ $('Get Full Result').item.json.statistics.total_changes }}

Szczegóły w załączniku.
```

---

## 🔐 Zabezpieczenia (Opcjonalne)

Jeśli chcesz zabezpieczyć API, możesz dodać Basic Auth lub API Key w n8n:

### Basic Auth w n8n

**HTTP Request Node:**
```
Authentication: Basic Auth
User: admin
Password: secretpassword
```

### API Key w Header

**HTTP Request Node:**
```
Authentication: Generic Credential Type
Add Header:
  Name: X-API-Key
  Value: your-secret-api-key
```

---

## 🐛 Obsługa Błędów w n8n

### Dodaj Error Handling

1. **Node:** HTTP Request (dowolny)
   - Settings → Continue On Fail: **TRUE**

2. **Node:** IF (sprawdź błędy)
   ```javascript
   Value 1: {{ $json.error }}
   Operation: Is Empty
   Value 2: (leave empty)
   ```
   - If FALSE (jest błąd): Wyślij powiadomienie lub zapisz log

### Przykład: Powiadomienie o Błędzie

**Node:** Send Email (lub Slack/Discord)

```javascript
Subject: ⚠️ Błąd w Porównywaniu Dokumentów
Body:
Wystąpił błąd podczas przetwarzania:

Błąd: {{ $('Check Status').item.json.error }}
Process ID: {{ $('Start Processing').item.json.process_id }}
Timestamp: {{ $now.format() }}
```

---

## 💾 Zapisywanie Wyników

### Do Pliku JSON

**Node:** Write Binary File

```javascript
File Path: /output/comparison_{{ $('Start Processing').item.json.process_id }}.json
File Name: comparison_result.json
Data: {{ JSON.stringify($json, null, 2) }}
```

### Do Bazy Danych

**Node:** Postgres / MySQL / MongoDB

```sql
INSERT INTO comparisons (
  process_id,
  document_pair_id,
  total_changes,
  created_at,
  result_json
) VALUES (
  '{{ $('Start Processing').item.json.process_id }}',
  '{{ $('Upload Documents').item.json.document_pair_id }}',
  {{ $('Get Full Result').item.json.statistics.total_changes }},
  NOW(),
  '{{ JSON.stringify($('Get Full Result').item.json) }}'
);
```

---

## 📊 Przykład: Dashboard w Google Sheets

**Node:** Google Sheets - Append

**Spreadsheet:** Document Comparisons
**Sheet:** Results

**Columns:**
```
A: Date = {{ $now.format('YYYY-MM-DD HH:mm:ss') }}
B: Process ID = {{ $('Start Processing').item.json.process_id }}
C: Total Changes = {{ $('Get Full Result').item.json.statistics.total_changes }}
D: Modified = {{ $('Get Full Result').item.json.statistics.modified_paragraphs }}
E: Added = {{ $('Get Full Result').item.json.statistics.added_paragraphs }}
F: Deleted = {{ $('Get Full Result').item.json.statistics.deleted_paragraphs }}
G: Status = Completed
```

---

## 🎯 Zaawansowane Użycie

### Batch Processing (Wiele Dokumentów)

1. **Node:** Code
   ```javascript
   // Lista par dokumentów
   const documentPairs = [
     { old: 'doc1_old.docx', new: 'doc1_new.docx' },
     { old: 'doc2_old.docx', new: 'doc2_new.docx' },
     { old: 'doc3_old.docx', new: 'doc3_new.docx' }
   ];

   return documentPairs.map(pair => ({ json: pair }));
   ```

2. **Node:** Split In Batches
   - Batch Size: 1

3. **Node:** Read Binary Files (old & new)
4. **Node:** Upload & Process (jak w podstawowym workflow)
5. Loop back to Split In Batches

### Scheduled Comparison (Automatyczne)

**Trigger:** Schedule Trigger
```
Mode: Every Hour
Hour: */6  (co 6 godzin)
```

Automatycznie porównuje dokumenty z określonego folderu co 6 godzin.

---

## 🔧 Troubleshooting

### Problem: Connection refused

**Rozwiązanie:**
- Sprawdź czy usługa działa: `curl http://localhost:8001/health`
- Zmień URL na właściwy (np. `http://192.168.1.100:8001` jeśli n8n jest na innym komputerze)

### Problem: Binary file not uploading

**Rozwiązanie:**
- Upewnij się że używasz **Multipart Form Data**
- Sprawdź nazwę pola binary: `{{ $binary.data }}` lub `{{ $binary.file }}`
- Użyj "Read Binary File" przed HTTP Request

### Problem: Status zawsze "processing"

**Rozwiązanie:**
- Dodaj Wait node (2-5 sekund)
- Sprawdź logi usługi czy przetwarzanie się nie zatrzymało
- Użyj pętli IF → Wait → Check Status

---

## 📞 Przykład: Integracja z Webhookiem

Trigger workflow przez webhook:

**Trigger Node:** Webhook
```
HTTP Method: POST
Path: document-compare
```

**Expected Body:**
```json
{
  "old_document_url": "https://storage.com/old.docx",
  "new_document_url": "https://storage.com/new.docx"
}
```

**Workflow:**
1. Webhook Trigger (otrzymaj URL-e)
2. HTTP Request (pobierz old document)
3. HTTP Request (pobierz new document)
4. Upload to API
5. Process & Get Results
6. Respond to Webhook (zwróć wyniki)

---

## ✅ Checklist Integracji

- [ ] Usługa działa na http://localhost:8001
- [ ] Health check zwraca status "healthy"
- [ ] Node "Upload Documents" skonfigurowany z Multipart Form Data
- [ ] Zapisane zmienne: document_pair_id, process_id
- [ ] Dodana pętla sprawdzania statusu (Wait + IF)
- [ ] Node'y pobierające wyniki skonfigurowane
- [ ] Obsługa błędów włączona (Continue On Fail)
- [ ] Wyniki zapisywane/przetwarzane zgodnie z potrzebami

---

## 📚 Dalsze Informacje

- Pełna dokumentacja API: `README.md`
- Szybki start: `QUICKSTART.md`
- Testowy skrypt: `test_simple.py`

## 🆘 Wsparcie

Jeśli masz problemy z integracją:
1. Sprawdź logi usługi
2. Przetestuj API z curl lub Postman
3. Sprawdź dokumentację n8n: https://docs.n8n.io/
