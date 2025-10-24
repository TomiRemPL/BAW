# 📜 BAW - Przewodnik po Skryptach

Kompletna dokumentacja wszystkich skryptów pomocniczych w projekcie BAW.

## 📋 Spis Treści

1. [Skrypty Zarządzania Usługami](#skrypty-zarządzania-usługami)
2. [Skrypty Diagnostyczne](#skrypty-diagnostyczne)
3. [Skrypty Konfiguracyjne](#skrypty-konfiguracyjne)
4. [Przykłady Użycia](#przykłady-użycia)
5. [Troubleshooting](#troubleshooting)

---

## 🎮 Skrypty Zarządzania Usługami

### `start_services.sh`

**Opis:** Uruchamia Backend (UslugaDoPorownan) i Frontend (SecureDocCompare) w osobnych sesjach screen.

**Lokalizacja:** `/home/debian/hack/BAW/start_services.sh`

**Funkcje:**
- ✅ Sprawdza wymagania wstępne (virtualenv, screen)
- ✅ Weryfikuje czy porty 8000 i 8001 są wolne
- ✅ Sprawdza czy screen sesje już nie istnieją
- ✅ Uruchamia obie usługi w tle
- ✅ Wykonuje health check po starcie
- ✅ Wyświetla pełne instrukcje zarządzania

**Użycie:**
```bash
cd /home/debian/hack/BAW
./start_services.sh
```

**Screen sesje:**
- Backend: `baw-backend` (port 8001)
- Frontend: `baw-frontend` (port 8000)

**Przykładowy output:**
```
╔════════════════════════════════════════════════════════════╗
║         BAW - Uruchamianie Usług (Screen Mode)           ║
╚════════════════════════════════════════════════════════════╝

📋 Sprawdzenia wstępne...
✅ Wszystkie wymagania spełnione

🔧 Backend (UslugaDoPorownan) - port 8001...
   Starting backend screen session...
✅ Backend uruchomiony w screen: baw-backend

🌐 Frontend (SecureDocCompare) - port 8000...
   Starting frontend screen session...
✅ Frontend uruchomiony w screen: baw-frontend

╔════════════════════════════════════════════════════════════╗
║                  ✅ USŁUGI URUCHOMIONE                     ║
╚════════════════════════════════════════════════════════════╝

📍 Dostępne endpointy:
   Backend API:  http://localhost:8001
   Frontend:     http://localhost:8000
```

**Błędy:**
- `❌ Port 8001 jest już zajęty` - Zatrzymaj proces na porcie lub użyj `./stop_services.sh`
- `❌ Screen 'baw-backend' już istnieje` - Użyj `./stop_services.sh` lub ręcznie: `screen -X -S baw-backend quit`
- `❌ Virtualenv nie istnieje` - Stwórz virtualenv: `python -m venv .venv`

---

### `stop_services.sh`

**Opis:** Zatrzymuje wszystkie uruchomione usługi BAW w screen.

**Lokalizacja:** `/home/debian/hack/BAW/stop_services.sh`

**Funkcje:**
- ✅ Zatrzymuje Frontend (SecureDocCompare)
- ✅ Zatrzymuje Backend (UslugaDoPorownan)
- ✅ Weryfikuje zamknięcie sesji
- ✅ Wyświetla podsumowanie

**Użycie:**
```bash
cd /home/debian/hack/BAW
./stop_services.sh
```

**Przykładowy output:**
```
╔════════════════════════════════════════════════════════════╗
║         BAW - Zatrzymywanie Usług (Screen Mode)          ║
╚════════════════════════════════════════════════════════════╝

🛑 Zatrzymuję screen: baw-frontend...
✅ Zatrzymano: baw-frontend

🛑 Zatrzymuję screen: baw-backend...
✅ Zatrzymano: baw-backend

╔════════════════════════════════════════════════════════════╗
║                  ✅ USŁUGI ZATRZYMANE                      ║
╚════════════════════════════════════════════════════════════╝
```

**Błędy:**
- `⚠️ Screen 'baw-backend' nie jest uruchomiony` - Usługa już zatrzymana (to nie jest błąd)
- `❌ Nie udało się zatrzymać` - Spróbuj ręcznie: `screen -X -S baw-backend quit` lub `killall screen`

---

### `status_services.sh`

**Opis:** Kompleksowa diagnostyka stanu wszystkich usług BAW.

**Lokalizacja:** `/home/debian/hack/BAW/status_services.sh`

**Funkcje:**
- ✅ Status screen sesji (aktywne/nieaktywne)
- ✅ Status portów (otwarty/zamknięty)
- ✅ Health check HTTP (zdrowy/niedostępny)
- ✅ Timestamp i status z API
- ✅ Lista wszystkich screen sesji
- ✅ Lista zajętych portów 8000/8001
- ✅ Sugerowane akcje do wykonania

**Użycie:**
```bash
cd /home/debian/hack/BAW
./status_services.sh
```

**Przykładowy output (usługi działają):**
```
╔════════════════════════════════════════════════════════════╗
║            BAW - Status Usług (Screen Mode)              ║
╚════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Backend (UslugaDoPorownan)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Screen Session:  ✅ Aktywny (baw-backend)
   Port 8001:       ✅ Otwarty
   Health Check:    ✅ Zdrowy (http://localhost:8001/health)
   Status:          healthy
   Timestamp:       2025-10-23T23:45:12.123456

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Frontend (SecureDocCompare)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Screen Session:  ✅ Aktywny (baw-frontend)
   Port 8000:       ✅ Otwarty
   Health Check:    ✅ Zdrowy (http://localhost:8000/health)
   Status:          healthy
   Timestamp:       2025-10-23T23:45:13.234567

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Dostępne Akcje
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ Wszystkie usługi działają
   Zatrzymaj:           ./stop_services.sh
   Podłącz do backendu: screen -r baw-backend
   Podłącz do frontendu:screen -r baw-frontend
   Odłącz (w screen):   Ctrl+A, D
```

**Przykładowy output (usługi zatrzymane):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Backend (UslugaDoPorownan)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Screen Session:  ❌ Nieaktywny
   Port 8001:       ❌ Zamknięty
   Health Check:    ❌ Niedostępny

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Dostępne Akcje
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ❌ Żadna usługa nie działa
   Uruchom:             ./start_services.sh
```

---

## 🔍 Skrypty Diagnostyczne

### `check_api.sh`

**Opis:** Kompleksowa diagnostyka API i dostępności serwisów.

**Lokalizacja:** `/home/debian/hack/BAW/check_api.sh`

**Funkcje:**
- ✅ Sprawdza czy API nasłuchuje na 0.0.0.0 (wszystkie interfejsy)
- ✅ Testuje lokalny dostęp (localhost)
- ✅ Testuje zewnętrzny dostęp (external IP)
- ✅ Sprawdza firewall (ufw, iptables)
- ✅ Sprawdza usługi systemd
- ✅ Sugeruje rozwiązania problemów

**Użycie:**
```bash
cd /home/debian/hack/BAW
./check_api.sh
```

**Kiedy używać:**
- API nie odpowiada z zewnątrz
- Połączenie odrzucane (connection refused)
- Timeout przy próbie połączenia
- Po zmianie konfiguracji firewall
- Po restarcie serwera

---

## ⚙️ Skrypty Konfiguracyjne

### `fix_firewall.sh`

**Opis:** Automatyczna naprawa konfiguracji firewall dla API.

**Lokalizacja:** `/home/debian/hack/BAW/fix_firewall.sh`

**Funkcje:**
- ✅ Otwiera port 8001 (Backend API)
- ✅ Otwiera port 8000 (Frontend)
- ✅ Działa z ufw i iptables
- ✅ Zapisuje reguły trwale
- ✅ Weryfikuje poprawność

**Użycie:**
```bash
cd /home/debian/hack/BAW
sudo ./fix_firewall.sh
```

**UWAGA:** Wymaga uprawnień root (sudo).

---

### `setup_nginx_proxy.sh`

**Opis:** Konfiguracja Nginx jako reverse proxy dla BAW.

**Lokalizacja:** `/home/debian/hack/BAW/setup_nginx_proxy.sh`

**Funkcje:**
- ✅ Instaluje Nginx (jeśli brak)
- ✅ Konfiguruje reverse proxy
- ✅ Ustawia przekierowanie HTTP → HTTPS
- ✅ Włącza kompresję gzip
- ✅ Konfiguruje cache dla statycznych plików

**Użycie:**
```bash
cd /home/debian/hack/BAW
sudo ./setup_nginx_proxy.sh
```

**UWAGA:** Wymaga uprawnień root (sudo).

---

## 💡 Przykłady Użycia

### Scenariusz 1: Pierwsze uruchomienie na serwerze

```bash
cd /home/debian/hack/BAW

# 1. Nadaj uprawnienia wykonywalne
chmod +x *.sh

# 2. Sprawdź status (powinno pokazać, że nic nie działa)
./status_services.sh

# 3. Uruchom usługi
./start_services.sh

# 4. Poczekaj 5 sekund i sprawdź status ponownie
sleep 5
./status_services.sh

# 5. Testuj API
curl http://localhost:8001/health
curl http://localhost:8000/health
```

### Scenariusz 2: Restart usług po aktualizacji kodu

```bash
cd /home/debian/hack/BAW

# 1. Zatrzymaj usługi
./stop_services.sh

# 2. Zaktualizuj kod (git pull, scp, itp.)
git pull origin master

# 3. Zaktualizuj zależności
source .venv/bin/activate
pip install -r requirements.txt

# 4. Uruchom ponownie
./start_services.sh

# 5. Sprawdź czy działa
./status_services.sh
```

### Scenariusz 3: Diagnoza problemów z dostępem

```bash
cd /home/debian/hack/BAW

# 1. Sprawdź status usług
./status_services.sh

# 2. Jeśli usługi działają, ale API nie odpowiada z zewnątrz
./check_api.sh

# 3. Jeśli check_api.sh wskazuje problem z firewall
sudo ./fix_firewall.sh

# 4. Sprawdź ponownie
./check_api.sh
```

### Scenariusz 4: Przeglądanie logów na żywo

```bash
# Opcja 1: Podłącz się do screen sesji backendu
screen -r baw-backend
# Zobacz logi w czasie rzeczywistym
# Odłącz się: Ctrl+A, potem D

# Opcja 2: Podłącz się do screen sesji frontendu
screen -r baw-frontend
# Zobacz logi w czasie rzeczywistym
# Odłącz się: Ctrl+A, potem D

# Opcja 3: Przewijanie historii logów w screen
screen -r baw-backend
# Naciśnij: Ctrl+A, potem [
# Używaj strzałek lub PgUp/PgDn do przewijania
# Naciśnij ESC aby wyjść z trybu przewijania
```

### Scenariusz 5: Wdrożenie produkcyjne z Nginx

```bash
cd /home/debian/hack/BAW

# 1. Uruchom usługi
./start_services.sh

# 2. Zainstaluj i skonfiguruj Nginx
sudo ./setup_nginx_proxy.sh

# 3. Otwórz porty w firewall
sudo ./fix_firewall.sh

# 4. Sprawdź wszystko
./status_services.sh

# 5. Testuj przez Nginx (port 80)
curl http://217.182.76.146/
curl http://217.182.76.146/api/health
```

---

## 🔧 Troubleshooting

### Problem: `./start_services.sh: Permission denied`

**Rozwiązanie:**
```bash
chmod +x start_services.sh stop_services.sh status_services.sh
```

### Problem: `screen: command not found`

**Rozwiązanie:**
```bash
sudo apt update
sudo apt install screen
```

### Problem: Port już zajęty (`Port 8001 jest już zajęty`)

**Rozwiązanie 1:** Zatrzymaj istniejące screen sesje
```bash
./stop_services.sh
```

**Rozwiązanie 2:** Znajdź i zabij proces na porcie
```bash
# Znajdź PID procesu
sudo ss -tlnp | grep :8001

# Zabij proces (zastąp PID)
kill -9 PID
```

**Rozwiązanie 3:** Sprawdź systemd (jeśli używasz)
```bash
sudo systemctl stop baw-backend
sudo systemctl stop baw-frontend
```

### Problem: Screen sesja istnieje, ale usługa nie działa

**Rozwiązanie:**
```bash
# 1. Podłącz się do sesji i zobacz błąd
screen -r baw-backend

# 2. Jeśli sesja jest pusta lub zawieszona, zabij ją
screen -X -S baw-backend quit

# 3. Uruchom ponownie
./start_services.sh
```

### Problem: Health check zwraca timeout

**Przyczyny:**
1. Usługa jeszcze się uruchamia (poczekaj 5-10 sekund)
2. Usługa się wykrzaczyła (sprawdź logi w screen)
3. Firewall blokuje (użyj `./check_api.sh`)

**Rozwiązanie:**
```bash
# Sprawdź szczegółowy status
./status_services.sh

# Podłącz się do screen i zobacz logi
screen -r baw-backend

# Jeśli błąd w kodzie, napraw i uruchom ponownie
./stop_services.sh
# ... naprawa kodu ...
./start_services.sh
```

### Problem: Nie mogę odłączyć się od screen

**Rozwiązanie:**
Naciśnij sekwencję: `Ctrl+A`, potem `D` (dwie osobne akcje)

1. Trzymaj `Ctrl` i naciśnij `A`
2. Puść oba klawisze
3. Naciśnij `D`

### Problem: Screen sesja "Attached" i nie mogę się podłączyć ponownie

**Rozwiązanie:**
```bash
# Wymuś odłączenie poprzedniej sesji i podłącz się
screen -d -r baw-backend
```

---

## 📚 Dodatkowe Zasoby

- **DEPLOYMENT.md** - Pełna instrukcja wdrożenia
- **README.md** - Ogólny opis projektu
- **API_DOCUMENTATION.md** - Dokumentacja API
- **PROGRESS_LOG.md** - Historia zmian

---

## 🎯 Szybki Przegląd Komend

```bash
# ZARZĄDZANIE USŁUGAMI
./start_services.sh              # Uruchom wszystko
./stop_services.sh               # Zatrzymaj wszystko
./status_services.sh             # Sprawdź status

# SCREEN
screen -list                     # Lista sesji
screen -r baw-backend            # Podłącz do backendu
screen -r baw-frontend           # Podłącz do frontendu
Ctrl+A, D                        # Odłącz się (w screen)

# DIAGNOSTYKA
./check_api.sh                   # Sprawdź API
sudo ./fix_firewall.sh           # Napraw firewall
curl http://localhost:8001/health # Test backendu
curl http://localhost:8000/health # Test frontendu

# LOGI
sudo journalctl -u baw-backend -f           # Logi systemd (live)
sudo journalctl -u baw-backend -n 100       # Ostatnie 100 linii
screen -r baw-backend                       # Logi w screen (live)
```

---

**Wersja:** 1.0.0
**Ostatnia aktualizacja:** 2025-10-24
**Testowane na:** Debian 11/12, Ubuntu 20.04/22.04
