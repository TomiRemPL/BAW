# Integracja n8n - System Podsumowań

Dokumentacja systemu edycji i zatwierdzania podsumowań zmian w dokumentach z integracją n8n.

## 📋 Spis Treści

- [Opis Systemu](#opis-systemu)
- [Architektura](#architektura)
- [API Endpoints](#api-endpoints)
- [Workflow n8n](#workflow-n8n)
- [Frontend - Edytor](#frontend---edytor)
- [Przykłady Użycia](#przykłady-użycia)

---

## Opis Systemu

System umożliwia:

1. **n8n** generuje podsumowanie zmian w dokumencie (np. przez LLM)
2. **n8n** wysyła podsumowanie do systemu wraz z metadanymi
3. **System** przechowuje podsumowanie ze statusem `pending_review`
4. **Użytkownik** dostaje link do edytora: `http://localhost:8000/summary/{process_id}`
5. **Użytkownik** edytuje tekst i metadane, zapisuje lub zatwierdza
6. **n8n** polluje endpoint statusu i czeka na zmianę na `approved`
7. **n8n** pobiera zatwierdzone podsumowanie i kontynuuje przetwarzanie

---

## Architektura

```
┌─────────────────────────────────────────────────────┐
│  n8n Workflow                                       │
│  1. Generuje podsumowanie (LLM)                     │
│  2. POST /api/summary (tworzy podsumowanie)         │
│  3. Czeka - polling GET /api/summary/{id}/status    │
│  4. Status = "approved" → GET /api/summary/{id}/    │
│     approved                                        │
│  5. Kontynuuje workflow z zatwierdzonym tekstem     │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP API
                   ▼
┌─────────────────────────────────────────────────────┐
│  UslugaDoPorownan (Backend) - Port 8001             │
│  - Przechowywanie podsumowań                        │
│  - Zarządzanie statusami                            │
│  - API dla n8n i frontendu                          │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP Proxy
                   ▼
┌─────────────────────────────────────────────────────┐
│  SecureDocCompare (Frontend) - Port 8000            │
│  - Strona edytora /summary/{process_id}             │
│  - Autoryzacja (wymagane logowanie)                 │
│  - Proxy do backend API                             │
└─────────────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Użytkownik                                         │
│  - Loguje się                                       │
│  - Edytuje podsumowanie                             │
│  - Zatwierdza lub odrzuca                           │
└─────────────────────────────────────────────────────┘
```

---

## API Endpoints

### Backend (UslugaDoPorownan - Port 8001)

#### 1. Utworzenie podsumowania

**Endpoint:** `POST /api/summary`

**Wywołujący:** n8n

**Request:**
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "summary_text": "Dokument wprowadza zmiany w następujących obszarach:\\n\\n1. **Ryzyko operacyjne** - nowe wymagania dotyczące...",
  "metadata": {
    "przedmiot_regulacji": "Dyrektywa DORA",
    "data_aktu": "2024-01-17",
    "data_wejscia_w_zycie": "2025-01-17",
    "dodatkowe_dane": {
      "typ_dokumentu": "regulacja_ue",
      "priorytet": "wysoki"
    }
  }
}
```

**Response:** `200 OK`
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "summary_text": "Dokument wprowadza zmiany...",
  "metadata": {
    "przedmiot_regulacji": "Dyrektywa DORA",
    "data_aktu": "2024-01-17",
    "data_wejscia_w_zycie": "2025-01-17"
  },
  "status": "pending_review",
  "created_at": "2025-10-27T10:00:00",
  "updated_at": null,
  "approved_at": null,
  "edited_by_user": false
}
```

---

#### 2. Sprawdzenie statusu (dla n8n)

**Endpoint:** `GET /api/summary/{process_id}/status`

**Wywołujący:** n8n (polling co 5-10 sekund)

**Response:** `200 OK`
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "pending_review",  // lub "approved", "rejected"
  "created_at": "2025-10-27T10:00:00",
  "updated_at": "2025-10-27T10:05:00",
  "approved_at": null
}
```

**Statusy:**
- `pending_review` - oczekuje na akceptację użytkownika
- `approved` - zatwierdzone, n8n może kontynuować
- `rejected` - odrzucone przez użytkownika

---

#### 3. Pobranie zatwierdzonego podsumowania (dla n8n)

**Endpoint:** `GET /api/summary/{process_id}/approved`

**Wywołujący:** n8n (po otrzymaniu statusu "approved")

**Response:** `200 OK`
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "summary_text": "Dokument wprowadza zmiany... [przeedytowany tekst]",
  "metadata": {
    "przedmiot_regulacji": "Dyrektywa DORA",
    "data_aktu": "2024-01-17",
    "data_wejscia_w_zycie": "2025-01-17"
  },
  "approved_at": "2025-10-27T10:10:00",
  "edited_by_user": true
}
```

**Błąd jeśli nie zatwierdzone:** `400 Bad Request`
```json
{
  "detail": "Podsumowanie nie zostało jeszcze zatwierdzone. Aktualny status: pending_review"
}
```

---

#### 4. Pobranie szczegółów podsumowania

**Endpoint:** `GET /api/summary/{process_id}`

**Wywołujący:** Frontend

**Response:** `200 OK`
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "summary_text": "Dokument wprowadza zmiany...",
  "metadata": {
    "przedmiot_regulacji": "Dyrektywa DORA",
    "data_aktu": "2024-01-17",
    "data_wejscia_w_zycie": "2025-01-17"
  },
  "status": "pending_review",
  "created_at": "2025-10-27T10:00:00",
  "updated_at": null,
  "approved_at": null,
  "edited_by_user": false
}
```

---

#### 5. Aktualizacja podsumowania

**Endpoint:** `PUT /api/summary/{process_id}`

**Wywołujący:** Frontend

**Request:**
```json
{
  "summary_text": "Zaktualizowany tekst podsumowania...",
  "metadata": {
    "przedmiot_regulacji": "Dyrektywa DORA (Digital Operational Resilience Act)",
    "data_aktu": "2024-01-17",
    "data_wejscia_w_zycie": "2025-01-17"
  }
}
```

**Response:** `200 OK` - zwraca pełny obiekt SummaryDetailResponse

**Uwaga:** Aktualizacja NIE zmienia statusu, tylko tekst i metadane.

---

#### 6. Zatwierdzenie/odrzucenie podsumowania

**Endpoint:** `POST /api/summary/{process_id}/approve`

**Wywołujący:** Frontend

**Request (zatwierdzenie):**
```json
{
  "approved": true
}
```

**Request (odrzucenie):**
```json
{
  "approved": false
}
```

**Response:** `200 OK` - zwraca pełny obiekt z nowym statusem

---

### Frontend (SecureDocCompare - Port 8000)

Wszystkie endpointy wymagają **autentykacji** (sesja cookie).

#### 1. Strona edytora

**Endpoint:** `GET /summary/{process_id}`

**Browser URL:** `http://localhost:8000/summary/660e8400-e29b-41d4-a716-446655440001`

**Zwraca:** HTML strona edytora

---

#### 2-6. Proxy do backend

Frontend udostępnia proxy endpointy (wymagają auth):

- `GET /api/summary/{process_id}` → proxy do backend
- `GET /api/summary/{process_id}/status` → proxy do backend
- `PUT /api/summary/{process_id}` → proxy do backend
- `POST /api/summary/{process_id}/approve` → proxy do backend

---

## Workflow n8n

### Krok 1: Wygeneruj podsumowanie

```javascript
// Node: LLM (Claude/GPT)
// Otrzymujesz tekst zmian z poprzedniego node
const changes = $input.item.json.full_result;

// Prompt dla LLM
const prompt = `Wygeneruj podsumowanie zmian w dokumencie regulacyjnym.
Zmiany: ${JSON.stringify(changes)}

Wymagania:
- Format Markdown
- Struktura: 1) Podsumowanie, 2) Kluczowe zmiany, 3) Wpływ na organizację
- Maksymalnie 500 słów
`;

// LLM generuje summary_text
return {
  summary_text: "..." // tekst od LLM
};
```

