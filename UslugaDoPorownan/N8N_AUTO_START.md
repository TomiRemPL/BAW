# 🚀 Automatyczne Uruchamianie Usługi z n8n

## Metody Uruchamiania

### ✅ METODA 1: Execute Command w n8n (ZALECANA)

Dodaj node "Execute Command" na początku workflow, który automatycznie uruchomi usługę.

#### Konfiguracja Node'a w n8n

**Node:** Execute Command

```
Name: Start API Service
Command: cmd.exe
Arguments:
  /c
  c:\Projects\BAW\UslugaDoPorownan\start_service.bat
```

**ALBO (jeśli używasz PowerShell):**

```
Name: Start API Service
Command: powershell.exe
Arguments:
  -File
  c:\Projects\BAW\UslugaDoPorownan\start_service.ps1
```

---

### 📋 Kompletny Workflow z Auto-Start

```
┌──────────────────────┐
│ 1. Manual Trigger    │
│    (Start)           │
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│ 2. Execute Command   │ ← URUCHOM USŁUGĘ
│    start_service.bat │
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│ 3. Wait              │
│    5 seconds         │
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│ 4. HTTP Request      │
│    Health Check      │
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│ 5. IF                │
│    Service Running?  │
└──────┬───┬───────────┘
       │   │
    YES│   │NO
       │   └──► Error / Retry
       │
┌──────▼───────────────┐
│ 6. Upload Documents  │
│    ...               │
│    (reszta workflow) │
└──────────────────────┘
```

---

## 🔧 Konfiguracja Krok po Kroku

### Krok 1: Dodaj Node "Execute Command"

1. W n8n kliknij **"+"** na początku workflow (przed Upload Documents)
2. Wyszukaj **"Execute Command"**
3. Skonfiguruj:

```
Name: Start API Service

Command: cmd.exe

Arguments (jako lista):
  - /c
  - c:\Projects\BAW\UslugaDoPorownan\start_service.bat

Lub jako string:
/c c:\Projects\BAW\UslugaDoPorownan\start_service.bat
```

### Krok 2: Dodaj Node "Wait"

```
Name: Wait for Service
Resume: After Time Interval
Amount: 5
Unit: Seconds
```

### Krok 3: Dodaj Node "HTTP Request - Health Check"

```
Name: Check if Service Running
Method: GET
URL: http://localhost:8001/health

Continue On Fail: Yes
```

### Krok 4: Dodaj Node "IF - Validate Service"

```
Name: Is Service Running?

Conditions:
  Value 1: {{ $('Check if Service Running').item.json.status }}
  Operation: Equal
  Value 2: healthy

TRUE → Kontynuuj workflow
FALSE → Wyświetl błąd lub spróbuj ponownie
```

---

## 🛑 Zatrzymywanie Usługi

### Opcja A: Na końcu workflow

Dodaj na końcu workflow node zatrzymujący usługę:

**Node:** Execute Command

```
Name: Stop API Service
Command: cmd.exe
Arguments:
  /c
  c:\Projects\BAW\UslugaDoPorownan\stop_service.bat
```

### Opcja B: Osobny Workflow

Stwórz osobny workflow tylko do zatrzymywania:

```
Manual Trigger
    ↓
Execute Command (stop_service.bat)
    ↓
Wait 2 seconds
    ↓
HTTP Request (Health Check - powinien zwrócić błąd)
    ↓
Display "Service Stopped"
```

---

## 🔄 Sprawdzanie Statusu

### Node do sprawdzania czy usługa działa:

**Node:** Execute Command

```
Name: Check Service Status
Command: cmd.exe
Arguments:
  /c
  c:\Projects\BAW\UslugaDoPorownan\check_service.bat

Output: {{ $json.stdout }}
```

Zwraca:
- Status JSON jeśli działa
- Error jeśli nie działa

---

## 📜 Skrypty Pomocnicze

Utworzone zostały 3 skrypty BAT:

### 1. `start_service.bat`
Uruchamia usługę, sprawdza czy już nie działa, czeka na start i weryfikuje.

**Użycie ręczne:**
```bash
cd c:\Projects\BAW\UslugaDoPorownan
start_service.bat
```

