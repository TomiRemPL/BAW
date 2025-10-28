# 🚀 Import dla N8N 1.111.0

**Wersja N8N:** 1.111.0 (November 2024)
**Data:** 2025-10-28
**Status:** ✅ Gotowy do importu

---

## 📦 PLIK DO IMPORTU

```
C:\Projects\BAW\API 04 Enhanced - N8N 1.111.0.json
```

**Rozmiar:** ~92 KB
**Węzłów:** 65 (+15 nowych)
**Kompatybilność:** ✅ N8N 1.111.0

---

## 🔧 CO ZOSTAŁO DOSTOSOWANE

### 1. Switch Node "Is Approved or Timeout?"
- ✅ `typeVersion: 3`
- ✅ `operator` jako string: `"equals"`, `"gte"`
- ✅ `rightValue` jako string: `"60"`, `"approved"`, `"rejected"`
- ✅ Struktura `rules: { rules: [...] }`
- ✅ Struktura `conditions: { conditions: [...] }`

### 2. Set Nodes (Init Counter, Increment Counter)
- ✅ `typeVersion: 3.4`
- ✅ Struktura `assignments: { assignments: [...] }`
- ✅ Każdy assignment ma: `id`, `name`, `value`, `type`

### 3. HTTP Request Nodes
- ✅ `typeVersion: 4.2`
- ✅ **Retry usunięty** z JSON (dodasz ręcznie po imporcie)
- ✅ `timeout` zachowany

### 4. Email Send Nodes
- ✅ `typeVersion: 2.1`
- ✅ Puste `options: {}` usunięte

### 5. Wait Nodes
- ✅ `typeVersion: 1`
- ✅ Unikalne `webhookId` dla każdego

### 6. Merge Nodes
- ✅ `typeVersion: 3.2`

### 7. Code Nodes
- ✅ `typeVersion: 2`

---

## 🚀 IMPORT - KROK PO KROKU

### KROK 1: Import do N8N

1. **Otwórz N8N:**
   ```
   http://localhost:5678
   ```

2. **Import workflow:**
   ```
   Workflows → Import from File
   ```

3. **Wybierz plik:**
   ```
   C:\Projects\BAW\API 04 Enhanced - N8N 1.111.0.json
   ```

4. **Kliknij Import**

5. **Sprawdź:**
   - ✓ Nazwa: "API 04"
   - ✓ Węzłów: 65
   - ✓ **Brak błędu "could not find property option"** ✅

---

### KROK 2: Dodaj Retry Logic (Ręcznie)

⚠️ **WAŻNE:** Retry configuration musi być dodana ręcznie w UI.

#### A) **Create Summary** (HTTP Request)

1. Kliknij węzeł **"Create Summary"**
2. Kliknij ikonę **Settings** ⚙️ (prawy górny róg)
3. **Retry On Fail:** ON ✅
4. **Max Tries:** `3`
5. **Wait Between Tries (ms):** `2000`
6. **Save**

#### B) **Check Summary Status** (HTTP Request)

1. Kliknij węzeł **"Check Summary Status"**
2. Settings ⚙️
3. **Retry On Fail:** ON ✅
4. **Max Tries:** `2`
5. **Wait Between Tries (ms):** `1000`
6. **Save**

#### C) **Get Approved Summary** (HTTP Request)

1. Kliknij węzeł **"Get Approved Summary"**
2. Settings ⚙️
3. **Retry On Fail:** ON ✅
4. **Max Tries:** `3`
5. **Wait Between Tries (ms):** `2000`
6. **Save**

---

### KROK 3: Weryfikacja Credentials

Sprawdź czy credentials działają:

1. **SMTP account 4** (ID: `2joSLF2U4RnAaaXW`)
   - N8N → Credentials → SMTP account 4
   - Test Connection → ✅ OK

2. **SeaTable account 3** (ID: `308kg9y7cDXLbrvU`)
   - N8N → Credentials → SeaTable account 3
   - Test Connection → ✅ OK

