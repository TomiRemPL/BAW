# 📄 Integracja Raportów HTML w N8N Workflow

**Data:** 2025-10-23
**Wersja:** 1.0.0
**Cel:** Dodanie generowania raportów HTML do istniejącego workflow N8N

---

## 🎯 Przegląd

Ten przewodnik pokazuje jak dodać generowanie raportów HTML do workflow N8N. Raport HTML będzie:
- ✅ Generowany automatycznie po zakończeniu porównania
- ✅ Zawierał osadzone dane JSON (działa offline)
- ✅ Zapisany do Dropbox jako pojedynczy plik HTML
- ✅ Gotowy do otwarcia w przeglądarce bez dodatkowych zależności

---

## 📊 Rozszerzona Struktura Workflow

```
[... istniejący workflow ...]
    ↓
[8. Get Deleted] ← /deleted
    ↓
[9. Combine All Results]
    ↓
[10. Convert to JSON File]
    ↓
[11. Save JSON to Dropbox]
    ↓
✨ [12. Generate HTML Report] ← NOWY! /api/report/{process_id}/generate
    ↓
✨ [13. Download HTML Report] ← NOWY! GET /reports/{filename}
    ↓
✨ [14. Save HTML to Dropbox] ← NOWY! /BAW_Results/report_{process_id}.html
    ↓
[15. Final Summary]
    ↓
END
```

---

## 🔧 Krok po kroku: Dodawanie raportów HTML

### Krok 1: Dodaj node "Generate HTML Report"

**Pozycja w workflow:** Po "Save JSON to Dropbox", przed "Final Summary"

**Konfiguracja Node:**
```json
{
  "parameters": {
    "url": "http://217.182.76.146/api/report/{{$json[\"process_id\"]}}/generate",
    "method": "GET",
    "authentication": "none",
    "options": {
      "timeout": 60000
    },
    "responseFormat": "json"
  },
  "name": "Generate HTML Report",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.1,
  "position": [1400, 400]
}
```

**Co robi:**
- Wywołuje endpoint generowania raportu HTML
- Timeout: 60 sekund (wystarczający dla generowania HTML)
- Zwraca JSON z informacjami o wygenerowanym raporcie

**Output:**
```json
{
  "success": true,
  "process_id": "f1e2d3c4-...",
  "report_url": "/reports/report_f1e2d3c4-..._20251023_231438.html",
  "report_filename": "report_f1e2d3c4-..._20251023_231438.html",
  "report_path": "C:\\Projects\\BAW\\...",
  "generated_at": "2025-10-23T23:14:38.123456",
  "message": "Raport HTML został wygenerowany pomyślnie"
}
```

---

### Krok 2: Dodaj node "Download HTML Report"

**Pozycja:** Po "Generate HTML Report"

**Konfiguracja Node:**
```json
{
  "parameters": {
    "url": "=http://217.182.76.146{{$json[\"report_url\"]}}",
    "method": "GET",
    "authentication": "none",
    "options": {
      "timeout": 60000,
      "response": {
        "response": {
          "fullResponse": false,
          "responseFormat": "file"
        }
      }
    }
  },
  "name": "Download HTML Report",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.1,
  "position": [1600, 400]
}
```

**Kluczowe parametry:**
- `responseFormat`: **"file"** (pobiera jako binary data)
- `fullResponse`: **false** (tylko treść pliku)
- URL: Używa `report_url` z poprzedniego kroku

**Output:**
- Binary data (plik HTML)
- ~55+ KB
- Gotowy do zapisu

---

### Krok 3: Dodaj node "Save HTML to Dropbox"

**Pozycja:** Po "Download HTML Report"

**Opcja A: Dropbox (Upload File)**

