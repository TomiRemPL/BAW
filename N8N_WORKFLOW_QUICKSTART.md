# 🚀 N8N Enhanced Workflow - Quick Start Guide

**Wersja:** 2.0.0
**Data:** 2025-10-28

---

## 📊 DIAGRAM PRZEPŁYWU

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         STARY FLOW (v1.0.0)                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Final Summary → AI Agent3 → Merge → AI Agent4 → Format Email          │
│                               ↑                         ↓               │
│                        Merge1 (text_v1/v2)       Send email → END       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         NOWY FLOW (v2.0.0)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Final Summary                                                          │
│       ↓                                                                 │
│  AI Agent3 (GPT-5 Analysis)                                             │
│       ↓                                                                 │
│  ┌────────────────────────────────┐                                    │
│  │ Create Summary                 │ POST /api/summary                  │
│  │ (Zapis w storage)              │                                    │
│  └────────────────────────────────┘                                    │
│       ↓                                                                 │
│  ┌────────────────────────────────┐                                    │
│  │ Send Edit Link Email           │ 📧 Email z linkiem                 │
│  │ (Do użytkownika)               │                                    │
│  └────────────────────────────────┘                                    │
│       ↓                                                                 │
│  Wait 30 Seconds                                                        │
│       ↓                                                                 │
│  Init Counter (iteration_count = 0)                                     │
│       ↓                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐       │
│  │                    POLLING LOOP                             │       │
│  │  ┌───────────────────────────────────────────────┐          │       │
│  │  │ Check Summary Status                          │          │       │
│  │  │ GET /api/summary/{id}/status                  │          │       │
│  │  └───────────────────────────────────────────────┘          │       │
│  │                       ↓                                     │       │
│  │  ┌───────────────────────────────────────────────┐          │       │
│  │  │ Increment Counter                             │          │       │
│  │  │ iteration_count++                             │          │       │
│  │  └───────────────────────────────────────────────┘          │       │
│  │                       ↓                                     │       │
│  │  ┌───────────────────────────────────────────────┐          │       │
│  │  │ Is Approved or Timeout?                       │          │       │
│  │  │ ┌─────────────────────────────────────┐       │          │       │
│  │  │ │ approved?    → Get Approved Summary │       │          │       │
│  │  │ │ rejected?    → Send Rejection Email │       │          │       │
│  │  │ │ timeout?     → Log Error + Alert    │       │          │       │
│  │  │ │ pending?     → Wait 10s → LOOP ↑    │       │          │       │
│  │  │ └─────────────────────────────────────┘       │          │       │
│  │  └───────────────────────────────────────────────┘          │       │
│  │                                                             │       │
│  │  Max 60 iteracji × 10s = 10 minut                          │       │
│  └─────────────────────────────────────────────────────────────┘       │
│                           ↓ (approved)                                  │
│  ┌────────────────────────────────┐                                    │
│  │ Get Approved Summary           │ GET /api/summary/{id}/approved     │
│  └────────────────────────────────┘                                    │
│       ↓                                                                 │
│  ┌────────────────────────────────┐                                    │
│  │ Merge Final Data               │ Summary + Report                   │
│  │ (Approved text + report link)  │                                    │
│  └────────────────────────────────┘                                    │
│       ↓                                                                 │
│  ┌────────────────────────────────┐                                    │
│  │ Format Final Email             │ HTML Template                      │
│  │ (Z zatwierdzonym tekstem)      │                                    │
│  └────────────────────────────────┘                                    │
│       ↓                                                                 │
│  ┌────────────────────────────────┐                                    │
│  │ Send Final Email               │ 📧 Finalny email                   │
│  └────────────────────────────────┘                                    │
│       ↓                                                                 │
│     END                                                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔥 SZYBKI START

### Krok 1: Przygotowanie Backend (UslugaDoPorownan)

Upewnij się że backend ma nowe API podsumowań (v1.1.0):

```bash
# Test endpointów
curl http://localhost:8001/health

# Sprawdź czy są statystyki summary:
# "total_summaries": 0, "pending_summaries": 0, "approved_summaries": 0
```

Jeśli brak statystyk → backend wymaga aktualizacji do v1.1.0

---

### Krok 2: Przygotowanie Frontend (SecureDocCompare)

Upewnij się że frontend ma editor podsumowań:

```bash
# Test URL:
curl http://localhost:8000/summary/test-123
# Powinno zwrócić stronę edytora lub 404 jeśli summary nie istnieje
```

---

### Krok 3: Import węzłów do N8N

#### Opcja A: Import z pliku JSON (zalecane)
1. Otwórz N8N: http://localhost:5678
2. Workflows → Import from File
3. Wybierz `API 04 Enhanced.json` (jeśli zostanie wygenerowany)

#### Opcja B: Manualne dodanie węzłów
1. Otwórz istniejący workflow "API 04"
2. Znajdź węzeł "AI Agent3"
3. Usuń połączenie: AI Agent3 → Merge
4. Dodaj 15 nowych węzłów (konfiguracje z N8N_WORKFLOW_ENHANCED.md)
5. Połącz węzły zgodnie z diagramem

