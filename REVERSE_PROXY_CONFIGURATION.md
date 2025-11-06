# Konfiguracja Reverse Proxy dla Edytora Podsumowań

## ✅ Status: SKONFIGUROWANE

Data konfiguracji: **2025-10-29**
Serwer: **217.182.76.146**
System: **Debian Linux**

---

## 📋 Co zostało zrobione

### 1. Zaktualizowano konfigurację Nginx

**Plik:** `/etc/nginx/sites-available/baw-api`

**Dodane sekcje:**

```nginx
# Frontend - SecureDocCompare (edytor podsumowań)
location /summary/ {
    proxy_pass http://localhost:8000/summary/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}

# API summary przez frontend (proxy do backend)
location /api/summary/ {
    proxy_pass http://localhost:8000/api/summary/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Content-Type application/json;

    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}

# Static files dla frontendu
location /static/ {
    proxy_pass http://localhost:8000/static/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;

    expires 1d;
    add_header Cache-Control "public, immutable";
}
```

### 2. Routing

| URL | Przekierowanie | Port | Usługa |
|-----|----------------|------|---------|
| `/summary/{id}` | → localhost:8000 | 8000 | SecureDocCompare (frontend) |
| `/api/summary/*` | → localhost:8000 | 8000 | SecureDocCompare (API proxy) |
| `/api/*` (inne) | → localhost:8001 | 8001 | Backend API |
| `/reports/` | → localhost:8001 | 8001 | Backend (raporty HTML) |
| `/static/` | → localhost:8000 | 8000 | SecureDocCompare (CSS/JS) |

### 3. Kolejność Location (WAŻNE!)

Nginx przetwarza location w kolejności **najbardziej szczegółowe → najmniej szczegółowe**.

Dlatego `/api/summary/` **MUSI BYĆ PRZED** `/api/` w konfiguracji:

```nginx
# ✅ POPRAWNIE - szczegółowe najpierw
location /api/summary/ { ... }
location /api/ { ... }

# ❌ ŹLE - ogólne zagłuszają szczegółowe
location /api/ { ... }
location /api/summary/ { ... }  # nigdy nie zostanie użyte!
```

---

## 🔍 Testy

### Test 1: Strona edytora

```bash
curl -I http://217.182.76.146/summary/test-123
```

**Oczekiwany wynik:** `HTTP/1.1 200 OK`

**Rzeczywisty wynik:** ✅ **200 OK** - strona HTML zwrócona

### Test 2: API GET summary

```bash
curl http://217.182.76.146/api/summary/demo-test-2025
```

**Oczekiwany wynik:** JSON z podsumowaniem lub 404 jeśli nie istnieje

**Rzeczywisty wynik:** ✅ Działa (404 dla nieistniejącego, JSON dla istniejącego)

### Test 3: Utworzenie testowego podsumowania

```bash
ssh debian@217.182.76.146 'curl -s -X POST "http://localhost:8001/api/summary" \
  -H "Content-Type: application/json" \
  -d "{\"process_id\":\"demo-test-2025\",\"summary_text\":\"Test\",\"metadata\":{}}"'
```

**Rzeczywisty wynik:** ✅ Utworzono podsumowanie

### Test 4: Otwarcie w przeglądarce

**URL:** http://217.182.76.146/summary/demo-test-2025

**Rzeczywisty wynik:** ✅ Strona się ładuje i pokazuje edytor

---

## 🚀 Usługi działające na serwerze

### Backend API (port 8001)

**Lokalizacja:** `/home/debian/hack/BAW/UslugaDoPorownan`

**Komenda:**
```bash
screen -dmS baw-backend bash -c "
  cd /home/debian/hack/BAW &&
  source .venv/bin/activate &&
  cd UslugaDoPorownan &&
  uvicorn main:app --host 0.0.0.0 --port 8001
"
```

**Status:** ✅ Uruchomiony (PID: 1557891)

### SecureDocCompare (port 8000)

**Lokalizacja:** `/home/debian/hack/BAW/SecureDocCompare`

**Komenda:**
```bash
screen -dmS baw-frontend bash -c "
  cd /home/debian/hack/BAW &&
  source .venv/bin/activate &&
  cd SecureDocCompare &&
  uvicorn main:app --host 0.0.0.0 --port 8000
"
```

**Status:** ✅ Uruchomiony (PID: 1557922)

---

## 🔗 Działające endpointy

### Frontend (przez Nginx)

| Endpoint | Opis |
|----------|------|
| `http://217.182.76.146/summary/{process_id}` | Strona edytora HTML |
| `http://217.182.76.146/static/css/style.css` | Pliki CSS |
| `http://217.182.76.146/static/js/app.js` | Pliki JS |