```json
{
  "parameters": {
    "resource": "file",
    "operation": "upload",
    "path": "=/BAW_Results/Reports/{{$json[\"report_filename\"]}}",
    "binaryData": true,
    "options": {
      "mode": "overwrite"
    }
  },
  "name": "Save HTML to Dropbox",
  "type": "n8n-nodes-base.dropbox",
  "typeVersion": 2,
  "position": [1800, 400],
  "credentials": {
    "dropboxApi": {
      "id": "1",
      "name": "Dropbox account"
    }
  }
}
```

**Opcja B: Google Drive (Upload File)**

```json
{
  "parameters": {
    "resource": "file",
    "operation": "upload",
    "name": "={{$json[\"report_filename\"]}}",
    "parents": {
      "folderName": "/BAW_Results/Reports"
    },
    "binaryData": true,
    "options": {}
  },
  "name": "Save HTML to Google Drive",
  "type": "n8n-nodes-base.googleDrive",
  "typeVersion": 3,
  "position": [1800, 400],
  "credentials": {
    "googleDriveOAuth2Api": {
      "id": "2",
      "name": "Google Drive account"
    }
  }
}
```

**Opcja C: Email (jako załącznik)**

```json
{
  "parameters": {
    "resource": "message",
    "operation": "send",
    "to": "user@example.com",
    "subject": "=Raport porównania dokumentów - {{$json[\"process_id\"]}}",
    "message": "=Raport HTML został wygenerowany.\n\nProcess ID: {{$json[\"process_id\"]}}\nData: {{$json[\"generated_at\"]}}\n\nW załączniku znajduje się interaktywny raport HTML.\nOtwórz go w przeglądarce aby zobaczyć szczegóły.",
    "attachments": "={{$json[\"report_filename\"]}}",
    "options": {
      "attachmentsPropertyName": "data"
    }
  },
  "name": "Send Email with HTML Report",
  "type": "n8n-nodes-base.gmail",
  "typeVersion": 2,
  "position": [1800, 400],
  "credentials": {
    "gmailOAuth2": {
      "id": "3",
      "name": "Gmail account"
    }
  }
}
```

---

### Krok 4: Zaktualizuj "Final Summary"

**Dodaj informacje o raporcie HTML do końcowego podsumowania:**