---

### Krok 4: Konfiguracja połączeń

**USUŃ stare połączenie:**
```
AI Agent3 → Merge (INPUT 0)
```

**DODAJ nowe połączenia:**
```
AI Agent3 → Create Summary
Create Summary → Send Edit Link Email
Send Edit Link Email → Wait for User
Wait for User → Init Counter
Init Counter → Check Summary Status
Check Summary Status → Increment Counter
Increment Counter → Is Approved or Timeout?

Is Approved or Timeout? (Output 0: approved) → Get Approved Summary
Is Approved or Timeout? (Output 1: rejected) → Send Rejection Email
Is Approved or Timeout? (Output 2: timeout) → Log Timeout Error
Is Approved or Timeout? (Output 3: continue_polling) → Wait 10 Seconds

Wait 10 Seconds → Check Summary Status (LOOP)

Get Approved Summary → Merge Final Data (INPUT 0)
HTTP Request (report) → Merge Final Data (INPUT 1)

Merge Final Data → Format Final Email
Format Final Email → Send Final Email

Log Timeout Error → Send Timeout Email
```

---

### Krok 5: Weryfikacja konfiguracji

**Sprawdź czy wszystkie węzły HTTP Request mają retry:**

1. Create Summary:
   ```json
   "options": {
     "timeout": 30000,
     "retry": {
       "maxTries": 3,
       "waitBetweenRetries": 2000
     }
   }
   ```

2. Check Summary Status:
   ```json
   "options": {
     "timeout": 10000,
     "retry": {
       "maxTries": 2,
       "waitBetweenRetries": 1000
     }
   }
   ```

3. Get Approved Summary:
   ```json
   "options": {
     "timeout": 10000,
     "retry": {
       "maxTries": 3,
       "waitBetweenRetries": 2000
     }
   }
   ```

---

### Krok 6: Test workflow

#### Test manualny:

1. **Uruchom workflow:**
   - Kliknij "Execute Workflow" w N8N
   - Lub poczekaj na Schedule Trigger (co 30 min)

2. **Sprawdź email "Edit Link":**
   - Temat: "⏳ Podsumowanie dokumentu wymaga zatwierdzenia"
   - Zawiera: Link do http://217.182.76.146/summary/{id}

3. **Otwórz link i edytuj:**
   - Edytor Quill.js powinien się załadować
   - Edytuj tekst podsumowania
   - Kliknij "✅ Zatwierdź"

4. **Sprawdź polling w N8N:**
   - W Executions → Zobacz aktywne wykonanie
   - Węzeł "Check Summary Status" powinien się powtarzać co 10s
   - Po zatwierdzeniu → "Is Approved or Timeout?" → approved

5. **Sprawdź finalny email:**
   - Temat: "✅ Nowy akt wewnętrzny - ZATWIERDZONE podsumowanie"
   - Zawiera: Zatwierdzone podsumowanie + link do raportu
   - Footer: "✅ Zatwierdzone przez: {user}, 📅 Data zatwierdzenia"

---

#### Test timeout:

1. Uruchom workflow
2. Otrzymaj email "Edit Link"
3. **NIE OTWIERAJ LINKU** (nie zatwierdzaj)
4. Czekaj 10 minut (60 iteracji × 10s)
5. Sprawdź email:
   - Temat: "⚠️ TIMEOUT - Brak zatwierdzenia podsumowania"
   - Status: TIMEOUT

---

#### Test odrzucenia:

1. Uruchom workflow
2. Otrzymaj email "Edit Link"
3. Otwórz link
4. Kliknij "❌ Odrzuć"
5. Sprawdź email:
   - Temat: "❌ Podsumowanie dokumentu zostało odrzucone"
   - Status: REJECTED

---

## 📋 CHECKLIST PRE-DEPLOYMENT

### Backend (UslugaDoPorownan):
- [ ] Version v1.1.0 wdrożony
- [ ] Endpoint POST /api/summary działa
- [ ] Endpoint GET /api/summary/{id}/status działa
- [ ] Endpoint GET /api/summary/{id}/approved działa
- [ ] Storage zapisuje podsumowania
- [ ] Health check zwraca summary statistics

