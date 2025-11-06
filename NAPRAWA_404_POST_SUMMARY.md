# Naprawa 404 - POST /api/summary

## ❌ Problem

Workflow n8n otrzymywał **404 Not Found** przy POST do `/api/summary`.

### Objawy:
```
Error code: 404
Full message: 404 - "{\"detail\":\"Not Found\"}"
URI: http://217.182.76.146/api/summary
Method: POST
```

---

## 🔍 Analiza

### Krok 1: Test backendu bezpośrednio

```bash
curl -X POST http://localhost:8001/api/summary \
  -H "Content-Type: application/json" \
  -d '{"process_id":"test","summary_text":"Test","metadata":{}}'
```

**Wynik:** ✅ **Działa** - backend zwraca 200 OK

### Krok 2: Sprawdzenie routingu Nginx

```bash
cat /etc/nginx/sites-available/baw-api | grep -A 10 "/api/summary"
```

**Znaleziono:**
```nginx
location /api/summary/ {
    proxy_pass http://localhost:8000/api/summary/;
    ...
}
```

### Problem zidentyfikowany:

1. **Location:** `/api/summary/` (ze slashem na końcu)
2. **Request:** `/api/summary` (bez slasha)
3. **Routing:** Request nie pasuje do location, trafia do ogólnego `/api/` → backend
4. **ALE:** Nginx widzi `/api/summary/` jako osobny location i przekierowuje do port 8000
5. **SecureDocCompare (8000):** Nie ma endpointu POST `/api/summary` - zwraca 404

---

## ✅ Rozwiązanie

### Zmiana strategii routingu

**PRZED (błędne):**
```nginx
# Przekierowywało /api/summary do SecureDocCompare
location /api/summary/ {
    proxy_pass http://localhost:8000/api/summary/;
}

# Ogólne /api/ do backendu
location /api/ {
    proxy_pass http://localhost:8001/api/;
}
```

**Problem:** POST `/api/summary` (bez trailing slash) nie pasował do `/api/summary/`, więc trafiał gdzieś indziej.

**PO (poprawne):**
```nginx
# WSZYSTKIE /api/* idą do backendu (w tym /api/summary)
location /api/ {
    proxy_pass http://localhost:8001/api/;
}

# Frontend tylko dla /summary/ (strona HTML)
location /summary/ {
    proxy_pass http://localhost:8000/summary/;
}
```

**Architektura:**
- **n8n POST `/api/summary`** → Nginx → **Backend (8001)** ✅
- **SecureDocCompare GET `/api/summary/{id}`** → SecureDocCompare (8000) → **proxy do Backend (8001)** ✅
- **Browser GET `/summary/{id}`** → Nginx → **SecureDocCompare (8000)** → HTML ✅

---

## 📊 Przebieg requestów

### Scenariusz 1: n8n tworzy podsumowanie

```
n8n → POST http://217.182.76.146/api/summary
        ↓
     Nginx (/api/ → 8001)
        ↓
   Backend API (8001)
        ↓
   Response: {"status": "pending_review", ...}
```

### Scenariusz 2: User edytuje przez browser

```
Browser → GET http://217.182.76.146/summary/{id}
            ↓
         Nginx (/summary/ → 8000)
            ↓
    SecureDocCompare (8000) - zwraca HTML
            ↓
         Browser renderuje stronę
```

### Scenariusz 3: JavaScript na stronie pobiera dane

```
Browser JS → GET http://217.182.76.146/api/summary/{id}
                ↓
             Nginx (/api/ → 8001)
                ↓
           Backend API (8001)
                ↓
           Response: JSON z podsumowaniem
```

**Uwaga:** SecureDocCompare ma proxy endpoints, które **również** wywołują backend na 8001, ale **przez Nginx wszystko idzie bezpośrednio do backendu**.

---

## 🧪 Testy

### Test 1: POST /api/summary (n8n)

```bash
curl -X POST http://217.182.76.146/api/summary \
  -H "Content-Type: application/json" \
  -d '{
    "process_id": "test-final",
    "summary_text": "Test",
    "metadata": {}
  }'
```

**Wynik:** ✅ **200 OK**
```json
{
  "process_id": "test-final",
  "status": "pending_review",
  "created_at": "...",
  ...
}
```

