# Dokumentacja API - Usługa Porównywania Dokumentów

## Informacje Ogólne

**Wersja:** 1.1.0
**Base URL:** `http://localhost:8001`
**Format:** JSON
**Framework:** FastAPI

Usługa porównywania dokumentów DOCX/PDF z zachowaniem struktury i znaczników zmian. API umożliwia upload dokumentów, asynchroniczne przetwarzanie, oraz generowanie raportów HTML.

---

## Spis Treści

1. [Podstawowe Endpointy](#podstawowe-endpointy)
2. [Upload i Przetwarzanie](#upload-i-przetwarzanie)
3. [Wyniki Porównania](#wyniki-porównania)
4. [System Podsumowań (n8n)](#system-podsumowań-n8n)
5. [Generowanie Raportów](#generowanie-raportów)
6. [Modele Danych](#modele-danych)
7. [Przepływ Pracy](#przepływ-pracy)
8. [Kody Błędów](#kody-błędów)

---

## Podstawowe Endpointy

### GET / - Root Endpoint

Zwraca informacje o usłudze i dostępnych endpointach.

**Request:**
```http
GET / HTTP/1.1
Host: localhost:8001
```

**Response:** `200 OK`
```json
{
  "service": "Usługa Porównywania Dokumentów",
  "version": "1.1.0",
  "status": "running",
  "endpoints": {
    "upload": "POST /api/documents/upload",
    "process": "POST /api/process",
    "status": "GET /api/status/{process_id}",
    "full": "GET /api/result/{process_id}/full",
    "modified": "GET /api/result/{process_id}/modified",
    "added": "GET /api/result/{process_id}/added",
    "deleted": "GET /api/result/{process_id}/deleted",
    "generate_report": "GET /api/report/{process_id}/generate"
  },
  "summary_endpoints": {
    "create": "POST /api/summary",
    "get_status": "GET /api/summary/{process_id}/status",
    "get_detail": "GET /api/summary/{process_id}",
    "get_approved": "GET /api/summary/{process_id}/approved",
    "update": "PUT /api/summary/{process_id}",
    "approve": "POST /api/summary/{process_id}/approve"
  }
}
```

---

### GET /health - Health Check

Sprawdza stan usługi i zwraca statystyki.

**Request:**
```http
GET /health HTTP/1.1
Host: localhost:8001
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2025-10-28T14:30:00.123456",
  "statistics": {
    "total_documents": 10,
    "total_processes": 8,
    "completed_processes": 7,
    "failed_processes": 1
  }
}
```

---

## Upload i Przetwarzanie

### POST /api/documents/upload - Upload Dokumentów

Załaduj parę dokumentów (stary i nowy) do porównania.

**Obsługiwane formaty:** `.docx`, `.pdf` (automatyczna konwersja PDF→DOCX)

**Request:**
```http
POST /api/documents/upload HTTP/1.1
Host: localhost:8001
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="old_document"; filename="dokument_v1.docx"
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document

[binary data]
------WebKitFormBoundary
Content-Disposition: form-data; name="new_document"; filename="dokument_v2.docx"
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document

[binary data]
------WebKitFormBoundary--
```

**Response:** `200 OK`
```json
{
  "document_pair_id": "c29d4e61-2963-48c7-a425-708b0c59be74",
  "status": "uploaded",
  "message": "Dokumenty zostały załadowane: dokument_v1.docx, dokument_v2.docx"
}
```

**Przykład z konwersją PDF:**
```json
{
  "document_pair_id": "f5a8e91b-3d72-4c1a-b829-9f6e0c8d5a42",
  "status": "uploaded",
  "message": "Dokumenty zostały załadowane: dokument_v1.pdf, dokument_v2.pdf\nStary dokument PDF skonwertowany (metoda: marker, jakość: 0.92)\nNowy dokument PDF skonwertowany (metoda: marker, jakość: 0.95)"
}
```

**Błędy:**
- `400 Bad Request` - Nieobsługiwany format pliku
- `500 Internal Server Error` - Błąd konwersji PDF lub zapisu

---

### POST /api/process - Rozpocznij Przetwarzanie

Uruchamia asynchroniczne porównywanie dokumentów.

**Request:**
```http
POST /api/process HTTP/1.1
Host: localhost:8001
Content-Type: application/json

{
  "document_pair_id": "c29d4e61-2963-48c7-a425-708b0c59be74"
}
```

**Response:** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "status": "started",
  "message": "Przetwarzanie zostało rozpoczęte"
}
```

**Błędy:**
- `404 Not Found` - Nie znaleziono pary dokumentów
- `500 Internal Server Error` - Błąd podczas uruchamiania procesu

---

### GET /api/status/{process_id} - Status Przetwarzania

Monitoruje postęp przetwarzania (polling endpoint).

**Request:**
```http
GET /api/status/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21 HTTP/1.1
Host: localhost:8001
```

**Response (w trakcie):** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "status": "processing",
  "progress": 50,
  "message": "Porównywanie dokumentów",
  "error": null,
  "started_at": "2025-10-28T14:30:00.123456",
  "completed_at": null
}
```

**Response (zakończone):** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "status": "completed",
  "progress": 100,
  "message": "Przetwarzanie zakończone pomyślnie",
  "error": null,
  "started_at": "2025-10-28T14:30:00.123456",
  "completed_at": "2025-10-28T14:30:15.789012"
}
```

**Response (błąd):** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "status": "error",
  "progress": 0,
  "message": "Błąd podczas przetwarzania",
  "error": "ValueError: Nieprawidłowy format dokumentu",
  "started_at": "2025-10-28T14:30:00.123456",
  "completed_at": null
}
```

**Statusy:** `pending`, `processing`, `completed`, `error`

**Błędy:**
- `404 Not Found` - Nie znaleziono procesu

---

## Wyniki Porównania

### GET /api/result/{process_id}/full - Pełny Dokument

Zwraca pełny dokument ze wszystkimi paragrafami, tabelami i znacznikami zmian.

**Request:**
```http
GET /api/result/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/full HTTP/1.1
Host: localhost:8001
```

**Response:** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "document_pair_id": "c29d4e61-2963-48c7-a425-708b0c59be74",
  "paragraphs": [
    {
      "index": 0,
      "text": "Rozdział 1. Postanowienia ogólne",
      "type": "unchanged",
      "old_text": null,
      "changes": null
    },
    {
      "index": 1,
      "text": "Regulamin określa zasady świadczenia usług bankowych w Banku XYZ S.A.",
      "type": "modified",
      "old_text": "Regulamin określa zasady świadczenia usług w Banku XYZ S.A.",
      "changes": [
        {
          "operation": "equal",
          "text": "Regulamin określa zasady świadczenia usług "
        },
        {
          "operation": "insert",
          "text": "bankowych "
        },
        {
          "operation": "equal",
          "text": "w Banku XYZ S.A."
        }
      ]
    },
    {
      "index": 2,
      "text": "Bank zapewnia bezpieczeństwo transakcji.",
      "type": "added",
      "old_text": null,
      "changes": null
    },
    {
      "index": 3,
      "text": "Dostęp do usług wymaga posiadania rachunku.",
      "type": "deleted",
      "old_text": "Dostęp do usług wymaga posiadania rachunku.",
      "changes": null
    }
  ],
  "tables": [
    {
      "index": 0,
      "rows": [
        ["Usługa", "Opłata", "Waluta"],
        ["Przelew krajowy", "5.00", "PLN"],
        ["Przelew zagraniczny", "25.00", "PLN"]
      ],
      "changes": [
        {
          "table_index": 0,
          "row_index": 1,
          "col_index": 1,
          "old_value": "3.00",
          "new_value": "5.00",
          "changes": [
            {
              "operation": "delete",
              "text": "3"
            },
            {
              "operation": "insert",
              "text": "5"
            },
            {
              "operation": "equal",
              "text": ".00"
            }
          ]
        }
      ]
    }
  ],
  "statistics": {
    "total_paragraphs": 4,
    "unchanged_paragraphs": 1,
    "modified_paragraphs": 1,
    "added_paragraphs": 1,
    "deleted_paragraphs": 1,
    "total_changes": 3,
    "tables_count": 1,
    "modified_cells": 1
  },
  "generated_at": "2025-10-28T14:30:15.789012"
}
```

**Błędy:**
- `404 Not Found` - Nie znaleziono wyników dla procesu

---

### GET /api/result/{process_id}/modified - Tylko Zmodyfikowane Zdania

Zwraca wyłącznie paragrafy, które zostały zmodyfikowane.

**Request:**
```http
GET /api/result/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/modified HTTP/1.1
Host: localhost:8001
```

**Response:** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "document_pair_id": "c29d4e61-2963-48c7-a425-708b0c59be74",
  "modified_sentences": [
    {
      "paragraph_index": 1,
      "old_text": "Regulamin określa zasady świadczenia usług w Banku XYZ S.A.",
      "new_text": "Regulamin określa zasady świadczenia usług bankowych w Banku XYZ S.A.",
      "changes": [
        {
          "operation": "equal",
          "text": "Regulamin określa zasady świadczenia usług "
        },
        {
          "operation": "insert",
          "text": "bankowych "
        },
        {
          "operation": "equal",
          "text": "w Banku XYZ S.A."
        }
      ]
    }
  ],
  "total_count": 1,
  "generated_at": "2025-10-28T14:30:20.123456"
}
```

---

### GET /api/result/{process_id}/added - Tylko Dodane Zdania

Zwraca wyłącznie paragrafy, które zostały dodane.

**Request:**
```http
GET /api/result/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/added HTTP/1.1
Host: localhost:8001
```

**Response:** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "document_pair_id": "c29d4e61-2963-48c7-a425-708b0c59be74",
  "added_sentences": [
    {
      "paragraph_index": 2,
      "text": "Bank zapewnia bezpieczeństwo transakcji."
    }
  ],
  "total_count": 1,
  "generated_at": "2025-10-28T14:30:21.123456"
}
```

---

### GET /api/result/{process_id}/deleted - Tylko Usunięte Zdania

Zwraca wyłącznie paragrafy, które zostały usunięte.

**Request:**
```http
GET /api/result/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/deleted HTTP/1.1
Host: localhost:8001
```

**Response:** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "document_pair_id": "c29d4e61-2963-48c7-a425-708b0c59be74",
  "deleted_sentences": [
    {
      "paragraph_index": 3,
      "text": "Dostęp do usług wymaga posiadania rachunku."
    }
  ],
  "total_count": 1,
  "generated_at": "2025-10-28T14:30:22.123456"
}
```

---

## System Podsumowań (n8n)

System integracji z n8n do automatycznego generowania i zatwierdzania podsumowań zmian przez LLM.

### POST /api/summary - Utwórz Podsumowanie

**Wywoływane przez:** n8n (po wygenerowaniu podsumowania przez LLM)

**Request:**
```http
POST /api/summary HTTP/1.1
Host: localhost:8001
Content-Type: application/json

{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "summary_text": "Regulamin został zaktualizowany o następujące zmiany:\n1. Dodano określenie 'bankowych' do zakresu usług\n2. Dodano nowy punkt o bezpieczeństwie transakcji\n3. Usunięto wymóg posiadania rachunku\n4. Zwiększono opłatę za przelew krajowy z 3 PLN do 5 PLN",
  "metadata": {
    "przedmiot_regulacji": "Regulamin świadczenia usług bankowych",
    "data_aktu": "2025-10-15",
    "data_wejscia_w_zycie": "2025-11-01",
    "dodatkowe_dane": {
      "autor": "Departament Prawny",
      "wersja": "2.0"
    }
  }
}
```

**Response:** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "summary_text": "Regulamin został zaktualizowany o następujące zmiany:\n1. Dodano określenie 'bankowych' do zakresu usług\n2. Dodano nowy punkt o bezpieczeństwie transakcji\n3. Usunięto wymóg posiadania rachunku\n4. Zwiększono opłatę za przelew krajowy z 3 PLN do 5 PLN",
  "metadata": {
    "przedmiot_regulacji": "Regulamin świadczenia usług bankowych",
    "data_aktu": "2025-10-15",
    "data_wejscia_w_zycie": "2025-11-01",
    "dodatkowe_dane": {
      "autor": "Departament Prawny",
      "wersja": "2.0"
    }
  },
  "status": "pending_review",
  "created_at": "2025-10-28T14:30:25.123456",
  "updated_at": null,
  "approved_at": null,
  "edited_by_user": false
}
```

---

### GET /api/summary/{process_id}/status - Status Podsumowania

**Wywoływane przez:** n8n (polling co kilka sekund, czekając na zatwierdzenie)

**Request:**
```http
GET /api/summary/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/status HTTP/1.1
Host: localhost:8001
```

**Response (oczekuje na zatwierdzenie):** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "status": "pending_review",
  "created_at": "2025-10-28T14:30:25.123456",
  "updated_at": null,
  "approved_at": null
}
```

**Response (zatwierdzone):** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "status": "approved",
  "created_at": "2025-10-28T14:30:25.123456",
  "updated_at": "2025-10-28T14:35:10.987654",
  "approved_at": "2025-10-28T14:35:10.987654"
}
```

**Statusy:** `pending_review`, `approved`, `rejected`

---

### GET /api/summary/{process_id} - Szczegóły Podsumowania

**Wywoływane przez:** n8n (po otrzymaniu statusu "approved")

**Request:**
```http
GET /api/summary/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21 HTTP/1.1
Host: localhost:8001
```

**Response:** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "summary_text": "Regulamin został zaktualizowany o następujące zmiany:\n1. Dodano określenie 'bankowych' do zakresu usług\n2. Dodano nowy punkt o bezpieczeństwie transakcji\n3. Usunięto wymóg posiadania rachunku\n4. Zwiększono opłatę za przelew krajowy z 3 PLN do 5 PLN",
  "metadata": {
    "przedmiot_regulacji": "Regulamin świadczenia usług bankowych",
    "data_aktu": "2025-10-15",
    "data_wejscia_w_zycie": "2025-11-01",
    "dodatkowe_dane": {
      "autor": "Departament Prawny",
      "wersja": "2.0"
    }
  },
  "status": "approved",
  "created_at": "2025-10-28T14:30:25.123456",
  "updated_at": "2025-10-28T14:35:10.987654",
  "approved_at": "2025-10-28T14:35:10.987654",
  "edited_by_user": false
}
```

---

### GET /api/summary/{process_id}/approved - Zatwierdzone Podsumowanie

**Wywoływane przez:** n8n (uproszczony endpoint zwracający tylko zatwierdzone podsumowanie)

**Request:**
```http
GET /api/summary/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/approved HTTP/1.1
Host: localhost:8001
```

**Response:** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "summary_text": "Regulamin został zaktualizowany o następujące zmiany:\n1. Dodano określenie 'bankowych' do zakresu usług\n2. Dodano nowy punkt o bezpieczeństwie transakcji\n3. Usunięto wymóg posiadania rachunku\n4. Zwiększono opłatę za przelew krajowy z 3 PLN do 5 PLN",
  "metadata": {
    "przedmiot_regulacji": "Regulamin świadczenia usług bankowych",
    "data_aktu": "2025-10-15",
    "data_wejscia_w_zycie": "2025-11-01",
    "dodatkowe_dane": {
      "autor": "Departament Prawny",
      "wersja": "2.0"
    }
  },
  "approved_at": "2025-10-28T14:35:10.987654",
  "edited_by_user": false
}
```

**Błędy:**
- `404 Not Found` - Nie znaleziono podsumowania
- `400 Bad Request` - Podsumowanie nie zostało jeszcze zatwierdzone

---

### PUT /api/summary/{process_id} - Aktualizuj Podsumowanie

**Wywoływane przez:** Frontend (po edycji podsumowania przez użytkownika)

**Request:**
```http
PUT /api/summary/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21 HTTP/1.1
Host: localhost:8001
Content-Type: application/json

{
  "summary_text": "Regulamin został zaktualizowany - najważniejsze zmiany:\n1. Rozszerzono zakres o usługi bankowe\n2. Dodano klauzulę bezpieczeństwa\n3. Zmieniono opłaty za przelewy krajowe",
  "metadata": {
    "przedmiot_regulacji": "Regulamin świadczenia usług bankowych",
    "data_aktu": "2025-10-15",
    "data_wejscia_w_zycie": "2025-11-01"
  }
}
```

**Response:** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "summary_text": "Regulamin został zaktualizowany - najważniejsze zmiany:\n1. Rozszerzono zakres o usługi bankowe\n2. Dodano klauzulę bezpieczeństwa\n3. Zmieniono opłaty za przelewy krajowe",
  "metadata": {
    "przedmiot_regulacji": "Regulamin świadczenia usług bankowych",
    "data_aktu": "2025-10-15",
    "data_wejscia_w_zycie": "2025-11-01"
  },
  "status": "pending_review",
  "created_at": "2025-10-28T14:30:25.123456",
  "updated_at": "2025-10-28T14:33:45.654321",
  "approved_at": null,
  "edited_by_user": true
}
```

---

### POST /api/summary/{process_id}/approve - Zatwierdź/Odrzuć Podsumowanie

**Wywoływane przez:** Frontend (po decyzji użytkownika)

**Request (zatwierdzenie):**
```http
POST /api/summary/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/approve HTTP/1.1
Host: localhost:8001
Content-Type: application/json

{
  "approved": true
}
```

**Request (odrzucenie):**
```http
POST /api/summary/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/approve HTTP/1.1
Host: localhost:8001
Content-Type: application/json

{
  "approved": false
}
```

**Response:** `200 OK`
```json
{
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "summary_text": "Regulamin został zaktualizowany - najważniejsze zmiany:\n1. Rozszerzono zakres o usługi bankowe\n2. Dodano klauzulę bezpieczeństwa\n3. Zmieniono opłaty za przelewy krajowe",
  "metadata": {
    "przedmiot_regulacji": "Regulamin świadczenia usług bankowych",
    "data_aktu": "2025-10-15",
    "data_wejscia_w_zycie": "2025-11-01"
  },
  "status": "approved",
  "created_at": "2025-10-28T14:30:25.123456",
  "updated_at": "2025-10-28T14:35:10.987654",
  "approved_at": "2025-10-28T14:35:10.987654",
  "edited_by_user": true
}
```

---

## Generowanie Raportów

### GET /api/report/{process_id}/generate - Generuj Raport HTML

Generuje statyczny raport HTML z pełnymi wynikami porównania.

**Request:**
```http
GET /api/report/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21/generate HTTP/1.1
Host: localhost:8001
```

**Response:** `200 OK`
```json
{
  "success": true,
  "process_id": "a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21",
  "report_url": "/reports/report_a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21_20251028_143530.html",
  "report_filename": "report_a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21_20251028_143530.html",
  "report_path": "C:\\Projects\\BAW\\UslugaDoPorownan\\output\\reports\\report_a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21_20251028_143530.html",
  "generated_at": "2025-10-28T14:35:30.123456",
  "message": "Raport HTML został wygenerowany pomyślnie"
}
```

**Dostęp do raportu:**
```http
GET /reports/report_a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21_20251028_143530.html HTTP/1.1
Host: localhost:8001
```

**Błędy:**
- `404 Not Found` - Nie znaleziono wyników dla procesu
- `500 Internal Server Error` - Błąd generowania raportu

---

## Modele Danych

### ChangeMarker
Reprezentuje pojedynczą operację w diff.

```json
{
  "operation": "insert",  // "delete" | "equal" | "insert"
  "text": "bankowych "
}
```

### ParagraphResult
Reprezentuje paragraf w dokumencie.

```json
{
  "index": 1,
  "text": "Nowy tekst paragrafu",
  "type": "modified",  // "unchanged" | "modified" | "added" | "deleted"
  "old_text": "Stary tekst paragrafu",
  "changes": [
    {"operation": "equal", "text": "..."},
    {"operation": "insert", "text": "..."}
  ]
}
```

### TableCellChange
Reprezentuje zmianę w komórce tabeli.

```json
{
  "table_index": 0,
  "row_index": 1,
  "col_index": 1,
  "old_value": "3.00",
  "new_value": "5.00",
  "changes": [
    {"operation": "delete", "text": "3"},
    {"operation": "insert", "text": "5"}
  ]
}
```

### StatisticsResult
Statystyki porównania.

```json
{
  "total_paragraphs": 4,
  "unchanged_paragraphs": 1,
  "modified_paragraphs": 1,
  "added_paragraphs": 1,
  "deleted_paragraphs": 1,
  "total_changes": 3,
  "tables_count": 1,
  "modified_cells": 1
}
```

### SummaryMetadata
Metadane dokumentu dla podsumowania.

```json
{
  "przedmiot_regulacji": "Regulamin świadczenia usług bankowych",
  "data_aktu": "2025-10-15",
  "data_wejscia_w_zycie": "2025-11-01",
  "dodatkowe_dane": {
    "autor": "Departament Prawny",
    "wersja": "2.0"
  }
}
```

---

## Przepływ Pracy

### 1. Podstawowy Przepływ (bez n8n)

```
1. Upload dokumentów
   POST /api/documents/upload
   → document_pair_id

2. Rozpocznij przetwarzanie
   POST /api/process
   → process_id

3. Monitoruj status (polling co 2s)
   GET /api/status/{process_id}
   → status: "pending" → "processing" → "completed"

4. Pobierz wyniki
   GET /api/result/{process_id}/full
   GET /api/result/{process_id}/modified
   GET /api/result/{process_id}/added
   GET /api/result/{process_id}/deleted

5. Wygeneruj raport HTML
   GET /api/report/{process_id}/generate
   → report_url
```

### 2. Przepływ z Integracją n8n

```
Frontend                    API                         n8n
   |                         |                           |
   |-- POST /upload -------->|                           |
   |<- document_pair_id -----|                           |
   |                         |                           |
   |-- POST /process ------->|                           |
   |<- process_id -----------|                           |
   |                         |                           |
   |-- GET /status --------->|                           |
   |<- status: completed ----|                           |
   |                         |                           |
   |-- GET /result/full ---->|                           |
   |<- full document --------|                           |
   |                         |                           |
   | (przekazuje wyniki)     |                           |
   |------------------------------------------>|          |
   |                         |                 (LLM generuje podsumowanie)
   |                         |<--- POST /api/summary ----|
   |                         |--- 200 OK (pending) ----->|
   |                         |                           |
   |                         |<--- GET /summary/status --|
   |-- Wyświetla podsumowanie                 (polling)  |
   |<- GET /summary ---------|                           |
   |                         |                           |
   | (użytkownik edytuje)    |                           |
   |-- PUT /summary -------->|                           |
   |<- updated summary ------|                           |
   |                         |                           |
   | (użytkownik zatwierdza) |                           |
   |-- POST /approve ------->|                           |
   |<- approved status ------|                           |
   |                         |                           |
   |                         |<--- GET /summary/status --|
   |                         |--- status: approved ----->|
   |                         |                           |
   |                         |<--- GET /approved --------|
   |                         |--- zatwierdzone dane ---->|
   |                         |                           |
   |                         |                (n8n kontynuuje workflow)
```

---

## Kody Błędów

### 200 OK
Żądanie powiodło się.

### 400 Bad Request
- Nieprawidłowy format pliku
- Podsumowanie nie zostało jeszcze zatwierdzone
- Błędne dane wejściowe

### 404 Not Found
- Nie znaleziono pary dokumentów
- Nie znaleziono procesu
- Nie znaleziono wyników
- Nie znaleziono podsumowania

### 500 Internal Server Error
- Błąd konwersji PDF
- Błąd przetwarzania dokumentów
- Błąd generowania raportu
- Błąd zapisu do storage

---

## Przykłady Użycia

### cURL - Upload i Przetwarzanie

```bash
# 1. Upload dokumentów
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@dokument_v1.docx" \
  -F "new_document=@dokument_v2.docx"

# Response: {"document_pair_id": "xxx-xxx-xxx", ...}

# 2. Rozpocznij przetwarzanie
curl -X POST http://localhost:8001/api/process \
  -H "Content-Type: application/json" \
  -d '{"document_pair_id": "xxx-xxx-xxx"}'

# Response: {"process_id": "yyy-yyy-yyy", ...}

# 3. Sprawdź status
curl http://localhost:8001/api/status/yyy-yyy-yyy

# 4. Pobierz wyniki
curl http://localhost:8001/api/result/yyy-yyy-yyy/full

# 5. Generuj raport
curl http://localhost:8001/api/report/yyy-yyy-yyy/generate
```

### Python - Pełny Workflow

```python
import requests
import time

API_BASE = "http://localhost:8001"

# Upload
with open("dokument_v1.docx", "rb") as old, open("dokument_v2.docx", "rb") as new:
    files = {
        "old_document": old,
        "new_document": new
    }
    r = requests.post(f"{API_BASE}/api/documents/upload", files=files)
    document_pair_id = r.json()["document_pair_id"]

# Process
r = requests.post(f"{API_BASE}/api/process", json={"document_pair_id": document_pair_id})
process_id = r.json()["process_id"]

# Poll status
while True:
    r = requests.get(f"{API_BASE}/api/status/{process_id}")
    status = r.json()["status"]
    if status == "completed":
        break
    elif status == "error":
        print("Error:", r.json()["error"])
        exit(1)
    time.sleep(2)

# Get results
r = requests.get(f"{API_BASE}/api/result/{process_id}/full")
results = r.json()
print(f"Total changes: {results['statistics']['total_changes']}")

# Generate report
r = requests.get(f"{API_BASE}/api/report/{process_id}/generate")
report_url = r.json()["report_url"]
print(f"Report: {API_BASE}{report_url}")
```

### JavaScript - Integracja n8n

```javascript
// n8n webhook - odbieranie wyników z frontendu
const processId = $input.item.json.process_id;
const fullResults = $input.item.json.results;

// Wywołaj LLM do wygenerowania podsumowania
const summary = await generateSummary(fullResults);

// Wyślij podsumowanie do API
const response = await $http.request({
  method: 'POST',
  url: `http://localhost:8001/api/summary`,
  body: {
    process_id: processId,
    summary_text: summary,
    metadata: {
      przedmiot_regulacji: "Regulamin",
      data_aktu: "2025-10-15"
    }
  }
});

