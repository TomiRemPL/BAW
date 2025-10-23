# 🔧 Modyfikacja dokumenty_wejsciowe.json - Krok Po Kroku

**Data:** 2025-10-23
**Cel:** Usunąć Dropbox, naprawić API BAW, dodać pełne pobieranie wyników

---

## 📋 Plan Działania

### ✅ Zachowujemy (nie ruszamy):
- Wszystkie nodes związane z BAW, SQL, SeaTable
- HTTP Request1 (login do BAW)
- HTTP Request2 (pobieranie plików z BAW)
- Code in JavaScript2 (łączenie binary data)
- Całą logikę biznesową (Select, Insert, Loop, If, Wait)

### ❌ Usuwamy (kompletnie):
1. **Read Old Document** (linia 650-663)
2. **Read New Document** (linia 664-677)
3. **Download a file** (linia 907-926)
4. **Download a file1** (linia 954-973)
5. **Download a file2** (linia 1118-1136)
6. **Upload a file** (linia 887-905)
7. **Edit Fields1** (linia 838-859)
8. **Code in JavaScript** (linia 860-872)
9. **Code in JavaScript1** (linia 873-885)
10. **Merge** (linia 927-941)
11. **Start** (linia 942-952) - START WORKFLOW
12. **Extract from File1** (linia 1046-1058)
13. **AI Agent1** (linia 988-1003)
14. **AI Agent2** (linia 1061-1075)
15. **OpenAI Chat Model3** (linia 1004-1028)
16. **OpenAI Chat Model5** (linia 1076-1100)
17. **Sticky Note3** (linia 1029-1044)
18. **Sticky Note7** (linia 1101-1116)

### 🔄 Modyfikujemy:
1. **Upload Documents** (linia 679-706) - naprawić URL i parametry
2. **Start Processing** (linia 707-730) - naprawić URL i body
3. **Check Status** (linia 746-759) - naprawić URL
4. **Get Full Result** (linia 796-809) - naprawić URL
5. **Get Modified** (linia 810-823) - naprawić URL
6. **Process Results** (linia 824-836) - ZASTĄPIĆ przez Combine All Results

### ➕ Dodajemy NOWE nodes:
1. **Get Added** - po "Get Modified"
2. **Get Deleted** - po "Get Added"
3. **Combine All Results** - po "Get Deleted"
4. **Final Summary** - na końcu

---

## 🛠️ Instrukcje Szczegółowe

### KROK 1: Otwórz plik w edytorze

Otwórz `C:\Projects\BAW\UslugaDoPorownan\dokumenty_wejsciowe.json` w **VSCode** lub **Notepad++**

---

### KROK 2: USUŃ nodes (18 bloków)

#### 2.1. Znajdź i USUŃ cały blok "Read Old Document"

**Szukaj:** `"name": "Read Old Document"`
**Linie:** ~650-663
**Usuń:** Cały blok od `{` do `},`

```json
// USUŃ TO:
{
  "parameters": {
    "filePath": "C:\\documents\\old_document.docx",
    "dataPropertyName": "old_file"
  },
  "id": "8ac0ec4b-f3ae-4aa6-a127-9e7d433da79e",
  "name": "Read Old Document",
  "type": "n8n-nodes-base.readBinaryFile",
  "typeVersion": 1,
  "position": [288, 1392],
  "retryOnFail": true
},
```

#### 2.2. Znajdź i USUŃ "Read New Document"

**Szukaj:** `"name": "Read New Document"`
**Usuń:** Cały blok

#### 2.3. Znajdź i USUŃ "Download a file"

**Szukaj:** `"name": "Download a file"`
**Usuń:** Cały blok (linia ~907-926)

#### 2.4. Znajdź i USUŃ "Download a file1"

**Szukaj:** `"name": "Download a file1"`
**Usuń:** Cały blok (linia ~954-973)

#### 2.5. Znajdź i USUŃ "Download a file2"

**Szukaj:** `"name": "Download a file2"`
**Usuń:** Cały blok (linia ~1118-1136)

#### 2.6. Znajdź i USUŃ "Upload a file"

**Szukaj:** `"name": "Upload a file"`
**Usuń:** Cały blok (linia ~887-905)

#### 2.7. Znajdź i USUŃ "Edit Fields1", "Code in JavaScript", "Code in JavaScript1"

**Szukaj kolejno każdego i usuń**

#### 2.8. Znajdź i USUŃ "Merge"

**Szukaj:** `"name": "Merge"`
**Usuń:** Cały blok (linia ~927-941)

#### 2.9. Znajdź i USUŃ "Start"

**Szukaj:** `"name": "Start"` (ten z position [, , 1824])
**Usuń:** Cały blok (linia ~942-952)