3. **OpenAi account 11** (ID: `im1Fo28cUIM0GySs`)
   - N8N → Credentials → OpenAi account 11
   - Test Connection → ✅ OK

---

### KROK 4: Weryfikacja Węzłów

Sprawdź kluczowe węzły:

#### ✓ **AI Agent3 → Create Summary**
```
Połączenie: AI Agent3 (output) → Create Summary (input)
NIE: AI Agent3 → Merge
```

#### ✓ **Is Approved or Timeout?** (4 wyjścia)
```
Output 0: approved → Get Approved Summary
Output 1: rejected → Send Rejection Email
Output 2: timeout → Log Timeout Error
Output 3: fallback (continue_polling) → Wait 10 Seconds
```

#### ✓ **Wait 10 Seconds → Check Summary Status** (LOOP)
```
Pętla pollingu: Wait 10s → Check Status → Increment → Is Approved?
```

#### ✓ **Init Counter** (wartości początkowe)
```
iteration_count: 0
summary_id: {{ $('Create Summary').item.json.summary_id }}
process_id: {{ $('Start Processing').item.json.process_id }}
```

---

### KROK 5: Test Workflow

#### Test 1: Approve Flow (5-10 min)

```bash
1. Execute Workflow (ręcznie)
2. Sprawdź email: "⏳ Podsumowanie wymaga zatwierdzenia"
3. Otwórz link: http://217.182.76.146/summary/{id}
4. Edytuj tekst → Zatwierdź ✅
5. Sprawdź email: "✅ ZATWIERDZONE podsumowanie"
```

**Oczekiwany rezultat:**
- ✅ 2 emaile otrzymane
- ✅ Workflow zakończony sukcesem
- ✅ Polling działał (Check Summary Status co 10s)

---

#### Test 2: Timeout Flow (10 min)

```bash
1. Execute Workflow
2. Otrzymaj email z linkiem
3. NIE OTWIERAJ linku (czekaj 10 minut)
4. Po 10 min → Email: "⚠️ TIMEOUT"
5. Sprawdź SeaTable → tabela "errors" → nowy wpis
```

**Oczekiwany rezultat:**
- ✅ Timeout po 60 iteracjach (60 × 10s = 10 min)
- ✅ Email alert
- ✅ Log w SeaTable

---

#### Test 3: Reject Flow (2 min)

```bash
1. Execute Workflow
2. Otwórz link z emaila
3. Kliknij: "❌ Odrzuć"
4. Sprawdź email: "❌ Podsumowanie odrzucone"
```

**Oczekiwany rezultat:**
- ✅ Rejection email
- ✅ Workflow zakończony

---

## ✅ CHECKLIST WDROŻENIOWY

### Import:
- [ ] Plik `API 04 Enhanced - N8N 1.111.0.json` zaimportowany
- [ ] Import bez błędów
- [ ] 65 węzłów widocznych

### Retry:
- [ ] Create Summary: Retry ON (tries=3, wait=2000ms)
- [ ] Check Summary Status: Retry ON (tries=2, wait=1000ms)
- [ ] Get Approved Summary: Retry ON (tries=3, wait=2000ms)

### Credentials:
- [ ] SMTP account 4 - Test OK
- [ ] SeaTable account 3 - Test OK
- [ ] OpenAi account 11 - Test OK

### Węzły:
- [ ] AI Agent3 → Create Summary (połączenie OK)
- [ ] Is Approved or Timeout? → 4 wyjścia
- [ ] Wait 10 Seconds → Check Summary Status (loop OK)
- [ ] Init Counter → wartości początkowe (iteration_count=0)

### Testy:
- [ ] Test 1: Approve flow - PASS
- [ ] Test 2: Timeout flow - PASS
- [ ] Test 3: Reject flow - PASS

