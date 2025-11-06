# Integracja Endpointów Summary w Workflow n8n

## Informacje o wersji

- **Wersja źródłowa:** API 04.json
- **Wersja docelowa:** API 05 - with summary.json
- **Liczba nodów:** 50 → 60 (+10 nowych nodów)
- **Wersja n8n:** 1.111.0
- **Data utworzenia:** 2025-10-29

## Przegląd zmian

Workflow został rozszerzony o pełną obsługę endpointów `/api/summary` zgodnie z dokumentacją API v1.1.0. Integracja umożliwia:

1. **Przesłanie podsumowania** wygenerowanego przez LLM do API
2. **Wysłanie maila** z informacją o konieczności weryfikacji
3. **Polling statusu** zatwierdzenia przez człowieka
4. **Pobranie zatwierdzonego** podsumowania
5. **Aktualizację finalnego maila** z zatwierdzonym tekstem

## Nowe nody

### 1. POST Summary to API
- **Typ:** HTTP Request
- **Endpoint:** `http://217.182.76.146/api/summary`
- **Metoda:** POST
- **Body:**
  ```json
  {
    "process_id": "{{ process_id }}",
    "summary_text": "{{ AI Agent4 output }}",
    "metadata": {
      "przedmiot_regulacji": "Dokument",
      "data_aktu": "",
      "data_wejscia_w_zycie": ""
    }
  }
  ```
- **Pozycja:** (1360, 356)

### 2. Send Review Email
- **Typ:** Email Send
- **Od:** ai_baw@credit-agricole.pl
- **Do:** trembiasz@credit-agricole.pl
- **Temat:** "Podsumowanie dokumentu - wymaga zatwierdzenia"
- **Treść:** Podsumowanie + instrukcje zatwierdzenia
- **Pozycja:** (1584, 356)

### 3. Wait Before Polling
- **Typ:** Wait
- **Czas:** 10 sekund
- **Cel:** Dać użytkownikowi czas przed rozpoczęciem pollingu
- **Pozycja:** (1808, 356)

### 4. Poll Summary Status
- **Typ:** HTTP Request
- **Endpoint:** `http://217.182.76.146/api/summary/{process_id}/status`
- **Metoda:** GET
- **Zwraca:** `{ "status": "pending_review" | "approved" | "rejected" }`
- **Pozycja:** (2032, 356)

### 5. Is Summary Approved?
- **Typ:** IF
- **Warunek:** `status === "approved"`
- **Output TRUE:** Przejdź do Get Approved Summary
- **Output FALSE:** Przejdź do Wait 5 Seconds → powrót do pollingu
- **Pozycja:** (2256, 284)

### 6. Wait 5 Seconds
- **Typ:** Wait
- **Czas:** 5 sekund
- **Cel:** Pętla pollingu - czekaj przed kolejnym sprawdzeniem
- **Pozycja:** (2256, 556)
- **Połączenie:** Wraca do "Poll Summary Status"

### 7. Get Approved Summary
- **Typ:** HTTP Request
- **Endpoint:** `http://217.182.76.146/api/summary/{process_id}/approved`
- **Metoda:** GET
- **Zwraca:**
  ```json
  {
    "summary_text": "...",
    "metadata": {...},
    "edited_by_user": true/false
  }
  ```
- **Pozycja:** (2480, 284)

### 8. Merge Approved with Report
- **Typ:** Merge
- **Input 1:** Get Approved Summary (zatwierdzone podsumowanie)
- **Input 2:** HTTP Request (raport HTML)
- **Cel:** Połączenie danych przed aktualizacją maila
- **Pozycja:** (2704, 428)

### 9. Update Email Content
- **Typ:** Code (JavaScript)
- **Funkcja:**
  - Pobiera zatwierdzone podsumowanie z API
  - Formatuje treść (punkty, HTML)
  - Dodaje informację czy było edytowane
  - Generuje pełny HTML maila (szablon z Code in JavaScript4)
- **Output:** `{ html: "...", approved_summary: "...", edited: true/false }`
- **Pozycja:** (2928, 428)

### 10. Sticky Note - Summary Integration
- **Typ:** Sticky Note
- **Treść:** Dokumentacja procesu integracji
- **Pozycja:** (1328, 100)

## Przebieg procesu (Flow)

