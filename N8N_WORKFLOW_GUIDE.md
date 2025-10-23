# 📋 Przewodnik N8N Workflow - BAW Document Comparison

**Data:** 2025-10-23
**Wersja:** 2.0 (Zaktualizowana)
**Plik:** `dokumenty_wejsciowe_UPDATED.json`

---

## 🎯 Co robi ten workflow?

Workflow automatycznie:
1. ✅ Pobiera dwa dokumenty z Dropbox (stara i nowa wersja)
2. ✅ Wysyła je do API BAW na porcie 80 (przez Nginx)
3. ✅ Czeka na zakończenie przetwarzania (loop z polling)
4. ✅ Pobiera **WSZYSTKIE** typy zmian (full, modified, added, deleted)
5. ✅ Łączy wyniki w jeden kompletny plik JSON
6. ✅ Zapisuje plik JSON do Dropbox
7. ✅ Zwraca podsumowanie

---

## 🔄 Zmiany w stosunku do starej wersji

### ❌ Stara wersja (problemy):
- Używała `http://localhost:8001` (nie działa z N8N)
- Błędne parametry uploadu (`data0`, `data1`)
- Brak pobierania added/deleted
- Brak zapisu wyników do pliku

### ✅ Nowa wersja (UPDATED):
- **URL zmienione** na `http://217.182.76.146` (Nginx port 80)
- **Naprawiony upload** - używa `old_file` i `new_file`
- **Pobiera wszystkie typy zmian:**
  - `/full` - pełny dokument ze wszystkimi paragrafami
  - `/modified` - tylko zmodyfikowane fragmenty
  - `/added` - tylko dodane fragmenty
  - `/deleted` - tylko usunięte fragmenty
- **Łączy wyniki** w jeden JSON
- **Zapisuje do Dropbox** jako plik JSON
- **Zwraca podsumowanie** z statystykami

---

## 📊 Struktura Workflow (12 kroków)

```
START
  ↓
[Download New Document] ──┐
[Download Old Document] ──┤
                          ↓
                   [Merge Files]
                          ↓
            [1. Upload Documents to BAW] ← http://217.182.76.146/api/documents/upload
                          ↓
              [2. Start Processing] ← http://217.182.76.146/api/process
                          ↓
                [Wait 3 Seconds]
                          ↓
                 [3. Check Status] ← http://217.182.76.146/api/status/{id}
                          ↓
              [4. Is Completed?]
                   ↙     ↘
             [YES]      [NO → Wait 2s → Loop back to Check Status]
                ↓
    [5. Get Full Result] ← /full
                ↓
    [6. Get Modified] ← /modified
                ↓
    [7. Get Added] ← /added
                ↓
    [8. Get Deleted] ← /deleted
                ↓
    [9. Combine All Results] (JavaScript)
                ↓
    [10. Convert to JSON File]
                ↓
    [11. Save to Dropbox] (/BAW_Results/{process_id}.json)
                ↓
    [12. Final Summary]
                ↓
              END
```

---

## 📁 Struktura Finalnego JSON

```json
{
  "metadata": {
    "process_id": "f1e2d3c4-...",
    "document_pair_id": "a1b2c3d4-...",
    "generated_at": "2025-10-23T12:34:56",
    "timestamp": "2025-10-23T12:35:00"
  },
  "statistics": {
    "total_paragraphs": 100,
    "unchanged": 70,
    "modified": 20,
    "added": 5,
    "deleted": 5,
    "change_percentage": 30.0
  },
  "full_document": {
    "paragraphs": [
      {
        "index": 0,
        "type": "unchanged|modified|added|deleted",
        "text": "Treść paragrafu...",
        "old_text": "Stara treść (dla modified/deleted)",
        "changes": [
          {
            "type": "insert|delete|equal",
            "text": "zmieniony fragment",
            "position": 10
          }
        ]
      }
    ],
    "tables": [...]
  },
  "changes_summary": {
    "modified": {
      "count": 20,
      "items": [
        {
          "paragraph_index": 5,
          "old_text": "Stary tekst",
          "new_text": "Nowy tekst",
          "changes": [...]
        }
      ]
    },
    "added": {
      "count": 5,
      "items": [
        {
          "paragraph_index": 10,
          "text": "Nowy paragraf"
        }
      ]
    },
    "deleted": {
      "count": 5,
      "items": [
        {
          "paragraph_index": 15,
          "text": "Usunięty paragraf"
        }
      ]
    }
  }
}
```