**UWAGA:** NIE usuwaj innych startów jak "Start Processing"!

#### 2.10. Znajdź i USUŃ wszystkie AI nodes

- "Extract from File1"
- "AI Agent1"
- "AI Agent2"
- "OpenAI Chat Model3"
- "OpenAI Chat Model5"
- "Sticky Note3" (GPT - analiza)
- "Sticky Note7" (GPT - analiza)

---

### KROK 3: NAPRAW istniejące nodes

#### 3.1. Napraw "Upload Documents"

**Znajdź:** `"name": "Upload Documents"`

**ZMIEŃ:**
```json
{
  "parameters": {
    "method": "POST",
    "url": "http://localhost:8001/api/documents/upload",  // ❌ STARE
    "sendBody": true,
    "contentType": "multipart-form-data",
    "bodyParameters": {
      "parameters": [
        {
          "name": "old_document",
          "value": "={{ $binary.data1 }}"  // ❌ STARE
        },
        {
          "name": "new_document",
          "value": "={{ $binary.data0 }}"  // ❌ STARE
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
    "url": "http://217.182.76.146/api/documents/upload",  // ✅ NOWE
    "sendBody": true,
    "contentType": "multipart-form-data",
    "bodyParameters": {
      "parameters": [
        {
          "name": "old_document",
          "inputDataFieldName": "=data1"  // ✅ NOWE
        },
        {
          "name": "new_document",
          "inputDataFieldName": "=data0"  // ✅ NOWE
        }
      ]
    },
    "options": {
      "timeout": 120000  // ✅ DODANE
    }
  }
}
```

#### 3.2. Napraw "Start Processing"

**Znajdź:** `"name": "Start Processing"`

**ZMIEŃ URL:**
```json
"url": "http://localhost:8001/api/process",  // ❌ STARE
```

**NA:**
```json
"url": "http://217.182.76.146/api/process",  // ✅ NOWE
```

**ZMIEŃ bodyParameters NA jsonBody:**
```json
"sendBody": true,
"bodyParameters": {
  "parameters": [
    {
      "name": "document_pair_id",
      "value": "={{ $('Upload Documents').item.json.document_pair_id }}"
    }
  ]
},
```

**NA:**
```json
"sendBody": true,
"contentType": "json",
"jsonBody": "={\n  \"document_pair_id\": \"{{ $json.document_pair_id }}\"\n}",
```

#### 3.3. Napraw "Check Status"

**Znajdź:** `"name": "Check Status"`

**ZMIEŃ:**
```json
"url": "=http://localhost:8001/api/status/..."
```

**NA:**
```json
"url": "=http://217.182.76.146/api/status/{{ $('Start Processing').item.json.process_id }}"
```

#### 3.4. Napraw "Get Full Result"

**Znajdź:** `"name": "Get Full Result"`

**ZMIEŃ:**
```json
"url": "=http://localhost:8001/api/result/..."
```

**NA:**
```json
"url": "=http://217.182.76.146/api/result/{{ $('Start Processing').item.json.process_id }}/full"
```

#### 3.5. Napraw "Get Modified"

**Znajdź:** `"name": "Get Modified"`

**ZMIEŃ:**
```json
"url": "=http://localhost:8001/api/result/..."
```

**NA:**
```json
"url": "=http://217.182.76.146/api/result/{{ $('Start Processing').item.json.process_id }}/modified"
```

---

### KROK 4: DODAJ nowe nodes

#### 4.1. Dodaj "Get Added"

**WSTAW PO "Get Modified"** (przed connection):

```json
{
  "parameters": {
    "url": "=http://217.182.76.146/api/result/{{ $('Start Processing').item.json.process_id }}/added",
    "options": {}
  },
  "id": "get-added-new-id",
  "name": "Get Added",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [2250, 256]
},
```

#### 4.2. Dodaj "Get Deleted"

**WSTAW PO "Get Added":**

```json
{
  "parameters": {
    "url": "=http://217.182.76.146/api/result/{{ $('Start Processing').item.json.process_id }}/deleted",
    "options": {}
  },
  "id": "get-deleted-new-id",
  "name": "Get Deleted",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [2450, 256]
},
```

#### 4.3. USUŃ "Process Results" i DODAJ "Combine All Results"

**Znajdź i USUŃ:** `"name": "Process Results"` (cały blok)

**DODAJ ZAMIAST:**

