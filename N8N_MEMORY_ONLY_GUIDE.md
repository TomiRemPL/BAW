# 🧠 N8N Workflow - Memory Only (Bez Zapisu na Dysku)

**Wersja:** 3.0 - Memory Only
**Data:** 2025-10-23
**Plik:** `n8n_workflow_memory_only.json`

---

## 🎯 Główna różnica

### ❌ Poprzednia wersja (dysk)
```
Download → ZAPIS NA DYSK N8N → Read File → Upload API
                ↑
           BLOKOWANE
```

### ✅ Nowa wersja (pamięć)
```
Download → BINARY DATA (pamięć) → Upload API
                ↑
         DZIAŁA!
```

---

## 🔑 Kluczowe zmiany

### 1. **Brak zapisu plików na dysku N8N**

**Przed:**
```yaml
type: n8n-nodes-base.readBinaryFile
parameters:
  filePath: "C:\\documents\\old.docx"  # ❌ Wymaga zapisu
```

**Teraz:**
```yaml
type: n8n-nodes-base.dropbox
parameters:
  operation: "download"
  binaryPropertyName: "old_file"  # ✅ Bezpośrednio do pamięci
```

### 2. **Binary data przepływa przez nodes**

```
Dropbox Download → old_file (binary)
                    ↓
                  Merge
                    ↓
              Upload API (używa old_file z binary)
```

### 3. **JSON w pamięci, nie w plikach**

**Node "13. Combine All Results"** zwraca JSON jako obiekt JavaScript:
```javascript
return { json: completeResult };  // Obiekt w pamięci
```

**Node "15. Save to Dropbox"** używa `fileContent` (tekst), nie `binaryData`:
```yaml
fileContent: "={{ JSON.stringify($json, null, 2) }}"
# Konwertuje JSON object → string → Dropbox
```

---

## 📊 Struktura Workflow (15 kroków)

```
┌──────────────────────────────────────────────┐
│  ETAP 1: Download (Binary Data)              │
├──────────────────────────────────────────────┤
│  [Start]                                     │
│     ├──→ [1. Download Old Document]          │
│     │        ↓ binary: old_file              │
│     │                                         │
│     └──→ [2. Download New Document]          │
│              ↓ binary: new_file              │
│                                               │
│  [3. Merge Documents]                        │
│     ↓ binary: {old_file, new_file}           │
└──────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────┐
│  ETAP 2: Upload (Binary → API)               │
├──────────────────────────────────────────────┤
│  [4. Upload to BAW API]                      │
│     - multipart/form-data                    │
│     - old_document: old_file (binary)        │
│     - new_document: new_file (binary)        │
│     ↓ json: {document_pair_id}               │
└──────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────┐
│  ETAP 3: Processing (JSON objects)           │
├──────────────────────────────────────────────┤
│  [5. Start Processing]                       │
│     ↓ json: {process_id}                     │
│                                               │
│  [6. Wait 3 Seconds]                         │
│     ↓                                         │
│                                               │
│  [7. Check Status] ←─────┐                   │
│     ↓ json: {status}     │                   │
│                           │                   │
│  [8. Is Completed?]       │                   │
│     ├─ YES ────→ Continue │                   │
│     └─ NO → [Wait 2s] ────┘                   │
└──────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────┐
│  ETAP 4: Results (JSON objects in memory)    │
├──────────────────────────────────────────────┤
│  [9. Get Full Result]                        │
│     ↓ json: {paragraphs[], tables[], ...}    │
│                                               │
│  [10. Get Modified]                          │
│     ↓ json: {modified_sentences[]}           │
│                                               │
│  [11. Get Added]                             │
│     ↓ json: {added_sentences[]}              │
│                                               │
│  [12. Get Deleted]                           │
│     ↓ json: {deleted_sentences[]}            │
└──────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────┐
│  ETAP 5: Output (JSON in memory)             │
├──────────────────────────────────────────────┤
│  [13. Combine All Results (JSON)]            │
│     ↓ json: {                                │
│         metadata, statistics,                │
│         full_document, changes_detail        │
│       }                                       │
│     ├──→ [14. Final Summary]                 │
│     │        ↓ json: summary                  │
│     │                                         │
│     └──→ [15. Save to Dropbox (Optional)]    │
│              - Konwersja JSON → string       │
│              - Zapis jako .json              │
└──────────────────────────────────────────────┘
```

---

## 💾 Gdzie są dane?

