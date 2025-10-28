# 🔍 Raport Weryfikacji Workflow N8N (API 04.json)

**Data:** 2025-10-28
**Wersja:** 1.0.0
**Workflow ID:** Dl3LQScHexBjc6Gh

---

## 📋 PODSUMOWANIE WYKONAWCZE

**Status workflow:** ✅ **PRAWIDŁOWY** (z drobnymi rekomendacjami)

Workflow N8N został przeanalizowany pod kątem:
- ✅ Poprawności konfiguracji węzłów
- ✅ Integracji z BAW API
- ✅ Logiki przepływu danych
- ✅ Obsługi błędów
- ⚠️ Możliwości optymalizacji

---

## 🏗️ STRUKTURA WORKFLOW

### Tryby uruchomienia:
1. **Manual Trigger** - Manualne uruchomienie (linie 3-13)
2. **Schedule Trigger** - Automatyczne uruchomienie co 30 minut (linie 74-93)

### Główne etapy procesu:

```
1. Obliczanie zakresu czasu
   ↓
2. Query MS SQL (Select_no_1) - Pobranie danych z BAW DB
   ↓
3. Loop Over Items - Przetwarzanie każdego dokumentu
   ↓
4. Check_if_exist (SeaTable) - Sprawdzenie czy już przetworzony
   ↓
5. Insert_into_db (SeaTable) - Zapis info o rozpoczęciu
   ↓
6. Select_no_2 (MS SQL) - Pobranie ID pliku
   ↓
7. Insert_into_db2 (SeaTable) - Update statusu
   ↓
8. Select_no3 (MS SQL) - Pobranie linków do plików
   ↓
9. insert_do_pobrania (SeaTable) - Zapis metadanych
   ↓
10. Split Out - Podzielenie na pojedyncze elementy
   ↓
11. HTTP Request1/2 - Download starej i nowej wersji
   ↓
12. Code in JavaScript2 - Przygotowanie plików binarnych
   ↓
13. [RÓWNOLEGLE]:
    - Extract from File (PDF stary) → Edit Fields1 → text_v1
    - Extract from File2 (PDF nowy) → Edit Fields → text_v2
    - Upload Documents (API BAW) → Start Processing
   ↓
14. Merge1 - Połączenie text_v1 + text_v2
   ↓
15. Wait 3 Seconds
   ↓
16. Check Status (polling loop)
   ↓
17. Is Completed? → [No] Wait 2 Seconds → Check Status (loop)
                  → [Yes] Get Full Result
   ↓
18. Final Summary (JavaScript)
   ↓
19. [RÓWNOLEGLE]:
    - AI Agent3 (GPT-5) → Analiza JSON
    - HTTP Request → Generate HTML Report
   ↓
20. Merge (połączenie AI + text_v1/v2)
   ↓
21. AI Agent4 (GPT-5) → Weryfikacja podsumowania
   ↓
22. Merge2 (połączenie AI + report link)
   ↓
23. Code in JavaScript4 → Formatowanie email HTML
   ↓
24. Send email → trembiasz@credit-agricole.pl
```

---

## 🔌 INTEGRACJA Z BAW API

### ✅ ZWERYFIKOWANE ENDPOINTY

| Węzeł | Endpoint | Status | Uwagi |
|-------|----------|--------|-------|
| **Upload Documents** | `POST /api/documents/upload` | ✅ OK | Linie 637-669, timeout 120s |
| **Start Processing** | `POST /api/process` | ✅ OK | Linie 670-693 |
| **Check Status** | `GET /api/status/{process_id}` | ✅ OK | Linie 709-722, polling loop |
| **Get Full Result** | `GET /api/result/{process_id}/full` | ⚠️ DISABLED | Linie 758-772, węzeł wyłączony! |
| **HTTP Request** | `GET /api/report/{process_id}/generate` | ✅ OK | Linie 972-996 |

### ⚠️ PROBLEMY ZIDENTYFIKOWANE

#### 1. Węzeł "Get Full Result" jest WYŁĄCZONY (disabled: true)
**Lokalizacja:** Linia 771
**Problem:** Węzeł który miał pobierać pełny wynik jest nieaktywny
**Konsekwencja:** Workflow przechodzi bezpośrednio do "Final Summary" bez pobrania danych