### API (przez Nginx → SecureDocCompare → Backend)

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/api/summary` | POST | Utwórz podsumowanie |
| `/api/summary/{id}` | GET | Pobierz podsumowanie |
| `/api/summary/{id}/status` | GET | Sprawdź status |
| `/api/summary/{id}` | PUT | Aktualizuj podsumowanie |
| `/api/summary/{id}/approve` | POST | Zatwierdź/odrzuć |

---

## 📧 Link w emailu n8n

**Format:**
```
http://217.182.76.146/summary/{{ process_id }}
```

**Przykład:**
```
http://217.182.76.146/summary/a8f3e71c-9d2b-4f1a-8e32-7c5d6b9a0f21
```

**Workflow:** `API 06 - with edit link.json`

**Node:** "Send Review Email"

---

## 🛠️ Zarządzanie

### Sprawdź status usług

```bash
# Backend
ssh debian@217.182.76.146 "ps aux | grep 'uvicorn.*8001'"

# Frontend
ssh debian@217.182.76.146 "ps aux | grep 'uvicorn.*8000'"
```

### Restart Nginx

```bash
ssh debian@217.182.76.146 "sudo systemctl reload nginx"
```

### Sprawdź logi Nginx

```bash
# Access log
ssh debian@217.182.76.146 "sudo tail -f /var/log/nginx/baw-api-access.log"

# Error log
ssh debian@217.182.76.146 "sudo tail -f /var/log/nginx/baw-api-error.log"
```

### Sprawdź logi aplikacji

```bash
# Backend (screen session)
ssh debian@217.182.76.146 "screen -r baw-backend"

# Frontend (screen session)
ssh debian@217.182.76.146 "screen -r baw-frontend"

# Wyjście z screen: Ctrl+A, D
```

---

## 🐛 Troubleshooting

### Problem: 502 Bad Gateway

**Przyczyna:** Usługa na porcie 8000 lub 8001 nie działa

**Rozwiązanie:**
```bash
# Sprawdź procesy
ssh debian@217.182.76.146 "ps aux | grep uvicorn"

# Sprawdź czy porty są otwarte
ssh debian@217.182.76.146 "netstat -tlnp | grep -E '8000|8001'"

# Uruchom ponownie usługi
ssh debian@217.182.76.146 "screen -ls"
```

### Problem: 404 Not Found na /summary/

**Przyczyna:** Nginx routing niepoprawny

**Rozwiązanie:**
```bash
# Sprawdź konfigurację
ssh debian@217.182.76.146 "sudo cat /etc/nginx/sites-enabled/baw-api | grep -A 5 'location /summary'"

# Test konfiguracji
ssh debian@217.182.76.146 "sudo nginx -t"

# Reload
ssh debian@217.182.76.146 "sudo systemctl reload nginx"
```

### Problem: Strona się ładuje ale nie pokazuje danych

**Przyczyna:** CORS lub backend API nie odpowiada

**Rozwiązanie:**
```bash
# Test bezpośrednio na backendzie
ssh debian@217.182.76.146 'curl http://localhost:8001/api/summary/test-123'

# Test przez frontend proxy
ssh debian@217.182.76.146 'curl http://localhost:8000/api/summary/test-123'

# Sprawdź console w przeglądarce (F12)
```

### Problem: Static files (CSS/JS) nie ładują się

**Przyczyna:** Brak konfiguracji `/static/` w Nginx

**Rozwiązanie:** Konfiguracja już dodana, sprawdź czy działa:
```bash
curl -I http://217.182.76.146/static/css/style.css
```

---

## ✅ Checklist konfiguracji

- [x] Nginx skonfigurowany
- [x] Backend API działa (port 8001)
- [x] SecureDocCompare działa (port 8000)
- [x] Routing `/summary/` działa
- [x] Routing `/api/summary/` działa
- [x] Static files `/static/` działają
- [x] Link w emailu zaktualizowany
- [x] Workflow `API 06` przygotowany
- [x] Testy przeszły pomyślnie

---

## 📝 Pliki konfiguracyjne

### Lokalne (rozwój)
- `C:\Projects\BAW\nginx-baw-api-updated.conf` - Gotowa konfiguracja
- `C:\Projects\BAW\API 06 - with edit link.json` - Workflow z linkiem

### Serwer produkcyjny
- `/etc/nginx/sites-available/baw-api` - Aktywna konfiguracja
- `/home/debian/hack/BAW/SecureDocCompare/` - Frontend
- `/home/debian/hack/BAW/UslugaDoPorownan/` - Backend

---

## 🎯 Następne kroki

1. ✅ **Konfiguracja działa** - użytkownicy mogą klikać link w mailu
2. **Monitoring** - dodać monitoring dostępności (opcjonalnie)
3. **SSL** - dodać certyfikat HTTPS (zalecane dla produkcji)
4. **Backup** - regularny backup konfiguracji Nginx

---

**Status:** ✅ **PRODUKCJA GOTOWA**

Link `http://217.182.76.146/summary/{process_id}` działa poprawnie i można go używać w workflow n8n.