| Etap | Typ danych | Lokalizacja | Czy na dysku N8N? |
|------|-----------|-------------|-------------------|
| Download | Binary | Pamięć N8N (binary property) | ❌ NIE |
| Merge | Binary | Pamięć N8N (binary property) | ❌ NIE |
| Upload API | Binary → HTTP | Request multipart | ❌ NIE |
| Results | JSON | Pamięć N8N (json property) | ❌ NIE |
| Combine | JSON Object | Pamięć N8N (json property) | ❌ NIE |
| Save Dropbox | String → Dropbox | Dropbox (chmura) | ❌ NIE (✅ Dropbox) |

**Wniosek:** ✅ Żaden plik NIE jest zapisywany na dysku serwera N8N!

---

## 🔍 Szczegóły kluczowych nodes

### Node 4: Upload to BAW API

```yaml
type: n8n-nodes-base.httpRequest
parameters:
  method: POST
  url: http://217.182.76.146/api/documents/upload
  contentType: multipart-form-data
  bodyParameters:
    - name: old_document
      inputDataFieldName: "=old_file"   # ← Wskazuje binary property
    - name: new_document
      inputDataFieldName: "=new_file"   # ← Wskazuje binary property
```

**Jak to działa:**
1. N8N czyta `$binary.old_file` z pamięci
2. Tworzy multipart/form-data request
3. Wysyła binary data bezpośrednio do API
4. **Brak pośredniego zapisu na dysku**

### Node 13: Combine All Results (JavaScript)

```javascript
// Pobierz JSON z poprzednich nodes (z pamięci)
const fullResult = $('9. Get Full Result').first().json;
const modifiedResult = $('10. Get Modified').first().json;
const addedResult = $('11. Get Added').first().json;
const deletedResult = $('12. Get Deleted').first().json;

// Utwórz kompletny obiekt
const completeResult = {
  metadata: { ... },
  statistics: { ... },
  full_document: {
    paragraphs: fullResult.paragraphs,  // ← Duży array, ale w pamięci
    tables: fullResult.tables
  },
  changes_detail: {
    modified: { ... },
    added: { ... },
    deleted: { ... }
  }
};

// Zwróć JSON object (w pamięci N8N)
return { json: completeResult };
```

**Uwaga:** Ten JSON może być duży (setki KB), ale N8N trzyma go w pamięci RAM, nie na dysku.

### Node 15: Save to Dropbox (Optional)

```yaml
type: n8n-nodes-base.dropbox
parameters:
  operation: upload
  path: "/BAW_Results/{{ $json.metadata.process_id }}.json"
  binaryData: false  # ← NIE używamy binary
  fileContent: "={{ JSON.stringify($json, null, 2) }}"
  # ↑ Konwersja JSON object → pretty-printed string
```

**Proces:**
1. JSON object w pamięci
2. `JSON.stringify()` konwertuje → string
3. Dropbox API tworzy plik tekstowy
4. **Plik trafia bezpośrednio do Dropbox (nie na dysk N8N)**

---

## 🚀 Jak używać?

### 1. Zaimportuj workflow

```
N8N → Workflows → Import from File
→ Wybierz: n8n_workflow_memory_only.json
```

### 2. Skonfiguruj Dropbox credentials

**Jeśli nie masz:**
1. https://www.dropbox.com/developers/apps
2. Create App → Scoped access → Full Dropbox
3. Skopiuj App key + App secret
4. N8N → Credentials → Dropbox API → Authorize

### 3. Zmień ścieżki do dokumentów

**Node "1. Download Old Document":**
```yaml
path: "/Twoj_folder/stara_wersja.docx"
```

**Node "2. Download New Document":**
```yaml
path: "/Twoj_folder/nowa_wersja.docx"
```

### 4. (Opcjonalnie) Wyłącz zapis do Dropbox

Jeśli chcesz tylko JSON w pamięci (bez zapisu):
- **Usuń połączenie** z node "13" do "15"
- Lub **disable** node "15. Save to Dropbox"

### 5. Uruchom workflow

1. Kliknij **Execute Workflow** (▶️)
2. Obserwuj wykonywanie
3. Sprawdź wyniki:
   - **Node "14. Final Summary"** - krótkie podsumowanie
   - **Node "13. Combine All Results"** - pełny JSON

---

## 📄 Przykładowy wynik

### Node "14. Final Summary"