// Polling statusu (co 5s przez max 5 min)
for (let i = 0; i < 60; i++) {
  await new Promise(resolve => setTimeout(resolve, 5000));

  const status = await $http.request({
    method: 'GET',
    url: `http://localhost:8001/api/summary/${processId}/status`
  });

  if (status.json.status === 'approved') {
    // Pobierz zatwierdzone podsumowanie
    const approved = await $http.request({
      method: 'GET',
      url: `http://localhost:8001/api/summary/${processId}/approved`
    });

    // Kontynuuj workflow z zatwierdzonym podsumowaniem
    return approved.json;
  }
}
```

---

## Uwagi Implementacyjne

### CORS
API obsługuje wszystkie originy (`*`) - w produkcji należy ograniczyć.

### Konwersja PDF
- Automatyczna konwersja PDF→DOCX przy uploadzie
- Metody: `marker` (domyślna), `pypdf`, `pdfplumber`
- Quality score: 0.0-1.0 (informacja o jakości konwersji)

### Asynchroniczne Przetwarzanie
- Wszystkie operacje I/O wykonywane asynchronicznie
- Background tasks dla długich operacji (porównywanie)
- Zalecany polling interval: 2 sekundy

### Storage
- In-memory storage (produkcja: Redis/PostgreSQL)
- Dane tracone przy restarcie serwisu
- Statyczne pliki raportów w `output/reports/`

### Statyczne Pliki
- Raporty HTML montowane pod `/reports/`
- Pełne raporty offline z osadzonymi danymi JSON

---

## Kontakt i Wsparcie

**Wersja API:** 1.1.0
**Framework:** FastAPI 0.100+
**Python:** 3.10+
**Dokumentacja interaktywna:** http://localhost:8001/docs
**ReDoc:** http://localhost:8001/redoc
**OpenAPI Schema:** http://localhost:8001/openapi.json
