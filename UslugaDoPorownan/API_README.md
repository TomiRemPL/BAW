# API - Usługa Porównywania Dokumentów - Szybki Start

## Spis Treści

- [Przegląd](#przegląd)
- [Szybki Start](#szybki-start)
- [Dokumentacja](#dokumentacja)
- [Przykłady Użycia](#przykłady-użycia)
- [Integracja n8n](#integracja-n8n)

---

## Przegląd

**Usługa Porównywania Dokumentów** to REST API do porównywania dokumentów DOCX/PDF z automatycznym wykrywaniem zmian i generowaniem raportów.

### Kluczowe Funkcje

✅ **Upload DOCX/PDF** - Automatyczna konwersja PDF→DOCX
✅ **Asynchroniczne Przetwarzanie** - Background processing z monitorowaniem statusu
✅ **Dokładna Analiza Zmian** - Diff na poziomie słów i znaków
✅ **Filtrowane Wyniki** - Full/Modified/Added/Deleted
✅ **Integracja n8n** - System podsumowań z zatwierdzaniem przez użytkownika
✅ **Raporty HTML** - Statyczne raporty offline

### Technologie

- **Framework:** FastAPI 0.100+
- **Python:** 3.10+
- **Async:** asyncio, background tasks
- **Dokumentacja:** Swagger UI, ReDoc

---

## Szybki Start

### 1. Uruchomienie Serwisu

```bash
# Instalacja zależności
pip install -r requirements.txt

# Uruchomienie serwera
uvicorn main:app --reload --port 8001

# Serwis dostępny na:
# http://localhost:8001
```

### 2. Sprawdzenie Statusu

```bash
curl http://localhost:8001/health
```

Odpowiedź:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-28T14:30:00.123456",
  "statistics": {...}
}
```

### 3. Pierwszy Request - Upload Dokumentów

```bash
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@dokument_v1.docx" \
  -F "new_document=@dokument_v2.docx"
```

Odpowiedź:
```json
{
  "document_pair_id": "c29d4e61-2963-48c7-a425-708b0c59be74",
  "status": "uploaded",
  "message": "Dokumenty zostały załadowane: dokument_v1.docx, dokument_v2.docx"
}
```

### 4. Rozpocznij Przetwarzanie

```bash
curl -X POST http://localhost:8001/api/process \
  -H "Content-Type: application/json" \
  -d '{"document_pair_id": "c29d4e61-2963-48c7-a425-708b0c59be74"}'
```

Odpowiedź:
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "status": "started",
  "message": "Przetwarzanie zostało rozpoczęte"
}
```

### 5. Monitoruj Status (Polling)

```bash
# Wykonuj co 2 sekundy, aż status = "completed"
curl http://localhost:8001/api/status/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21
```

Odpowiedź (w trakcie):
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "status": "processing",
  "progress": 50,
  "message": "Porównywanie dokumentów"
}
```

Odpowiedź (zakończone):
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "status": "completed",
  "progress": 100,
  "message": "Przetwarzanie zakończone pomyślnie"
}
```

### 6. Pobierz Wyniki

```bash
# Pełny dokument
curl http://localhost:8001/api/result/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/full

# Tylko zmodyfikowane
curl http://localhost:8001/api/result/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/modified

# Tylko dodane
curl http://localhost:8001/api/result/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/added

# Tylko usunięte
curl http://localhost:8001/api/result/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/deleted
```

### 7. Generuj Raport HTML

```bash
curl http://localhost:8001/api/report/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/generate
```

Odpowiedź:
```json
{
  "success": true,
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "report_url": "/reports/report_a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21_20251028_143530.html"
}
```

Otwórz raport w przeglądarce:
```
http://localhost:8001/reports/report_a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21_20251028_143530.html
```

---

## Dokumentacja

### Interaktywna Dokumentacja

- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc
- **OpenAPI Schema:** http://localhost:8001/openapi.json

### Pliki Dokumentacji

- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Kompletna dokumentacja wszystkich endpointów
- **[API_TESTS.http](./API_TESTS.http)** - Testy HTTP dla REST Client (VS Code)

### Struktura Endpointów

#### 🔹 Podstawowe
- `GET /` - Informacje o usłudze
- `GET /health` - Health check

#### 🔹 Upload & Processing
- `POST /api/documents/upload` - Upload dokumentów
- `POST /api/process` - Rozpocznij przetwarzanie
- `GET /api/status/{process_id}` - Status przetwarzania

#### 🔹 Wyniki
- `GET /api/result/{process_id}/full` - Pełny dokument
- `GET /api/result/{process_id}/modified` - Zmodyfikowane zdania
- `GET /api/result/{process_id}/added` - Dodane zdania
- `GET /api/result/{process_id}/deleted` - Usunięte zdania

#### 🔹 Podsumowania (n8n)
- `POST /api/summary` - Utwórz podsumowanie
- `GET /api/summary/{process_id}/status` - Status podsumowania
- `GET /api/summary/{process_id}` - Szczegóły podsumowania
- `GET /api/summary/{process_id}/approved` - Zatwierdzone podsumowanie
- `PUT /api/summary/{process_id}` - Aktualizuj podsumowanie
- `POST /api/summary/{process_id}/approve` - Zatwierdź/odrzuć

#### 🔹 Raporty
- `GET /api/report/{process_id}/generate` - Generuj raport HTML

---

## Przykłady Użycia

### Python

```python
import requests
import time

API_BASE = "http://localhost:8001"

# 1. Upload
with open("dokument_v1.docx", "rb") as old, open("dokument_v2.docx", "rb") as new:
    files = {"old_document": old, "new_document": new}
    r = requests.post(f"{API_BASE}/api/documents/upload", files=files)
    doc_pair_id = r.json()["document_pair_id"]

# 2. Process
r = requests.post(f"{API_BASE}/api/process", json={"document_pair_id": doc_pair_id})
process_id = r.json()["process_id"]

# 3. Poll status
while True:
    r = requests.get(f"{API_BASE}/api/status/{process_id}")
    if r.json()["status"] == "completed":
        break
    time.sleep(2)

# 4. Get results
r = requests.get(f"{API_BASE}/api/result/{process_id}/full")
results = r.json()

print(f"Zmiany: {results['statistics']['total_changes']}")
print(f"Dodane: {results['statistics']['added_paragraphs']}")
print(f"Usunięte: {results['statistics']['deleted_paragraphs']}")
print(f"Zmodyfikowane: {results['statistics']['modified_paragraphs']}")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

const API_BASE = 'http://localhost:8001';

async function compareDocuments(oldPath, newPath) {
  // 1. Upload
  const formData = new FormData();
  formData.append('old_document', fs.createReadStream(oldPath));
  formData.append('new_document', fs.createReadStream(newPath));

  const uploadRes = await axios.post(`${API_BASE}/api/documents/upload`, formData);
  const docPairId = uploadRes.data.document_pair_id;

  // 2. Process
  const processRes = await axios.post(`${API_BASE}/api/process`, {
    document_pair_id: docPairId
  });
  const processId = processRes.data.process_id;

  // 3. Poll status
  while (true) {
    const statusRes = await axios.get(`${API_BASE}/api/status/${processId}`);
    if (statusRes.data.status === 'completed') break;
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  // 4. Get results
  const resultsRes = await axios.get(`${API_BASE}/api/result/${processId}/full`);
  return resultsRes.data;
}

compareDocuments('dokument_v1.docx', 'dokument_v2.docx')
  .then(results => {
    console.log('Total changes:', results.statistics.total_changes);
  });
```

### REST Client (VS Code Extension)

Użyj pliku [API_TESTS.http](./API_TESTS.http):

1. Zainstaluj rozszerzenie **REST Client** w VS Code
2. Otwórz plik `API_TESTS.http`
3. Kliknij "Send Request" nad wybranym requestem
4. Zobacz response w nowym panelu

---

## Integracja n8n

### Przepływ Pracy

```
Frontend → API → n8n → LLM → API → Frontend
```

### Krok po Kroku

#### 1. Frontend: Porównaj Dokumenty
```javascript
// Upload i przetwarzanie (jak w przykładzie Python)
const results = await getFullResults(processId);
```

#### 2. Frontend → n8n: Przekaż Wyniki
```javascript
// Webhook n8n
await axios.post('https://n8n.example.com/webhook/compare-results', {
  process_id: processId,
  results: results
});
```

#### 3. n8n: Generuj Podsumowanie (LLM)
```javascript
// W n8n workflow
const llmPrompt = `Przeanalizuj zmiany i wygeneruj podsumowanie:
${JSON.stringify(results)}`;

const summary = await callLLM(llmPrompt);
```

#### 4. n8n → API: Zapisz Podsumowanie
```javascript
// W n8n
await axios.post(`${API_BASE}/api/summary`, {
  process_id: processId,
  summary_text: summary,
  metadata: {
    przedmiot_regulacji: "Regulamin",
    data_aktu: "2025-10-15"
  }
});
```

#### 5. Frontend: Wyświetl Podsumowanie
```javascript
const summary = await axios.get(`${API_BASE}/api/summary/${processId}`);
// Wyświetl edytowalny textarea z summary.summary_text
```

#### 6. Frontend → API: Edytuj i Zatwierdź
```javascript
// Edycja
await axios.put(`${API_BASE}/api/summary/${processId}`, {
  summary_text: editedSummary
});

// Zatwierdzenie
await axios.post(`${API_BASE}/api/summary/${processId}/approve`, {
  approved: true
});
```

#### 7. n8n: Polling Statusu
```javascript
// W n8n - polling co 5s
while (true) {
  const status = await axios.get(`${API_BASE}/api/summary/${processId}/status`);

  if (status.data.status === 'approved') {
    const approved = await axios.get(`${API_BASE}/api/summary/${processId}/approved`);
    // Kontynuuj workflow z zatwierdzonym podsumowaniem
    break;
  }

  await sleep(5000);
}
```

### Przykład n8n Workflow

```json
{
  "nodes": [
    {
      "name": "Webhook - Receive Results",
      "type": "n8n-nodes-base.webhook",
      "webhookId": "compare-results"
    },
    {
      "name": "LLM - Generate Summary",
      "type": "n8n-nodes-base.openAi"
    },
    {
      "name": "API - Create Summary",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:8001/api/summary",
        "method": "POST"
      }
    },
    {
      "name": "Wait Loop - Poll Status",
      "type": "n8n-nodes-base.waitForWebhook",
      "polling": true,
      "interval": 5000
    },
    {
      "name": "API - Get Approved",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:8001/api/summary/{{$node['Webhook'].json.process_id}}/approved"
      }
    }
  ]
}
```

---

## Wskazówki Deweloperskie

### Polling Best Practices

```python
import time

def wait_for_completion(process_id, max_wait=300, interval=2):
    """Czeka na zakończenie przetwarzania z timeout."""
    start = time.time()

    while time.time() - start < max_wait:
        r = requests.get(f"{API_BASE}/api/status/{process_id}")
        status = r.json()["status"]

        if status == "completed":
            return True
        elif status == "error":
            raise Exception(f"Processing error: {r.json()['error']}")

        time.sleep(interval)

    raise TimeoutError(f"Processing timeout after {max_wait}s")
```

### Error Handling

```python
try:
    r = requests.post(f"{API_BASE}/api/process", json={"document_pair_id": doc_id})
    r.raise_for_status()
except requests.HTTPError as e:
    if e.response.status_code == 404:
        print("Nie znaleziono dokumentów")
    elif e.response.status_code == 500:
        print("Błąd serwera:", e.response.json()["detail"])
```

### Testowanie

```bash
# Użyj pliku API_TESTS.http
# lub
pytest test_api_integration.py
```

---

## FAQ

**Q: Jakie formaty dokumentów są obsługiwane?**
A: DOCX (natywnie) i PDF (z automatyczną konwersją do DOCX).

**Q: Jak długo trwa przetwarzanie?**
A: Typowo 5-30 sekund w zależności od rozmiaru dokumentów.

**Q: Czy API wymaga autentykacji?**
A: Obecnie nie. W produkcji zalecane dodanie API keys lub OAuth2.

**Q: Czy wyniki są persystowane?**
A: Obecnie przechowywane in-memory. W produkcji należy użyć Redis/PostgreSQL.

**Q: Jaki jest maksymalny rozmiar dokumentu?**
A: Domyślnie 50 MB (konfigurowane w nginx: `client_max_body_size`).

**Q: Czy można porównać więcej niż 2 dokumenty?**
A: Nie, API wspiera tylko parę dokumentów (stary + nowy).

---

## Troubleshooting

### Problem: 500 Internal Server Error przy uploading PDF

**Rozwiązanie:**
- Sprawdź logi: `tail -f output/app.log`
- Upewnij się, że zainstalowano zależności PDF: `pip install marker-pdf pypdf pdfplumber`

### Problem: Timeout podczas przetwarzania

**Rozwiązanie:**
- Zwiększ timeout w kliencie (domyślnie 2 min)
- Sprawdź rozmiar dokumentów (duże pliki > 10MB mogą trwać dłużej)

### Problem: CORS errors w przeglądarce

**Rozwiązanie:**
- API ma włączone CORS dla wszystkich originów
- Sprawdź konfigurację proxy (jeśli używasz)

---

## Kontakt

**Wersja:** 1.1.0
**Python:** 3.10+
**Framework:** FastAPI 0.100+

**Dokumentacja:**
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

**Pliki:**
- [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) - Pełna dokumentacja
- [API_TESTS.http](./API_TESTS.http) - Testy HTTP
