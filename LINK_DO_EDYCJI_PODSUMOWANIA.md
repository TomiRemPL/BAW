# Jak Dodano Link do Edycji Podsumowania w Mailu

## Przegląd

Do workflow n8n **API 06 - with edit link.json** został dodany działający link do edycji podsumowania w emailu wysyłanym do użytkownika.

---

## 🎯 Rozwiązanie

### 1. Istniejący Frontend (SecureDocCompare)

Aplikacja **SecureDocCompare** (`C:\Projects\BAW\SecureDocCompare`) zawiera już gotowy frontend do edycji podsumowań:

- **Route:** `GET /summary/{process_id}`
- **Template:** `templates/summary_editor.html`
- **API Proxy:** Endpointy przekierowujące żądania do backend API (217.182.76.146:8001)

#### Dostępne endpointy w SecureDocCompare:

```python
# Strona edytora (HTML)
GET /summary/{process_id}

# API proxy (nie wymaga autentykacji - dla n8n)
GET /api/summary/{process_id}              # Pobierz podsumowanie
GET /api/summary/{process_id}/status       # Status zatwierdzenia
PUT /api/summary/{process_id}              # Aktualizuj treść
POST /api/summary/{process_id}/approve     # Zatwierdź/odrzuć
```

#### Port i adres:

- **Development:** `http://localhost:8000`
- **Production:** `http://217.182.76.146` (SecureDocCompare)

---

## 📧 Zaktualizowany Email

### Node: Send Review Email

Email został zaktualizowany i zawiera:

1. **Wizualne podsumowanie** wygenerowane przez AI
2. **Instrukcje dla użytkownika** (4 kroki)
3. **Duży, widoczny przycisk** z linkiem do edytora
4. **Process ID** dla debugowania

### Link w emailu:

```
http://217.182.76.146/summary/{{ process_id }}
```

Gdzie `{{ process_id }}` jest automatycznie podstawiany przez n8n z node "Start Processing".

### Przykładowy wygląd maila:

```html
┌──────────────────────────────────────────────┐
│  📝 Podsumowanie dokumentu - weryfikacja     │
│  [gradient header]                           │
├──────────────────────────────────────────────┤
│                                              │
│  Witaj!                                      │
│                                              │
│  System AI wygenerował podsumowanie zmian... │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ 📄 Wygenerowane podsumowanie:          │ │
│  │ [tekst z AI Agent4]                    │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ 💡 Co dalej?                           │ │
│  │ 1. Kliknij link                        │ │
│  │ 2. Przejrzyj treść                     │ │
│  │ 3. Zatwierdź lub odrzuć                │ │
│  └────────────────────────────────────────┘ │
│                                              │
│      ┌──────────────────────────────┐       │
│      │ 🔗 Otwórz edytor podsumowania │       │
│      │   [zielony przycisk]          │       │
│      └──────────────────────────────┘       │
│                                              │
│  Process ID: abc-123-def                     │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 🖥️ Strona Edytora

### Funkcjonalności:

1. **Automatyczne załadowanie danych**
   - Pobiera podsumowanie z API na podstawie `process_id` z URL
   - Wyświetla metadata (przedmiot, daty, etc.)
   - Pokazuje aktualny status (pending_review/approved/rejected)

2. **Edycja podsumowania**
   - Textarea z możliwością modyfikacji tekstu
   - Licznik znaków
   - Porównanie z oryginalnym podsumowaniem

3. **Trzy akcje:**
   - **💾 Zapisz zmiany** - Aktualizuje podsumowanie (PUT /api/summary/{id})
   - **✅ Zatwierdź** - Zatwierdza podsumowanie (POST /api/summary/{id}/approve)
   - **❌ Odrzuć** - Odrzuca podsumowanie (POST /api/summary/{id}/approve)

4. **Responsywny design**
   - Gradient background
   - Czytelny layout
   - Mobile-friendly

### Komunikacja z backend:

```javascript
// Przykład zatwierdzenia
POST http://217.182.76.146/api/summary/{process_id}/approve
Content-Type: application/json

{
  "approved": true
}

// SecureDocCompare proxy do:
POST http://localhost:8001/api/summary/{process_id}/approve
```

---

## 🔄 Przebieg procesu z linkiem

```
1. AI Agent4 generuje podsumowanie
   ↓
2. POST Summary to API (zapisuje w backend)
   ↓
3. Send Review Email
   📧 Email z linkiem: http://217.182.76.146/summary/{process_id}
   ↓
4. Użytkownik klika link
   🌐 Otwiera się strona edytora w przeglądarce
   ↓
5. Użytkownik edytuje i zatwierdza
   ✅ Kliknięcie "Zatwierdź" → POST /approve
   ↓
6. Poll Summary Status wykrywa zmianę
   🔄 status: "pending_review" → "approved"
   ↓
7. Get Approved Summary
   📥 Pobiera zatwierdzone podsumowanie
   ↓
