# 🔗 Integracja z N8N - BAW API

Instrukcja integracji API porównywania dokumentów z platformą N8N.

---

## 📋 Spis Treści

1. [Wymagania](#wymagania)
2. [Szybki Start](#szybki-start)
3. [Przykładowe Workflow](#przykładowe-workflow)
4. [Konfiguracja Nodes](#konfiguracja-nodes)
5. [Troubleshooting](#troubleshooting)

---

## 🔧 Wymagania

### Po stronie serwera BAW:

- ✅ Backend uruchomiony na porcie 8001
- ✅ Firewall otwarty dla portu 8001
- ✅ Publiczny dostęp: `http://217.182.76.146:8001`

### Weryfikacja:

```bash
# Na serwerze
curl http://localhost:8001/health

# Z zewnątrz
curl http://217.182.76.146:8001/health
```

**Oczekiwana odpowiedź:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T...",
  "statistics": {...}
}
```

---

## 🚀 Szybki Start

### Test połączenia w N8N

1. **Utwórz nowy workflow** w N8N
2. **Dodaj node: HTTP Request**
3. **Konfiguracja:**
   - **Method:** `GET`
   - **URL:** `http://217.182.76.146:8001/health`
   - **Authentication:** `None`
   - **Options → Response Format:** `JSON`

4. **Execute Node**

**Wynik powinien zawierać:**
```json
{
  "status": "healthy",
  "timestamp": "...",
  "statistics": {
    "total_documents": 0,
    "total_processes": 0,
    "completed_processes": 0,
    "failed_processes": 0
  }
}
```

---

## 📊 Przykładowe Workflow

### Workflow 1: Proste porównanie dokumentów

#### Krok 1: Upload dokumentów

**Node: HTTP Request**

```yaml
Method: POST
URL: http://217.182.76.146:8001/api/documents/upload
Authentication: None
Body Content Type: Multipart-Form
Body Parameters:
  - Name: old_document
    Type: Binary Data
    Value: {{ $binary.old_file }}
  - Name: new_document
    Type: Binary Data
    Value: {{ $binary.new_file }}
```

**Odpowiedź:**
```json
{
  "document_pair_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "uploaded",
  "message": "Dokumenty zostały załadowane..."
}
```

#### Krok 2: Rozpocznij przetwarzanie

**Node: HTTP Request**

```yaml
Method: POST
URL: http://217.182.76.146:8001/api/process
Authentication: None
Headers:
  - Name: Content-Type
    Value: application/json
Body:
  {
    "document_pair_id": "{{ $json.document_pair_id }}"
  }
```

**Odpowiedź:**
```json
{
  "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
  "status": "started",
  "message": "Przetwarzanie zostało rozpoczęte"
}
```

#### Krok 3: Sprawdź status (loop)

**Node: HTTP Request + Wait + Loop**

```yaml
Method: GET
URL: http://217.182.76.146:8001/api/status/{{ $json.process_id }}
Authentication: None
```

**Logika:**
- Jeśli `status === "completed"` → Kontynuuj
- Jeśli `status === "processing"` → Wait 2s + Retry
- Jeśli `status === "error"` → Stop Workflow

#### Krok 4: Pobierz wyniki

**Node: HTTP Request**

```yaml
Method: GET
URL: http://217.182.76.146:8001/api/result/{{ $json.process_id }}/full
Authentication: None
```

**Odpowiedź:**
```json
{
  "process_id": "...",
  "document_pair_id": "...",
  "paragraphs": [...],
  "tables": [...],
  "statistics": {
    "total_paragraphs": 10,
    "unchanged": 5,
    "modified": 3,
    "added": 1,
    "deleted": 1,
    "change_percentage": 50.0
  },
  "generated_at": "..."
}
```

---

## ⚙️ Konfiguracja Nodes

### Node 1: Upload Files (HTTP Request)

**Szczegółowa konfiguracja:**

```
┌─────────────────────────────────────┐
│ HTTP Request Node                   │
├─────────────────────────────────────┤
│ Name: Upload Documents              │
│ Method: POST                        │
│ URL: http://217.182.76.146:8001    │
│      /api/documents/upload          │
│                                     │
│ Authentication: None                │
│                                     │
│ Body Content Type:                  │
│   Multipart-Form Data              │
│                                     │
│ Parameters:                         │
│   □ old_document (File)            │
│     Type: Binary Data               │
│     Input Binary Field: old_file    │
│                                     │
│   □ new_document (File)            │
│     Type: Binary Data               │
│     Input Binary Field: new_file    │
│                                     │
│ Response Format: JSON               │
│ Timeout: 120000 (120s)             │
└─────────────────────────────────────┘
```

**Uwaga:** Pliki muszą być dostarczone przez poprzedni node (np. "Read Binary File" lub "HTTP Request" pobierający pliki).

### Node 2: Start Processing (HTTP Request)

```
┌─────────────────────────────────────┐
│ HTTP Request Node                   │
├─────────────────────────────────────┤
│ Name: Start Processing              │
│ Method: POST                        │
│ URL: http://217.182.76.146:8001    │
│      /api/process                   │
│                                     │
│ Authentication: None                │
│                                     │
│ Headers:                            │
│   Content-Type: application/json    │
│                                     │
│ Body Content Type: JSON             │
│                                     │
│ Body (JSON):                        │
│ {                                   │
│   "document_pair_id":               │
│     "{{$json.document_pair_id}}"    │
│ }                                   │
│                                     │
│ Response Format: JSON               │
└─────────────────────────────────────┘
```

### Node 3: Check Status (Loop Until Complete)

**Struktura workflow:**

```
HTTP Request → IF → Switch
    ↑               ↓
    └─── Wait ←─────┘
```

**HTTP Request Node:**

```
┌─────────────────────────────────────┐
│ HTTP Request Node                   │
├─────────────────────────────────────┤
│ Name: Check Status                  │
│ Method: GET                         │
│ URL: http://217.182.76.146:8001    │
│      /api/status/{{$json.process_id}}│
│                                     │
│ Authentication: None                │
│ Response Format: JSON               │
└─────────────────────────────────────┘
```

**IF Node:**

```
┌─────────────────────────────────────┐
│ IF Node                             │
├─────────────────────────────────────┤
│ Condition:                          │
│   {{ $json.status }} === "completed"│
│                                     │
│ TRUE  → Get Results                 │
│ FALSE → Wait Node → Loop Back       │
└─────────────────────────────────────┘
```

**Wait Node:**

```
┌─────────────────────────────────────┐
│ Wait Node                           │
├─────────────────────────────────────┤
│ Time: 2 seconds                     │
└─────────────────────────────────────┘
```

### Node 4: Get Results (HTTP Request)

```
┌─────────────────────────────────────┐
│ HTTP Request Node                   │
├─────────────────────────────────────┤
│ Name: Get Full Results              │
│ Method: GET                         │
│ URL: http://217.182.76.146:8001    │
│      /api/result/{{$json.process_id}}│
│      /full                          │
│                                     │
│ Authentication: None                │
│ Response Format: JSON               │
└─────────────────────────────────────┘
```

**Alternatywne endpointy:**
- `/modified` - Tylko zmodyfikowane fragmenty
- `/added` - Tylko dodane fragmenty
- `/deleted` - Tylko usunięte fragmenty

---

## 🧪 Przykładowy JSON Workflow (Import do N8N)

Możesz zaimportować ten workflow bezpośrednio do N8N:

```json
{
  "name": "BAW Document Comparison",
  "nodes": [
    {
      "parameters": {
        "method": "GET",
        "url": "http://217.182.76.146:8001/health"
      },
      "name": "Health Check",
      "type": "n8n-nodes-base.httpRequest",
      "position": [250, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "http://217.182.76.146:8001/api/documents/upload",
        "sendBody": true,
        "contentType": "multipart-form-data",
        "bodyParameters": {
          "parameters": [
            {
              "name": "old_document",
              "value": "={{ $binary.old_file }}"
            },
            {
              "name": "new_document",
              "value": "={{ $binary.new_file }}"
            }
          ]
        }
      },
      "name": "Upload Documents",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300]
    }
  ],
  "connections": {
    "Health Check": {
      "main": [[{"node": "Upload Documents", "type": "main", "index": 0}]]
    }
  }
}
```

**Jak zaimportować:**
1. W N8N: Menu → Workflows → Import from File/URL
2. Wklej powyższy JSON
3. Dostosuj parametry (ścieżki do plików, etc.)

---

## 🔧 Troubleshooting

### Problem 1: Connection Refused / Timeout

**Objawy:**
```
Error: connect ECONNREFUSED 217.182.76.146:8001
// lub
Error: Request timeout
```

**Rozwiązanie:**

1. **Sprawdź firewall na serwerze:**
   ```bash
   ssh debian@217.182.76.146
   sudo ufw status | grep 8001
   # Jeśli brak, dodaj:
   sudo ufw allow 8001/tcp
   ```

2. **Sprawdź czy backend działa:**
   ```bash
   sudo systemctl status baw-backend
   ```

3. **Test połączenia z zewnątrz:**
   ```bash
   curl http://217.182.76.146:8001/health
   ```

4. **Użyj narzędzia diagnostycznego:**
   ```bash
   cd /home/debian/hack/BAW
   ./check_api.sh
   ```

### Problem 2: 404 Not Found

**Objawy:**
```json
{
  "detail": "Not Found"
}
```

**Rozwiązanie:**
- Sprawdź URL endpointu (literówka?)
- Sprawdź czy używasz poprawnej metody HTTP (GET/POST)
- Sprawdź dokumentację: `/docs` (Swagger)

**Poprawne URL-e:**
```
✓ http://217.182.76.146:8001/health
✓ http://217.182.76.146:8001/api/documents/upload
✓ http://217.182.76.146:8001/api/process
✗ http://217.182.76.146:8001/upload (zły)
✗ http://217.182.76.146:8001/documents (zły)
```

### Problem 3: 500 Internal Server Error

**Objawy:**
```json
{
  "detail": "Błąd podczas ładowania dokumentów: ..."
}
```

**Rozwiązanie:**
- Sprawdź logi na serwerze:
  ```bash
  sudo journalctl -u baw-backend -n 100
  ```
- Sprawdź format plików (DOCX/PDF)
- Sprawdź rozmiar plików (max 50MB)

### Problem 4: CORS Error (w przeglądarce)

**Objawy:**
```
Access to XMLHttpRequest ... has been blocked by CORS policy
```

**Rozwiązanie:**
- API ma CORS otwarty (`allow_origins=["*"]`)
- Jeśli nadal problem, dodaj headers w N8N:
  ```
  Origin: http://your-n8n-domain.com
  ```

### Problem 5: Długi czas przetwarzania

**Objawy:**
- Status "processing" przez > 2 minuty

**Rozwiązanie:**
- To normalne dla dużych PDF (20+ stron)
- Zwiększ timeout w N8N do 180s
- Sprawdź progress w API:
  ```bash
  curl http://217.182.76.146:8001/api/status/{process_id}
  ```

---

## 📊 Monitorowanie

### Endpoint do monitorowania

```
GET http://217.182.76.146:8001/health
```

**Użyj w N8N jako "Health Check" co 5 minut:**

```
┌─────────────────────────────────────┐
│ Cron Node (co 5 min)                │
│         ↓                           │
│ HTTP Request (health)               │
│         ↓                           │
│ IF (status !== "healthy")           │
│         ↓                           │
│ Send Alert (email/slack)            │
└─────────────────────────────────────┘
```

---

## 📚 Powiązane Dokumenty

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Pełna dokumentacja API
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment i konfiguracja firewall
- **[test.prod.http](test.prod.http)** - Przykłady testów (REST Client)

---

## 📞 Wsparcie

Jeśli potrzebujesz pomocy:

1. **Sprawdź logi:** `sudo journalctl -u baw-backend -n 100`
2. **Użyj diagnostyki:** `./check_api.sh`
3. **Napraw firewall:** `sudo ./fix_firewall.sh`
4. **Dokumentacja API:** `http://217.182.76.146:8001/docs` (Swagger)

---

**Ostatnia aktualizacja:** 2025-10-23
**Wersja:** 1.0.0