### 2. `stop_service.bat`
Zatrzymuje usługę poprzez znalezienie procesu na porcie 8001.

**Użycie ręczne:**
```bash
cd c:\Projects\BAW\UslugaDoPorownan
stop_service.bat
```

### 3. `check_service.bat`
Sprawdza czy usługa działa (curl na /health).

**Użycie ręczne:**
```bash
cd c:\Projects\BAW\UslugaDoPorownan
check_service.bat
```

---

## 🐍 Wersja PowerShell (dla zaawansowanych)

Jeśli wolisz PowerShell, mogę utworzyć wersje .ps1 tych skryptów.

---

## ⚡ METODA 2: Webhook Auto-Start (zawsze działająca usługa)

Zamiast uruchamiać usługę z n8n, ustaw ją jako usługę systemową:

### Windows Service (NSSM)

1. **Pobierz NSSM** (Non-Sucking Service Manager):
   https://nssm.cc/download

2. **Zainstaluj usługę:**

```bash
nssm install DocumentComparisonService

# W oknie dialogowym:
Path: C:\Python311\python.exe
Startup directory: c:\Projects\BAW\UslugaDoPorownan
Arguments: -m uvicorn main:app --host 0.0.0.0 --port 8001
```

3. **Uruchom usługę:**

```bash
nssm start DocumentComparisonService
```

Teraz usługa będzie działać zawsze w tle, również po restarcie systemu!

---

## 🔐 METODA 3: Docker (jeśli używasz Dockera)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  document-comparison:
    build: .
    ports:
      - "8001:8001"
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
```

### Uruchomienie z n8n:

**Node:** Execute Command

```
Command: docker-compose
Arguments:
  -f
  c:\Projects\BAW\UslugaDoPorownan\docker-compose.yml
  up
  -d
```

---

## 🎯 Zalecana Konfiguracja

### Dla Produkcji:
**Używaj Windows Service (NSSM)** - usługa działa zawsze w tle

### Dla Rozwoju/Testów:
**Używaj Execute Command w n8n** - usługa startuje tylko gdy potrzebna

### Dla Zaawansowanych:
**Używaj Docker** - izolacja i łatwość deploymentu

---

## 📊 Przykładowy Workflow z Auto-Start

### Pełny workflow ze sprawdzaniem:

```javascript
// Node 1: Try to Start Service
Execute Command: start_service.bat

// Node 2: Wait
Wait: 5 seconds

// Node 3: Health Check
HTTP Request: GET /health

// Node 4: IF Check
IF {{ $json.status }} == "healthy":
  → Continue to document upload
ELSE:
  → Retry or Notify Error

// Node 5-N: Normal workflow
Upload → Process → Get Results
```

---

## 🐛 Troubleshooting

### Problem: "Execute Command" node nie działa

**Rozwiązanie:**
1. Sprawdź uprawnienia n8n do wykonywania komend
2. Użyj pełnych ścieżek (nie relatywnych)
3. Sprawdź logi n8n: `~/.n8n/logs/`

### Problem: Skrypt BAT nie uruchamia usługi

**Rozwiązanie:**
1. Uruchom skrypt ręcznie z cmd.exe i sprawdź błędy
2. Sprawdź czy Python jest w PATH
3. Upewnij się że port 8001 jest wolny

### Problem: Usługa uruchamia się ale n8n nie widzi

**Rozwiązanie:**
1. Zwiększ czas Wait (do 10 sekund)
2. Sprawdź firewall (Windows Defender)
3. Użyj `http://127.0.0.1:8001` zamiast `localhost`

---

## ✅ Checklist

- [ ] Skrypty BAT utworzone i przetestowane ręcznie
- [ ] Node "Execute Command" dodany do workflow
- [ ] Node "Wait" (5 sec) dodany po Execute Command
- [ ] Node "Health Check" dodany do weryfikacji
- [ ] Workflow przetestowany end-to-end
- [ ] (Opcjonalnie) Usługa Windows skonfigurowana dla produkcji

---

## 🎉 Gotowe!

Teraz Twój workflow automatycznie uruchomi usługę przed rozpoczęciem porównywania dokumentów!
