# Skrypty Zarządzania Serwisami - Windows

Dokumentacja skryptów do zarządzania serwisami BAW w środowisku Windows (testowym).

## 📋 Dostępne Skrypty

### PowerShell (.ps1)

| Skrypt | Opis |
|--------|------|
| `start_services.ps1` | Uruchamia oba serwisy w osobnych oknach |
| `stop_services.ps1` | Zatrzymuje wszystkie uruchomione serwisy |
| `check_services.ps1` | Sprawdza status i health endpoints |

### Batch (.bat)

| Skrypt | Opis |
|--------|------|
| `start_services.bat` | Uruchamia oba serwisy (alternatywa CMD) |
| `stop_services.bat` | Zatrzymuje serwisy (alternatywa CMD) |
| `check_services.bat` | Sprawdza status (alternatywa CMD) |

---

## 🚀 Uruchamianie Serwisów

### PowerShell (Rekomendowane)

```powershell
# Uruchom z katalogu BAW
.\start_services.ps1
```

**Co robi skrypt:**
1. Sprawdza środowisko wirtualne Python
2. Weryfikuje czy porty 8000 i 8001 są wolne
3. Uruchamia **Backend** (UslugaDoPorownan) na porcie **8001** w nowym oknie
4. Uruchamia **Frontend** (SecureDocCompare) na porcie **8000** w nowym oknie
5. Sprawdza health endpoints
6. Opcjonalnie otwiera przeglądarkę

**Wynik:**
- 2 nowe okna PowerShell z działającymi serwisami
- Logi widoczne w czasie rzeczywistym
- Auto-reload włączony (zmiana kodu → restart)

---

### Batch (Alternatywa CMD)

```cmd
start_services.bat
```

Funkcjonalność identyczna jak PowerShell, ale dla terminala CMD.

---

## 🛑 Zatrzymywanie Serwisów

### Metoda 1: Skrypt PowerShell

```powershell
.\stop_services.ps1
```

**Co robi:**
1. Znajduje procesy na portach 8000 i 8001
2. Wyświetla informacje o procesach (PID, nazwa)
3. Prosi o potwierdzenie
4. Zatrzymuje procesy (taskkill)
5. Weryfikuje czy porty są wolne

---

### Metoda 2: Skrypt Batch

```cmd
stop_services.bat
```

Uproszczona wersja dla CMD.

---

### Metoda 3: Ręcznie

Zamknij okna terminali z uruchomionymi serwisami (Ctrl+C lub kliknij X).

---

## 🔍 Sprawdzanie Statusu

### PowerShell

```powershell
.\check_services.ps1
```

**Wyświetla:**
- Status portów (URUCHOMIONY/ZATRZYMANY)
- PID procesów
- Czas uruchomienia
- Health check endpoints
- Statystyki (dokumenty, procesy, podsumowania)
- Podsumowanie stanu systemu

**Przykładowy output:**
```
========================================
  Status serwisów BAW
========================================

[1/3] Sprawdzanie portów...

Backend (Port 8001): URUCHOMIONY
  PID: 12345
  Proces: python
  Czas uruchomienia: 2025-10-27 10:00:00

Frontend (Port 8000): URUCHOMIONY
  PID: 12346
  Proces: python
  Czas uruchomienia: 2025-10-27 10:00:05

[2/3] Sprawdzanie health endpoints...

Backend Health: OK
  Status: healthy
  Statystyki:
    - Dokumenty: 5
    - Procesy: 10
    - Podsumowania: 3
    - Oczekujące: 1
    - Zatwierdzone: 2

Frontend Health: OK
  Status: healthy
  Backend API: http://localhost:8001

[3/3] Test połączenia...

Backend API (/): 200 OK
Frontend (/): 200 OK

========================================
  Status: WSZYSTKO DZIAŁA
========================================
```

---

### Batch

```cmd
check_services.bat
```

Uproszczona wersja bez szczegółowych statystyk.

---

## 📝 Wymagania

### Przed pierwszym uruchomieniem:

1. **Środowisko wirtualne:**
   ```powershell
   python -m venv .venv
   ```

2. **Instalacja zależności:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. **Konfiguracja (opcjonalna):**
   ```powershell
   # SecureDocCompare/.env
   APP_PASSWORD=TwojeHaslo
   DOCUMENT_API_URL=http://localhost:8001
   APP_PORT=8000
   PRODUCTION=false
   ```

---

## 🔧 Rozwiązywanie Problemów

### Problem: "Wykonywanie skryptów jest wyłączone w tym systemie"

**Rozwiązanie:**
```powershell
# Uruchom PowerShell jako Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Lub uruchom jednokrotowo:**
```powershell
powershell -ExecutionPolicy Bypass -File .\start_services.ps1
```

---

### Problem: Port 8000 lub 8001 jest zajęty

**Rozwiązanie 1: Zatrzymaj zajmujący proces**
```powershell
# Znajdź proces
netstat -ano | findstr ":8001"