```json
{
  "parameters": {
    "jsCode": "// Łączenie wszystkich wyników w jeden obiekt JSON\nconst fullResult = $('Get Full Result').first().json;\nconst modifiedResult = $('Get Modified').first().json;\nconst addedResult = $('Get Added').first().json;\nconst deletedResult = $('Get Deleted').first().json;\n\nconst finalResult = {\n  metadata: {\n    process_id: fullResult.process_id,\n    document_pair_id: fullResult.document_pair_id,\n    generated_at: fullResult.generated_at,\n    timestamp: new Date().toISOString()\n  },\n  statistics: fullResult.statistics,\n  full_document: {\n    paragraphs: fullResult.paragraphs,\n    tables: fullResult.tables || []\n  },\n  changes_summary: {\n    modified: {\n      count: modifiedResult.total_count,\n      items: modifiedResult.modified_sentences\n    },\n    added: {\n      count: addedResult.total_count,\n      items: addedResult.added_sentences\n    },\n    deleted: {\n      count: deletedResult.total_count,\n      items: deletedResult.deleted_sentences\n    }\n  }\n};\n\nreturn { json: finalResult };"
  },
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [2650, 256],
  "id": "combine-all-results-id",
  "name": "Combine All Results"
},
```

#### 4.4. Dodaj "Final Summary"

**WSTAW NA KOŃCU nodes (przed `]`):**

```json
{
  "parameters": {
    "jsCode": "// Podsumowanie końcowe\nconst stats = $json.statistics;\nconst summary = $json.changes_summary;\n\nreturn {\n  json: {\n    success: true,\n    message: \"Dokument pomyślnie przetworzony!\",\n    process_id: $json.metadata.process_id,\n    total_changes: stats.modified + stats.added + stats.deleted,\n    modified_count: summary.modified.count,\n    added_count: summary.added.count,\n    deleted_count: summary.deleted.count,\n    change_percentage: stats.change_percentage,\n    complete_json: $json\n  }\n};"
  },
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [2850, 256],
  "id": "final-summary-new-id",
  "name": "Final Summary"
}
```

---

### KROK 5: NAPRAW connections

#### 5.1. Znajdź sekcję `"connections": {`

#### 5.2. USUŃ connections dla usuniętych nodes:

- "Read Old Document"
- "Read New Document"
- "Download a file"
- "Download a file1"
- "Download a file2"
- "Upload a file"
- "Edit Fields1"
- "Code in JavaScript"
- "Code in JavaScript1"
- "Merge"
- "Start"
- "Extract from File1"
- "AI Agent1", "AI Agent2"
- "OpenAI Chat Model3", "OpenAI Chat Model5"

#### 5.3. ZMIEŃ connection "Get Modified"

**ZMIEŃ:**
```json
"Get Modified": {
  "main": [
    [
      {
        "node": "Process Results",  // ❌ STARE
        "type": "main",
        "index": 0
      }
    ]
  ]
}
```

**NA:**
```json
"Get Modified": {
  "main": [
    [
      {
        "node": "Get Added",  // ✅ NOWE
        "type": "main",
        "index": 0
      }
    ]
  ]
}
```

#### 5.4. DODAJ nowe connections

**DODAJ PO "Get Modified":**

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
},
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
},
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

### KROK 6: Walidacja JSON

Przed zapisaniem:
1. Użyj **JSON Validator** (jsonlint.com)
2. Sprawdź czy brak przecinków na końcu ostatniego elementu
3. Sprawdź czy wszystkie nawiasy są zamknięte

---

## 🧪 Test

Po modyfikacji, zaimportuj do N8N i sprawdź:

1. ✅ HTTP Request2 pobiera plik z BAW (binary data w pamięci)
2. ✅ Code in JavaScript2 łączy binary data (data0, data1)
3. ✅ Upload Documents wysyła do http://217.182.76.146
4. ✅ Start Processing uruchamia porównanie
5. ✅ Loop polling czeka na zakończenie
6. ✅ Get Full Result, Modified, Added, Deleted - pobierają wyniki
7. ✅ Combine All Results - łączy wszystko w jeden JSON
8. ✅ Final Summary - zwraca podsumowanie z complete_json

---

## 📊 Finalny JSON

Ostatni node "Final Summary" zwróci:

```json
{
  "success": true,
  "message": "Dokument pomyślnie przetworzony!",
  "process_id": "abc-123",
  "total_changes": 25,
  "modified_count": 15,
  "added_count": 5,
  "deleted_count": 5,
  "change_percentage": 12.5,
  "complete_json": {
    "metadata": {...},
    "statistics": {...},
    "full_document": {
      "paragraphs": [...],
      "tables": [...]
    },
    "changes_summary": {
      "modified": {...},
      "added": {...},
      "deleted": {...}
    }
  }
}
```

---

**Autor:** BAW Project
**Data:** 2025-10-23
**Wersja:** Memory-Only (bez Dropbox)