```json
{
  "success": true,
  "message": "Document comparison completed successfully",
  "execution_summary": {
    "process_id": "f1e2d3c4-...",
    "document_pair_id": "a1b2c3d4-...",
    "processed_at": "2025-10-23T12:34:56.789Z"
  },
  "statistics": {
    "total_paragraphs": 100,
    "total_changes": 25,
    "change_percentage": 25.0,
    "change_severity": "MEDIUM",
    "requires_review": true
  },
  "changes_breakdown": {
    "unchanged": 75,
    "modified": 18,
    "added": 4,
    "deleted": 3
  },
  "full_json_available": true,
  "next_steps": "High priority - manual review required"
}
```

### Node "13. Combine All Results (JSON)"

```json
{
  "metadata": {
    "process_id": "f1e2d3c4-b5a6-7890-cdef-1234567890ab",
    "document_pair_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "generated_at": "2025-10-23T12:34:00.000Z",
    "processed_at": "2025-10-23T12:34:56.789Z"
  },
  "statistics": {
    "total_paragraphs": 100,
    "unchanged": 75,
    "modified": 18,
    "added": 4,
    "deleted": 3,
    "change_percentage": 25.0
  },
  "full_document": {
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
      // ... więcej paragrafów
    ],
    "tables": [
      // ... tabele jeśli są
    ]
  },
  "changes_detail": {
    "modified": {
      "count": 18,
      "sentences": [
        {
          "paragraph_index": 1,
          "old_text": "To jest stary tekst.",
          "new_text": "To jest nowy tekst.",
          "changes": [...]
        }
        // ... więcej zmodyfikowanych
      ]
    },
    "added": {
      "count": 4,
      "sentences": [
        {
          "paragraph_index": 2,
          "text": "Całkowicie nowy paragraf."
        }
        // ... więcej dodanych
      ]
    },
    "deleted": {
      "count": 3,
      "sentences": [
        {
          "paragraph_index": 5,
          "text": "Ten paragraf został usunięty."
        }
        // ... więcej usuniętych
      ]
    }
  },
  "summary": {
    "total_changes": 25,
    "change_severity": "MEDIUM",
    "requires_review": true
  }
}
```

---

## 🔄 Integracja z innymi systemami

### Opcja 1: Webhook (wysyłka JSON)

Dodaj node **HTTP Request** po "13. Combine All Results":

```yaml
type: n8n-nodes-base.httpRequest
parameters:
  method: POST
  url: "https://twoj-system.com/api/document-changes"
  sendBody: true
  contentType: json
  jsonBody: "={{ $json }}"  # Wysyła cały JSON
```

### Opcja 2: Database (zapis do PostgreSQL)

Dodaj node **Postgres**:

```yaml
type: n8n-nodes-base.postgres
parameters:
  operation: insert
  table: document_comparisons
  columns: process_id, statistics, full_json
  values:
    - "={{ $json.metadata.process_id }}"
    - "={{ JSON.stringify($json.statistics) }}"
    - "={{ JSON.stringify($json) }}"
```

### Opcja 3: Email z podsumowaniem

Dodaj node **Send Email** po "14. Final Summary":

```yaml
type: n8n-nodes-base.emailSend
parameters:
  toEmail: "team@example.com"
  subject: "Document Comparison: {{ $json.execution_summary.process_id }}"
  text: |
    Total changes: {{ $json.statistics.total_changes }}
    Severity: {{ $json.statistics.change_severity }}
    Requires review: {{ $json.statistics.requires_review }}

    Modified: {{ $json.changes_breakdown.modified }}
    Added: {{ $json.changes_breakdown.added }}
    Deleted: {{ $json.changes_breakdown.deleted }}
```

### Opcja 4: Slack notification

Dodaj node **Slack**:

```yaml
type: n8n-nodes-base.slack
parameters:
  channel: "#document-reviews"
  text: |
    🔔 New document comparison completed!

    📊 Changes: {{ $json.statistics.total_changes }}
    ⚠️ Severity: {{ $json.statistics.change_severity }}
    👀 Review needed: {{ $json.statistics.requires_review }}
```

---

## ⚡ Performance

### Zużycie pamięci

Typowy dokument 50-100 stron:

| Komponent | Rozmiar | Typ |
|-----------|---------|-----|
| Binary DOCX (old) | ~500 KB | Binary data |
| Binary DOCX (new) | ~500 KB | Binary data |
| Full Result JSON | ~200 KB | JSON object |
| Modified JSON | ~50 KB | JSON object |
| Added JSON | ~20 KB | JSON object |
| Deleted JSON | ~20 KB | JSON object |
| Combined JSON | ~300 KB | JSON object |
| **TOTAL** | **~1.6 MB** | **Pamięć RAM** |