---

### Krok 2: Wyślij do systemu

```javascript
// Node: HTTP Request
{
  "method": "POST",
  "url": "http://localhost:8001/api/summary",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "process_id": "{{ $json.process_id }}",
    "summary_text": "{{ $json.summary_text }}",
    "metadata": {
      "przedmiot_regulacji": "Dyrektywa DORA",
      "data_aktu": "2024-01-17",
      "data_wejscia_w_zycie": "2025-01-17"
    }
  }
}

// Response: summary object ze statusem "pending_review"
```

---

### Krok 3: Wyślij powiadomienie do użytkownika

```javascript
// Node: Email / Slack / Teams
{
  "to": "user@example.com",
  "subject": "Nowe podsumowanie do zatwierdzenia",
  "body": `
    Wygenerowano podsumowanie zmian w dokumencie.

    Link do edycji:
    http://localhost:8000/summary/{{ $json.process_id }}

    Zaloguj się i zatwierdź podsumowanie, aby kontynuować proces.
  `
}
```

---

### Krok 4: Czekaj na zatwierdzenie (polling)

```javascript
// Node: Loop
// Repeat: Until condition is true
// Max iterations: 120 (10 minut przy 5-sekundowym interval)

// Sub-Node 1: HTTP Request - Check Status
{
  "method": "GET",
  "url": "http://localhost:8001/api/summary/{{ $json.process_id }}/status"
}

// Sub-Node 2: Wait
{
  "duration": 5000 // 5 sekund
}

// Sub-Node 3: Condition
{
  "condition": "{{ $json.status === 'approved' }}"
}

// Jeśli true → wyjdź z loop
// Jeśli false → czekaj dalej
```