```
┌──────────────────────────────────────────────────────────────────────┐
│  ISTNIEJĄCY WORKFLOW (bez zmian)                                     │
│  Upload → Process → Polling → Final Summary → AI Agent3 → AI Agent4  │
└────────────────────────────────────────────┬─────────────────────────┘
                                             │
                                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  NOWA SEKCJA: OBSŁUGA SUMMARY                                        │
├──────────────────────────────────────────────────────────────────────┤
│  1. POST Summary to API                                              │
│     └─> Wysyła podsumowanie z AI Agent4 do API                       │
│         Response: { status: "pending_review", created_at: ... }      │
│                                                                       │
│  2. Send Review Email                                                │
│     └─> Mail do użytkownika: "Sprawdź i zatwierdź podsumowanie"     │
│                                                                       │
│  3. Wait Before Polling (10s)                                        │
│     └─> Daj czas użytkownikowi przed pollingiem                     │
│                                                                       │
│  4. ┌─────────────────────────────────────────┐                     │
│     │ PĘTLA POLLINGU                          │                     │
│     │                                          │                     │
│     │ Poll Summary Status ──> Is Approved?    │                     │
│     │         ▲                    │           │                     │
│     │         │                    │           │                     │
│     │         │               NO   │  YES      │                     │
│     │         │                    │           │                     │
│     │    Wait 5 Seconds ◄──────────┘           │                     │
│     │                                          │                     │
│     └──────────────────────────────────────────┘                     │
│                                     │                                │
│                                     ▼                                │
│  5. Get Approved Summary                                             │
│     └─> Pobierz zatwierdzone podsumowanie (+ info czy edytowane)    │
│                                                                       │
├──────────────────────────────────────────────────────────────────────┤
│  MERGE Z ISTNIEJĄCYM PROCESEM                                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  HTTP Request (raport) ───┐                                          │
│                            ├──> Merge Approved with Report           │
│  Get Approved Summary ─────┘         │                               │
│                                      ▼                                │
│                           Update Email Content                       │
│                                      │                                │
│                                      ▼                                │
│                               Send email (finalny)                   │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Zmiany w połączeniach

### Zmodyfikowane połączenia:

1. **AI Agent4**
   - **PRZED:** → Merge2
   - **PO:** → POST Summary to API

2. **HTTP Request** (raport)
   - **PRZED:** → Merge2
   - **PO:** → Merge2 **ORAZ** → Merge Approved with Report

3. **Send email**
   - **PRZED:** Otrzymuje dane z Code in JavaScript4
   - **PO:** Otrzymuje dane z Update Email Content

### Nowe połączenia:

```
POST Summary to API → Send Review Email
Send Review Email → Wait Before Polling
Wait Before Polling → Poll Summary Status
Poll Summary Status → Is Summary Approved?
Is Summary Approved? (TRUE) → Get Approved Summary
Is Summary Approved? (FALSE) → Wait 5 Seconds
Wait 5 Seconds → Poll Summary Status (PĘTLA)
Get Approved Summary → Merge Approved with Report
HTTP Request → Merge Approved with Report
Merge Approved with Report → Update Email Content
Update Email Content → Send email
```

## Endpointy API wykorzystywane przez workflow

### 1. POST /api/summary
- **Wywoływany przez:** POST Summary to API
- **Cel:** Przesłanie podsumowania wygenerowanego przez LLM
- **Request:**
  ```json
  {
    "process_id": "uuid",
    "summary_text": "tekst podsumowania",
    "metadata": {
      "przedmiot_regulacji": "...",
      "data_aktu": "...",
      "data_wejscia_w_zycie": "..."
    }
  }
  ```
- **Response:**
  ```json
  {
    "status": "pending_review",
    "created_at": "2025-10-29T...",
    ...
  }
  ```

### 2. GET /api/summary/{process_id}/status
- **Wywoływany przez:** Poll Summary Status
- **Cel:** Sprawdzenie czy użytkownik zatwierdził podsumowanie
- **Response:**
  ```json
  {
    "process_id": "uuid",
    "status": "pending_review" | "approved" | "rejected",
    "created_at": "...",
    "approved_at": null | "..."
  }
  ```

### 3. GET /api/summary/{process_id}/approved
- **Wywoływany przez:** Get Approved Summary
- **Cel:** Pobranie zatwierdzonego podsumowania
- **Response:**
  ```json
  {
    "process_id": "uuid",
    "summary_text": "zatwierdzone podsumowanie",
    "metadata": {...},
    "approved_at": "...",
    "edited_by_user": true/false
  }
  ```

## Konfiguracja

### Wymagane zmienne środowiskowe:
- Brak nowych zmiennych - używa istniejących konfiguracji SMTP i OpenAI

### Wymagane credentiale:
- **SMTP:** "SMTP account 4" (id: 2joSLF2U4RnAaaXW)
- **OpenAI:** "OpenAi account 11" (id: im1Fo28cUIM0GySs)

### Parametry do dostosowania:

1. **Czas pollingu:**
   - `Wait Before Polling`: 10 sekund (można zmienić)
   - `Wait 5 Seconds`: 5 sekund (częstotliwość sprawdzania)
   - **Brak timeoutu** - będzie czekać nieskończenie długo (należy dodać logikę timeout po 30 min)

2. **Email z prośbą o weryfikację:**
   - Odbiorca: trembiasz@credit-agricole.pl
   - Treść w node "Send Review Email" - można dostosować

3. **Metadata:**
   - Obecnie ustawione na wartości domyślne
   - Można rozszerzyć o dane z dokumentu

## Instrukcja importu do n8n

1. Otwórz n8n (wersja 1.111.0)
2. Kliknij **"Workflows"** w menu głównym
3. Kliknij **"Add workflow"** → **"Import from File"**
4. Wybierz plik: `API 05 - with summary.json`
5. Kliknij **"Import"**
6. Sprawdź czy wszystkie credentiale są poprawnie podłączone:
   - SMTP account 4
   - OpenAi account 11
   - Microsoft SQL account 3
   - SeaTable account 3
7. **WAŻNE:** Sprawdź połączenia między nodami wizualnie
8. Zapisz workflow

## Weryfikacja poprawności

### Sprawdzenie struktury:

```python
import json

