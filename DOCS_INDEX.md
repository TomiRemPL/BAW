# 📚 Indeks Dokumentacji - Projekt BAW

Kompleksowy przewodnik po dokumentacji projektu porównywania dokumentów bankowych.

## 🗂️ Struktura Dokumentacji

### Główny Katalog (`/BAW`)

| Plik | Opis | Dla kogo |
|------|------|----------|
| [README.md](README.md) | **Start tutaj!** Ogólny opis projektu, architektura, instalacja | Wszyscy |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Szczegółowe instrukcje wdrożenia na Debian z pyenv, systemd, nginx | DevOps, Admin |
| [DOCS_INDEX.md](DOCS_INDEX.md) | Ten plik - indeks całej dokumentacji | Wszyscy |
| [VSCODE_SETUP.md](VSCODE_SETUP.md) | **NOWY!** Konfiguracja Visual Studio Code, debugowanie, tasks | Developer |
| [PROGRESS_LOG.md](PROGRESS_LOG.md) | Historia postępu prac i stan projektu | Manager, Developer |
| [PDF_CONVERSION_SUMMARY.md](PDF_CONVERSION_SUMMARY.md) | Podsumowanie implementacji konwersji PDF→DOCX | Developer |
| [requirements.txt](requirements.txt) | Wspólne zależności Python dla całego projektu | Developer |
| [test.http](test.http) | **NOWY!** Testy API dla REST Client (VSCode) | Developer, API User |
| [CLAUDE.md](CLAUDE.md) | Instrukcje dla Claude Code AI | Developer |

### SecureDocCompare (`/SecureDocCompare`)

| Plik | Opis | Dla kogo |
|------|------|----------|
| [README.md](SecureDocCompare/README.md) | Dokumentacja frontendu - funkcje, konfiguracja, API | Developer, User |
| [QUICK_START.md](SecureDocCompare/QUICK_START.md) | Szybki start - Windows i Linux, krok po kroku | Wszyscy |
| [SECURITY.md](SecureDocCompare/SECURITY.md) | Szczegóły zabezpieczeń, testy, rekomendacje | Security, DevOps |
| [.env.example](.env.example) | Przykładowa konfiguracja środowiskowa | Developer |

### UslugaDoPorownan (`/UslugaDoPorownan`)

| Plik | Opis | Dla kogo |
|------|------|----------|
| [README.md](UslugaDoPorownan/README.md) | Dokumentacja API backendu - endpointy, przykłady curl | Developer, API User |
| [QUICKSTART.md](UslugaDoPorownan/QUICKSTART.md) | Szybki start backendu API | Developer |
| [PROJECT_SUMMARY.md](UslugaDoPorownan/PROJECT_SUMMARY.md) | Podsumowanie projektu UslugaDoPorownan | Manager, Developer |

---

## 🚀 Ścieżki Nauki

### Jestem nowy w projekcie

1. Zacznij od [README.md](README.md) - zrozum architekturę
2. Przeczytaj [SecureDocCompare/QUICK_START.md](SecureDocCompare/QUICK_START.md)
3. Zainstaluj i uruchom lokalnie
4. Przetestuj podstawowe funkcje

### Chcę wdrożyć na serwer

1. Przeczytaj [README.md](README.md) - sekcja "Wymagania"
2. Podążaj za [DEPLOYMENT.md](DEPLOYMENT.md) krok po kroku
3. Skonfiguruj [SecureDocCompare/.env](SecureDocCompare/.env.example)
4. Zobacz [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) dla checklisty bezpieczeństwa

### Chcę rozwijać funkcje

1. Zrozum strukturę z [README.md](README.md)
2. Frontend: czytaj [SecureDocCompare/README.md](SecureDocCompare/README.md)
3. Backend API: czytaj [UslugaDoPorownan/README.md](UslugaDoPorownan/README.md)
4. Zobacz [CLAUDE.md](CLAUDE.md) dla pomocy AI

### Interesuję się bezpieczeństwem

1. [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) - szczegóły zabezpieczeń
2. [DEPLOYMENT.md](DEPLOYMENT.md) - sekcje: HTTPS, Firewall, systemd
3. [SecureDocCompare/README.md](SecureDocCompare/README.md) - sekcja "Funkcje bezpieczeństwa"

### Chcę użyć API

1. [UslugaDoPorownan/README.md](UslugaDoPorownan/README.md) - pełna dokumentacja API
2. [UslugaDoPorownan/QUICKSTART.md](UslugaDoPorownan/QUICKSTART.md) - szybki start
3. [test.http](test.http) - przykłady zapytań API dla REST Client
4. Przykłady curl i integracji

### Pracuję w Visual Studio Code

1. [VSCODE_SETUP.md](VSCODE_SETUP.md) - **Start tutaj!** Kompletna konfiguracja VSCode
2. Zainstaluj rekomendowane rozszerzenia (`.vscode/extensions.json`)
3. Użyj debugowania (`F5`) i tasków (`Ctrl+Shift+P` → Tasks)
4. Testuj API przez [test.http](test.http) z rozszerzeniem REST Client