---

### Krok 5: Pobierz zatwierdzone podsumowanie

```javascript
// Node: HTTP Request
{
  "method": "GET",
  "url": "http://localhost:8001/api/summary/{{ $json.process_id }}/approved"
}

// Response:
{
  "process_id": "...",
  "summary_text": "... [przeedytowany tekst]",
  "metadata": {...},
  "approved_at": "2025-10-27T10:10:00",
  "edited_by_user": true
}
```

---

### Krok 6: Kontynuuj workflow

```javascript
// Node: Further Processing
const approvedSummary = $json.summary_text;
const metadata = $json.metadata;

// Użyj zatwierdzonego tekstu do:
// - Wygenerowania PDF raportu
// - Wysłania email do zarządu
// - Zapisania w bazie danych
// - ...
```

---

## Frontend - Edytor

### URL

```
http://localhost:8000/summary/{process_id}
```

Przykład:
```
http://localhost:8000/summary/660e8400-e29b-41d4-a716-446655440001
```

### Funkcje

1. **Edycja tekstu**
   - Textarea z podglądem liczby znaków
   - Formatowanie Markdown (przyciski: bold, italic, lista, nagłówki)
   - Auto-save co 30 sekund

2. **Metadane**
   - Przedmiot regulacji (text input)
   - Data aktu (date picker)
   - Data wejścia w życie (date picker)
   - Rozszerzalne o dodatkowe pola

3. **Przyciski akcji**
   - **Zapisz roboczo** - zapisuje zmiany bez zmiany statusu
   - **Zatwierdź** - zmienia status na "approved", n8n może kontynuować
   - **Odrzuć** - zmienia status na "rejected"
   - **Anuluj** - powrót do dashboard

4. **Status badge**
   - Żółty: "Oczekuje na akceptację" (pending_review)
   - Zielony: "Zatwierdzono" (approved)
   - Czerwony: "Odrzucono" (rejected)

---

## Przykłady Użycia

### Przykład 1: Pełny workflow

```bash
# 1. n8n tworzy podsumowanie
curl -X POST http://localhost:8001/api/summary \
  -H "Content-Type: application/json" \
  -d '{
    "process_id": "test-123",
    "summary_text": "Dokument wprowadza zmiany...",
    "metadata": {
      "przedmiot_regulacji": "DORA",
      "data_aktu": "2024-01-17",
      "data_wejscia_w_zycie": "2025-01-17"
    }
  }'

# Response: {"process_id": "test-123", "status": "pending_review", ...}

# 2. Użytkownik otwiera link
# http://localhost:8000/summary/test-123

# 3. n8n polluje status (co 5 sekund)
curl http://localhost:8001/api/summary/test-123/status

# Response: {"status": "pending_review", ...}

# 4. Użytkownik zatwierdza w interfejsie
# (kliknięcie przycisku "Zatwierdź")

# 5. n8n ponownie sprawdza status
curl http://localhost:8001/api/summary/test-123/status

# Response: {"status": "approved", ...}

# 6. n8n pobiera zatwierdzone podsumowanie
curl http://localhost:8001/api/summary/test-123/approved

# Response: {"summary_text": "...", "approved_at": "...", ...}
```

---

### Przykład 2: Edycja przez użytkownika

