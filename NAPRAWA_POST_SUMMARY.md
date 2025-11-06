# Naprawa Node "POST Summary to API"

## ❌ Problem

Node **"POST Summary to API"** w workflow używał niepoprawnego formatu body - `bodyParameters` zamiast JSON.

### Objawy:
- Błąd przy wysyłaniu POST do `/api/summary`
- Backend API nie otrzymuje danych w formacie JSON
- Możliwy błąd 400 Bad Request lub 422 Unprocessable Entity

---

## 🔍 Analiza

### ❌ Niepoprawna konfiguracja (API 06):

```json
{
  "method": "POST",
  "url": "http://217.182.76.146/api/summary",
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "process_id",
        "value": "={{ $('Start Processing').item.json.process_id }}"
      },
      {
        "name": "summary_text",
        "value": "={{ $('AI Agent4').item.json.output }}"
      },
      {
        "name": "metadata",
        "value": "={{ { \"przedmiot_regulacji\": \"Dokument\", ... } }}"
      }
    ]
  }
}
```

**Problem:** `bodyParameters` wysyła dane jako **form-data** (`application/x-www-form-urlencoded`), a nie jako JSON!

---

## ✅ Rozwiązanie

### ✅ Poprawna konfiguracja (API 08):

```json
{
  "method": "POST",
  "url": "http://217.182.76.146/api/summary",
  "authentication": "none",
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "={{ JSON.stringify({
    process_id: $('Start Processing').item.json.process_id,
    summary_text: $('AI Agent4').item.json.output,
    metadata: {
      przedmiot_regulacji: \"Dokument\",
      data_aktu: \"\",
      data_wejscia_w_zycie: \"\"
    }
  }) }}",
  "options": {
    "timeout": 30000
  }
}
```

**Kluczowe zmiany:**
1. ✅ `specifyBody: "json"` - określa że wysyłamy JSON
2. ✅ `jsonBody` - zawiera wyrażenie n8n z `JSON.stringify()`
3. ✅ Usunięto `bodyParameters`

---

## 🔧 Jak to naprawić

### Automatycznie (zalecane):

```bash
cd C:\Projects\BAW
python fix_post_summary_v2.py
```

To wygeneruje plik **`API 08 - fixed POST v2.json`** z naprawionym nodem.

### Ręcznie w n8n:

1. Otwórz workflow w n8n
2. Kliknij node **"POST Summary to API"**
3. W sekcji **Body**:
   - Wybierz: **"JSON"**
   - W polu JSON wklej:
     ```javascript
     ={{ JSON.stringify({
       process_id: $('Start Processing').item.json.process_id,
       summary_text: $('AI Agent4').item.json.output,
       metadata: {
         przedmiot_regulacji: "Dokument",
         data_aktu: "",
         data_wejscia_w_zycie: ""
       }
     }) }}
     ```
4. Zapisz workflow

---

## 📊 Porównanie

| Element | PRZED (błędne) | PO (poprawne) |
|---------|----------------|---------------|
| **Body type** | bodyParameters | jsonBody |
| **Content-Type** | application/x-www-form-urlencoded | application/json |
| **Format** | Form data | JSON string |
| **specifyBody** | brak | "json" |
| **Składnia** | Parameters array | JSON.stringify() |

---

## 🧪 Test

### Przed naprawą:
```bash
# Request wyglądał tak (form-data):
POST /api/summary HTTP/1.1
Content-Type: application/x-www-form-urlencoded

process_id={{ ... }}&summary_text={{ ... }}&metadata={{ ... }}
```

### Po naprawie:
```bash
# Request wygląda tak (JSON):
POST /api/summary HTTP/1.1
Content-Type: application/json

{
  "process_id": "abc-123",
  "summary_text": "Podsumowanie...",
  "metadata": {
    "przedmiot_regulacji": "Dokument",
    "data_aktu": "",
    "data_wejscia_w_zycie": ""
  }
}
```

---

## ✅ Weryfikacja

Po imporcie **API 08 - fixed POST v2.json**:

1. **Sprawdź node** "POST Summary to API":
   - Body → JSON ✅
   - jsonBody zawiera `JSON.stringify()` ✅

2. **Test workflow**:
   ```
   Uruchom workflow → sprawdź logi node "POST Summary to API"
   ```

3. **Oczekiwany wynik**:
   ```json
   {
     "process_id": "...",
     "status": "pending_review",
     "created_at": "...",
     ...
   }
   ```

---

## 📁 Pliki

### Wersje workflow:

| Plik | Status | Opis |
|------|--------|------|
| API 04.json | ❌ | Bazowy (bez summary) |
| API 05.json | ❌ | +10 nodów summary |
| API 06.json | ❌ | +link w mailu |
| API 07.json | ⚠️ | Próba naprawy #1 (niepoprawna składnia) |
| **API 08.json** | ✅ | **Naprawiony POST (użyj tego!)** |

### Skrypty naprawy:

- `fix_post_summary_node.py` - Wersja 1 (niepoprawna)
- `fix_post_summary_v2.py` - Wersja 2 (poprawna) ✅

---

## 🎯 Workflow gotowy do importu:

**Plik:** `API 08 - fixed POST v2.json`

**Zawiera:**
- ✅ 60 nodów (50 oryginalnych + 10 dla summary)
- ✅ Link w emailu: `http://217.182.76.146/summary/{id}`
- ✅ Poprawnie działający POST Summary to API
- ✅ Wszystkie połączenia zachowane

---

## 🐛 Dlaczego to się stało?

Podczas automatycznego generowania workflow (przez `extend_workflow.py`), node został utworzony z `bodyParameters` zamiast `jsonBody`.

**Przyczyna:** Kod generujący użył składni dla **form-data** zamiast **JSON body**.

**Lekcja:** Przy tworzeniu nodów HTTP Request w n8n zawsze używać:
- `specifyBody: "json"`
- `jsonBody` z `JSON.stringify()`

---

## 📚 Dokumentacja n8n

### HTTP Request Node - JSON Body

Składnia n8n dla JSON body:

```javascript
={{ JSON.stringify({
  field1: $('NodeName').item.json.value1,
  field2: "static value",
  nested: {
    key: $('NodeName').item.json.value2
  }
}) }}
```

**Ważne:**
- Używaj `JSON.stringify()` aby przekonwertować obiekt na string
- Nie używaj `toJsonString()` - to nie działa dla całego obiektu
- Odwołania do innych nodów: `$('NodeName').item.json.field`

---

## ✅ Checklist

Po imporcie nowego workflow sprawdź:

- [ ] Node "POST Summary to API" używa JSON body
- [ ] jsonBody zawiera `JSON.stringify()`
- [ ] URL: `http://217.182.76.146/api/summary`
- [ ] Timeout: 30000ms
- [ ] Połączenia: AI Agent4 → POST Summary to API
- [ ] Test: Uruchom workflow i sprawdź logi

---

**Status:** ✅ **NAPRAWIONE**

Użyj pliku **`API 08 - fixed POST v2.json`** do importu w n8n.