**Rekomendacja:**
```json
// Linia 771: Usuń "disabled": true
{
  "parameters": {
    "url": "=http://217.182.76.146/api/result/{{ $('Start Processing').item.json.process_id }}/full",
    "options": {}
  },
  "id": "07c199d5-75e5-4ab2-9443-e297e2e09403",
  "name": "Get Full Result",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [-688, 444],
  "disabled": false  // ZMIENIĆ NA FALSE LUB USUNĄĆ LINIĘ
}
```

#### 2. Brak obsługi timeout w polling loop
**Lokalizacja:** Check Status → Is Completed? → Wait 2 Seconds → Check Status
**Problem:** Brak limitu iteracji - może zapętlić się w nieskończoność
**Konsekwencja:** Zużycie zasobów, brak informacji o błędzie

**Rekomendacja:** Dodać węzeł licznika lub timeout po maksymalnie 60 iteracjach (2 minuty):
- Po 60 iteracjach → Error handling node
- Log błędu do SeaTable
- Wysłanie powiadomienia email

#### 3. Brak użycia nowych API podsumowań (v1.1.0)
**Dostępne endpointy (nieużywane):**
- `POST /api/summary` - Utworzenie podsumowania
- `GET /api/summary/{id}/status` - Status podsumowania
- `GET /api/summary/{id}` - Szczegóły
- `PUT /api/summary/{id}` - Aktualizacja
- `POST /api/summary/{id}/approve` - Zatwierdzenie
- `GET /api/summary/{id}/approved` - Pobranie zatwierdzonego

**Obecne podejście:**
AI Agent3 generuje podsumowanie → AI Agent4 weryfikuje → Email

**Zalecane podejście (z API summary):**
1. AI Agent3 generuje podsumowanie
2. **POST /api/summary** - Zapisanie podsumowania w bazie
3. **Email z linkiem:** http://localhost:8000/summary/{id}
4. Użytkownik edytuje w interfejsie webowym
5. **Polling:** GET /api/summary/{id}/status (co 10s)
6. Po zatwierdzeniu: **GET /api/summary/{id}/approved**
7. Kontynuacja workflow (email końcowy)

**Korzyści:**
- ✅ Podsumowania zapisane w storage (możliwość późniejszego odczytu)
- ✅ Użytkownik może edytować w wygodnym interfejsie
- ✅ Historia zmian
- ✅ Zatwierdzenie przez użytkownika przed wysłaniem finalnego email

---

## 🤖 KONFIGURACJA AI

### AI Agent3 (Analiza JSON)
**Model:** Azure GPT-5 Chat
**Lokalizacja:** Linie 823-865
**Credentials:** OpenAi account 11 (ID: im1Fo28cUIM0GySs)

**Zadanie:**
- Analiza JSON z porównaniem dokumentów
- Wykrywanie przeniesionych treści (>90% podobieństwa)
- Ignorowanie zmian redakcyjnych
- Generowanie 5-7 najważniejszych zmian

**System Prompt (fragmenty):**
```
⚠️ KRYTYCZNE - WYKRYWANIE I POMIJANIE PRZENIESIONYCH TREŚCI:
1. Porównaj wszystkie paragrafy "deleted" z "added"
2. Jeśli >90% podobieństwa → POMIŃ
3. Raportuj TYLKO:
   - Rzeczywiście nową treść
   - Rzeczywiście usuniętą treść
   - Istotne modyfikacje

OCZEKIWANY FORMAT:
Maksymalnie 5-7 najważniejszych zmian w punktach
```

**Status:** ✅ **Dobrze skonfigurowany**

---

### AI Agent4 (Weryfikacja)
**Model:** Azure GPT-5 Chat
**Lokalizacja:** Linie 1009-1050
**Credentials:** OpenAi account 11 (ID: im1Fo28cUIM0GySs)

**Zadanie:**
- Weryfikacja podsumowania z AI Agent3
- Sprawdzenie prawdziwości zmian
- Usunięcie przeformułowań bez zmiany znaczenia
- Ostateczna lista 5-7 zmian

**System Prompt (fragmenty):**
```
1. SPRAWDŹ PRAWDZIWOŚĆ
   - Czy każda zmiana faktycznie występuje?

2. SPRAWDŹ ISTOTNOŚĆ MERYTORYCZNĄ
   USUŃ:
   - Przeformułowania bez zmiany znaczenia
   - Zmiany struktury zdania
   - Przeniesienia tekstu

   ZACHOWAJ:
   - Zmiany wartości liczbowych
   - Zmiany zakresu zastosowania
   - Nowe/usunięte sekcje

PYTANIE TESTOWE:
"Czy ta zmiana wymaga innych działań lub wpływa na prawa i obowiązki?"
- Jeśli NIE → usuń
- Jeśli TAK → zachowaj
```