```javascript
// Frontend JavaScript - zapisanie roboczej wersji

const summaryText = document.getElementById('summaryText').value;
const metadata = {
  przedmiot_regulacji: document.getElementById('przedmiotRegulacji').value,
  data_aktu: document.getElementById('dataAktu').value,
  data_wejscia_w_zycie: document.getElementById('dataWejsciaWZycie').value
};

const response = await fetch(`/api/summary/${processId}`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    summary_text: summaryText,
    metadata: metadata
  })
});

const result = await response.json();
// result.status nadal "pending_review"
// result.edited_by_user = true
```

---

### Przykład 3: Zatwierdzenie

```javascript
// Frontend JavaScript - zatwierdzenie

const response = await fetch(`/api/summary/${processId}/approve`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ approved: true })
});

const result = await response.json();
// result.status = "approved"
// result.approved_at = "2025-10-27T10:10:00"
```

---

## Rozszerzanie Metadanych

System jest zaprojektowany tak, aby łatwo dodawać nowe metadane.

### Backend (models.py)

```python
class SummaryMetadata(BaseModel):
    przedmiot_regulacji: Optional[str] = None
    data_aktu: Optional[str] = None
    data_wejscia_w_zycie: Optional[str] = None

    # NOWE POLA - dodaj tutaj
    organ_wydajacy: Optional[str] = None
    numer_aktu: Optional[str] = None
    link_do_zrodla: Optional[str] = None

    # Pole catch-all dla dynamicznych danych
    dodatkowe_dane: Optional[Dict[str, Any]] = None
```

### Frontend (summary_editor.html)

Dodaj nowe inputy w sekcji `.metadata-grid`:

```html
<div class="form-group">
    <label for="organWydajacy">Organ wydający</label>
    <input type="text" id="organWydajacy" placeholder="np. Komisja Europejska">
</div>
```

Zaktualizuj JavaScript:

```javascript
const metadata = {
    przedmiot_regulacji: document.getElementById('przedmiotRegulacji').value,
    data_aktu: document.getElementById('dataAktu').value,
    data_wejscia_w_zycie: document.getElementById('dataWejsciaWZycie').value,

    // NOWE POLA
    organ_wydajacy: document.getElementById('organWydajacy').value,
    numer_aktu: document.getElementById('numerAktu').value,
    link_do_zrodla: document.getElementById('linkDoZrodla').value
};
```

---

## Troubleshooting

### Problem: Status nigdy nie zmienia się na "approved"

**Rozwiązanie:**
1. Sprawdź czy użytkownik kliknął "Zatwierdź" w interfejsie
2. Sprawdź logi backendu: `Zatwierdzono podsumowanie dla procesu: {id}`
3. Sprawdź czy n8n używa poprawnego `process_id`

---

### Problem: 404 Not Found dla /api/summary/{id}

**Rozwiązanie:**
1. Sprawdź czy podsumowanie zostało utworzone (POST /api/summary)
2. Sprawdź czy używasz poprawnego `process_id`
3. Sprawdź czy process istnieje w storage

---

### Problem: Frontend nie ładuje danych

**Rozwiązanie:**
1. Sprawdź czy użytkownik jest zalogowany
2. Sprawdź console w przeglądarce (F12)
3. Sprawdź czy backend działa: `curl http://localhost:8001/health`
4. Sprawdź logi SecureDocCompare

---

## Statystyki Storage

Nowe statystyki w `/health`:

```json
{
  "status": "healthy",
  "timestamp": "2025-10-27T10:00:00",
  "statistics": {
    "total_documents": 10,
    "total_processes": 15,
    "completed_processes": 12,
    "processing_count": 1,
    "error_count": 2,
    "cached_results": 12,
    "total_summaries": 8,
    "pending_summaries": 2,
    "approved_summaries": 6
  }
}
```

---

## Bezpieczeństwo

### Frontend
- ✅ Wymagana autentykacja (sesja cookie)
- ✅ Rate limiting (20 req/min)
- ✅ Walidacja process_id
- ✅ HTTPS w produkcji

### Backend
- ✅ CORS włączony dla frontendu
- ✅ Walidacja Pydantic
- ✅ Logowanie wszystkich operacji
- ✅ Brak public access (tylko przez frontend lub n8n)

### n8n
- ⚠️ n8n powinien używać API klucza (do implementacji)
- ⚠️ Rate limiting dla n8n polling (do implementacji)

---

## Wersjonowanie

- **Backend:** v1.1.0
- **Frontend:** v1.0.0
- **API:** Stabilne, backwards-compatible

---

## Kontakt

Pytania? Zobacz główny README.md lub DEPLOYMENT.md

**Dokumentacja stworzona:** 2025-10-27
**Status:** ✅ Production Ready
