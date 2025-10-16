# 🔧 Ręczna Konfiguracja Workflow w n8n

Jeśli import pliku JSON nie działa, zbuduj workflow ręcznie:

## Krok 1: Utwórz Nowy Workflow

1. W n8n kliknij **"+"** (New Workflow)
2. Nadaj nazwę: **"Document Comparison"**

## Krok 2: Dodaj Node'y

### Node 1: Manual Trigger (Start)

1. Kliknij **"Add first step"**
2. Wybierz **"On clicking 'Test workflow'"** (Manual Trigger)
3. Gotowe - to będzie punkt startowy

### Node 2: HTTP Request - Upload Documents

1. Kliknij **"+"** po Manual Trigger
2. Wyszukaj i wybierz **"HTTP Request"**
3. Skonfiguruj:

```
Name: Upload Documents
Method: POST
URL: http://localhost:8001/api/documents/upload

Authentication: None

Body/Parameters:
  - Kliknij "Add Parameter"
  - Type: Multipart Form Data
  - Name: old_document
    Value: Kliknij icon "Expression" i wpisz:
    {{ $json.old_document }}

  - Kliknij "Add Parameter"
  - Name: new_document
    Value: {{ $json.new_document }}
```

**UWAGA:** Zamiast używać Read Binary File, możesz użyć gotowych URL-i lub ścieżek.

### Node 3: HTTP Request - Start Processing

1. Kliknij **"+"** po Upload Documents
2. Wybierz **"HTTP Request"**
3. Skonfiguruj:

```
Name: Start Processing
Method: POST
URL: http://localhost:8001/api/process

Send Body: Yes
Body Content Type: JSON

Body:
{
  "document_pair_id": "={{ $('Upload Documents').item.json.document_pair_id }}"
}
```

**Jak wpisać expression:**
- Kliknij na pole "Body"
- Kliknij ikonę **"</>"** (Expression)
- Wpisz: `{{ $('Upload Documents').item.json.document_pair_id }}`

### Node 4: Wait

1. Kliknij **"+"** po Start Processing
2. Wybierz **"Wait"**
3. Skonfiguruj:

```
Name: Wait 3 Seconds
Resume: After Time Interval
Amount: 3
Unit: Seconds
```

### Node 5: HTTP Request - Check Status

1. Kliknij **"+"** po Wait
2. Wybierz **"HTTP Request"**
3. Skonfiguruj:

```
Name: Check Status
Method: GET

URL: (kliknij Expression icon)
=http://localhost:8001/api/status/{{ $('Start Processing').item.json.process_id }}
```

### Node 6: IF - Is Completed?

1. Kliknij **"+"** po Check Status
2. Wybierz **"IF"**
3. Skonfiguruj:

```
Name: Is Completed?

Conditions:
  - Condition Type: String
  - Value 1: (Expression) {{ $json.status }}
  - Operation: Equal
  - Value 2: completed
```

### Node 7: Wait (Loop)

1. Z wyjścia **"false"** node'a IF kliknij **"+"**
2. Wybierz **"Wait"**
3. Skonfiguruj:

```
Name: Wait 2 Seconds
Resume: After Time Interval
Amount: 2
Unit: Seconds
```

4. **POŁĄCZ** wyjście tego Wait z powrotem do **"Check Status"**
   - Przeciągnij strzałkę z Wait 2 Seconds do Check Status

### Node 8: HTTP Request - Get Full Result

1. Z wyjścia **"true"** node'a IF kliknij **"+"**
2. Wybierz **"HTTP Request"**
3. Skonfiguruj:

```
Name: Get Full Result
Method: GET

URL: (Expression)
=http://localhost:8001/api/result/{{ $('Start Processing').item.json.process_id }}/full
```

### Node 9: HTTP Request - Get Modified

1. Kliknij **"+"** po Get Full Result
2. Wybierz **"HTTP Request"**
3. Skonfiguruj:

```
Name: Get Modified
Method: GET

URL: (Expression)
=http://localhost:8001/api/result/{{ $('Start Processing').item.json.process_id }}/modified
```

### Node 10: Code (Przetwarzanie Wyników)

1. Kliknij **"+"** po Get Modified
2. Wybierz **"Code"**
3. Skonfiguruj:

```
Name: Process Results
Mode: Run Once for All Items

JavaScript Code:
```

```javascript
const fullResult = $input.first().json;
const stats = fullResult.statistics;

const summary = {
  timestamp: new Date().toISOString(),
  process_id: fullResult.process_id,
  total_changes: stats.total_changes,
  modified: stats.modified_paragraphs,
  added: stats.added_paragraphs,
  deleted: stats.deleted_paragraphs,
  severity: stats.total_changes > 10 ? 'HIGH' : 'LOW'
};

return [{ json: summary }];
```

## Krok 3: Połącz Node'y

Sprawdź czy wszystkie node'y są poprawnie połączone:

```
Manual Trigger
    ↓
Upload Documents
    ↓
Start Processing
    ↓
Wait 3 Seconds
    ↓
Check Status ←─────┐
    ↓              │
IF Is Completed?   │
    ↓              │
    ├─ TRUE → Get Full Result → Get Modified → Process Results
    │
    └─ FALSE → Wait 2 Seconds ─┘
```

## Krok 4: Test Workflow

### Testuj z przykładowymi danymi:

1. Kliknij na node **"Manual Trigger"**
2. Kliknij **"Execute Node"**
3. W oknie "Add Test Data" wpisz:

```json
{
  "old_document": "path_to_old.docx",
  "new_document": "path_to_new.docx"
}
```

**LUB** użyj curl do uploadu plików:

### Uproszczony Workflow dla Testów

Jeśli chcesz przetestować tylko z upload plików przez API:

1. **Zainstaluj Postman lub użyj curl**
2. Najpierw upload dokumenty przez curl:

```bash
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@c:\documents\old.docx" \
  -F "new_document=@c:\documents\new.docx"
```

3. Skopiuj `document_pair_id` z odpowiedzi
4. W n8n użyj prostszego workflow:

### Uproszczony Workflow (bez uploadu):

#### Node 1: Manual Trigger
```json
Test Data:
{
  "document_pair_id": "skopiuj-id-tutaj"
}
```

#### Node 2: Start Processing
```
POST http://localhost:8001/api/process
Body: { "document_pair_id": "{{ $json.document_pair_id }}" }
```

#### Node 3-9: (jak wyżej - Wait, Check Status, IF, Get Results...)

## Krok 5: Zapisz i Uruchom

1. Kliknij **"Save"** w górnym prawym rogu
2. Kliknij **"Execute Workflow"** (przycisk Play)
3. Obserwuj wykonanie każdego node'a
4. Sprawdź wyniki w ostatnim node'ie

## Wskazówki

### Jak wpisać Expression w n8n:

1. Kliknij na pole tekstowe
2. Zobaczysz ikonę **"</>"** - kliknij ją
3. Wpisz expression z `{{ }}`
4. Kliknij poza polem aby zatwierdzić

### Jak połączyć node'y:

- Najedź na node
- Pojawi się kropka po prawej stronie
- Przeciągnij strzałkę do następnego node'a

### Jak utworzyć pętlę (loop):

- Z node'a "Wait 2 Seconds" przeciągnij strzałkę z powrotem do "Check Status"
- Pozwoli to sprawdzać status wielokrotnie

## Gotowe! 🎉

Masz teraz w pełni funkcjonalny workflow do porównywania dokumentów!
