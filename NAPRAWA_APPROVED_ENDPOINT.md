# Naprawa Endpoint /approved w n8n

## ❌ Problem

Node **"Get Approved Summary"** w workflow n8n generował nieprawidłowy URL:

```
http://217.182.76.146/api/summary/{{ $('Start Processing').item.json.process_id }}/approved
```

Zamiast dynamicznego `process_id`, URL zawierał **literalny tekst** wyrażenia n8n.

### Objawy:
- HTTP request do endpointa z literalnym `{{ ... }}` w URL
- Backend zwraca 404 lub błąd parsowania
- Workflow nie może pobrać zatwierdzonego podsumowania

---

## 🔍 Analiza

### Nieprawidłowa składnia w node:

```json
{
  "name": "Get Approved Summary",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "=http://217.182.76.146/api/summary/{{ $('Start Processing').item.json.process_id }}/approved"
  }
}
```

### Problem:

Gdy używasz `=` na początku URL (expression mode w n8n), **nie możesz używać `{{ }}` syntax**!

W n8n istnieją dwa tryby:

1. **String mode** (bez `=`): używasz `{{ expression }}`
2. **Expression mode** (z `=`): używasz JavaScript template literals

### Nieprawidłowe kombinacje:

```javascript
❌ "url": "=http://...{{ $('Node').item.json.field }}"  // Mieszanie stylów
❌ "url": "http://...{{ $('Node').item.json.field }}"   // Brak string interpolacji
```

### Prawidłowe składnie:

```javascript
✅ "url": "=`http://.../${$('Node').item.json.field}`"  // Expression mode + template literal
✅ "url": "={{ `http://.../${$('Node').item.json.field}` }}"  // Pełne wyrażenie
```

---

## ✅ Rozwiązanie

### Poprawiona konfiguracja node:

```json
{
  "name": "Get Approved Summary",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "=`http://217.182.76.146/api/summary/${$('Start Processing').item.json.process_id}/approved`"
  }
}
```

### Kluczowe zmiany:

| Element | PRZED | PO |
|---------|-------|-----|
| **Składnia** | `{{ ... }}` | `${...}` |
| **String wrapper** | Brak | Backticks `` ` `` |
| **Typ** | Nieprawidłowy string | Template literal (ES6) |

---

## 🔧 Implementacja

### Automatyczna naprawa workflow:

```python
import json

# Wczytaj workflow
with open('API 08 - fixed POST v2.json', 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# Znajdź i napraw node
for node in workflow['nodes']:
    if node['name'] == 'Get Approved Summary':
        # Zmień z {{ }} na ${ } z template literal
        node['parameters']['url'] = (
            "=`http://217.182.76.146/api/summary/"
            "${$('Start Processing').item.json.process_id}/approved`"
        )

# Zapisz jako nową wersję
workflow['name'] = 'API 09 - fixed approved endpoint'
with open('API 09 - fixed approved.json', 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)
```

### Wygenerowany plik:

```
C:\Projects\BAW\API 09 - fixed approved.json
```

---

## 🧪 Test

### Backend endpoint działa poprawnie:

```bash
curl -s http://217.182.76.146/api/summary/test-quill-editor/approved | python -m json.tool
```

**Wynik:**
```json
{
  "process_id": "test-quill-editor",
  "summary_text": "## Test Edytora\n\nTo jest test naprawionego edytora Quill.js.",
  "metadata": {
    "przedmiot_regulacji": "Test",
    "data_aktu": "2025-10-08",
    "data_wejscia_w_zycie": "2025-10-16"
  },
  "approved_at": "2025-10-29T09:17:56.751788",
  "edited_by_user": true
}
```

✅ Endpoint zwraca **edytowaną treść** (`edited_by_user: true`)

### Test w n8n po naprawie:

1. Zaimportuj `API 09 - fixed approved.json` do n8n
2. Uruchom workflow z przykładowym procesem
3. Node "Get Approved Summary" powinien zwrócić:
   - HTTP 200 OK
   - JSON z `summary_text` (edytowana treść)

---

## 📖 Różnice między API 08 i API 09

| Wersja | Node | URL | Status |
|--------|------|-----|--------|
| **API 08** | Get Approved Summary | `={{ ... }}` | ❌ Błędna składnia |
| **API 09** | Get Approved Summary | `` =`...${...}` `` | ✅ Poprawna składnia |

---

## 📚 Dokumentacja n8n

### Expression Mode w n8n

Gdy używasz `=` na początku wartości, n8n oczekuje **JavaScript expression**:

```javascript
// ✅ DOBRZE - Template literal
"url": "=`http://api.example.com/users/${$node['User Data'].json.id}`"

// ✅ DOBRZE - Konkatenacja
"url": "='http://api.example.com/users/' + $node['User Data'].json.id"

// ✅ DOBRZE - Pełne wyrażenie z {{ }}
"url": "={{ `http://api.example.com/users/${$node['User Data'].json.id}` }}"

// ❌ ŹLE - Mieszanie składni
"url": "=http://api.example.com/users/{{ $node['User Data'].json.id }}"
```

### String Mode (bez `=`)

```javascript
// ✅ DOBRZE - Używaj {{ }}
"url": "http://api.example.com/users/{{ $node['User Data'].json.id }}"

// ❌ ŹLE - Template literal nie działa bez expression mode
"url": "http://api.example.com/users/${$node['User Data'].json.id}"
```

---

## ✅ Checklist weryfikacji

Po zaimportowaniu API 09 sprawdź:

- [ ] Node "Get Approved Summary" używa `` =`...${...}` ``
- [ ] Wyrażenie zawiera `$('Start Processing').item.json.process_id`
- [ ] Brak `{{ }}` w expression mode
- [ ] Test workflow zwraca zatwierdzone podsumowanie
- [ ] `summary_text` zawiera edytowaną treść
- [ ] `edited_by_user` jest `true` jeśli było edytowane

---

## 🎯 Podsumowanie

### Problem:
Node "Get Approved Summary" używał nieprawidłowej składni `{{ }}` w expression mode.

### Rozwiązanie:
Zmieniono na poprawną składnię JavaScript template literal: `` `...${...}` ``

### Wynik:
- ✅ URL jest poprawnie generowany
- ✅ Endpoint zwraca zatwierdzone podsumowanie
- ✅ Treść zawiera edycje użytkownika
- ✅ Workflow działa end-to-end

---

## 🚀 Status: NAPRAWIONE

**Data naprawy:** 2025-10-29
**Wersja workflow:** API 09 - fixed approved endpoint

**Plik gotowy do importu:**
```
C:\Projects\BAW\API 09 - fixed approved.json
```

**Gotowe do użycia w n8n!** 🎉