---

## 🎯 Częste Scenariusze

### Instalacja Lokalna (Windows Development)

```
README.md → SecureDocCompare/QUICK_START.md → Testowanie
```

**Pliki:**
1. [README.md](README.md) - sekcja "Instalacja - Windows"
2. [SecureDocCompare/QUICK_START.md](SecureDocCompare/QUICK_START.md) - sekcja "Windows"

### Deployment na Debian

```
README.md → DEPLOYMENT.md → SecureDocCompare/SECURITY.md
```

**Pliki:**
1. [README.md](README.md) - sekcja "Wymagania - Debian"
2. [DEPLOYMENT.md](DEPLOYMENT.md) - pełna instrukcja
3. [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) - checklist

### Konfiguracja Zabezpieczeń

```
SecureDocCompare/SECURITY.md → SecureDocCompare/.env → DEPLOYMENT.md (nginx/HTTPS)
```

**Pliki:**
1. [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) - wszystkie mechanizmy
2. [SecureDocCompare/.env.example](SecureDocCompare/.env.example) - przykładowa konfiguracja
3. [DEPLOYMENT.md](DEPLOYMENT.md) - sekcje nginx i Let's Encrypt

### Integracja z API

```
UslugaDoPorownan/README.md → UslugaDoPorownan/QUICKSTART.md → Przykłady curl
```

**Pliki:**
1. [UslugaDoPorownan/README.md](UslugaDoPorownan/README.md) - dokumentacja endpointów
2. [UslugaDoPorownan/QUICKSTART.md](UslugaDoPorownan/QUICKSTART.md) - szybki start

---

## 📖 Szczegółowy Opis Plików

### README.md (Główny)
**Lokalizacja:** `/BAW/README.md`

Główna dokumentacja projektu zawierająca:
- Przegląd architektury (Frontend + Backend)
- Wymagania systemowe (Python 3.11.9, Windows/Debian)
- Instrukcje instalacji dla Windows i Linux
- Komendy uruchomienia obu komponentów
- Konfiguracja i zmienne środowiskowe
- Troubleshooting i FAQ
- Bezpieczeństwo (development vs production)

**Kiedy czytać:** Zawsze jako pierwszy dokument!

---

### DEPLOYMENT.md
**Lokalizacja:** `/BAW/DEPLOYMENT.md`

Kompletny przewodnik wdrożenia produkcyjnego:
- Instalacja Python 3.11.9 przez pyenv
- Konfiguracja środowiska wirtualnego
- Automatyzacja z systemd (auto-start)
- Nginx reverse proxy
- HTTPS z Let's Encrypt
- Firewall (ufw)
- Monitoring i logi
- Backup i aktualizacje

**Kiedy czytać:** Przed wdrożeniem na serwer produkcyjny

---

### SecureDocCompare/README.md
**Lokalizacja:** `/BAW/SecureDocCompare/README.md`

Dokumentacja frontendu:
- System logowania i autentykacji
- Formularz uploadu plików
- Interfejs wyników
- 5 warstw zabezpieczeń
- API endpoints frontendu
- Konfiguracja (.env)

**Kiedy czytać:** Pracujesz z frontendem lub chcesz zrozumieć UI

---

### SecureDocCompare/QUICK_START.md
**Lokalizacja:** `/BAW/SecureDocCompare/QUICK_START.md`

Szybki start w 5 krokach:
- Instalacja dla Windows (development)
- Instalacja dla Debian/Linux (production)
- Pierwsze uruchomienie
- Troubleshooting
- Testowanie

**Kiedy czytać:** Chcesz szybko uruchomić projekt

---

### SecureDocCompare/SECURITY.md
**Lokalizacja:** `/BAW/SecureDocCompare/SECURITY.md`

Szczegółowa dokumentacja zabezpieczeń:
- System autentykacji (hasła, sesje, cookies)
- Walidacja plików (typy, rozmiary)
- Rate limiting (20 req/min)
- Bezpieczne nagłówki HTTP (CSP, HSTS, etc.)
- Path safety i walidacja parametrów
- Znane ograniczenia
- Rekomendacje dla produkcji
- Testy zabezpieczeń
- Checklist bezpieczeństwa

**Kiedy czytać:** Wdrażasz produkcyjnie lub interesujesz się bezpieczeństwem

---

### UslugaDoPorownan/README.md
**Lokalizacja:** `/BAW/UslugaDoPorownan/README.md`

Pełna dokumentacja API backendu:
- Wszystkie endpointy z przykładami curl
- Modele danych (request/response)
- Algorytm porównywania
- Typy zmian (unchanged, modified, added, deleted)
- Przykłady użycia (kompletny workflow)
- Troubleshooting

**Kiedy czytać:** Integrujesz się z API lub rozwijasz backend

---

### UslugaDoPorownan/QUICKSTART.md
**Lokalizacja:** `/BAW/UslugaDoPorownan/QUICKSTART.md`