```javascript
// W node "Final Summary" (type: Code/Function)
const processId = $input.first().json.process_id;
const reportFilename = $input.first().json.report_filename;
const reportUrl = $input.first().json.report_url;

// Dane z poprzednich kroków
const fullResult = $('Get Full Result').first().json;
const statistics = fullResult.statistics;

return {
  json: {
    success: true,
    process_id: processId,
    timestamp: new Date().toISOString(),

    // Statystyki
    statistics: {
      total_paragraphs: statistics.total_paragraphs,
      unchanged: statistics.unchanged,
      modified: statistics.modified,
      added: statistics.added,
      deleted: statistics.deleted,
      total_changes: statistics.total_changes,
      change_percentage: statistics.change_percentage
    },

    // Pliki wyjściowe
    output_files: {
      json: `/BAW_Results/${processId}.json`,
      html_report: `/BAW_Results/Reports/${reportFilename}`,
      html_report_url: `http://217.182.76.146${reportUrl}`
    },

    // Podsumowanie zmian
    summary: {
      severity: statistics.total_changes > 10 ? "HIGH" :
                statistics.total_changes > 5 ? "MEDIUM" : "LOW",
      requires_review: statistics.total_changes > 0,
      message: `Znaleziono ${statistics.total_changes} zmian w dokumencie`
    },

    message: "Przetwarzanie zakończone pomyślnie. Raport JSON i HTML zapisane."
  }
};
```

**Output przykład:**
```json
{
  "success": true,
  "process_id": "f1e2d3c4-...",
  "timestamp": "2025-10-23T23:15:00.000Z",
  "statistics": {
    "total_paragraphs": 64,
    "unchanged": 52,
    "modified": 12,
    "added": 0,
    "deleted": 0,
    "total_changes": 12,
    "change_percentage": 18.75
  },
  "output_files": {
    "json": "/BAW_Results/f1e2d3c4-....json",
    "html_report": "/BAW_Results/Reports/report_f1e2d3c4-..._20251023_231438.html",
    "html_report_url": "http://217.182.76.146/reports/report_f1e2d3c4-..._20251023_231438.html"
  },
  "summary": {
    "severity": "MEDIUM",
    "requires_review": true,
    "message": "Znaleziono 12 zmian w dokumencie"
  },
  "message": "Przetwarzanie zakończone pomyślnie. Raport JSON i HTML zapisane."
}
```

---

## 🔄 Kompletny Workflow JSON (fragmenty do dodania)

### Node 12: Generate HTML Report

```json
{
  "id": "generate-html-report",
  "name": "Generate HTML Report",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.1,
  "position": [1400, 400],
  "parameters": {
    "url": "http://217.182.76.146/api/report/{{$json[\"process_id\"]}}/generate",
    "method": "GET",
    "authentication": "none",
    "options": {
      "timeout": 60000
    },
    "responseFormat": "json"
  }
}
```

### Node 13: Download HTML Report

```json
{
  "id": "download-html-report",
  "name": "Download HTML Report",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.1,
  "position": [1600, 400],
  "parameters": {
    "url": "=http://217.182.76.146{{$json[\"report_url\"]}}",
    "method": "GET",
    "authentication": "none",
    "options": {
      "timeout": 60000,
      "response": {
        "response": {
          "fullResponse": false,
          "responseFormat": "file"
        }
      }
    }
  }
}
```

### Node 14: Save HTML to Dropbox

```json
{
  "id": "save-html-dropbox",
  "name": "Save HTML to Dropbox",
  "type": "n8n-nodes-base.dropbox",
  "typeVersion": 2,
  "position": [1800, 400],
  "parameters": {
    "resource": "file",
    "operation": "upload",
    "path": "=/BAW_Results/Reports/{{$json[\"report_filename\"]}}",
    "binaryData": true,
    "options": {
      "mode": "overwrite"
    }
  },
  "credentials": {
    "dropboxApi": {
      "id": "1",
      "name": "Dropbox account"
    }
  }
}
```

### Connections (dodatkowe)

```json
{
  "connections": {
    "Save JSON to Dropbox": {
      "main": [
        [
          {
            "node": "Generate HTML Report",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate HTML Report": {
      "main": [
        [
          {
            "node": "Download HTML Report",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Download HTML Report": {
      "main": [
        [
          {
            "node": "Save HTML to Dropbox",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Save HTML to Dropbox": {
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
  }
}
```

---

## 🧪 Testowanie

### Test 1: Pojedynczy raport

1. **Uruchom workflow** z parą dokumentów
2. **Sprawdź logi** node "Generate HTML Report":
   ```
   ✅ Success: true
   ✅ Report URL: /reports/report_...html
   ```
3. **Sprawdź Dropbox** - powinny być 2 pliki:
   - `{process_id}.json` (wyniki JSON)
   - `Reports/report_{process_id}_{timestamp}.html` (raport HTML)
4. **Pobierz HTML** z Dropbox i otwórz w przeglądarce
5. **Sprawdź** czy raport wyświetla się poprawnie (auto-display)

### Test 2: Error handling

**Scenariusz:** Nieprawidłowy process_id

```
Input do "Generate HTML Report":
{
  "process_id": "invalid-id-12345"
}

Expected Output:
{
  "statusCode": 404,
  "error": "Not Found",
  "message": "Nie znaleziono wyników dla process_id: invalid-id-12345"
}
```

**Dodaj error handling:**

```json
{
  "parameters": {
    "url": "...",
    "options": {
      "response": {
        "response": {
          "neverError": true
        }
      }
    }
  }
}
```

Następnie dodaj node "Check if Report Generated":

```javascript
// Code node po "Generate HTML Report"
const response = $input.first().json;

if (response.success === true) {
  return {
    json: response
  };
} else {
  // Błąd - nie generuj raportu HTML, przejdź do Final Summary
  throw new Error(`Nie udało się wygenerować raportu: ${response.message || 'Unknown error'}`);
}
```

---

## ⚙️ Konfiguracja zaawansowana

### Opcja 1: Warunkowe generowanie (tylko jeśli są zmiany)

**Dodaj node "Check if Changes Exist" po "Get Full Result":**

```javascript
// Code node
const statistics = $input.first().json.statistics;

if (statistics.total_changes > 0) {
  // Są zmiany - generuj raport HTML
  return {
    json: {
      generate_report: true,
      process_id: $input.first().json.process_id
    }
  };
} else {
  // Brak zmian - pomiń raport HTML
  return {
    json: {
      generate_report: false,
      process_id: $input.first().json.process_id
    }
  };
}
```

**Dodaj IF node:**

```json
{
  "parameters": {
    "conditions": {
      "boolean": [
        {
          "value1": "={{$json[\"generate_report\"]}}",
          "value2": true
        }
      ]
    }
  },
  "name": "IF Changes Exist",
  "type": "n8n-nodes-base.if",
  "position": [1300, 400]
}
```

**Routing:**
- TRUE → Generate HTML Report
- FALSE → Final Summary (bez raportu HTML)

### Opcja 2: Automatyczne wysyłanie emaila z raportem

**Node: Send Email with Report**

```json
{
  "parameters": {
    "resource": "message",
    "operation": "send",
    "to": "={{$json[\"recipient_email\"]}}",
    "subject": "=Raport porównania dokumentów - {{$json[\"process_id\"]}}",
    "emailType": "html",
    "message": "=<html>\n<body>\n  <h2>Raport Porównania Dokumentów</h2>\n  \n  <p><strong>Process ID:</strong> {{$json[\"process_id\"]}}</p>\n  <p><strong>Data:</strong> {{$json[\"generated_at\"]}}</p>\n  \n  <h3>Statystyki:</h3>\n  <ul>\n    <li>Total Changes: {{$json[\"statistics\"][\"total_changes\"]}}</li>\n    <li>Modified: {{$json[\"statistics\"][\"modified\"]}}</li>\n    <li>Added: {{$json[\"statistics\"][\"added\"]}}</li>\n    <li>Deleted: {{$json[\"statistics\"][\"deleted\"]}}</li>\n  </ul>\n  \n  <p>W załączniku znajduje się interaktywny raport HTML.<br>\n  Otwórz go w przeglądarce aby zobaczyć szczegóły wszystkich zmian.</p>\n  \n  <p><a href=\"http://217.182.76.146{{$json[\"report_url\"]}}\">Otwórz raport online</a></p>\n</body>\n</html>",
    "attachments": "report",
    "options": {
      "attachmentsPropertyName": "data"
    }
  },
  "name": "Send Email with Report",
  "type": "n8n-nodes-base.gmail"
}
```

### Opcja 3: Webhook notification

**Wyślij webhook do innego systemu gdy raport jest gotowy:**

```json
{
  "parameters": {
    "url": "https://your-system.com/api/webhook",
    "method": "POST",
    "authentication": "none",
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={\n  \"event\": \"report_generated\",\n  \"process_id\": \"{{$json[\"process_id\"]}}\",\n  \"report_url\": \"http://217.182.76.146{{$json[\"report_url\"]}}\",\n  \"report_filename\": \"{{$json[\"report_filename\"]}}\",\n  \"statistics\": {{$json[\"statistics\"]}}\n}",
    "options": {}
  },
  "name": "Send Webhook Notification",
  "type": "n8n-nodes-base.httpRequest"
}
```

---

## 📊 Performance

### Czas wykonania (dodatkowe nodes)

| Node | Średni czas | Uwagi |
|------|-------------|-------|
| Generate HTML Report | 1-3s | Zależy od rozmiaru danych JSON |
| Download HTML Report | 1-2s | ~55 KB transfer |
| Save HTML to Dropbox | 2-5s | Zależy od połączenia |
| **Łącznie dodatkowe** | **4-10s** | Akceptowalne dla workflow |

### Optymalizacja

**Równoległe wykonanie (parallel processing):**

```
[Save JSON to Dropbox] ──┬→ [Generate HTML Report] → [Download] → [Save HTML]
                         └→ [Send Email Notification]
                         └→ [Update Database]
                                ↓
                         [Wait for All] → [Final Summary]
```

Użyj node **"Wait"** z opcją **"Wait for all branches"**

---

## 🔧 Troubleshooting

### Problem 1: 404 Not Found przy generowaniu

**Objaw:**
```json
{
  "statusCode": 404,
  "detail": "Nie znaleziono wyników dla process_id: ..."
}
```

**Rozwiązanie:**
1. Sprawdź czy process_id jest poprawny
2. Sprawdź logi "Get Full Result" - czy zakończył się sukcesem
3. Dodaj wait 1-2s przed generowaniem raportu

### Problem 2: Raport HTML jest pusty

**Objaw:** Plik HTML istnieje ale nie wyświetla danych

**Rozwiązanie:**
1. Sprawdź response z "Generate HTML Report":
   ```javascript
   if (response.success !== true) {
     throw new Error('Report generation failed');
   }
   ```
2. Sprawdź rozmiar pliku (powinien być ~55+ KB)
3. Sprawdź logi backendu: `tail -f output/app.log | grep "generate_html_report"`

### Problem 3: Timeout przy pobieraniu

**Objaw:** Request timeout po 30-60s

**Rozwiązanie:**
Zwiększ timeout w node "Download HTML Report":
```json
{
  "options": {
    "timeout": 120000  // 120 sekund
  }
}
```

### Problem 4: Dropbox upload error

**Objaw:**
```
Error: Failed to upload file to Dropbox
```

**Rozwiązanie:**
1. Sprawdź credentials Dropbox
2. Sprawdź czy folder `/BAW_Results/Reports/` istnieje
3. Sprawdź czy binary data jest dostępne:
   ```javascript
   // Debug node przed Save to Dropbox
   console.log('Binary data:', $input.first().binary);
   ```

---

## 📚 Przykładowy kompletny workflow

### Import do N8N

Skopiuj poniższy JSON i zaimportuj do N8N:

```json
{
  "name": "BAW Document Comparison with HTML Report",
  "nodes": [
    {
      "id": "start",
      "name": "Start",
      "type": "n8n-nodes-base.start",
      "position": [240, 300]
    },
    {
      "id": "upload-docs",
      "name": "Upload Documents",
      "type": "n8n-nodes-base.httpRequest",
      "position": [440, 300],
      "parameters": {
        "url": "http://217.182.76.146/api/documents/upload",
        "method": "POST"
      }
    },
    {
      "id": "start-processing",
      "name": "Start Processing",
      "type": "n8n-nodes-base.httpRequest",
      "position": [640, 300],
      "parameters": {
        "url": "http://217.182.76.146/api/process",
        "method": "POST"
      }
    },
    {
      "id": "wait-processing",
      "name": "Wait for Processing",
      "type": "n8n-nodes-base.wait",
      "position": [840, 300]
    },
    {
      "id": "get-full-result",
      "name": "Get Full Result",
      "type": "n8n-nodes-base.httpRequest",
      "position": [1040, 300],
      "parameters": {
        "url": "=http://217.182.76.146/api/result/{{$json[\"process_id\"]}}/full",
        "method": "GET"
      }
    },
    {
      "id": "save-json-dropbox",
      "name": "Save JSON to Dropbox",
      "type": "n8n-nodes-base.dropbox",
      "position": [1240, 300],
      "parameters": {
        "resource": "file",
        "operation": "upload"
      }
    },
    {
      "id": "generate-html",
      "name": "Generate HTML Report",
      "type": "n8n-nodes-base.httpRequest",
      "position": [1440, 300],
      "parameters": {
        "url": "=http://217.182.76.146/api/report/{{$json[\"process_id\"]}}/generate",
        "method": "GET"
      }
    },
    {
      "id": "download-html",
      "name": "Download HTML Report",
      "type": "n8n-nodes-base.httpRequest",
      "position": [1640, 300],
      "parameters": {
        "url": "=http://217.182.76.146{{$json[\"report_url\"]}}",
        "method": "GET",
        "options": {
          "response": {
            "response": {
              "responseFormat": "file"
            }
          }
        }
      }
    },
    {
      "id": "save-html-dropbox",
      "name": "Save HTML to Dropbox",
      "type": "n8n-nodes-base.dropbox",
      "position": [1840, 300],
      "parameters": {
        "resource": "file",
        "operation": "upload",
        "path": "=/BAW_Results/Reports/{{$json[\"report_filename\"]}}",
        "binaryData": true
      }
    },
    {
      "id": "final-summary",
      "name": "Final Summary",
      "type": "n8n-nodes-base.code",
      "position": [2040, 300],
      "parameters": {
        "jsCode": "return [{ json: { success: true, message: 'Done' } }]"
      }
    }
  ],
  "connections": {
    "start": { "main": [[{ "node": "upload-docs" }]] },
    "upload-docs": { "main": [[{ "node": "start-processing" }]] },
    "start-processing": { "main": [[{ "node": "wait-processing" }]] },
    "wait-processing": { "main": [[{ "node": "get-full-result" }]] },
    "get-full-result": { "main": [[{ "node": "save-json-dropbox" }]] },
    "save-json-dropbox": { "main": [[{ "node": "generate-html" }]] },
    "generate-html": { "main": [[{ "node": "download-html" }]] },
    "download-html": { "main": [[{ "node": "save-html-dropbox" }]] },
    "save-html-dropbox": { "main": [[{ "node": "final-summary" }]] }
  }
}
```

---

## 📝 Podsumowanie

### Co zostało dodane:

1. ✅ **Node: Generate HTML Report** - wywołuje endpoint generowania
2. ✅ **Node: Download HTML Report** - pobiera wygenerowany plik HTML
3. ✅ **Node: Save HTML to Dropbox** - zapisuje HTML do Dropbox
4. ✅ **Zaktualizowany Final Summary** - zawiera informacje o raporcie HTML

### Korzyści:

- ✅ **Offline viewing** - raport działa bez serwera
- ✅ **Single file** - wszystkie dane w jednym pliku HTML
- ✅ **Interactive** - filtry, hover effects, responsive
- ✅ **Archival** - łatwe przechowywanie i udostępnianie
- ✅ **No dependencies** - nie wymaga dodatkowych bibliotek

### Następne kroki:

1. Zaimportuj workflow do N8N
2. Skonfiguruj credentials (Dropbox/Gmail)
3. Przetestuj z przykładowymi dokumentami
4. Dostosuj routing według potrzeb (email, webhook, etc.)

---

## 📚 Powiązane dokumenty

- **[HTML_REPORT_ENDPOINT.md](HTML_REPORT_ENDPOINT.md)** - Szczegółowa dokumentacja endpointu
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Kompletna dokumentacja API
- **[N8N_WORKFLOW_GUIDE.md](N8N_WORKFLOW_GUIDE.md)** - Podstawowy workflow N8N
- **[N8N_INTEGRATION.md](N8N_INTEGRATION.md)** - Wprowadzenie do integracji N8N

---

**Data utworzenia:** 2025-10-23
**Wersja:** 1.0.0
**Autor:** TomiRemPL + Claude Code (Anthropic)
**Status:** ✅ Ready to use