### Frontend (SecureDocCompare):
- [ ] Editor podsumowań działa (http://localhost:8000/summary/{id})
- [ ] Quill.js ładuje się poprawnie
- [ ] Buttons: Save, Approve, Reject działają
- [ ] PUT /api/summary/{id} (proxy) działa
- [ ] POST /api/summary/{id}/approve (proxy) działa

### N8N Workflow:
- [ ] 15 nowych węzłów dodanych
- [ ] Połączenia zgodne z diagramem
- [ ] Retry logic skonfigurowany
- [ ] Email credentials: SMTP account 4 (OK)
- [ ] SeaTable credentials: SeaTable account 3 (OK)
- [ ] Hardcoded IP: 217.182.76.146 (zachowany)
- [ ] Hardcoded email: trembiasz@credit-agricole.pl (zachowany)

### Testy:
- [ ] Test manualny: Approve → Final email ✅
- [ ] Test timeout: 10 minut → Timeout email ⚠️
- [ ] Test rejection: Reject → Rejection email ❌
- [ ] Test polling loop: Max 60 iteracji
- [ ] Test error handling: Log do SeaTable

---

## 🎯 KLUCZOWE RÓŻNICE v1.0 vs v2.0

| Funkcja | v1.0.0 | v2.0.0 Enhanced |
|---------|--------|-----------------|
| **Edycja podsumowania** | ❌ Nie | ✅ Tak (UI) |
| **Zatwierdzenie** | ❌ Automatyczne | ✅ Manualne przez użytkownika |
| **Timeout protection** | ❌ Brak | ✅ 10 minut (60 iter) |
| **Error handling** | ❌ Brak | ✅ Log + Email alerts |
| **Persistence** | ❌ Nie | ✅ Storage (in-memory) |
| **Email notifications** | 1 (final) | 4 (edit link + final + timeout + rejected) |
| **Polling** | Tylko status procesu | Status procesu + Status podsumowania |
| **AI verification** | 2-stage (Agent3 + Agent4) | 2-stage + Human approval |

---

## 🚨 TROUBLESHOOTING

### Problem: "Create Summary" zwraca 404

**Diagnoza:**
Backend nie ma endpointu POST /api/summary

**Rozwiązanie:**
```bash
# Sprawdź wersję backend:
curl http://217.182.76.146/health

# Jeśli brak "total_summaries" w odpowiedzi:
# Backend wymaga aktualizacji do v1.1.0
```

---

### Problem: Email "Edit Link" nie zawiera linku

**Diagnoza:**
Frontend nie ma edytora podsumowań

**Rozwiązanie:**
```bash
# Test frontend:
curl http://217.182.76.146/summary/test-123

# Jeśli 404 → Frontend wymaga aktualizacji
```

---

### Problem: Polling nigdy się nie kończy

**Diagnoza:**
- Frontend nie aktualizuje statusu
- Timeout nie działa

**Rozwiązanie:**
```bash
# Sprawdź czy węzeł "Increment Counter" działa:
# W N8N Executions → Zobacz wartość iteration_count
# Powinna rosnąć: 1, 2, 3, ... 60

# Sprawdź węzeł "Is Approved or Timeout?":
# Output 2 (timeout) powinien się wywołać gdy iteration_count >= 60
```

---

### Problem: Finalny email nie zawiera zatwierdzonego tekstu

**Diagnoza:**
- GET /api/summary/{id}/approved zwraca pusty tekst
- Merge Final Data nie łączy danych poprawnie

**Rozwiązanie:**
```bash
# Test API:
curl http://217.182.76.146/api/summary/{id}/approved

# Powinno zwrócić:
# {
#   "summary_text": "Zatwierdzona treść...",
#   "metadata": { "approved_by": "...", "approved_at": "..." }
# }

# Sprawdź w N8N:
# Węzeł "Get Approved Summary" → Output → $json.summary_text
```

---

## 📞 WSPARCIE

**Dokumentacja:**
- [N8N_WORKFLOW_VERIFICATION.md](N8N_WORKFLOW_VERIFICATION.md) - Analiza v1.0.0
- [N8N_WORKFLOW_ENHANCED.md](N8N_WORKFLOW_ENHANCED.md) - Dokumentacja v2.0.0 (15 węzłów)
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API endpoints (v1.2.0)
- [N8N_SUMMARY_INTEGRATION.md](N8N_SUMMARY_INTEGRATION.md) - Workflow integracji
- [test_summaries.http](test_summaries.http) - Testy API

**API Endpoints (Backend):**
- Health check: http://217.182.76.146/health
- API docs: http://217.182.76.146/docs
- Reports: http://217.182.76.146/reports/{filename}

**Frontend:**
- Summary editor: http://217.182.76.146/summary/{id}
- Login: http://217.182.76.146/login

**N8N:**
- Workflow interface: http://localhost:5678 (local dev)
- Executions: http://localhost:5678/executions
- Credentials: http://localhost:5678/credentials

---

## ✅ PODSUMOWANIE

**Status wdrożenia:** ✅ **Gotowe do testów**

**Co zostało zrobione:**
1. ✅ Analiza istniejącego workflow (v1.0.0)
2. ✅ Zidentyfikowanie problemów (P0-P3)
3. ✅ Zaprojektowanie enhanced workflow (v2.0.0)
4. ✅ Przygotowanie konfiguracji 15 nowych węzłów
5. ✅ Dodanie timeout protection (10 minut)
6. ✅ Implementacja error handling (log + email)
7. ✅ Integracja API podsumowań (6 endpointów)
8. ✅ Przygotowanie dokumentacji (3 pliki MD)

**Następny krok:**
👉 **Import węzłów do N8N i test workflow**

---

**Data:** 2025-10-28
**Wersja:** 2.0.0
**Przygotowane przez:** Claude Code

**Koniec Quick Start Guide**