**Status:** ✅ **Bardzo dobrze skonfigurowany** (dwuetapowa weryfikacja)

---

## 📊 PRZETWARZANIE PDF

### Extract from File (Stary dokument)
**Lokalizacja:** Linie 881-895
**Typ:** PDF extraction
**Binary Property:** `data0`
**Output:** → Edit Fields1 → `text_v1`

### Extract from File2 (Nowy dokument)
**Lokalizacja:** Linie 942-956
**Typ:** PDF extraction
**Binary Property:** `data1`
**Output:** → Edit Fields → `text_v2`

**Merge1:**
Łączy `text_v1` i `text_v2` przed przekazaniem do AI Agent4

**Status:** ✅ **Poprawnie skonfigurowane**

---

## 📧 GENEROWANIE EMAIL

### Code in JavaScript4 (HTML Template)
**Lokalizacja:** Linie 1052-1063
**Funkcja:** Formatowanie email HTML z:
- Logo Credit Agricole (base64)
- Tabela z metadanymi dokumentu
- Podsumowanie zmian (lista punktowana)
- Link do szczegółowej analizy: `http://217.182.76.146/reports/${fileid}`

**Template:**
```html
<table border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td>Logo CA (80x80)</td>
    <td>Dzień dobry, zapoznaj się z nowym aktem wewnętrznym</td>
  </tr>
  <tr><td colspan="2">Linia rozdzielająca (#009795)</td></tr>
  <tr>
    <td>Typ aktu</td>
    <td>Zarządzenie</td>
  </tr>
  <!-- ... metadane ... -->
  <tr>
    <td>Podsumowanie zmian</td>
    <td>${formattedContent}</td> <!-- Lista punktowana z AI Agent4 -->
  </tr>
  <tr>
    <td>Szczegółowa analiza zmian</td>
    <td><a href="http://217.182.76.146/reports/${fileid}">Link</a></td>
  </tr>
</table>
```

**Kolory:**
- `#009795` - Duck blue (główny akcent)
- `#707173` - Szary tekst
- Font: 11pt/12pt

**Status:** ✅ **Dobrze zaprojektowany**

---

### Send email
**Lokalizacja:** Linie 800-822
**Typ:** n8n-nodes-base.emailSend
**Credentials:** SMTP account 4 (ID: 2joSLF2U4RnAaaXW)

**Konfiguracja:**
- **From:** ai_baw@credit-agricole.pl
- **To:** trembiasz@credit-agricole.pl
- **Subject:** "Podsumowanie zmian w dokumentach"
- **HTML:** `={{ $json.html }}`

**Status:** ✅ **Poprawnie skonfigurowane**

---

## 🗄️ INTEGRACJA Z BAZAMI DANYCH

### MS SQL Queries (3 węzły)

#### 1. Select_no_1 (Linie 139-158)
**Cel:** Pobranie dokumentów do przetworzenia z BAW DB
**Query:** Wybiera dokumenty z określonego zakresu czasu (obliczony wcześniej)

#### 2. Select_no_2 (Linie 160-179)
**Cel:** Pobranie ID pliku dla dokumentu

#### 3. Select_no3 (Linie 380-397)
**Cel:** Pobranie linków do plików (stary + nowy)

**Status:** ✅ **Poprawnie skonfigurowane**

---

### SeaTable Operations (4 węzły)

#### 1. Check_if_exist (Linie 180-238)
**Cel:** Sprawdzenie czy dokument już był przetwarzany
**Credentials:** SeaTable account 3 (ID: 308kg9y7cDXLbrvU)

#### 2. Insert_into_db (Linie 239-285)
**Cel:** Zapis informacji o rozpoczęciu przetwarzania

#### 3. Insert_into_db2 (Linie 286-332)
**Cel:** Update statusu przetwarzania

#### 4. insert_do_pobrania (Linie 592-636)
**Cel:** Zapis metadanych dokumentu (MasterDocumentId, wersja, file_id, nazwa, link)

**Status:** ✅ **Poprawnie skonfigurowane**

---

## 🔄 LOGIKA PRZEPŁYWU

### Loop Over Items
**Typ:** Split In Batches
**Lokalizacja:** Linie 94-138
**Funkcja:** Przetwarzanie dokumentów pojedynczo
**Reset:** `true` (poprawne)

