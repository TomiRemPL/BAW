# 🔧 Integracja BAW API - Przewodnik Naprawy

**Data:** 2025-10-23
**Plik:** `dokumenty_wejsciowe.json`

---

## 🎯 Problem

Twój obecny workflow pobiera dokumenty z Dropbox i częściowo łączy się z API BAW, ale:

1. ❌ **Błędne URL-e** - używa `localhost:8001` zamiast `http://217.182.76.146`
2. ❌ **Błędny upload** - używa `data0`, `data1` zamiast `old_file`, `new_file`
3. ❌ **Niepełne pobieranie** - brakuje endpointów `/added` i `/deleted`
4. ❌ **Brak łączenia wyników** - nie ma node do połączenia wszystkich JSONów
5. ❌ **Brak połączeń** - nodes nie są ze sobą połączone

---

## ✅ Rozwiązanie - 2 Opcje

### **Opcja A: Użyj gotowego naprawionego workflow**

Plik: `dokumenty_wejsciowe_FIXED.json` (właśnie utworzony)

**Co zawiera:**
- ✅ Poprawne URL-e (http://217.182.76.146)
- ✅ Prawidłowy upload (old_file, new_file)
- ✅ Wszystkie 4 typy wyników (full, modified, added, deleted)
- ✅ Łączenie wyników w jeden JSON
- ✅ Podsumowanie końcowe
- ✅ Wszystkie połączenia między nodes

**Jak zaimportować:**
1. Otwórz N8N
2. Menu → **Workflows** → **Import from File**
3. Wybierz: `C:\Projects\BAW\UslugaDoPorownan\dokumenty_wejsciowe_FIXED.json`
4. Zmień ścieżki do plików w Dropbox (nodes: "Download New Document", "Download Old Document")

---

### **Opcja B: Napraw istniejący workflow ręcznie**

Jeśli chcesz zachować swoje istniejące nodes (SQL, BAW, SeaTable itp.) i tylko DOROBIĆ integrację z API BAW.

#### **Krok 1: Znajdź i popraw node "Upload Documents"**

**Lokalizacja w pliku:** Linia 679-706

**ZMIEŃ:**
```json
{
  "parameters": {
    "method": "POST",
    "url": "http://localhost:8001/api/documents/upload",  // ❌ ZŁY URL
    "sendBody": true,
    "contentType": "multipart-form-data",
    "bodyParameters": {
      "parameters": [
        {
          "name": "old_document",
          "value": "={{ $binary.data1 }}"  // ❌ ZŁE POLE
        },
        {
          "name": "new_document",
          "value": "={{ $binary.data0 }}"  // ❌ ZŁE POLE
        }
      ]
    },
    "options": {}
  }
}
```

**NA:**
```json
{
  "parameters": {
    "method": "POST",
    "url": "http://217.182.76.146/api/documents/upload",  // ✅ POPRAWNE
    "sendBody": true,
    "contentType": "multipart-form-data",
    "bodyParameters": {
      "parameters": [
        {
          "name": "old_document",
          "inputDataFieldName": "=old_file"  // ✅ POPRAWNE
        },
        {
          "name": "new_document",
          "inputDataFieldName": "=new_file"  // ✅ POPRAWNE
        }
      ]
    },
    "options": {
      "timeout": 120000  // ✅ DODANE - timeout 120s
    }
  }
}
```

---

#### **Krok 2: Popraw node "Start Processing"**

**Lokalizacja w pliku:** Linia 707-730

**ZMIEŃ:**
```json
{
  "parameters": {
    "method": "POST",
    "url": "http://localhost:8001/api/process",  // ❌ ZŁY URL
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        {
          "name": "document_pair_id",
          "value": "={{ $('Upload Documents').item.json.document_pair_id }}"
        }
      ]
    }
  }
}
```

**NA:**
```json
{
  "parameters": {
    "method": "POST",
    "url": "http://217.182.76.146/api/process",  // ✅ POPRAWNE
    "sendBody": true,
    "contentType": "json",  // ✅ DODANE
    "jsonBody": "={\n  \"document_pair_id\": \"{{ $json.document_pair_id }}\"\n}",  // ✅ ZMIENIONE
    "options": {}
  }
}
```

---

#### **Krok 3: Popraw node "Check Status"**

**Lokalizacja w pliku:** Linia 747-759

**ZMIEŃ:**
```json
"url": "=http://localhost:8001/api/status/{{ $('Start Processing').item.json.process_id }}"
```

**NA:**
```json
"url": "=http://217.182.76.146/api/status/{{ $('Start Processing').item.json.process_id }}"
```

---

#### **Krok 4: Popraw node "Get Full Result"**

**Lokalizacja w pliku:** Linia 797-809

**ZMIEŃ:**
```json
"url": "=http://localhost:8001/api/result/{{ $('Start Processing').item.json.process_id }}/full"
```

**NA:**
```json
"url": "=http://217.182.76.146/api/result/{{ $('Start Processing').item.json.process_id }}/full"
```

---

#### **Krok 5: Popraw node "Get Modified"**

**Lokalizacja w pliku:** Linia 810-823

**ZMIEŃ:**
```json
"url": "=http://localhost:8001/api/result/{{ $('Start Processing').item.json.process_id }}/modified"
```

**NA:**
```json
"url": "=http://217.182.76.146/api/result/{{ $('Start Processing').item.json.process_id }}/modified"
```

---

#### **Krok 6: DODAJ nowy node "Get Added"**

**Wstaw po node "Get Modified":**

```json
{
  "parameters": {
    "url": "=http://217.182.76.146/api/result/{{ $('Start Processing').item.json.process_id }}/added",
    "options": {}
  },
  "id": "get-added-node",
  "name": "Get Added",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [2250, 256]
}
```

**Połączenie:**
```json
"Get Modified": {
  "main": [
    [
      {
        "node": "Get Added",
        "type": "main",
        "index": 0
      }
    ]
  ]
}
```

---

#### **Krok 7: DODAJ nowy node "Get Deleted"**

**Wstaw po node "Get Added":**

```json
{
  "parameters": {
    "url": "=http://217.182.76.146/api/result/{{ $('Start Processing').item.json.process_id }}/deleted",
    "options": {}
  },
  "id": "get-deleted-node",
  "name": "Get Deleted",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [2450, 256]
}
```

**Połączenie:**
```json
"Get Added": {
  "main": [
    [
      {
        "node": "Get Deleted",
        "type": "main",
        "index": 0
      }
    ]
  ]
}
```

---

#### **Krok 8: DODAJ node "Combine All Results"**

**Wstaw po node "Get Deleted":**

```json
{
  "parameters": {
    "jsCode": "// Łączenie wszystkich wyników w jeden obiekt JSON\nconst fullResult = $('Get Full Result').first().json;\nconst modifiedResult = $('Get Modified').first().json;\nconst addedResult = $('Get Added').first().json;\nconst deletedResult = $('Get Deleted').first().json;\n\nconst finalResult = {\n  metadata: {\n    process_id: fullResult.process_id,\n    document_pair_id: fullResult.document_pair_id,\n    generated_at: fullResult.generated_at,\n    timestamp: new Date().toISOString()\n  },\n  statistics: fullResult.statistics,\n  full_document: {\n    paragraphs: fullResult.paragraphs,\n    tables: fullResult.tables || []\n  },\n  changes_summary: {\n    modified: {\n      count: modifiedResult.total_count,\n      items: modifiedResult.modified_sentences\n    },\n    added: {\n      count: addedResult.total_count,\n      items: addedResult.added_sentences\n    },\n    deleted: {\n      count: deletedResult.total_count,\n      items: deletedResult.deleted_sentences\n    }\n  }\n};\n\nreturn { json: finalResult };"
  },
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [2650, 256],
  "id": "combine-all-results",
  "name": "Combine All Results"
}
```

**Połączenie:**
```json
"Get Deleted": {
  "main": [
    [
      {
        "node": "Combine All Results",
        "type": "main",
        "index": 0
      }
    ]
  ]
}
```

---

#### **Krok 9: ZMIEŃ node "Process Results"**

**Lokalizacja w pliku:** Linia 824-836

**USUŃ ten node** i zastąp go nowym **"Final Summary":**

```json
{
  "parameters": {
    "jsCode": "// Podsumowanie końcowe\nconst stats = $json.statistics;\nconst summary = $json.changes_summary;\n\nreturn {\n  json: {\n    success: true,\n    message: \"Dokument pomyślnie przetworzony!\",\n    process_id: $json.metadata.process_id,\n    total_changes: stats.modified + stats.added + stats.deleted,\n    modified_count: summary.modified.count,\n    added_count: summary.added.count,\n    deleted_count: summary.deleted.count,\n    change_percentage: stats.change_percentage,\n    complete_json: $json\n  }\n};"
  },
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [2850, 256],
  "id": "final-summary-node",
  "name": "Final Summary"
}
```

**Połączenie:**
```json
"Combine All Results": {
  "main": [
    [
      {
        "node": "Final Summary",
        "type": "main",
        "index": 0
      }
    ]
  ]
}
```

---

#### **Krok 10: Podłącz do istniejącego workflow**

Znajdź node który pobiera dokumenty z BAW (prawdopodobnie "HTTP Request2" lub "insert_do_pobrania").

**ZMIEŃ połączenie:**

Zamiast kierować do AI Agent, podłącz do Merge Files:

```json
"insert_do_pobrania": {
  "main": [
    [
      {
        "node": "Merge Files",
        "type": "main",
        "index": 0
      }
    ]
  ]
}
```

---

## 📊 Finalny Flow

```
[Twój istniejący workflow]
         ↓
[insert_do_pobrania] → (pobiera dokumenty z BAW)
         ↓
   [Merge Files] → (łączy binary data)
         ↓
[Upload Documents] → http://217.182.76.146/api/documents/upload
         ↓
[Start Processing] → http://217.182.76.146/api/process
         ↓
  [Wait 3 Seconds]
         ↓
  [Check Status] ←─────┐
         ↓              │
  [Is Completed?]      │
     ↙        ↘         │
  [YES]      [NO]      │
    ↓         ↓        │
    ↓   [Wait 2s] ─────┘
    ↓
[Get Full Result] → /full
    ↓
[Get Modified] → /modified
    ↓
[Get Added] → /added
    ↓
[Get Deleted] → /deleted
    ↓
[Combine All Results] → (JavaScript - łączy wszystkie JSONy)
    ↓
[Final Summary] → (zwraca kompletny wynik)
```

---

## 🧪 Test

Po naprawieniu, uruchom workflow i sprawdź ostatni node "Final Summary":

```json
{
  "success": true,
  "message": "Dokument pomyślnie przetworzony!",
  "process_id": "abc123...",
  "total_changes": 25,
  "modified_count": 15,
  "added_count": 5,
  "deleted_count": 5,
  "change_percentage": 12.5,
  "complete_json": {
    "metadata": { ... },
    "statistics": { ... },
    "full_document": { ... },
    "changes_summary": { ... }
  }
}
```

---

## 📝 Podsumowanie zmian

| Node | Zmiana |
|------|--------|
| Upload Documents | URL: localhost → 217.182.76.146, data0/data1 → old_file/new_file |
| Start Processing | URL: localhost → 217.182.76.146, bodyParameters → jsonBody |
| Check Status | URL: localhost → 217.182.76.146 |
| Get Full Result | URL: localhost → 217.182.76.146 |
| Get Modified | URL: localhost → 217.182.76.146 |
| **Get Added** | **NOWY NODE** - pobiera dodane paragrafy |
| **Get Deleted** | **NOWY NODE** - pobiera usunięte paragrafy |
| **Combine All Results** | **NOWY NODE** - łączy wszystkie wyniki |
| **Final Summary** | **ZASTĄPIŁ Process Results** - zwraca kompletny JSON |

---

**Autor:** BAW Project
**Data:** 2025-10-23