---

## 🚀 Jak zaimportować i uruchomić?

### Krok 1: Import do N8N

1. Otwórz N8N
2. Menu → **Workflows** → **Import from File**
3. Wybierz plik: `C:\Projects\BAW\UslugaDoPorownan\dokumenty_wejsciowe_UPDATED.json`
4. Kliknij **Import**

### Krok 2: Skonfiguruj Credentials

**Dropbox (jeśli nie masz):**
1. Idź do: https://www.dropbox.com/developers/apps
2. Utwórz app → Wybierz "Scoped access" → "Full Dropbox"
3. Skopiuj **App key** i **App secret**
4. W N8N: **Credentials** → **Create New** → **Dropbox API**
5. Wklej credentials i autoryzuj

### Krok 3: Zmień ścieżki do plików

W nodes **"Download New Document"** i **"Download Old Document"**:

```yaml
# Zmień ścieżki na swoje pliki w Dropbox:
path: "/Twoj_folder/stara_wersja.docx"
path: "/Twoj_folder/nowa_wersja.docx"
```

### Krok 4: Uruchom Workflow

1. Kliknij **"Execute Workflow"** (przycisk play ▶️)
2. Obserwuj postęp wykonywania
3. Po zakończeniu sprawdź **node "12. Final Summary"** - zobaczysz:

```json
{
  "success": true,
  "message": "Dokument pomyślnie przetworzony!",
  "process_id": "...",
  "total_changes": 30,
  "modified_count": 20,
  "added_count": 5,
  "deleted_count": 5,
  "change_percentage": 30.0,
  "file_saved": "BAW_Results/f1e2d3c4-....json"
}
```

4. **Plik JSON** zostanie zapisany w Dropbox: `/BAW_Results/{process_id}.json`

---

## 🔍 Troubleshooting

### Problem 1: "Connection refused" lub "Timeout"

**Przyczyna:** API nie jest dostępne lub firewall blokuje.

**Rozwiązanie:**
```bash
# Na serwerze sprawdź:
sudo systemctl status baw-backend
sudo systemctl status nginx

# Test z twojego komputera:
curl http://217.182.76.146/health
```

### Problem 2: Upload zwraca błąd 400

**Przyczyna:** Złe parametry binary data.

**Rozwiązanie:**
- Sprawdź czy node "Merge Files" łączy oba pliki
- Sprawdź czy binary fields to `old_file` i `new_file`

### Problem 3: Loop działa w nieskończoność

**Przyczyna:** Status nigdy nie wraca "completed".

**Rozwiązanie:**
```bash
# Sprawdź logi backendu:
sudo journalctl -u baw-backend -n 100

# Sprawdź status ręcznie:
curl http://217.182.76.146/api/status/{process_id}
```

### Problem 4: Brak pliku w Dropbox

**Przyczyna:** Błąd zapisu lub brak uprawnień.

**Rozwiązanie:**
- Sprawdź credentials Dropbox w N8N
- Sprawdź czy folder `/BAW_Results/` istnieje (utwórz ręcznie)

---

## 📝 Dostosowanie Workflow

### Zmiana źródła dokumentów

Obecnie workflow pobiera z Dropbox. Możesz zmienić na:

**Opcja A: Lokalne pliki**
```yaml
# Zamiast "Download from Dropbox"
# Użyj "Read Binary File":
type: n8n-nodes-base.readBinaryFile
parameters:
  filePath: "C:\\documents\\old.docx"
  dataPropertyName: "old_file"
```

**Opcja B: HTTP Request (pobieranie z URL)**
```yaml
type: n8n-nodes-base.httpRequest
parameters:
  method: GET
  url: "https://twoja-strona.pl/old.docx"
  options:
    response:
      responseFormat: "file"
```

**Opcja C: Google Drive**
```yaml
type: n8n-nodes-base.googleDrive
parameters:
  operation: "download"
  fileId: "1ABC..."
```

### Dodanie powiadomień

Dodaj node **"Send Email"** po "12. Final Summary":

```yaml
type: n8n-nodes-base.emailSend
parameters:
  toEmail: "twoj-email@example.com"
  subject: "BAW: Dokument przetworzony"
  text: "Znaleziono {{ $json.total_changes }} zmian"
```

