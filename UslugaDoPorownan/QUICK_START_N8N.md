# ⚡ Szybki Start - Uruchamianie Usługi z n8n

## ✅ TAK! Możesz uruchomić usługę z n8n

Utworzyłem gotowe skrypty do zarządzania usługą.

---

## 🎯 Metoda 1: Execute Command w n8n

### Dodaj ten Node na początku workflow:

**Node Type:** Execute Command

```
Name: Start API Service

Command: powershell.exe
Arguments:
  -ExecutionPolicy
  Bypass
  -File
  c:\Projects\BAW\UslugaDoPorownan\start_service.ps1
```

**LUB (jeśli wolisz cmd.exe):**

```
Name: Start API Service

Command: cmd.exe
Arguments:
  /c
  c:\Projects\BAW\UslugaDoPorownan\start_service.bat
```

---

## 📋 Kompletny Workflow z Auto-Start

```
1. Manual Trigger
    ↓
2. Execute Command (start_service.ps1)  ← URUCHOM USŁUGĘ
    ↓
3. Wait (5 sekund)
    ↓
4. HTTP Request (/health) - sprawdź czy działa
    ↓
5. Upload Documents
    ↓
6. Start Processing
    ↓
7. Check Status (loop)
    ↓
8. Get Results
```

---

## 📁 Dostępne Skrypty

### ✅ Utworzone właśnie:

#### 1. **start_service.ps1** / **start_service.bat**
- Uruchamia usługę
- Sprawdza czy już nie działa
- Czeka 5 sekund
- Weryfikuje uruchomienie

#### 2. **stop_service.ps1** / **stop_service.bat**
- Zatrzymuje usługę
- Znajduje proces na porcie 8001
- Zabija proces

#### 3. **check_service.ps1** / **check_service.bat**
- Sprawdza status usługi
- Zwraca JSON ze statusem

---

## 🧪 Test Ręczny

### PowerShell (zalecane):

```powershell
# Uruchom usługę
cd c:\Projects\BAW\UslugaDoPorownan
powershell -ExecutionPolicy Bypass -File start_service.ps1

# Sprawdź status
curl http://localhost:8001/health

# Zatrzymaj usługę
powershell -ExecutionPolicy Bypass -File stop_service.ps1
```

### CMD:

```bash
# Uruchom usługę
cd c:\Projects\BAW\UslugaDoPorownan
start_service.bat

# Sprawdź status
curl http://localhost:8001/health

# Zatrzymaj usługę
stop_service.bat
```

---

## 🔧 Konfiguracja w n8n - Szczegóły

### Execute Command Node - Pełna Konfiguracja:

```
┌─────────────────────────────────────┐
│ Execute Command                     │
├─────────────────────────────────────┤
│ Name: Start API Service             │
│ Command: powershell.exe             │
│ Arguments:                          │
│   [-ExecutionPolicy]                │
│   [Bypass]                          │
│   [-File]                           │
│   [c:\Projects\BAW\...\start_...ps1]│
│                                     │
│ Continue On Fail: No                │
└─────────────────────────────────────┘
```

### Wait Node:

```
┌─────────────────────────────────────┐
│ Wait                                │
├─────────────────────────────────────┤
│ Resume: After Time Interval         │
│ Amount: 5                           │
│ Unit: Seconds                       │
└─────────────────────────────────────┘
```

### Health Check Node:

```
┌─────────────────────────────────────┐
│ HTTP Request                        │
├─────────────────────────────────────┤
│ Name: Verify Service Started        │
│ Method: GET                         │
│ URL: http://localhost:8001/health   │
│ Continue On Fail: Yes               │
└─────────────────────────────────────┘
```

### IF Validation Node:

```
┌─────────────────────────────────────┐
│ IF                                  │
├─────────────────────────────────────┤
│ Name: Is Service Running?           │
│                                     │
│ Condition:                          │
│   Value 1: {{ $json.status }}       │
│   Operation: Equal                  │
│   Value 2: healthy                  │
│                                     │
│ TRUE → Continue workflow            │
│ FALSE → Show error / Retry          │
└─────────────────────────────────────┘
```

---

## 🚀 Metoda 2: Windows Service (Produkcja)

Dla środowiska produkcyjnego, zainstaluj jako usługę Windows:

### Użyj NSSM (Non-Sucking Service Manager):

```bash
# Pobierz NSSM z: https://nssm.cc/download

# Zainstaluj usługę
nssm install DocumentComparisonAPI

# W oknie dialogowym:
Path: C:\Python311\python.exe
Startup: c:\Projects\BAW\UslugaDoPorownan
Arguments: -m uvicorn main:app --host 0.0.0.0 --port 8001

# Uruchom
nssm start DocumentComparisonAPI
```

Usługa będzie działać zawsze, również po restarcie systemu!

---

## 💡 Najlepsze Praktyki

### Dla Rozwoju/Testów:
✅ **Użyj Execute Command w n8n**
- Uruchamia usługę tylko gdy potrzebna
- Łatwe debugowanie
- Nie zajmuje zasobów gdy nie używana

### Dla Produkcji:
✅ **Zainstaluj jako Windows Service**
- Zawsze dostępna
- Auto-restart po błędach
- Uruchamia się po restarcie systemu
- Nie trzeba czekać na start

---

## 🐛 Troubleshooting

### Problem: Execute Command nie działa w n8n

**Rozwiązanie:**
1. Sprawdź uprawnienia n8n do wykonywania komend
2. Użyj **pełnych ścieżek** (nie relatywnych)
3. Sprawdź czy Python jest w PATH
4. Spróbuj uruchomić skrypt ręcznie najpierw

### Problem: Skrypt uruchomił się ale usługa nie odpowiada

**Rozwiązanie:**
1. Zwiększ czas Wait do 10 sekund
2. Sprawdź logi: `c:\Projects\BAW\UslugaDoPorownan\*.log`
3. Sprawdź czy port 8001 nie jest zajęty: `netstat -ano | findstr 8001`
4. Wyłącz firewall tymczasowo do testów

### Problem: PowerShell - execution policy

**Rozwiązanie:**
```powershell
# Ustaw policy na Bypass dla pojedynczego uruchomienia
powershell -ExecutionPolicy Bypass -File start_service.ps1

# LUB ustaw globalnie
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## ✅ Checklist

- [x] Skrypty `.ps1` i `.bat` utworzone
- [ ] Skrypty przetestowane ręcznie (start → check → stop)
- [ ] Node "Execute Command" dodany do n8n
- [ ] Node "Wait 5 sec" dodany po Execute Command
- [ ] Node "HTTP Request /health" dodany
- [ ] Node "IF" do weryfikacji dodany
- [ ] Cały workflow przetestowany
- [ ] (Opcjonalnie) Windows Service zainstalowana dla produkcji

---

## 📚 Więcej Informacji

- **Pełny przewodnik:** `N8N_AUTO_START.md`
- **Przewodnik n8n:** `N8N_GUIDE.md`
- **Import do n8n:** `IMPORT_DO_N8N.md`
- **API dokumentacja:** `README.md`

---

## 🎉 Gotowe!

Teraz możesz uruchamiać usługę bezpośrednio z workflow n8n!

**Szybki test:**
```bash
cd c:\Projects\BAW\UslugaDoPorownan
powershell -ExecutionPolicy Bypass -File start_service.ps1
```

Powinno wyświetlić:
```
[OK] Usluga uruchomiona pomyslnie na http://localhost:8001
```