### Switch (Routing)
**Lokalizacja:** Linie 333-379
**Logika:**
- **Ścieżka 0:** Dokument nowy → Insert_into_db + Loop Over Items
- **Ścieżka 1:** Dokument już przetworzony → Loop Over Items + Event_log

**Status:** ✅ **Poprawna logika**

---

### Is Completed? (Polling)
**Lokalizacja:** Linie 723-742
**Typ:** IF node
**Warunek:** `$json.status == "completed"`

**Ścieżki:**
- **True:** → Get Full Result (⚠️ DISABLED!) → Final Summary
- **False:** → Wait 2 Seconds → Check Status (loop)

**Status:** ⚠️ **Działa, ale bez timeoutu**

---

## 🚨 ZIDENTYFIKOWANE PROBLEMY

### Priorytet P0 (Krytyczny)

#### P0-1: Get Full Result WYŁĄCZONY
**Opis:** Węzeł pobierający pełny wynik jest disabled
**Lokalizacja:** Linia 771
**Fix:**
```json
"disabled": false  // lub usuń całą linię
```

---

### Priorytet P1 (Ważny)

#### P1-1: Brak timeout w polling loop
**Opis:** Check Status może się zapętlić w nieskończoność
**Rozwiązanie:**
- Dodać węzeł licznika (np. Set node z incrementem)
- IF: jeśli licznik > 60 → Error handler
- Timeout = 60 iteracji × 2s = 2 minuty

#### P1-2: Brak error handlingu dla API calls
**Węzły bez error handlingu:**
- Upload Documents
- Start Processing
- Check Status
- HTTP Request (generate report)

**Rozwiązanie:**
- Dodać Error Workflow
- Logowanie błędów do SeaTable
- Email z notyfikacją o błędzie

---

### Priorytet P2 (Rekomendacja)

#### P2-1: Nieużywane API podsumowań (v1.1.0)
**Opis:** Workflow nie korzysta z nowych 6 endpointów summary
**Korzyści z użycia:**
- Zapis podsumowań w storage
- Edycja przez użytkownika w UI
- Historia zmian
- Zatwierdzanie przed wysłaniem

**Implementacja:**
1. Po AI Agent3 → POST /api/summary
2. Email z linkiem do edycji
3. Polling: GET /api/summary/{id}/status
4. Po approved → GET /api/summary/{id}/approved
5. Kontynuacja workflow

#### P2-2: Hardcoded IP address
**Lokalizacja:** Wszystkie API calls
**Problem:** `http://217.182.76.146/api/...`
**Rozwiązanie:**
- Utworzyć zmienną globalną: `BAW_API_URL`
- Użyć: `={{ $env.BAW_API_URL }}/api/...`

#### P2-3: Hardcoded email recipient
**Lokalizacja:** Send email (linia 802)
**Problem:** `trembiasz@credit-agricole.pl`
**Rozwiązanie:**
- Przechowywać listę odbiorców w SeaTable
- Dynamiczne pobieranie based on document type/owner

---

### Priorytet P3 (Nice-to-have)

#### P3-1: Brak retry logic
**Opis:** API calls nie mają automatycznego retry
**Rozwiązanie:** Ustawić `options.retry` dla HTTP Request nodes:
```json
"options": {
  "timeout": 120000,
  "retry": {
    "maxTries": 3,
    "waitBetweenRetries": 5000
  }
}
```

#### P3-2: Brak webhook dla status updates
**Opis:** Polling każde 2s jest nieefektywny
**Rozwiązanie:**
- BAW API wysyła webhook po zakończeniu
- N8N nasłuchuje na webhookURL
- Eliminacja polling loop

---

## 📈 STATYSTYKI WORKFLOW

| Metryka | Wartość |
|---------|---------|
| **Łączna liczba węzłów** | 40 |
| **HTTP Request nodes** | 6 |
| **AI Agent nodes** | 2 |
| **MS SQL nodes** | 3 |
| **SeaTable nodes** | 4 |
| **Code nodes** | 5 |
| **Merge nodes** | 3 |
| **Wait nodes** | 2 |
| **Conditional nodes** | 3 |
| **Extract PDF nodes** | 2 |
| **Email node** | 1 |

**Złożoność:** 🟡 **ŚREDNIA** (40 węzłów, 2-3 gałęzie równoległe)

---

## ✅ MOCNE STRONY WORKFLOW

