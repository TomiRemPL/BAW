# Dokumentacja Zabezpieczeń

## 🔒 Zaimplementowane mechanizmy zabezpieczeń

### 1. System Autentykacji

**Implementacja:** `auth.py`

#### Funkcje:
- **Hasło dostępu** - Pojednicze hasło do aplikacji (proste, ale skuteczne dla lokalnego użytku)
- **Hashowanie** - SHA-256 z użyciem `secrets.compare_digest()` (ochrona przed timing attacks)
- **Zarządzanie sesjami** - Token-based sessions z automatycznym wygasaniem
- **Timeout sesji** - Domyślnie 60 minut, konfigurowalne

#### Mechanizm:
```python
# Logowanie
verify_password(password) -> bool

# Sesja
session_id = session_manager.create_session()
session_manager.validate_session(session_id) -> bool

# Wylogowanie
session_manager.destroy_session(session_id)
```

#### Cookies:
- `httponly=True` - JavaScript nie ma dostępu
- `secure=True` (produkcja) - Tylko HTTPS
- `samesite="strict"` - Ochrona przed CSRF
- `max_age` - Automatyczne wygasanie

---

### 2. Walidacja Plików

**Implementacja:** `middleware.py` + `main.py`

#### Sprawdzenia:
1. **Rozszerzenie pliku** - Tylko `.docx`
2. **Rozmiar pliku** - Max 50MB (konfigurowalne)
3. **Content-Type** - MIME type validation
4. **Content-Length** - Pre-upload check

#### Konfiguracja (`config.py`):
```python
max_file_size: int = 50 * 1024 * 1024  # 50MB
allowed_extensions: set = {".docx"}
```

#### Ochrona przed:
- Upload złośliwych plików
- Upload plików za dużych (DoS)
- Path traversal attacks

---

### 3. Rate Limiting

**Implementacja:** `middleware.py` - `RateLimitMiddleware`

#### Mechanizm:
- **Limit:** 20 requestów na minutę (konfigurowalne)
- **Tracking:** Per IP address
- **Window:** Sliding window 1 minuta
- **Wyłączenia:** Pliki statyczne (`/static/`)

#### Konfiguracja:
```python
max_requests_per_minute: int = 20
```

#### Response przy przekroczeniu:
```json
{
  "detail": "Zbyt wiele żądań. Spróbuj ponownie za chwilę."
}
```
Status: `429 Too Many Requests`

#### Ochrona przed:
- Brute force attacks na hasło
- DoS attacks
- Nadmiernym zużyciem zasobów

---

### 4. Bezpieczne Nagłówki HTTP

**Implementacja:** `middleware.py` - `SecurityHeadersMiddleware`

#### Nagłówki:

1. **X-Content-Type-Options: nosniff**
   - Zapobiega MIME-type sniffing
   - Przeglądarka musi respektować Content-Type

2. **X-Frame-Options: DENY**
   - Zapobiega clickjacking
   - Strona nie może być osadzona w iframe

3. **X-XSS-Protection: 1; mode=block**
   - Aktywuje filtr XSS w przeglądarce
   - Blokuje renderowanie przy wykryciu XSS

4. **Strict-Transport-Security**
   - `max-age=31536000` (1 rok)
   - `includeSubDomains`
   - Wymusza HTTPS

5. **Content-Security-Policy**
   ```
   default-src 'self';
   script-src 'self' 'unsafe-inline';
   style-src 'self' 'unsafe-inline';
   img-src 'self' data:;
   font-src 'self';
   connect-src 'self';
   ```
   - Ogranicza źródła zasobów
   - Ochrona przed XSS i injection attacks

6. **Server: SecureDocCompare**
   - Ukrywa wersję i typ serwera

#### Ochrona przed:
- XSS (Cross-Site Scripting)
- Clickjacking
- MIME-type confusion
- Man-in-the-middle (MITM)
- Content injection

---

### 5. Walidacja Parametrów i Path Safety

**Implementacja:** `main.py`

#### Mechanizmy:
1. **Brak bezpośredniego file access** - Wszystkie operacje przez API
2. **UUID validation** - IDs są UUID4, nie ścieżki
3. **Proxy pattern** - Frontend nie ma dostępu do systemu plików
4. **FastAPI validation** - Automatyczna walidacja typów

#### Ochrona przed:
- Path traversal (`../../../etc/passwd`)
- Directory listing
- Unauthorized file access
- SQL injection (nie używamy SQL, ale podobne ataki)

---

## 🛡️ Dodatkowe zabezpieczenia

### CORS
```python
CORSMiddleware(
    allow_origins=["*"],  # W produkcji: konkretne domeny
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
**Uwaga:** W produkcji ogranicz `allow_origins`!

### Error Handling
- Ogólne komunikaty błędów (nie ujawniamy szczegółów)
- Szczegółowe logi tylko w konsoli serwera
- Brak stack traces w odpowiedziach HTTP

### Logging
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```
- Logowanie prób logowania
- Logowanie błędów
- Brak logowania wrażliwych danych (hasła, tokeny)