with open("API 05 - with summary.json") as f:
    data = json.load(f)

# Podstawowe sprawdzenia
assert data["name"] == "API 05 - with summary"
assert len(data["nodes"]) == 60
assert len([n for n in data["nodes"] if "Summary" in n["name"]]) >= 3

# Sprawdź czy wszystkie nody mają unikalne ID
ids = [n["id"] for n in data["nodes"]]
assert len(ids) == len(set(ids)), "Duplicate node IDs found!"

print("✓ Struktura poprawna")
```

### Test workflow:

1. Uruchom workflow manualnie (`When clicking 'Execute workflow'`)
2. Sprawdź logi każdego nowego noda
3. Zweryfikuj czy email z prośbą o weryfikację został wysłany
4. Zatwierdź podsumowanie przez frontend API
5. Sprawdź czy finalny mail został wysłany z zatwierdzonym tekstem

## Rozwiązywanie problemów

### Problem: Pętla pollingu działa nieskończenie długo
**Rozwiązanie:** Dodaj node Timeout lub ogranicz liczbę iteracji

### Problem: Email z weryfikacją nie zawiera linka do edycji
**Rozwiązanie:** Należy rozszerzyć API o endpoint zwracający URL frontendu

### Problem: Metadata są puste
**Rozwiązanie:** Rozszerz node "POST Summary to API" o pobieranie danych z dokumentu

### Problem: Workflow nie importuje się
**Rozwiązanie:**
1. Sprawdź wersję n8n (musi być >= 1.111.0)
2. Sprawdź czy plik JSON jest poprawny (walidacja JSON)
3. Sprawdź czy wszystkie credentiale istnieją

## Następne kroki / Ulepszenia

1. **Timeout dla pollingu:** Dodać maksymalny czas oczekiwania (np. 30 minut)
2. **Frontend do edycji:** Stworzyć dedykowany interfejs do edycji podsumowań
3. **Dynamiczne metadata:** Pobierać dane z dokumentu automatycznie
4. **Webhook zamiast pollingu:** Użyć webhook gdy status się zmieni
5. **Obsługa rejection:** Co się dzieje gdy użytkownik odrzuci podsumowanie?
6. **Logging:** Dodać szczegółowe logi do SeaTable
7. **Notyfikacje:** Powiadomienia push/Slack o konieczności weryfikacji

## Wersjonowanie

- **v1.0** (2025-10-29): Pierwsza wersja z obsługą summary
- **Bazuje na:** API 04.json (50 nodów)

## Autor

Wygenerowane automatycznie przez Claude Code na podstawie:
- Dokumentacji API v1.1.0 (`API_DOCUMENTATION.md`)
- Istniejącego workflow `API 04.json`
- Specyfikacji n8n 1.111.0

---

**Uwaga:** Ten workflow wymaga działającego API pod adresem `http://217.182.76.146/` z obsługą endpointów `/api/summary/*`