**Wniosek:** Dla typowych dokumentów workflow zajmuje < 2 MB pamięci.

### Czas wykonania

| Etap | Czas |
|------|------|
| Download 2x DOCX | ~2-5s |
| Upload to API | ~3-8s |
| Processing (backend) | ~10-30s |
| Polling (loop) | ~6-12s |
| Get Results (4 calls) | ~2-4s |
| Combine + Save | ~1-2s |
| **TOTAL** | **~25-60s** |

---

## 🐛 Troubleshooting

### Problem 1: "Binary data not found"

**Objawy:**
```
Error: No binary data found for property 'old_file'
```

**Przyczyna:** Merge node nie połączył binary data.

**Rozwiązanie:**
1. Sprawdź czy oba Download nodes mają `binaryPropertyName`
2. Sprawdź połączenia: oба Download → Merge (input 0 i 1)
3. Sprawdź w Merge node → "Preview" → "Binary" tab

### Problem 2: "JSON too large"

**Objawy:**
```
Error: Response entity too large
```

**Przyczyna:** JSON > 10 MB (bardzo duży dokument).

**Rozwiązanie:**
1. Podziel dokument na mniejsze części
2. Lub nie łącz wszystkich wyników - używaj tylko `/modified`
3. Lub zwiększ limit w N8N config: `N8N_PAYLOAD_SIZE_MAX=100`

### Problem 3: Upload API timeout

**Objawy:**
```
Error: Request timeout after 120000ms
```

**Przyczyna:** Pliki PDF zbyt duże, konwersja trwa > 120s.

**Rozwiązanie:**
Zwiększ timeout w node "4. Upload to BAW API":
```yaml
options:
  timeout: 180000  # 3 minuty
```

### Problem 4: Loop nieskończony

**Objawy:** Workflow wykonuje się > 5 minut, ciągle czeka.

**Przyczyna:** Backend nigdy nie zwraca `status: "completed"`.

**Rozwiązanie:**
1. Sprawdź logi backendu: `sudo journalctl -u baw-backend -n 100`
2. Sprawdź status ręcznie: `curl http://217.182.76.146/api/status/{id}`
3. Dodaj timeout node (np. max 10 iteracji)

---

## 🔒 Bezpieczeństwo

### Dane w pamięci

✅ **Plusy:**
- Brak wrażliwych plików na dysku N8N
- Automatyczne czyszczenie po wykonaniu
- Brak śladu na serwerze

⚠️ **Minusy:**
- Dane w RAM (potencjalny memory dump)
- Logi N8N mogą zawierać fragmenty JSON

### Rekomendacje

1. **Disable execution logging** dla wrażliwych danych:
```yaml
# N8N settings
N8N_LOG_LEVEL=error
N8N_LOG_OUTPUT=console
```

2. **Szyfruj Dropbox:**
- Użyj Dropbox Business z szyfrowaniem
- Lub szyfruj JSON przed zapisem (node Crypto)

3. **Limit retention:**
- Ustawiaj automatyczne usuwanie w Dropbox (np. 30 dni)

---

## 📚 Dokumenty powiązane

- **[N8N_WORKFLOW_GUIDE.md](N8N_WORKFLOW_GUIDE.md)** - Poprzednia wersja (z zapisem)
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Dokumentacja BAW API
- **[N8N_INTEGRATION.md](N8N_INTEGRATION.md)** - Ogólna integracja N8N

---

## ✅ Checklist

Przed uruchomieniem sprawdź:

- [ ] Serwer BAW działa (`curl http://217.182.76.146/health`)
- [ ] Credentials Dropbox w N8N skonfigurowane
- [ ] Ścieżki do plików w Dropbox są poprawne
- [ ] Dokumenty DOCX/PDF istnieją w Dropbox
- [ ] (Opcjonalnie) Folder `/BAW_Results/` istnieje w Dropbox

Po uruchomieniu:

- [ ] Node "14. Final Summary" pokazuje sukces
- [ ] `total_changes` jest > 0 (jeśli są zmiany)
- [ ] (Jeśli włączone) Plik JSON w Dropbox `/BAW_Results/`

---

**Autor:** BAW Project
**Data:** 2025-10-23
**Wersja:** 3.0 - Memory Only
**Status:** ✅ Production Ready (bez zapisu na dysku N8N)