Szybki start backendu API:
- Instalacja i uruchomienie
- Podstawowe testy
- Pierwsze użycie API

**Kiedy czytać:** Chcesz szybko przetestować backend API

---

## 🔍 Wyszukiwanie w Dokumentacji

### Szukam informacji o...

| Temat | Plik |
|-------|------|
| Instalacja Windows | [README.md](README.md) sekcja "Instalacja - Windows" |
| Instalacja Debian/Linux | [DEPLOYMENT.md](DEPLOYMENT.md) |
| Python 3.11.9 + pyenv | [DEPLOYMENT.md](DEPLOYMENT.md) sekcja "Instalacja Python" |
| Hasło i logowanie | [SecureDocCompare/README.md](SecureDocCompare/README.md), [SECURITY.md](SecureDocCompare/SECURITY.md) |
| Rate limiting | [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) sekcja "Rate Limiting" |
| HTTPS i SSL | [DEPLOYMENT.md](DEPLOYMENT.md) sekcja "HTTPS z Let's Encrypt" |
| systemd auto-start | [DEPLOYMENT.md](DEPLOYMENT.md) sekcja "Automatyzacja" |
| nginx konfiguracja | [DEPLOYMENT.md](DEPLOYMENT.md) sekcja "Nginx" |
| API endpointy | [UslugaDoPorownan/README.md](UslugaDoPorownan/README.md) |
| Przykłady curl | [UslugaDoPorownan/README.md](UslugaDoPorownan/README.md) |
| Testowanie API (REST Client) | [test.http](test.http) |
| VSCode konfiguracja | [VSCODE_SETUP.md](VSCODE_SETUP.md) |
| Debugowanie w VSCode | [VSCODE_SETUP.md](VSCODE_SETUP.md) sekcja "Debugowanie" |
| Konwersja PDF→DOCX | [PDF_CONVERSION_SUMMARY.md](PDF_CONVERSION_SUMMARY.md) |
| Historia zmian | [PROGRESS_LOG.md](PROGRESS_LOG.md) |
| Troubleshooting | [README.md](README.md), [QUICK_START.md](SecureDocCompare/QUICK_START.md), [VSCODE_SETUP.md](VSCODE_SETUP.md) |
| Bezpieczeństwo | [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) |
| Konfiguracja .env | [SecureDocCompare/.env.example](SecureDocCompare/.env.example) |

---

## 📊 Status Dokumentacji

| Dokument | Status | Ostatnia aktualizacja | Wersja |
|----------|--------|----------------------|--------|
| README.md | ✅ Aktualny | 2025-10-21 | 1.0.0 |
| DEPLOYMENT.md | ✅ Aktualny | 2025-10-21 | 1.0.0 |
| VSCODE_SETUP.md | ✅ Aktualny | 2025-10-22 | 1.0.0 |
| PROGRESS_LOG.md | ✅ Aktualny | 2025-10-22 | 1.0.1 |
| PDF_CONVERSION_SUMMARY.md | ✅ Aktualny | 2025-10-21 | 1.0.0 |
| test.http | ✅ Aktualny | 2025-10-22 | 1.0.0 |
| SecureDocCompare/README.md | ✅ Aktualny | 2025-10-20 | 1.0.0 |
| SecureDocCompare/QUICK_START.md | ✅ Aktualny | 2025-10-21 | 1.0.0 |
| SecureDocCompare/SECURITY.md | ✅ Aktualny | 2025-10-20 | 1.0.0 |
| UslugaDoPorownan/README.md | ✅ Aktualny | 2025-10-15 | 1.0.0 |
| requirements.txt | ✅ Aktualny | 2025-10-21 | Python 3.11-3.13 |
| .vscode/ (konfiguracja) | ✅ Aktualny | 2025-10-22 | 1.0.0 |

---

## 🛠️ Aktualizacja Dokumentacji

Jeśli znajdziesz nieaktualną informację:

1. Sprawdź datę ostatniej aktualizacji
2. Porównaj z aktualnym kodem
3. Zaktualizuj odpowiedni plik .md
4. Dodaj notatkę o zmianie w sekcji "Changelog" (jeśli istnieje)

---

## 📞 Wsparcie

- **Dokumentacja:** Ten indeks + pliki .md
- **Issues:** GitHub Issues
- **Development:** Claude Code AI (zobacz [CLAUDE.md](CLAUDE.md))

---

**Ostatnia aktualizacja:** 2025-10-22
**Wersja indeksu:** 1.1.0
**Projekt:** BAW - Porównywanie Dokumentów Bankowych

**Changelog 1.1.0:**
- Dodano VSCODE_SETUP.md - kompletna konfiguracja Visual Studio Code
- Dodano test.http - testy API dla REST Client
- Dodano .vscode/ - settings, launch, tasks, extensions, snippets
- Dodano .editorconfig - uniwersalne ustawienia edytora
- Zaktualizowano .gitignore - współdzielenie konfiguracji VSCode
