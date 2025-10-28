# 🧪 Przewodnik Testowania API - BAW Document Comparison

**Wersja:** 1.0
**Data:** 2025-10-28
**Plik testowy:** `test_complete_api.http`

---

## 📋 Spis Treści

1. [Szybki Start](#szybki-start)
2. [Instalacja Narzędzi](#instalacja-narzędzi)
3. [Struktura Testów](#struktura-testów)
4. [Scenariusze Testowe](#scenariusze-testowe)
5. [Checklist Testów](#checklist-testów)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Szybki Start

### Krok 1: Otwórz plik testowy

```
C:\Projects\BAW\test_complete_api.http
```

### Krok 2: Sprawdź URL

Na górze pliku znajdź:
```http
@backend_url = http://217.182.76.146:8001
@frontend_url = http://217.182.76.146:8000
```

### Krok 3: Uruchom pierwszy test

1. Znajdź: `### 1.1. Informacje o serwisie`
2. Kliknij **"Send Request"** nad kodem
3. Zobacz odpowiedź w nowym oknie po prawej

### Krok 4: Wykonaj pełny workflow

Przejdź do [Scenariusza 1](#scenariusz-1-pełny-workflow-porównywania) poniżej.

---

## 🛠️ Instalacja Narzędzi

### Visual Studio Code + REST Client

#### 1. Otwórz VSCode

```bash
code .
```

#### 2. Zainstaluj REST Client

- Naciśnij **Ctrl+Shift+X**
- Wyszukaj: **"REST Client"**
- Autor: **humao**
- Kliknij **Install**

#### 3. Otwórz plik testowy

```bash
code test_complete_api.http
```

#### 4. Użycie

- **Kliknij** "Send Request" nad requestem
- **LUB** Ctrl+Alt+R

---

### Alternatywnie: curl (Bash)

Jeśli wolisz terminal:

```bash
# Health check
curl http://217.182.76.146:8001/health

# Upload
curl -X POST http://217.182.76.146:8001/api/documents/upload \
  -F "old_document=@stara_wersja/dokument.docx" \
  -F "new_document=@nowa_wersja/dokument.docx"
```

---

## 📊 Struktura Testów

Plik `test_complete_api.http` jest podzielony na **9 sekcji**:

| Sekcja | Zawartość | Liczba testów |
|--------|-----------|---------------|
| 1 | Podstawowe endpointy | 2 |
| 2 | Upload i przetwarzanie | 4 |
| 3 | Status i wyniki | 5 |
| 4 | Raporty HTML | 1 |
| 5 | System podsumowań | 7 |
| 6 | Frontend API | 12 |
| 7 | Testy błędów | 10 |
| 8 | Scenariusze E2E | 4 |
| 9 | Notatki i wskazówki | - |

**Razem:** 45+ requestów + 4 scenariusze E2E = **~60 testów**

---

## 🎯 Scenariusze Testowe

### Scenariusz 1: Pełny Workflow Porównywania

**Cel:** Upload dokumentów → Przetwarzanie → Wyniki → Raport HTML

**Czas:** ~30 sekund - 2 minuty (zależy od rozmiaru dokumentów)

#### Krok 1: Upload Dokumentów

```http
POST {{backend_url}}/api/documents/upload
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="old_document"; filename="old.docx"
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document

< ./stara_wersja/dokument.docx
------WebKitFormBoundary
Content-Disposition: form-data; name="new_document"; filename="new.docx"
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document

< ./nowa_wersja/dokument.docx
------WebKitFormBoundary--
```

**Oczekiwana odpowiedź:**
```json
{
  "document_pair_id": "a1b2c3d4-...",
  "status": "uploaded",
  "message": "Dokumenty zostały załadowane: old.docx, new.docx"
}
```

**Akcja:** Skopiuj `document_pair_id` i wstaw do zmiennej `@document_pair_id` na górze pliku.

---

#### Krok 2: Rozpocznij Przetwarzanie

```http
POST {{backend_url}}/api/process
Content-Type: application/json

{
  "document_pair_id": "{{document_pair_id}}"
}
```

**Oczekiwana odpowiedź:**
```json
{
  "process_id": "f1e2d3c4-...",
  "status": "started",
  "message": "Przetwarzanie zostało rozpoczęte"
}
```

**Akcja:** Skopiuj `process_id` i wstaw do zmiennej `@process_id`.

---

#### Krok 3: Polling Statusu

**Wywołuj co 2 sekundy** aż `status` = `"completed"`:

```http
GET {{backend_url}}/api/status/{{process_id}}
Accept: application/json
```

**Możliwe statusy:**

1. `pending` (progress: 0)
2. `processing` (progress: 10-99)
3. `completed` (progress: 100) ✅
4. `error` ❌

**Przykładowa odpowiedź:**
```json
{
  "process_id": "f1e2d3c4-...",
  "status": "processing",
  "progress": 50,
  "message": "Porównywanie dokumentów",
  "started_at": "2025-10-28T10:30:00",
  "completed_at": null,
  "error": null
}
```

---

#### Krok 4: Pobierz Wyniki

##### 4a. Pełny wynik

```http
GET {{backend_url}}/api/result/{{process_id}}/full
Accept: application/json
```

**Zawiera:**
- Wszystkie paragrafy (unchanged, modified, added, deleted)
- Tabele z zmianami
- Statystyki

##### 4b. Tylko zmodyfikowane

```http
GET {{backend_url}}/api/result/{{process_id}}/modified
Accept: application/json
```

##### 4c. Tylko dodane

```http
GET {{backend_url}}/api/result/{{process_id}}/added
Accept: application/json
```

##### 4d. Tylko usunięte

```http
GET {{backend_url}}/api/result/{{process_id}}/deleted
Accept: application/json
```

---

#### Krok 5: Wygeneruj Raport HTML

```http
GET {{backend_url}}/api/report/{{process_id}}/generate
Accept: application/json
```

**Odpowiedź:**
```json
{
  "success": true,
  "report_url": "/reports/report_..._20251028_231438.html",
  "report_filename": "report_..._20251028_231438.html",
  "generated_at": "2025-10-28T23:14:38"
}
```

**Pobierz raport:**
```bash
curl http://217.182.76.146:8001/reports/report_..._20251028_231438.html > raport.html
```

**Otwórz w przeglądarce:**
```bash
# Windows
start raport.html

# Linux/Mac
open raport.html
```

---

### Scenariusz 2: Workflow z Podsumowaniem i Zatwierdzeniem

**Cel:** Porównanie → Podsumowanie → Edycja → Zatwierdzenie

**Czas:** ~5-15 minut (zależy od czasu edycji użytkownika)

**Uczestnicy:**
- **N8N Workflow** (automatyzacja)
- **Backend API** (przetwarzanie)
- **Użytkownik** (edycja w przeglądarce)

#### Krok 1: Upload + Process

Wykonaj [Scenariusz 1](#scenariusz-1-pełny-workflow-porównywania) kroki 1-4.

---

#### Krok 2: Utwórz Podsumowanie

```http
POST {{backend_url}}/api/summary
Content-Type: application/json

{
  "process_id": "{{process_id}}",
  "summary_text": "# Podsumowanie zmian\n\n## Kluczowe zmiany\n\n1. Test",
  "metadata": {
    "przedmiot_regulacji": "Dyrektywa DORA"
  }
}
```

**Odpowiedź:**
```json
{
  "process_id": "...",
  "status": "pending_review",
  "created_at": "2025-10-28T10:00:00",
  "edited_by_user": false
}
```

**Akcja:** Skopiuj `process_id` do zmiennej `@summary_process_id`.

---

#### Krok 3: Otwórz Summary Editor

**W przeglądarce:**
```
http://217.182.76.146:8000/summary/{{summary_process_id}}
```

**Uwaga:** Wymaga zalogowania! Hasło w env `FRONTEND_PASSWORD`.

---

#### Krok 4: Edytuj Podsumowanie

**W przeglądarce:**
1. Edytuj tekst
2. Edytuj metadane
3. Kliknij **"Zapisz"**

**LUB przez API:**
```http
PUT {{backend_url}}/api/summary/{{summary_process_id}}
Content-Type: application/json

{
  "summary_text": "# Podsumowanie (EDYTOWANE)...",
  "metadata": {"przedmiot_regulacji": "DORA Updated"}
}
```

**Odpowiedź:**
```json
{
  "process_id": "...",
  "status": "pending_review",
  "updated_at": "2025-10-28T10:05:00",
  "edited_by_user": true
}
```

---

#### Krok 5: Zatwierdź

**W przeglądarce:**
- Kliknij **"Zatwierdź"** ✅

**LUB przez API:**
```http
POST {{backend_url}}/api/summary/{{summary_process_id}}/approve
Content-Type: application/json

{
  "approved": true
}
```

**Odpowiedź:**
```json
{
  "process_id": "...",
  "status": "approved",
  "approved_at": "2025-10-28T10:10:00"
}
```

---

#### Krok 6: Pobierz Zatwierdzone (n8n)

**Sprawdź status (polling):**
```http
GET {{backend_url}}/api/summary/{{summary_process_id}}/status
```

**Gdy status = "approved", pobierz dane:**
```http
GET {{backend_url}}/api/summary/{{summary_process_id}}/approved
```

**Odpowiedź:**
```json
{
  "process_id": "...",
  "summary_text": "# Podsumowanie (EDYTOWANE)...",
  "metadata": {...},
  "approved_at": "2025-10-28T10:10:00",
  "edited_by_user": true
}
```

---

### Scenariusz 3: Workflow Odrzucenia

**Cel:** Użytkownik odrzuca podsumowanie

**Czas:** ~2 minuty

#### Kroki 1-4: Jak w Scenariuszu 2

---

#### Krok 5: Odrzuć

**W przeglądarce:**
- Kliknij **"Odrzuć"** ❌

**LUB przez API:**
```http
POST {{backend_url}}/api/summary/{{summary_process_id}}/approve
Content-Type: application/json

{
  "approved": false
}
```

**Odpowiedź:**
```json
{
  "process_id": "...",
  "status": "rejected",
  "approved_at": null
}
```

---

#### Krok 6: Sprawdź Status

```http
GET {{backend_url}}/api/summary/{{summary_process_id}}/status
```

**Odpowiedź:**
```json
{
  "process_id": "...",
  "status": "rejected",
  "created_at": "...",
  "updated_at": "...",
  "approved_at": null
}
```

---

### Scenariusz 4: Polling Timeout (n8n)

**Cel:** Symulacja timeout po 10 minutach bez reakcji użytkownika

**Czas:** 10 minut

#### Krok 1-2: Utwórz podsumowanie

Jak w Scenariuszu 2, kroki 1-2.

---

#### Krok 3: Polling (n8n)

**Wywołuj co 5-10 sekund:**
```http
GET {{backend_url}}/api/summary/{{summary_process_id}}/status
```

**Licznik iteracji:** 60 × 10s = 10 minut

---

#### Krok 4: Timeout (n8n workflow)

Po 60 iteracjach (10 minut):
- N8N wykrywa timeout
- N8N loguje błąd do SeaTable
- N8N wysyła email alert

**Uwaga:** Logika timeout jest w N8N workflow, nie w API!

---

## ✅ Checklist Testów

### Backend API (16 endpointów)

#### Podstawowe:
- [ ] GET `/` - Informacje o serwisie
- [ ] GET `/health` - Health check

#### Document Processing:
- [ ] POST `/api/documents/upload` - Upload DOCX
- [ ] POST `/api/documents/upload` - Upload PDF
- [ ] POST `/api/documents/upload` - Upload mieszany
- [ ] POST `/api/process` - Rozpocznij przetwarzanie
- [ ] GET `/api/status/{process_id}` - Status

#### Results:
- [ ] GET `/api/result/{process_id}/full` - Pełny wynik
- [ ] GET `/api/result/{process_id}/modified` - Zmodyfikowane
- [ ] GET `/api/result/{process_id}/added` - Dodane
- [ ] GET `/api/result/{process_id}/deleted` - Usunięte

#### Reports:
- [ ] GET `/api/report/{process_id}/generate` - Generuj raport

#### Summary System:
- [ ] POST `/api/summary` - Utwórz podsumowanie
- [ ] GET `/api/summary/{id}/status` - Status podsumowania
- [ ] GET `/api/summary/{id}` - Szczegóły
- [ ] GET `/api/summary/{id}/approved` - Pobierz zatwierdzone
- [ ] PUT `/api/summary/{id}` - Aktualizuj
- [ ] POST `/api/summary/{id}/approve` - Zatwierdź/odrzuć

---

### Frontend API (16 endpointów)

#### Podstawowe:
- [ ] GET `/health` - Health check
- [ ] GET `/` - Dashboard
- [ ] POST `/api/login` - Logowanie
- [ ] POST `/api/logout` - Wylogowanie

#### Summary Editor:
- [ ] GET `/summary/{id}` - UI edytora

#### Proxy do Backend:
- [ ] POST `/api/upload` - Upload (proxy)
- [ ] POST `/api/process/{id}` - Process (proxy)
- [ ] GET `/api/status/{id}` - Status (proxy)
- [ ] GET `/api/result/{id}/full` - Full (proxy)
- [ ] GET `/api/result/{id}/modified` - Modified (proxy)
- [ ] GET `/api/result/{id}/added` - Added (proxy)
- [ ] GET `/api/result/{id}/deleted` - Deleted (proxy)
- [ ] GET `/api/summary/{id}` - Get summary (proxy)
- [ ] GET `/api/summary/{id}/status` - Status summary (proxy)
- [ ] PUT `/api/summary/{id}` - Update summary (proxy)
- [ ] POST `/api/summary/{id}/approve` - Approve (proxy)

---

### Testy Błędów

- [ ] 400: Upload nieprawidłowy format (.txt)
- [ ] 404: Process z nieistniejącym document_pair_id
- [ ] 404: Status nieistniejącego procesu
- [ ] 404: Wynik nieistniejącego procesu
- [ ] 404: Raport nieistniejącego procesu
- [ ] 404: Status nieistniejącego podsumowania
- [ ] 400: Pobierz niezatwierdzone podsumowanie
- [ ] 404: Aktualizuj nieistniejące podsumowanie
- [ ] 404: Zatwierdź nieistniejące podsumowanie
- [ ] 400: Utwórz duplikat podsumowania

---

### Scenariusze E2E

- [ ] Scenariusz 1: Pełny workflow porównywania
- [ ] Scenariusz 2: Workflow z podsumowaniem i zatwierdzeniem
- [ ] Scenariusz 3: Workflow odrzucenia
- [ ] Scenariusz 4: Polling timeout

---

## 🐛 Troubleshooting

### Problem: "Cannot connect to backend"

**Sprawdź:**
```bash
# Czy backend działa?
curl http://217.182.76.146:8001/health

# Czy port 8001 jest otwarty?
telnet 217.182.76.146 8001
```

**Rozwiązanie:**
1. Sprawdź czy backend jest uruchomiony
2. Sprawdź firewall (port 8001)
3. Sprawdź URL w zmiennych (@backend_url)

---

### Problem: "404 Not Found" na endpoincie

**Sprawdź:**
1. Czy URL jest poprawny?
2. Czy endpoint istnieje w dokumentacji?
3. Czy używasz poprawnej metody (GET/POST/PUT)?

**Przykład:**
```
❌ GET /api/summary/{id}/approve
✅ POST /api/summary/{id}/approve
```

---

### Problem: "401 Unauthorized" (frontend)

**Przyczyna:** Brak session cookie lub nieważna sesja

**Rozwiązanie:**
1. Zaloguj się w przeglądarce: http://217.182.76.146:8000
2. Otwórz DevTools (F12) → Application → Cookies
3. Skopiuj `session_id`
4. Użyj w nagłówku:
   ```http
   Cookie: session_id=YOUR_SESSION_ID
   ```

---

### Problem: "400 Bad Request" (summary approved)

**Komunikat:**
```json
{
  "detail": "Podsumowanie nie zostało jeszcze zatwierdzone. Aktualny status: pending_review"
}
```

**Przyczyna:** Próba pobrania niezatwierdzonego podsumowania

**Rozwiązanie:**
1. Sprawdź status: `GET /api/summary/{id}/status`
2. Jeśli status != "approved", najpierw zatwierdź:
   ```http
   POST /api/summary/{id}/approve
   {"approved": true}
   ```
3. Potem pobierz: `GET /api/summary/{id}/approved`

---

### Problem: "500 Internal Server Error"

**Sprawdź:**
1. Logi backendu (console)
2. Czy plik DOCX/PDF jest prawidłowy?
3. Czy backend ma uprawnienia do zapisu (uploads/, output/reports/)

**Debugging:**
```bash
# Sprawdź logi
ssh debian@217.182.76.146 "tail -f /path/to/backend/logs"

# Sprawdź uprawnienia
ssh debian@217.182.76.146 "ls -la /path/to/backend/uploads"
```

---

### Problem: Upload pliku nie działa (REST Client)

**Przyczyna:** Ścieżka do pliku jest nieprawidłowa

**Rozwiązanie:**
```http
# POPRAWNE (ścieżka względna):
< ./stara_wersja/dokument.docx

# POPRAWNE (ścieżka bezwzględna):
< C:/Projects/BAW/stara_wersja/dokument.docx

# BŁĘDNE:
< stara_wersja/dokument.docx
```

---

### Problem: Polling trwa bardzo długo

**Przyczyny:**
1. Duży dokument (>50 stron)
2. PDF conversion (wolniejsze)
3. Backend przeciążony

**Monitorowanie:**
```http
GET {{backend_url}}/api/status/{{process_id}}
```

Sprawdzaj `progress` (0-100) i `message`.

**Typowe czasy:**
- DOCX (10 stron): ~5-10s
- DOCX (100 stron): ~30-60s
- PDF (10 stron): ~20-40s (z konwersją)

---

## 📚 Powiązane Dokumenty

- **API_COMPLETE_REFERENCE.md** - Kompletna dokumentacja API
- **test_complete_api.http** - Plik testowy (ten przewodnik)
- **N8N_SUMMARY_INTEGRATION.md** - Integracja n8n
- **IMPORT_FINAL_N8N_1.111.0.md** - Import workflow n8n

---

**Data:** 2025-10-28
**Wersja:** 1.0
**Autor:** Claude Code

**Powodzenia z testowaniem!** 🚀