---

## 🚨 Znane ograniczenia

### 1. Single password authentication
- **Ograniczenie:** Wszystcy użytkownicy używają tego samego hasła
- **Ryzyko:** Brak audytu kto się logował
- **Mitigacja:** Dla lokalnego użytku akceptowalne
- **Upgrade path:** Dodać bazę użytkowników (SQLite/PostgreSQL)

### 2. In-memory session storage
- **Ograniczenie:** Sesje znikają po restarcie
- **Ryzyko:** Użytkownicy muszą się ponownie zalogować
- **Mitigacja:** Akceptowalne dla lokalnego użytku
- **Upgrade path:** Redis lub database-backed sessions

### 3. Rate limiting per IP
- **Ograniczenie:** Za NAT wielu użytkowników = jeden IP
- **Ryzyko:** Legalni użytkownicy mogą być zablokowani
- **Mitigacja:** Zwiększ limit lub wyłącz za NAT
- **Upgrade path:** Token-based rate limiting

### 4. No HTTPS enforcement in dev
- **Ograniczenie:** Development używa HTTP
- **Ryzyko:** Man-in-the-middle w sieci lokalnej
- **Mitigacja:** `PRODUCTION=true` wymusza secure cookies
- **Upgrade path:** Użyj reverse proxy (nginx) z HTTPS

### 5. File storage on disk
- **Ograniczenie:** Pliki są zapisywane na dysku
- **Ryzyko:** Potencjalny wyciek danych
- **Mitigacja:** Katalog `uploads/` w `.gitignore`
- **Upgrade path:** Encryption at rest lub cloud storage

---

## 🔧 Rekomendacje dla produkcji

### Must-have:

1. **HTTPS**
   ```bash
   # Użyj nginx jako reverse proxy
   server {
       listen 443 ssl;
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;

       location / {
           proxy_pass http://localhost:8000;
       }
   }
   ```

2. **Zmień hasło**
   ```env
   APP_PASSWORD=bardzo-dluge-i-skomplikowane-haslo
   ```

3. **Wygeneruj SECRET_KEY**
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

4. **Ustaw PRODUCTION=true**
   ```env
   PRODUCTION=true
   ```

5. **Ogranicz CORS**
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

### Nice-to-have:

1. **Firewall**
   ```bash
   # Zezwól tylko z konkretnych IP
   ufw allow from 192.168.1.0/24 to any port 8000
   ```

2. **Monitoring i alerty**
   - Failed login attempts
   - Rate limit violations
   - Error rates

3. **Backup sesji**
   - Redis dla persistent sessions

4. **Audit logging**
   - Kto się logował
   - Jakie pliki uploadował
   - Jakie operacje wykonał

5. **File encryption**
   - Szyfruj pliki w `uploads/`

---

## 📋 Checklist bezpieczeństwa

Przed wdrożeniem produkcyjnym:

- [ ] Zmieniono domyślne hasło
- [ ] Wygenerowano unikalny SECRET_KEY
- [ ] Ustawiono PRODUCTION=true
- [ ] Skonfigurowano HTTPS
- [ ] Ograniczono CORS do konkretnych domen
- [ ] Skonfigurowano firewall
- [ ] Sprawdzono że .env nie jest w repozytorium
- [ ] Ustawiono właściwe uprawnienia plików (chmod)
- [ ] Skonfigurowano automatyczne backupy
- [ ] Włączono monitoring i logi
- [ ] Przetestowano wszystkie funkcje bezpieczeństwa

---

## 🔍 Testowanie zabezpieczeń

### Test 1: Autentykacja
```bash
# Bez logowania - powinno pokazać stronę logowania
curl http://localhost:8000/

# Z błędnym hasłem - 401
curl -X POST http://localhost:8000/api/login -d "password=wrong"

# Z dobrym hasłem - przekierowanie + cookie
curl -X POST http://localhost:8000/api/login -d "password=correct" -v
```

### Test 2: Rate limiting
```bash
# 25 requestów w ciągu minuty - ostatnie powinny dać 429
for i in {1..25}; do
    curl http://localhost:8000/health
    sleep 2
done
```

### Test 3: Walidacja plików
```bash
# Plik .txt zamiast .docx - 400
curl -X POST http://localhost:8000/api/upload \
  -F "old_document=@test.txt" \
  -F "new_document=@test.docx"

# Plik za duży - 413
# (utwórz plik > 50MB)
```

### Test 4: Nagłówki bezpieczeństwa
```bash
curl -I http://localhost:8000/
# Sprawdź czy są obecne wszystkie security headers
```

---

## 📞 Kontakt w sprawie bezpieczeństwa

Jeśli znajdziesz lukę w zabezpieczeniach, zgłoś ją odpowiedzialnie.

**Nie zgłaszaj publicznie** - skontaktuj się bezpośrednio z zespołem rozwoju.

---

## 📚 Dodatkowe zasoby

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