### Test 2: GET /summary/{id} (strona HTML)

```bash
curl -I http://217.182.76.146/summary/test-final
```

**Wynik:** ✅ **200 OK** - HTML strona

### Test 3: GET /api/summary/{id} (API)

```bash
curl http://217.182.76.146/api/summary/test-final
```

**Wynik:** ✅ **200 OK** - JSON z podsumowaniem

---

## 📁 Pliki

### Konfiguracja Nginx

**Plik lokalny:** `C:\Projects\BAW\nginx-baw-api-final.conf`

**Plik na serwerze:** `/etc/nginx/sites-available/baw-api`

**Zastosowanie:**
```bash
scp nginx-baw-api-final.conf debian@217.182.76.146:/tmp/
ssh debian@217.182.76.146 "sudo cp /tmp/nginx-baw-api-final.conf /etc/nginx/sites-available/baw-api"
ssh debian@217.182.76.146 "sudo nginx -t && sudo systemctl reload nginx"
```

---

## ✅ Workflow gotowy

**Plik:** `API 08 - fixed POST v2.json`

**Status:**
- ✅ Node POST Summary to API naprawiony (JSON body)
- ✅ Nginx routing naprawiony (wszystko /api/* → 8001)
- ✅ Link w emailu działa
- ✅ Strona edytora działa

---

## 🎯 Podsumowanie zmian

| Element | Przed | Po |
|---------|-------|-----|
| **Nginx /api/summary/** | → port 8000 (SecureDocCompare) | **Usunięto** |
| **Nginx /api/** | → port 8001 (Backend) | ✅ Pozostaje |
| **POST /api/summary** | 404 Not Found ❌ | 200 OK ✅ |
| **GET /summary/{id}** | 200 OK ✅ | 200 OK ✅ |
| **GET /api/summary/{id}** | 200 OK ✅ | 200 OK ✅ |

---

## 🐛 Dlaczego to się stało?

Poprzednia konfiguracja próbowała routing `/api/summary` przez SecureDocCompare, aby ten mógł działać jako proxy. **Ale:**

1. SecureDocCompare proxy **sam wywołuje backend na 8001**
2. Nie ma potrzeby routować przez niego z Nginx
3. Prostsze rozwiązanie: **Wszystko /api/* bezpośrednio do backendu**

---

## 📚 Lekcja

### Routing Nginx - kolejność ma znaczenie

```nginx
# ❌ ŹLE - szczegółowe po ogólnym
location /api/ { ... }           # To pasuje do /api/summary
location /api/summary/ { ... }   # Nigdy nie zostanie użyte!

# ✅ DOBRZE - szczegółowe przed ogólnym
location /api/summary/ { ... }   # Najpierw sprawdza szczegółowe
location /api/ { ... }           # Potem ogólne

# ✅ NAJLEPIEJ - jedno ogólne, proste
location /api/ { ... }           # Wszystko /api/* w jednym miejscu
```

### Trailing slash

```nginx
location /api/summary/ { ... }   # Pasuje: /api/summary/xxx
                                  # NIE pasuje: /api/summary

location /api/summary { ... }    # Pasuje: /api/summary
                                  # Pasuje też: /api/summary/xxx
```

---

## ✅ Checklist weryfikacji

Po zastosowaniu naprawy sprawdź:

- [ ] `curl -X POST http://217.182.76.146/api/summary ...` → 200 OK
- [ ] `curl http://217.182.76.146/summary/test-123` → 200 OK (HTML)
- [ ] `curl http://217.182.76.146/api/summary/test-123` → 200 OK (JSON)
- [ ] W n8n: Node "POST Summary to API" zwraca status "pending_review"
- [ ] Link w emailu otwiera stronę edytora
- [ ] Strona edytora ładuje dane z API

---

## 🚀 Status: NAPRAWIONE

**Data naprawy:** 2025-10-29

**Pliki:**
- ✅ `nginx-baw-api-final.conf` - Finalna konfiguracja Nginx
- ✅ `API 08 - fixed POST v2.json` - Workflow z naprawionym POST

**Testy:**
- ✅ POST /api/summary → 200 OK
- ✅ GET /summary/{id} → 200 OK
- ✅ GET /api/summary/{id} → 200 OK

**Gotowe do produkcji!** 🎉