### Produkcja:
- [ ] Backend: v1.1.0 z API podsumowań
- [ ] Frontend: Editor podsumowań działa
- [ ] Workflow: Active = ON
- [ ] Schedule: Co 30 minut

---

## 📊 STATYSTYKI

| Metryka | Before | After |
|---------|--------|-------|
| Węzłów | 50 | **65** (+15) |
| API calls | 6 | **11** (+5) |
| Email notifications | 1 | **4** (+3) |
| Error handling | 0 | **3** (+3) |
| Timeout protection | ❌ | ✅ (10 min) |
| User approval | ❌ | ✅ (UI editor) |

---

## 🐛 TROUBLESHOOTING

### Problem: Nadal "could not find property option"

**Sprawdź:**
1. Czy importujesz właściwy plik: `API 04 Enhanced - N8N 1.111.0.json`
2. Czy wersja N8N to naprawdę 1.111.0 (Settings → About)
3. Czy plik ma ~92 KB

**Debugging:**
```bash
# Sprawdź strukturę Switch node:
python -c "import json; w=json.load(open('API 04 Enhanced - N8N 1.111.0.json','r',encoding='utf-8')); node=[n for n in w['nodes'] if n['name']=='Is Approved or Timeout?'][0]; print('Operator:', node['parameters']['rules']['rules'][0]['conditions']['conditions'][0]['operator'])"

# Powinno zwrócić: Operator: equals
```

### Problem: Email nie wysyła

**Rozwiązanie:**
```
Credentials → SMTP account 4 → Test Connection
Jeśli błąd → zaktualizuj hasło/ustawienia SMTP
```

### Problem: Backend zwraca 404 na /api/summary

**Rozwiązanie:**
```bash
# Sprawdź czy backend ma v1.1.0:
curl http://217.182.76.146/health | grep "total_summaries"

# Jeśli brak → deploy nowej wersji backend
```

### Problem: Polling nie kończy się po 10 minutach

**Sprawdź:**
1. Węzeł "Increment Counter":
   - `iteration_count` rośnie? (1, 2, 3... 60)

2. Węzeł "Is Approved or Timeout?":
   - Warunek timeout: `iteration_count >= 60`
   - rightValue: `"60"` (string!)

3. Executions:
   - N8N → Executions → Zobacz aktywne wykonanie
   - Sprawdź ile iteracji przeszło

---

## 📄 PLIKI

### Do importu:
- ⭐ **`API 04 Enhanced - N8N 1.111.0.json`** - **UŻYJ TEGO**

### Backup:
- `API 04.json.backup` - Oryginalny workflow

### Wcześniejsze wersje (nie używaj):
- `API 04 Enhanced.json` - Z błędem
- `API 04 Enhanced Fixed.json` - Dla starszego N8N
- `API 04 Enhanced v2.json` - Uproszczony

### Dokumentacja:
- `N8N_WORKFLOW_VERIFICATION.md` - Analiza v1.0.0
- `N8N_WORKFLOW_ENHANCED.md` - Dokumentacja v2.0.0
- `N8N_WORKFLOW_QUICKSTART.md` - Quick Start
- `WORKFLOW_MODIFICATION_SUMMARY.md` - Podsumowanie zmian
- `IMPORT_N8N_1.111.0.md` - Ten dokument

### Skrypty:
- `fix_workflow_n8n_1_111.py` - Generator dla N8N 1.111.0

---

## 🎯 PODSUMOWANIE

**Plik dla N8N 1.111.0:**
```
API 04 Enhanced - N8N 1.111.0.json
```

**Po imporcie:**
1. ✅ Dodaj retry w 3 węzłach HTTP Request (ręcznie)
2. ✅ Sprawdź credentials (3)
3. ✅ Wykonaj testy (3)
4. ✅ Aktywuj workflow

**To powinno działać!** 🚀

---

**Data:** 2025-10-28
**Przygotowane dla:** N8N 1.111.0
**Przygotowane przez:** Claude Code

**Powodzenia z importem!** 🎉