# Zatrzymaj (zamień 12345 na właściwy PID)
taskkill /F /PID 12345
```

**Rozwiązanie 2: Użyj stop_services.ps1**
```powershell
.\stop_services.ps1
```

---

### Problem: "Nie znaleziono środowiska wirtualnego"

**Rozwiązanie:**
```powershell
# Utwórz środowisko wirtualne
python -m venv .venv

# Aktywuj
.\.venv\Scripts\Activate.ps1

# Zainstaluj zależności
pip install -r requirements.txt
```

---

### Problem: Serwisy uruchamiają się, ale health check zwraca błąd

**Rozwiązanie:**

1. Sprawdź logi w oknach terminali
2. Poczekaj 5-10 sekund na pełny start
3. Sprawdź ręcznie:
   ```powershell
   curl http://localhost:8001/health
   curl http://localhost:8000/health
   ```

---

### Problem: Okna terminali zamykają się natychmiast

**Możliwe przyczyny:**
- Błąd w kodzie Python
- Brak zainstalowanych zależności
- Błąd składni w main.py

**Rozwiązanie:**

Uruchom ręcznie, aby zobaczyć błąd:
```powershell
.\.venv\Scripts\Activate.ps1
cd UslugaDoPorownan
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

---

## 🎯 Szybki Start (TL;DR)

```powershell
# 1. Uruchom serwisy
.\start_services.ps1

# 2. Sprawdź status
.\check_services.ps1

# 3. Otwórz przeglądarkę
start http://localhost:8000

# 4. Zatrzymaj serwisy (po zakończeniu)
.\stop_services.ps1
```

---

## 📊 Porównanie: PowerShell vs Batch

| Funkcja | PowerShell | Batch |
|---------|-----------|-------|
| Kolorowy output | ✅ Tak | ❌ Nie |
| Health check | ✅ Szczegółowy | ⚠️ Podstawowy |
| Statystyki | ✅ Pełne | ❌ Brak |
| Weryfikacja portów | ✅ Szczegółowa | ⚠️ Podstawowa |
| Obsługa błędów | ✅ Rozbudowana | ⚠️ Podstawowa |
| Szybkość | ⚡ Szybki | ⚡ Szybki |

**Rekomendacja:** Użyj PowerShell dla lepszego doświadczenia.

---

## 🔐 Bezpieczeństwo

### Środowisko testowe (development):

- ✅ HTTP jest OK (localhost)
- ✅ Auto-reload włączony
- ✅ Debug mode
- ✅ Porty 8000/8001 lokalnie

### Produkcja (nie używaj tych skryptów):

- ❌ Nie używaj `--reload`
- ❌ Nie używaj `localhost` tylko dla produkcji
- ✅ Użyj systemd (Linux) lub Windows Service
- ✅ Skonfiguruj HTTPS
- ✅ Użyj reverse proxy (nginx)

Zobacz: `DEPLOYMENT.md` dla instrukcji produkcyjnych.

---

## 📚 Dodatkowe Zasoby

- **Główna dokumentacja:** `README.md`
- **Wdrożenie produkcyjne:** `DEPLOYMENT.md`
- **Integracja n8n:** `N8N_SUMMARY_INTEGRATION.md`
- **Backend API:** `UslugaDoPorownan/README.md`
- **Frontend:** `SecureDocCompare/README.md`

---

## 🛠️ Modyfikacja Skryptów

### Zmiana portów

Edytuj skrypty i zmień:
- `8001` → nowy port backendu
- `8000` → nowy port frontendu

**Nie zapomnij** zaktualizować także:
- `SecureDocCompare/.env` → `DOCUMENT_API_URL`
- `UslugaDoPorownan/main.py` → `port=` w `uvicorn.run()`

---

### Dodanie auto-restart przy błędzie

Edytuj `start_services.ps1`:

```powershell
# Zamiast:
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Użyj pętli:
while ($true) {
    uvicorn main:app --host 0.0.0.0 --port 8001 --reload
    Write-Host "Restart za 5 sekund..."
    Start-Sleep -Seconds 5
}
```

---

## 📞 Wsparcie

**Pytania?** Sprawdź:
1. Ten plik (`WINDOWS_SCRIPTS.md`)
2. Logi w oknach terminali
3. `README.md` - główna dokumentacja
4. `DEPLOYMENT.md` - wdrożenie

**Znalazłeś błąd?** Zgłoś w repozytorium projektu.

---

**Wersja:** 1.0.0
**Data:** 2025-10-27
**System:** Windows 10/11
**Python:** 3.11.9
**Status:** ✅ Przetestowane
