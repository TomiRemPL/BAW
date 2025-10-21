# Quick Start Guide - SecureDocCompare

## 🚀 Szybki start w 5 krokach

### Wymagania
- **Python:** 3.11.9
- **System:** Windows 10/11 lub Debian/Linux
- **Backend:** UslugaDoPorownan musi działać na porcie 8001

---

## Windows (Development)

### 1. Zainstaluj zależności
```bash
cd c:/Projects/BAW
pip install -r requirements.txt
```

### 2. Skonfiguruj hasło
Edytuj plik `.env`:
```bash
cd SecureDocCompare
notepad .env
```

Zmień hasło:
```env
APP_PASSWORD=TwojeNoweHaslo123!
```

### 3. Uruchom backend (w osobnym terminalu)
```bash
cd c:/Projects/BAW
.venv\Scripts\activate
cd UslugaDoPorownan
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 4. Uruchom frontend
```bash
cd c:/Projects/BAW
.venv\Scripts\activate
cd SecureDocCompare
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Otwórz w przeglądarce
http://localhost:8000

---

## Debian/Linux (Production)

### 1. Zainstaluj Python 3.11.9 przez pyenv

```bash
# Zainstaluj zależności
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Zainstaluj pyenv
curl https://pyenv.run | bash

# Konfiguracja bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Przeładuj
exec $SHELL

# Zainstaluj Python 3.11.9
pyenv install 3.11.9
pyenv global 3.11.9

# Sprawdź
python --version  # Powinno być: Python 3.11.9
```

### 2. Stwórz środowisko i zainstaluj zależności

```bash
# Przejdź do projektu
cd /home/debian/hack/BAW

# Stwórz środowisko wirtualne
python -m venv .venv

# Aktywuj
source .venv/bin/activate

# Zainstaluj zależności
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Skonfiguruj hasło
```bash
cd /home/debian/hack/BAW/SecureDocCompare
nano .env
```

Ustaw:
```env
APP_PASSWORD=TwojeSuperbezpieczneHaslo123!
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(48))")
DOCUMENT_API_URL=http://localhost:8001
APP_PORT=8000
PRODUCTION=true
```

### 4. Uruchom backend (Terminal 1)
```bash
cd /home/debian/hack/BAW
source .venv/bin/activate
cd UslugaDoPorownan
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 5. Uruchom frontend (Terminal 2)
```bash
cd /home/debian/hack/BAW
source .venv/bin/activate
cd SecureDocCompare
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Otwórz w przeglądarce
http://IP_SERWERA:8000

---

## 📝 Pierwsze użycie

1. **Zaloguj się** - użyj hasła z pliku `.env`
2. **Wybierz pliki** - starą i nową wersję dokumentu (.docx)
3. **Wgraj dokumenty** - kliknij "Wgraj dokumenty"
4. **Rozpocznij analizę** - kliknij "Rozpocznij analizę"
5. **Pobierz wyniki** - wybierz typ wyniku (pełny, zmodyfikowane, dodane, usunięte)

---

## 🔧 Rozwiązywanie problemów

### Problem: "Connection refused" do API
**Rozwiązanie:** Upewnij się, że UslugaDoPorownan działa na porcie 8001

```bash
# Sprawdź backend
curl http://localhost:8001/health

# Powinno zwrócić:
# {"status":"healthy", ...}
```

### Problem: "Nieprawidłowe hasło"
**Rozwiązanie:** Sprawdź plik `.env` i wartość `APP_PASSWORD`

```bash
# Wyświetl hasło
cat .env | grep APP_PASSWORD
```

### Problem: "Module not found"
**Rozwiązanie:** Zainstaluj zależności

```bash
# Aktywuj środowisko
source .venv/bin/activate  # Linux
.venv\Scripts\activate      # Windows

# Zainstaluj
pip install -r requirements.txt
```

### Problem: Port 8000 jest zajęty
**Rozwiązanie:** Zmień port w pliku `.env`:

```env
APP_PORT=8080
```

Następnie uruchom:
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Problem: Python nie jest 3.11.9
**Rozwiązanie Windows:**
- Zainstaluj Python 3.11.9 z python.org
- Stwórz środowisko używając: `py -3.11 -m venv .venv`

**Rozwiązanie Linux:**
```bash
# Użyj pyenv
pyenv install 3.11.9
pyenv global 3.11.9
python --version  # Sprawdź
```

---

## 📊 Testowanie

### Test 1: Health Check

```bash
# Backend
curl http://localhost:8001/health

# Frontend
curl http://localhost:8000/health
```

### Test 2: Upload dokumentów

```bash
# Przygotuj dwa pliki DOCX: stary.docx i nowy.docx

curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@stary.docx" \
  -F "new_document=@nowy.docx"

# Powinno zwrócić document_pair_id
```

---

## 🎯 Następne kroki

- Przeczytaj [README.md](README.md) dla szczegółowej dokumentacji
- Zobacz [SECURITY.md](SECURITY.md) dla informacji o zabezpieczeniach
- W produkcji przeczytaj [../DEPLOYMENT.md](../DEPLOYMENT.md) dla wdrożenia na serwer

---

## 💡 Wskazówki

- **Trzymaj hasło w tajemnicy** - nie udostępniaj nikomu
- **Nie commituj pliku `.env`** do repozytorium Git
- **Regularnie czyść katalog `uploads/`** - stare pliki mogą zajmować miejsce
- **Monitoruj logi** w konsoli - pokazują błędy i ostrzeżenia
- **Używaj HTTPS** w produkcji (nginx + Let's Encrypt)

---

## 🔐 Bezpieczeństwo

### Development (localhost)
- HTTP jest OK
- Proste hasło jest akceptowalne
- Rate limiting: 20 req/min
- Max rozmiar pliku: 50MB

### Production (serwer)
- **WYMAGANE HTTPS** (używaj nginx + certbot)
- **Silne hasło** (min. 16 znaków, cyfry, znaki specjalne)
- **Zmień SECRET_KEY** (wygeneruj losowy: `python -c "import secrets; print(secrets.token_urlsafe(48))"`)
- **Ustaw PRODUCTION=true** w `.env`
- **Firewall** - ogranicz dostęp do portów 8000/8001

---

## 📞 Potrzebujesz pomocy?

1. Sprawdź logi w konsoli
2. Przeczytaj [README.md](README.md) i [SECURITY.md](SECURITY.md)
3. Zobacz główny [../README.md](../README.md) dla całego projektu BAW
4. Sprawdź [../DEPLOYMENT.md](../DEPLOYMENT.md) dla instrukcji wdrożenia

---

**Wersja:** 1.0.0
**Python:** 3.11.9
**Status:** ✅ Production Ready