1. ✅ **Dwuetapowa weryfikacja AI** (Agent3 + Agent4) - eliminacja false positives
2. ✅ **Dokładne prompty** - szczegółowe instrukcje wykrywania przeniesionych treści
3. ✅ **Równoległe przetwarzanie** - PDF extraction + API upload jednocześnie
4. ✅ **Deduplikacja** - Check_if_exist zapobiega duplikatom
5. ✅ **Profesjonalny email** - HTML template z logo i tabelą
6. ✅ **Timeout na upload** - 120s dla dużych plików
7. ✅ **Split In Batches** - przetwarzanie pojedyncze, nie wszystkie naraz
8. ✅ **Struktura logiczna** - czytelny przepływ danych

---

## 📋 REKOMENDACJE WDROŻENIOWE

### 🔴 DO NATYCHMIASTOWEGO WDROŻENIA (P0)

1. **Włączyć węzeł "Get Full Result"**
   ```json
   // Linia 771: Zmienić
   "disabled": false
   ```

---

### 🟡 DO WDROŻENIA W CIĄGU TYGODNIA (P1)

2. **Dodać timeout dla polling loop**
   - Węzeł licznika iteracji
   - IF: iteracje > 60 → Error handler
   - Email notyfikacja o błędzie

3. **Dodać Error Workflow**
   - Catch errors z HTTP Request nodes
   - Log do SeaTable (tabela: errors)
   - Email alert

---

### 🟢 DO ROZWAŻENIA (P2)

4. **Integracja z API podsumowań v1.1.0**
   - POST /api/summary po AI Agent3
   - Email z linkiem do edycji
   - Polling GET /api/summary/{id}/status
   - GET /api/summary/{id}/approved po zatwierdzeniu

5. **Parametryzacja URL i email**
   - Zmienna globalna: `BAW_API_URL`
   - Lista odbiorców w SeaTable

---

### 🔵 OPTYMALIZACJE (P3)

6. **Retry logic dla API calls**
   - `maxTries: 3`, `waitBetweenRetries: 5000ms`

7. **Webhook zamiast pollingu**
   - BAW API → Webhook N8N po zakończeniu
   - Eliminacja Wait 2 Seconds loop

---

## 📊 OCENA KOŃCOWA

| Kategoria | Ocena | Komentarz |
|-----------|-------|-----------|
| **Architektura** | 9/10 | Czytelna, logiczna struktura |
| **Integracja API** | 7/10 | Podstawowe API OK, brak summary API |
| **Obsługa błędów** | 5/10 | Brak error handlingu i timeoutów |
| **AI/LLM** | 10/10 | Doskonałe prompty, dwuetapowa weryfikacja |
| **Wydajność** | 8/10 | Równoległe przetwarzanie, dobry timeout |
| **Utrzymanie** | 7/10 | Hardcoded wartości, brak zmiennych |
| **Bezpieczeństwo** | 8/10 | Credentials OK, brak retry może prowadzić do utraty danych |

**OCENA OGÓLNA:** 📊 **8/10** (Bardzo dobry workflow z drobnymi niedociągnięciami)

---

## 📝 PODSUMOWANIE

### ✅ Co działa dobrze:
- Kompletna integracja z BAW API (upload, process, status, report)
- Doskonała konfiguracja AI Agent (GPT-5)
- Deduplikacja przez SeaTable
- Profesjonalny email HTML
- Równoległe przetwarzanie PDF + Upload

### ⚠️ Co wymaga poprawy:
- **Krytyczne:** Włączyć węzeł "Get Full Result" (disabled)
- **Ważne:** Dodać timeout dla polling loop
- **Ważne:** Dodać error handling
- **Rekomendacja:** Użyć nowych API podsumowań (v1.1.0)
- **Rekomendacja:** Parametryzacja URL i email

### 🎯 Priorytetowa akcja:
**Natychmiast zmienić `"disabled": false` w węźle "Get Full Result" (linia 771)**

---

## 📞 KONTAKT

**Raport przygotowany przez:** Claude Code
**Data:** 2025-10-28
**Wersja dokumentu:** 1.0.0
**Powiązane dokumenty:**
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - v1.2.0
- [N8N_SUMMARY_INTEGRATION.md](N8N_SUMMARY_INTEGRATION.md) - Dokumentacja API podsumowań
- [test_summaries.http](test_summaries.http) - Testy API podsumowań

---

**Koniec raportu weryfikacji workflow N8N**
