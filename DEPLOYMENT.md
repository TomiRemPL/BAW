# 🚀 Deployment na Debian - Instrukcja Wdrożenia

Szczegółowa instrukcja wdrożenia projektu BAW na serwer Debian z Python 3.11.9.

## 📋 Spis Treści

1. [Wymagania](#wymagania)
2. [Instalacja Python 3.11.9 przez pyenv](#instalacja-python-3119-przez-pyenv)
3. [Konfiguracja Projektu](#konfiguracja-projektu)
4. [Uruchomienie Aplikacji](#uruchomienie-aplikacji)
5. [Automatyzacja z systemd](#automatyzacja-z-systemd)
6. [Nginx Reverse Proxy](#nginx-reverse-proxy)
7. [HTTPS z Let's Encrypt](#https-z-lets-encrypt)
8. [Monitoring i Logi](#monitoring-i-logi)
9. [Backup i Aktualizacje](#backup-i-aktualizacje)

---

## 🔧 Wymagania

### Serwer
- **OS:** Debian 11+ (Bullseye lub nowszy)
- **RAM:** Minimum 1GB (zalecane 2GB)
- **Dysk:** 5GB wolnego miejsca
- **Dostęp:** SSH z uprawnieniami sudo
- **Sieć:** Otwarte porty 8000, 8001 (lub 80, 443 dla nginx)

### Lokalne (opcjonalnie)
- Klient SSH (PuTTY, OpenSSH)
- Klient SFTP (WinSCP, FileZilla) do kopiowania plików

---

## 📥 Instalacja Python 3.11.9 przez pyenv

### Krok 1: Zainstaluj zależności systemowe

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
git
```

### Krok 2: Zainstaluj pyenv

```bash
# Pobierz i zainstaluj pyenv
curl https://pyenv.run | bash

# Dodaj do ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Przeładuj konfigurację
exec $SHELL
```

### Krok 3: Zainstaluj Python 3.11.9

```bash
# Instalacja (trwa 5-10 minut)
pyenv install 3.11.9

# Ustaw jako globalną wersję
pyenv global 3.11.9

# Sprawdź
python --version  # Powinno pokazać: Python 3.11.9
which python      # Powinno pokazać: /home/debian/.pyenv/shims/python
```

---

## 📦 Konfiguracja Projektu

### Krok 1: Przygotuj katalog

```bash
# Stwórz strukturę katalogów
mkdir -p /home/debian/hack/BAW
cd /home/debian/hack/BAW
```

### Krok 2: Skopiuj pliki projektu

**Opcja A: Git (jeśli używasz)**
```bash
git clone https://github.com/twoje-repo/BAW.git
cd BAW
```

**Opcja B: SFTP/SCP**
```bash
# Z lokalnego komputera (Windows/Linux)
scp -r c:/Projects/BAW/* debian@IP_SERWERA:/home/debian/hack/BAW/

# Lub użyj WinSCP / FileZilla
```

### Krok 3: Stwórz środowisko wirtualne

```bash
cd /home/debian/hack/BAW

# Usuń stare środowiska jeśli istnieją
rm -rf .venv
rm -rf UslugaDoPorownan/.venv
rm -rf SecureDocCompare/.venv

# Stwórz nowe wspólne środowisko
python -m venv .venv

# Aktywuj
source .venv/bin/activate

# Sprawdź
which python  # Powinno pokazać: /home/debian/hack/BAW/.venv/bin/python
python --version  # Python 3.11.9
```

### Krok 4: Zainstaluj zależności

```bash
# Aktywuj środowisko (jeśli nie aktywne)
source .venv/bin/activate

# Zaktualizuj pip
pip install --upgrade pip

# Zainstaluj wszystkie zależności
pip install -r requirements.txt

# Sprawdź zainstalowane pakiety
pip list | grep -E "fastapi|pydantic|uvicorn|httpx"
```

### Krok 5: Skonfiguruj SecureDocCompare

```bash
cd /home/debian/hack/BAW/SecureDocCompare

# Skopiuj przykładową konfigurację
cp .env.example .env

# Edytuj konfigurację
nano .env
```

Ustaw w `.env`:
```env
# WAŻNE: Zmień hasło!
APP_PASSWORD=TwojeSuperbezpieczneHaslo123!

# Wygeneruj SECRET_KEY (użyj polecenia poniżej)
SECRET_KEY=wygenerowany-losowy-klucz-64-znaki

# URL do API (na tym samym serwerze)
DOCUMENT_API_URL=http://localhost:8001

# Port
APP_PORT=8000

# Tryb produkcyjny
PRODUCTION=true
```

**Generowanie SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Skopiuj wygenerowany klucz do `SECRET_KEY` w pliku `.env`.

---

## 🎮 Uruchomienie Aplikacji

### Test Manualny

#### Terminal 1 - Backend (UslugaDoPorownan)

```bash
cd /home/debian/hack/BAW
source .venv/bin/activate
cd UslugaDoPorownan
uvicorn main:app --host 0.0.0.0 --port 8001
```

#### Terminal 2 - Frontend (SecureDocCompare)

```bash
cd /home/debian/hack/BAW
source .venv/bin/activate
cd SecureDocCompare
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Sprawdź czy działa:

```bash
# Health check backendu
curl http://localhost:8001/health

# Health check frontendu
curl http://localhost:8000/health

# Z przeglądarki (jeśli firewall pozwala)
# http://IP_SERWERA:8000
```

---

## 🔥 Konfiguracja Firewall

**WAŻNE:** Aby API było dostępne z zewnątrz (np. z N8N, innych systemów), musisz otworzyć porty w firewallu.

### Automatyczna naprawa (ZALECANE)

Użyj przygotowanego skryptu:

```bash
cd /home/debian/hack/BAW

# Skopiuj skrypty z repozytorium (jeśli nie masz)
# lub pobierz z GitHub

# Nadaj uprawnienia
chmod +x check_api.sh fix_firewall.sh

# Diagnoza problemu
./check_api.sh

# Automatyczna naprawa
sudo ./fix_firewall.sh
```

### Manualna konfiguracja UFW (Ubuntu/Debian)

```bash
# Sprawdź status
sudo ufw status

# Otwórz porty
sudo ufw allow 8001/tcp comment 'BAW Backend API'
sudo ufw allow 8000/tcp comment 'BAW Frontend'

# Sprawdź ponownie
sudo ufw status numbered

# Przeładuj (jeśli potrzeba)
sudo ufw reload
```

### Manualna konfiguracja iptables

```bash
# Sprawdź aktualne reguły
sudo iptables -L INPUT -n

# Dodaj reguły ACCEPT
sudo iptables -I INPUT -p tcp --dport 8001 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT

# Zapisz reguły (Debian)
sudo mkdir -p /etc/iptables
sudo iptables-save | sudo tee /etc/iptables/rules.v4

# Automatyczne wczytywanie po restarcie
sudo apt install iptables-persistent
```

### Weryfikacja dostępu

```bash
# Test lokalny
curl http://localhost:8001/health

# Test z serwera (zewnętrzne IP)
EXTERNAL_IP=$(curl -s ifconfig.me)
curl http://$EXTERNAL_IP:8001/health

# Test z innego komputera (zastąp IP)
curl http://217.182.76.146:8001/health
```

**Oczekiwana odpowiedź:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T...",
  "statistics": {...}
}
```

### Troubleshooting

Jeśli API nadal nie odpowiada:

1. **Sprawdź czy backend działa:**
   ```bash
   sudo systemctl status baw-backend
   ```

2. **Sprawdź czy port nasłuchuje:**
   ```bash
   sudo ss -tlnp | grep 8001
   # Powinno pokazać: *:8001 (oznacza wszystkie interfejsy)
   ```

3. **Sprawdź logi:**
   ```bash
   sudo journalctl -u baw-backend -n 50
   ```

4. **Sprawdź cloud firewall:**
   - AWS: Security Groups
   - Azure: Network Security Groups
   - Google Cloud: Firewall Rules
   - OVH/Hetzner: Firewall w panelu

5. **Użyj narzędzia diagnostycznego:**
   ```bash
   ./check_api.sh
   ```

---

## 🔄 Automatyzacja z systemd

Aby aplikacje uruchamiały się automatycznie przy starcie systemu.

### Backend Service

```bash
# Stwórz plik usługi
sudo nano /etc/systemd/system/baw-backend.service
```

Wklej:
```ini
[Unit]
Description=BAW Backend API (UslugaDoPorownan)
After=network.target

[Service]
Type=simple
User=debian
WorkingDirectory=/home/debian/hack/BAW/UslugaDoPorownan
Environment="PATH=/home/debian/hack/BAW/.venv/bin:/home/debian/.pyenv/shims:/usr/bin:/bin"
ExecStart=/home/debian/hack/BAW/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Frontend Service

```bash
# Stwórz plik usługi
sudo nano /etc/systemd/system/baw-frontend.service
```

Wklej:
```ini
[Unit]
Description=BAW Frontend (SecureDocCompare)
After=network.target baw-backend.service

[Service]
Type=simple
User=debian
WorkingDirectory=/home/debian/hack/BAW/SecureDocCompare
Environment="PATH=/home/debian/hack/BAW/.venv/bin:/home/debian/.pyenv/shims:/usr/bin:/bin"
EnvironmentFile=/home/debian/hack/BAW/SecureDocCompare/.env
ExecStart=/home/debian/hack/BAW/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Włącz i uruchom usługi

```bash
# Przeładuj konfigurację systemd
sudo systemctl daemon-reload

# Włącz autostart
sudo systemctl enable baw-backend
sudo systemctl enable baw-frontend

# Uruchom usługi
sudo systemctl start baw-backend
sudo systemctl start baw-frontend

# Sprawdź status
sudo systemctl status baw-backend
sudo systemctl status baw-frontend

# Zobacz logi
sudo journalctl -u baw-backend -f
sudo journalctl -u baw-frontend -f
```

### Zarządzanie usługami

```bash
# Start
sudo systemctl start baw-backend baw-frontend

# Stop
sudo systemctl stop baw-backend baw-frontend

# Restart
sudo systemctl restart baw-backend baw-frontend

# Status
sudo systemctl status baw-backend baw-frontend

# Logi (live)
sudo journalctl -u baw-backend -u baw-frontend -f

# Logi (ostatnie 100 linii)
sudo journalctl -u baw-backend -n 100
```

---

## 🌐 Nginx Reverse Proxy

Aby dostęp był przez standardowe porty 80/443.

### Instalacja Nginx

```bash
sudo apt update
sudo apt install nginx
```

### Konfiguracja

```bash
sudo nano /etc/nginx/sites-available/baw
```

Wklej:
```nginx
server {
    listen 80;
    server_name twoja-domena.com;  # Lub IP serwera

    # Frontend
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (jeśli potrzebne)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8001/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Aktywuj konfigurację

```bash
# Stwórz symlink
sudo ln -s /etc/nginx/sites-available/baw /etc/nginx/sites-enabled/

# Usuń domyślną konfigurację
sudo rm /etc/nginx/sites-enabled/default

# Testuj konfigurację
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

Teraz dostęp przez: `http://IP_SERWERA` lub `http://twoja-domena.com`

---

## 🔒 HTTPS z Let's Encrypt

### Instalacja Certbot

```bash
sudo apt install certbot python3-certbot-nginx
```

### Wygeneruj certyfikat

```bash
# Zastąp twoja-domena.com swoją domeną
sudo certbot --nginx -d twoja-domena.com

# Odpowiedz na pytania:
# - Email: twoj@email.com
# - Zgoda na ToS: Yes
# - Przekierowanie HTTP -> HTTPS: Yes (zalecane)
```

### Auto-odnowienie

```bash
# Testuj odnowienie
sudo certbot renew --dry-run

# Certbot automatycznie dodaje cron job do odnowienia
# Sprawdź:
sudo systemctl status certbot.timer
```

---

## 📊 Monitoring i Logi

### Logi systemd

```bash
# Logi w czasie rzeczywistym
sudo journalctl -u baw-backend -u baw-frontend -f

# Logi z ostatniej godziny
sudo journalctl -u baw-backend --since "1 hour ago"

# Logi z błędami
sudo journalctl -u baw-backend -p err
```

### Logi nginx

```bash
# Access log
sudo tail -f /var/log/nginx/access.log

# Error log
sudo tail -f /var/log/nginx/error.log
```

### Monitoring zasobów

```bash
# CPU i RAM
htop

# Procesy Pythona
ps aux | grep python

# Porty
sudo netstat -tulpn | grep -E "8000|8001"
```

---

## 💾 Backup i Aktualizacje

### Backup konfiguracji

```bash
# Backup plików .env
cp /home/debian/hack/BAW/SecureDocCompare/.env /home/debian/backups/baw-env-$(date +%Y%m%d).bak

# Backup całego projektu
tar -czf /home/debian/backups/baw-$(date +%Y%m%d).tar.gz /home/debian/hack/BAW
```

### Aktualizacja kodu

```bash
# Zatrzymaj usługi
sudo systemctl stop baw-backend baw-frontend

# Skopiuj nowy kod (SCP/Git)
# ...

# Aktywuj środowisko i zainstaluj zależności
cd /home/debian/hack/BAW
source .venv/bin/activate
pip install -r requirements.txt

# Uruchom ponownie
sudo systemctl start baw-backend baw-frontend

# Sprawdź status
sudo systemctl status baw-backend baw-frontend
```

---

## 🔥 Firewall

```bash
# Zainstaluj ufw
sudo apt install ufw

# Pozwól na SSH (WAŻNE!)
sudo ufw allow 22/tcp

# Pozwól na HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Opcjonalnie: Pozwól bezpośrednio na porty aplikacji
# sudo ufw allow 8000/tcp
# sudo ufw allow 8001/tcp

# Włącz firewall
sudo ufw enable

# Sprawdź status
sudo ufw status
```

---

## ✅ Checklist Produkcyjny

Przed uruchomieniem w produkcji sprawdź:

- [ ] Python 3.11.9 zainstalowany przez pyenv
- [ ] Środowisko wirtualne stworzone i aktywne
- [ ] Wszystkie zależności zainstalowane (`pip list`)
- [ ] Hasło zmienione w `SecureDocCompare/.env`
- [ ] `SECRET_KEY` wygenerowany i ustawiony
- [ ] `PRODUCTION=true` w `.env`
- [ ] Usługi systemd skonfigurowane i działające
- [ ] Nginx zainstalowany i skonfigurowany
- [ ] HTTPS certyfikat zainstalowany (jeśli domena)
- [ ] Firewall skonfigurowany
- [ ] Backup konfiguracji wykonany
- [ ] Logi działają poprawnie

---

## 📞 Pomoc

Jeśli napotkasz problemy:

1. Sprawdź logi: `sudo journalctl -u baw-backend -u baw-frontend`
2. Sprawdź status: `sudo systemctl status baw-backend baw-frontend`
3. Sprawdź połączenie: `curl http://localhost:8000/health`
4. Zobacz dokumentację: `README.md`, `SecureDocCompare/SECURITY.md`

---

**Wersja:** 1.0.0
**Ostatnia aktualizacja:** 2025-10-21
**Testowane na:** Debian 11 (Bullseye) i Debian 12 (Bookworm)