8. Update Email Content
   ✏️ Formatuje ostateczną wersję maila
   ↓
9. Send email (finalny)
   📧 Mail z zatwierdzonym podsumowaniem
```

---

## 📂 Pliki

### Workflow:
- **Źródłowy:** `API 05 - with summary.json`
- **Zaktualizowany:** `API 06 - with edit link.json`
- **Zmiana:** Node "Send Review Email" - dodano link i styling

### Frontend:
- **Aplikacja:** `C:\Projects\BAW\SecureDocCompare\main.py`
- **Template:** `C:\Projects\BAW\SecureDocCompare\templates\summary_editor.html`
- **Konfiguracja:** `C:\Projects\BAW\SecureDocCompare\config.py`

### Skrypty:
- **Generowanie workflow:** `extend_workflow.py`
- **Dodanie linku:** `update_workflow_with_link.py`

---

## 🚀 Deployment

### Wymagania:

1. **Backend API** (port 8001)
   ```bash
   cd C:\Projects\BAW\UslugaDoPorownan
   uvicorn main:app --host 0.0.0.0 --port 8001
   ```

2. **SecureDocCompare** (port 8000)
   ```bash
   cd C:\Projects\BAW\SecureDocCompare
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. **Nginx** (reverse proxy)
   - Port 80 → Backend (8001)
   - `/summary/*` → SecureDocCompare (8000)

### Przykładowa konfiguracja Nginx:

```nginx
server {
    listen 80;
    server_name 217.182.76.146;

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8001/api/;
        proxy_set_header Host $host;
    }

    location /reports/ {
        proxy_pass http://localhost:8001/reports/;
        proxy_set_header Host $host;
    }

    # Frontend edycji podsumowania
    location /summary/ {
        proxy_pass http://localhost:8000/summary/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # API proxy dla summary (z SecureDocCompare)
    location /api/summary/ {
        proxy_pass http://localhost:8000/api/summary/;
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://localhost:8001/;
        proxy_set_header Host $host;
    }
}
```

---

## ✅ Weryfikacja

### Test 1: Czy link działa?

1. Uruchom oba serwisy
2. Stwórz podsumowanie przez API:
   ```bash
   curl -X POST http://217.182.76.146/api/summary \
     -H "Content-Type: application/json" \
     -d '{
       "process_id": "test-123",
       "summary_text": "Test podsumowania",
       "metadata": {}
     }'
   ```

3. Otwórz w przeglądarce:
   ```
   http://217.182.76.146/summary/test-123
   ```

4. Powinieneś zobaczyć stronę edytora z "Test podsumowania"

### Test 2: Czy zatwierdzanie działa?

1. Na stronie edytora kliknij "Zatwierdź"
2. Sprawdź status:
   ```bash
   curl http://217.182.76.146/api/summary/test-123/status
   ```

3. Powinno zwrócić: `{"status": "approved", ...}`

---

## 🔧 Troubleshooting

### Problem: Link nie otwiera się

**Rozwiązanie:**
- Sprawdź czy SecureDocCompare działa: `curl http://217.182.76.146/health`
- Sprawdź logi Nginx: `sudo tail -f /var/log/nginx/error.log`
- Sprawdź czy port 8000 jest dostępny: `netstat -tlnp | grep 8000`

### Problem: Strona ładuje się, ale nie pokazuje danych

**Rozwiązanie:**
- Sprawdź konsole JS w przeglądarce (F12)
- Sprawdź czy backend API odpowiada: `curl http://217.182.76.146/api/summary/test-123`
- Sprawdź CORS w backend API

### Problem: Po zatwierdzeniu status nie zmienia się

**Rozwiązanie:**
- Sprawdź czy endpoint `/approve` działa:
  ```bash
  curl -X POST http://217.182.76.146/api/summary/test-123/approve \
    -H "Content-Type: application/json" \
    -d '{"approved": true}'
  ```
- Sprawdź logi backend API

---

## 📊 Podsumowanie zmian

| Element | Przed | Po |
|---------|-------|-----|
| **Email** | Tylko tekst podsumowania | Tekst + link do edycji |
| **Link** | Brak | `http://217.182.76.146/summary/{id}` |
| **Frontend** | Brak | SecureDocCompare `/summary/{id}` |
| **Edycja** | Niemożliwa | Textarea + przyciski |
| **Workflow** | API 05 | **API 06 - with edit link** |

---

## 📝 Następne kroki (opcjonalne)

1. **Dodać timeout** do pollingu (np. 30 minut)
2. **Powiadomienia** - SMS/Slack gdy jest do zatwierdzenia
3. **Historia zmian** - kto i kiedy edytował
4. **Wersjonowanie** - zapisywać każdą wersję podsumowania
5. **Podgląd różnic** - pokazać co użytkownik zmienił vs AI

---

**Autorzy:**
- Frontend: SecureDocCompare (istniejący)
- Integracja n8n: Claude Code
- Dokumentacja: 2025-10-29

**Status:** ✅ Gotowe do użycia