### Zapis do bazy danych

Dodaj node **"Postgres"** zamiast Dropbox:

```yaml
type: n8n-nodes-base.postgres
parameters:
  operation: "insert"
  table: "document_comparisons"
  columns: "process_id, total_changes, json_data"
```

---

## 🎨 Wizualizacja Flow

```
┌─────────────────────────────────────────────────────────────┐
│  ETAP 1: Pobranie dokumentów                                │
│  ┌──────────────┐    ┌──────────────┐                       │
│  │ New Document │    │ Old Document │                       │
│  │  (Dropbox)   │    │  (Dropbox)   │                       │
│  └──────┬───────┘    └──────┬───────┘                       │
│         └──────────┬─────────┘                               │
│                    ↓                                         │
│             ┌─────────────┐                                  │
│             │ Merge Files │                                  │
│             └──────┬──────┘                                  │
└────────────────────┼──────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  ETAP 2: Upload do BAW API                                  │
│             ┌──────────────────────┐                         │
│             │ Upload Documents     │                         │
│             │ (BAW API - Nginx)    │                         │
│             └──────┬───────────────┘                         │
│                    ↓                                         │
│             ┌──────────────────────┐                         │
│             │ Start Processing     │                         │
│             └──────┬───────────────┘                         │
└────────────────────┼──────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  ETAP 3: Polling (czekanie na wynik)                        │
│             ┌──────────────────────┐                         │
│             │ Wait 3 Seconds       │                         │
│             └──────┬───────────────┘                         │
│                    ↓                                         │
│      ┌─────────────────────────────┐                         │
│      │  Check Status (Loop)        │←──────┐                 │
│      └─────────┬───────────────────┘       │                 │
│                ↓                            │                 │
│         ┌─────────────┐                    │                 │
│         │ Completed?  │──NO→ Wait 2s ──────┘                 │
│         └──────┬──────┘                                      │
│                YES                                            │
└────────────────┼──────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  ETAP 4: Pobieranie wszystkich wyników                      │
│      ┌─────────────────┐                                    │
│      │ Get Full Result │                                    │
│      └────────┬─────────┘                                    │
│               ↓                                              │
│      ┌─────────────────┐                                    │
│      │ Get Modified    │                                    │
│      └────────┬─────────┘                                    │
│               ↓                                              │
│      ┌─────────────────┐                                    │
│      │ Get Added       │                                    │
│      └────────┬─────────┘                                    │
│               ↓                                              │
│      ┌─────────────────┐                                    │
│      │ Get Deleted     │                                    │
│      └────────┬─────────┘                                    │
└───────────────┼──────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────────────────────┐
│  ETAP 5: Przetwarzanie i zapis                              │
│      ┌─────────────────────┐                                │
│      │ Combine All Results │ (JavaScript)                   │
│      └────────┬────────────┘                                │
│               ↓                                              │
│      ┌─────────────────────┐                                │
│      │ Convert to JSON     │                                │
│      └────────┬────────────┘                                │
│               ↓                                              │
│      ┌─────────────────────┐                                │
│      │ Save to Dropbox     │ (/BAW_Results/...)             │
│      └────────┬────────────┘                                │
│               ↓                                              │
│      ┌─────────────────────┐                                │
│      │ Final Summary       │ (Podsumowanie)                 │
│      └─────────────────────┘                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 Powiązane dokumenty

- **[API_DOCUMENTATION.md](../API_DOCUMENTATION.md)** - Pełna dokumentacja API
- **[N8N_INTEGRATION.md](../N8N_INTEGRATION.md)** - Integracja z N8N
- **[test.prod.http](../test.prod.http)** - Testy API (REST Client)

---

## ✅ Checklist przed uruchomieniem

- [ ] Serwer BAW działa (`sudo systemctl status baw-backend`)
- [ ] Nginx działa (`sudo systemctl status nginx`)
- [ ] API odpowiada (`curl http://217.182.76.146/health`)
- [ ] Credentials Dropbox skonfigurowane w N8N
- [ ] Ścieżki do plików w Dropbox są poprawne
- [ ] Folder `/BAW_Results/` istnieje w Dropbox

---

**Autor:** BAW Project
**Data:** 2025-10-23
**Wersja:** 2.0
