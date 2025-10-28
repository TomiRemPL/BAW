# 📚 Indeks Dokumentacji - Projekt BAW

Kompleksowy przewodnik po dokumentacji projektu porównywania dokumentów bankowych.

## 🗂️ Struktura Dokumentacji

### Główny Katalog (`/BAW`)

| Plik | Opis | Dla kogo |
|------|------|----------|
| [README.md](README.md) | **Start tutaj!** Ogólny opis projektu, architektura, instalacja | Wszyscy |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Szczegółowe instrukcje wdrożenia na Debian z pyenv, systemd, nginx, firewall | DevOps, Admin |
| [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) | **NOWY!** Przewodnik po skryptach zarządzania usługami (start/stop/status) | DevOps, Admin |
| [DOCS_INDEX.md](DOCS_INDEX.md) | Ten plik - indeks całej dokumentacji | Wszyscy |
| [VSCODE_SETUP.md](VSCODE_SETUP.md) | Konfiguracja Visual Studio Code, debugowanie, tasks | Developer |
| [PROGRESS_LOG.md](PROGRESS_LOG.md) | Historia postępu prac i stan projektu | Manager, Developer |
| [PDF_CONVERSION_SUMMARY.md](PDF_CONVERSION_SUMMARY.md) | Podsumowanie implementacji konwersji PDF→DOCX | Developer |
| [HTML_REPORT_ENDPOINT.md](HTML_REPORT_ENDPOINT.md) | **NOWY!** Dokumentacja endpointu generowania raportów HTML | Developer, API User |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Kompletna dokumentacja API (~900 linii, 9 endpointów) | Developer, API User |
| [N8N_INTEGRATION.md](N8N_INTEGRATION.md) | Integracja z N8N, workflow automation | DevOps, Automation |
| [N8N_WORKFLOW_GUIDE.md](N8N_WORKFLOW_GUIDE.md) | Przewodnik workflow N8N v2.0 | DevOps, Automation |
| [N8N_MEMORY_ONLY_GUIDE.md](N8N_MEMORY_ONLY_GUIDE.md) | Przewodnik memory-only workflow N8N v3.0 | DevOps, Security |
| [N8N_HTML_REPORT_INTEGRATION.md](N8N_HTML_REPORT_INTEGRATION.md) | **NOWY!** Integracja raportów HTML w N8N | DevOps, Automation |
| [requirements.txt](requirements.txt) | Wspólne zależności Python dla całego projektu | Developer |
| [test.http](test.http) | Testy API dla REST Client (produkcja) | Developer, API User |
| [test.local.http](test.local.http) | Testy API dla localhost | Developer |
| [test.prod.http](test.prod.http) | Testy API dla produkcji (217.182.76.146) | Developer, API User |
| [test_summaries.http](test_summaries.http) | **NOWY!** Testy endpointów podsumowań (n8n integration) | Developer, API User |
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
| [PROMPTS_CHANGELOG.md](UslugaDoPorownan/PROMPTS_CHANGELOG.md) | **NOWY!** Changelog aktualizacji promptów LLM v2.0 - eliminacja halucynacji, analiza ryzyka (~755 linii) | Developer, LLM User, Compliance |

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
3. Użyj skryptów z [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) do zarządzania usługami (start/stop/status)
4. Skonfiguruj [SecureDocCompare/.env](SecureDocCompare/.env.example)
5. Zobacz [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) dla checklisty bezpieczeństwa

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

### Chcę zintegrować z N8N

1. [N8N_INTEGRATION.md](N8N_INTEGRATION.md) - **Start tutaj!** Wprowadzenie do integracji N8N
2. [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Pełna lista endpointów z przykładami
3. [N8N_WORKFLOW_GUIDE.md](N8N_WORKFLOW_GUIDE.md) - Workflow v2.0 (podstawowy)
4. [N8N_MEMORY_ONLY_GUIDE.md](N8N_MEMORY_ONLY_GUIDE.md) - Workflow v3.0 (bez zapisu na dysku)
5. [N8N_HTML_REPORT_INTEGRATION.md](N8N_HTML_REPORT_INTEGRATION.md) - **NOWY!** Generowanie raportów HTML w N8N
6. [test.prod.http](test.prod.http) - Testowanie endpointów produkcyjnych

### Chcę generować raporty HTML

1. [HTML_REPORT_ENDPOINT.md](HTML_REPORT_ENDPOINT.md) - **Start tutaj!** Dokumentacja endpointu raportów
2. [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Kompletna dokumentacja API
3. [UslugaDoPorownan/README.md](UslugaDoPorownan/README.md) - Backend API
4. [test.http](test.http) - Przykłady zapytań API (REST Client)

### Chcę używać analizy LLM dla zmian w dokumentach

1. [UslugaDoPorownan/PROMPTS_CHANGELOG.md](UslugaDoPorownan/PROMPTS_CHANGELOG.md) - **Start tutaj!** Kompletna dokumentacja promptów LLM v2.0
2. Plik `UslugaDoPorownan/prompt_system.txt` - Prompt systemowy (359 linii, 5 zasad, 11 regulacji)
3. Plik `UslugaDoPorownan/prompt_user.txt` - Prompt użytkownika (355 linii, matryca zgodności, analiza ryzyka)
4. [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Pobieranie JSON z `/api/result/{process_id}/full`

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
README.md → DEPLOYMENT.md → SCRIPTS_GUIDE.md → SecureDocCompare/SECURITY.md
```

**Pliki:**
1. [README.md](README.md) - sekcja "Wymagania - Debian"
2. [DEPLOYMENT.md](DEPLOYMENT.md) - pełna instrukcja
3. [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) - zarządzanie usługami (start/stop/status)
4. [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) - checklist

### Zarządzanie Usługami (Screen Mode)

```
SCRIPTS_GUIDE.md → start_services.sh → status_services.sh → stop_services.sh
```

**Pliki:**
1. [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) - **Start tutaj!** Kompletny przewodnik skryptów
2. `start_services.sh` - Uruchomienie Backend + Frontend w screen
3. `stop_services.sh` - Zatrzymanie wszystkich usług
4. `status_services.sh` - Kompleksowy status i health check

**Szybki start:**
```bash
cd /home/debian/hack/BAW
chmod +x *.sh
./start_services.sh      # Uruchom usługi
./status_services.sh     # Sprawdź status
screen -r baw-backend    # Zobacz logi
./stop_services.sh       # Zatrzymaj usługi
```

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
| **Uruchamianie usług (screen)** | [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md), `start_services.sh` |
| **Zatrzymywanie usług** | [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md), `stop_services.sh` |
| **Status usług i health check** | [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md), `status_services.sh` |
| Hasło i logowanie | [SecureDocCompare/README.md](SecureDocCompare/README.md), [SECURITY.md](SecureDocCompare/SECURITY.md) |
| Rate limiting | [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) sekcja "Rate Limiting" |
| HTTPS i SSL | [DEPLOYMENT.md](DEPLOYMENT.md) sekcja "HTTPS z Let's Encrypt" |
| systemd auto-start | [DEPLOYMENT.md](DEPLOYMENT.md) sekcja "Automatyzacja" |
| **Nginx reverse proxy** | [DEPLOYMENT.md](DEPLOYMENT.md) sekcja "Nginx", `setup_nginx_proxy.sh` |
| **Firewall (ufw, iptables)** | [DEPLOYMENT.md](DEPLOYMENT.md) sekcja "Konfiguracja Firewall", `fix_firewall.sh` |
| **API - Kompletna dokumentacja** | [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - 9 endpointów |
| API endpointy | [UslugaDoPorownan/README.md](UslugaDoPorownan/README.md) |
| Przykłady curl | [UslugaDoPorownan/README.md](UslugaDoPorownan/README.md), [API_DOCUMENTATION.md](API_DOCUMENTATION.md) |
| Testowanie API (REST Client) | [test.http](test.http), [test.local.http](test.local.http), [test.prod.http](test.prod.http) |
| **Generowanie raportów HTML** | [HTML_REPORT_ENDPOINT.md](HTML_REPORT_ENDPOINT.md) - endpoint `/api/report/{process_id}/generate` |
| **N8N Integracja** | [N8N_INTEGRATION.md](N8N_INTEGRATION.md) |
| **N8N Workflow v2.0** | [N8N_WORKFLOW_GUIDE.md](N8N_WORKFLOW_GUIDE.md) |
| **N8N Memory-Only v3.0** | [N8N_MEMORY_ONLY_GUIDE.md](N8N_MEMORY_ONLY_GUIDE.md) |
| **Diagnostyka API** | `check_api.sh`, [API_DOCUMENTATION.md](API_DOCUMENTATION.md) sekcja "Troubleshooting" |
| VSCode konfiguracja | [VSCODE_SETUP.md](VSCODE_SETUP.md) |
| Debugowanie w VSCode | [VSCODE_SETUP.md](VSCODE_SETUP.md) sekcja "Debugowanie" |
| Konwersja PDF→DOCX | [PDF_CONVERSION_SUMMARY.md](PDF_CONVERSION_SUMMARY.md) |
| Historia zmian | [PROGRESS_LOG.md](PROGRESS_LOG.md) |
| Troubleshooting | [README.md](README.md), [QUICK_START.md](SecureDocCompare/QUICK_START.md), [VSCODE_SETUP.md](VSCODE_SETUP.md), [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) |
| Bezpieczeństwo | [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) |
| Konfiguracja .env | [SecureDocCompare/.env.example](SecureDocCompare/.env.example) |
| **Prompty LLM do analizy zmian** | [UslugaDoPorownan/PROMPTS_CHANGELOG.md](UslugaDoPorownan/PROMPTS_CHANGELOG.md) |
| **Analiza ryzyka przez LLM** | [UslugaDoPorownan/PROMPTS_CHANGELOG.md](UslugaDoPorownan/PROMPTS_CHANGELOG.md) sekcja "Obszary Analizy Ryzyka" |
| **Regulacje bankowe (DORA, AML, KYC)** | [UslugaDoPorownan/PROMPTS_CHANGELOG.md](UslugaDoPorownan/PROMPTS_CHANGELOG.md) sekcja "Regulacje do Weryfikacji" |
| **Matryca zgodności regulacyjnej** | [UslugaDoPorownan/PROMPTS_CHANGELOG.md](UslugaDoPorownan/PROMPTS_CHANGELOG.md) sekcja "Matryca Zgodności" |

---

## 📊 Status Dokumentacji

| Dokument | Status | Ostatnia aktualizacja | Wersja |
|----------|--------|----------------------|--------|
| README.md | ✅ Aktualny | 2025-10-21 | 1.0.0 |
| **DEPLOYMENT.md** | ✅ Aktualny | 2025-10-24 | 1.2.0 |
| **SCRIPTS_GUIDE.md** | ✅ Aktualny | 2025-10-24 | 1.0.0 |
| **DOCS_INDEX.md** | ✅ Aktualny | 2025-10-24 | 1.5.0 |
| VSCODE_SETUP.md | ✅ Aktualny | 2025-10-22 | 1.0.0 |
| **PROGRESS_LOG.md** | ✅ Aktualny | 2025-10-24 | 1.4.0 |
| PDF_CONVERSION_SUMMARY.md | ✅ Aktualny | 2025-10-21 | 1.0.0 |
| **HTML_REPORT_ENDPOINT.md** | ✅ Aktualny | 2025-10-23 | 1.0.0 |
| **API_DOCUMENTATION.md** | ✅ Aktualny | 2025-10-28 | 1.2.0 |
| **N8N_INTEGRATION.md** | ✅ Aktualny | 2025-10-23 | 1.0.0 |
| **N8N_WORKFLOW_GUIDE.md** | ✅ Aktualny | 2025-10-23 | 2.0.0 |
| **N8N_MEMORY_ONLY_GUIDE.md** | ✅ Aktualny | 2025-10-23 | 3.0.0 |
| **N8N_HTML_REPORT_INTEGRATION.md** | ✅ Aktualny | 2025-10-23 | 1.0.0 |
| test.http | ✅ Aktualny | 2025-10-23 | 1.1.0 |
| **test.local.http** | ✅ Aktualny | 2025-10-23 | 1.0.0 |
| **test.prod.http** | ✅ Aktualny | 2025-10-23 | 1.0.0 |
| **test_summaries.http** | ✅ Aktualny | 2025-10-28 | 1.0.0 |
| SecureDocCompare/README.md | ✅ Aktualny | 2025-10-20 | 1.0.0 |
| SecureDocCompare/QUICK_START.md | ✅ Aktualny | 2025-10-21 | 1.0.0 |
| SecureDocCompare/SECURITY.md | ✅ Aktualny | 2025-10-20 | 1.0.0 |
| UslugaDoPorownan/README.md | ✅ Aktualny | 2025-10-15 | 1.0.0 |
| requirements.txt | ✅ Aktualny | 2025-10-21 | Python 3.11-3.13 |
| .vscode/ (konfiguracja) | ✅ Aktualny | 2025-10-22 | 1.0.0 |
| **start_services.sh** | ✅ Aktualny | 2025-10-24 | 1.0.0 |
| **stop_services.sh** | ✅ Aktualny | 2025-10-24 | 1.0.0 |
| **status_services.sh** | ✅ Aktualny | 2025-10-24 | 1.0.0 |
| **UslugaDoPorownan/PROMPTS_CHANGELOG.md** | ✅ Aktualny | 2025-10-24 | 2.0.0 |
| **UslugaDoPorownan/prompt_system.txt** | ✅ Aktualny | 2025-10-24 | 2.0.0 |
| **UslugaDoPorownan/prompt_user.txt** | ✅ Aktualny | 2025-10-24 | 2.0.0 |

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

**Ostatnia aktualizacja:** 2025-10-28
**Wersja indeksu:** 1.7.0
**Projekt:** BAW - Porównywanie Dokumentów Bankowych

**Changelog 1.7.0 (2025-10-28):**
- Zaktualizowano **API_DOCUMENTATION.md** (wersja 1.2.0) - dodano 6 endpointów podsumowań
- Dodano **test_summaries.http** do tabeli plików głównego katalogu
- Zaktualizowano tabelę statusu dokumentacji (dodano test_summaries.http)
- Dodano informację o 16 endpointach API (10 podstawowych + 6 summary)
- Zaktualizowano datę ostatniej aktualizacji API_DOCUMENTATION.md na 2025-10-28

**Changelog 1.6.0 (2025-10-25):**
- Dodano **UslugaDoPorownan/PROMPTS_CHANGELOG.md** - kompletna dokumentacja aktualizacji promptów LLM v2.0 (~755 linii)
- Zaktualizowano **UslugaDoPorownan/prompt_system.txt** (+403 linie, +664%) - wersja 2.0.0
- Zaktualizowano **UslugaDoPorownan/prompt_user.txt** (+385 linii, +473%) - wersja 2.0.0
- Dodano nową ścieżkę nauki: "Chcę używać analizy LLM dla zmian w dokumentach"
- Rozszerzona tabela "Szukam informacji o..." - dodano 4 wpisy o promptach LLM i analizie ryzyka
- Zaktualizowana tabela statusu dokumentacji (dodano 3 pliki związane z LLM)
- Kluczowe funkcjonalności:
  - 5 zasad przeciw halucynacjom (90% redukcja ryzyka)
  - Kontekst polski bank + KNF
  - 5 obszarów ryzyka (kredytowe, operacyjne, finansowe, compliance, ESG)
  - 11 grup regulacji (DORA, AML, KYC, FATCA, CRS, RODO, MiFID II, Bazylea, KNF, Prawo Bankowe, PSD2)
  - Matryca zgodności regulacyjnej
  - Priorytetowe działania Top 5 z deadline
  - Rozszerzona analiza ryzyka (H/M/L)
  - 6-punktowa kontrola jakości

**Changelog 1.5.0 (2025-10-24):**
- Dodano **SCRIPTS_GUIDE.md** - kompletny przewodnik po skryptach zarządzania usługami (~800 linii)
- Utworzono 3 nowe skrypty: `start_services.sh`, `stop_services.sh`, `status_services.sh`
- Zaktualizowano **DEPLOYMENT.md** (wersja 1.2.0) - dodano sekcję "Opcja 1: Automatyczne Uruchomienie (ZALECANE) - Screen Mode"
- Zaktualizowano **PROGRESS_LOG.md** (wersja 1.4.0) - dodano sekcję o skryptach zarządzania usługami (2025-10-24)
- Rozszerzona sekcja "Chcę wdrożyć na serwer" - dodano krok 3 (skrypty zarządzania)
- Dodano nową sekcję "Zarządzanie Usługami (Screen Mode)" w częstych scenariuszach
- Rozszerzona tabela "Szukam informacji o..." - dodano 3 wpisy o zarządzaniu usługami
- Zaktualizowana tabela statusu dokumentacji (dodano 3 skrypty .sh)

**Changelog 1.4.0 (2025-10-23):**
- Dodano **N8N_HTML_REPORT_INTEGRATION.md** - przewodnik integracji raportów HTML w N8N workflow
- Zaktualizowano sekcję "Chcę zintegrować z N8N" - dodano krok 5 (generowanie raportów HTML)
- Zaktualizowana tabela statusu dokumentacji (23 pliki)

**Changelog 1.3.0 (2025-10-23):**
- Dodano **HTML_REPORT_ENDPOINT.md** - dokumentacja endpointu generowania raportów HTML
- Zaktualizowano **API_DOCUMENTATION.md** (wersja 1.1.0) - dodano endpoint 10: `/api/report/{process_id}/generate`
- Zaktualizowano **PROGRESS_LOG.md** (wersja 1.3.0) - dodano sekcję o endpointcie raportów HTML
- Dodano sekcję "Chcę generować raporty HTML" w ścieżkach nauki
- Rozszerzona tabela "Szukam informacji o..." (generowanie raportów HTML)
- Zaktualizowana tabela statusu dokumentacji (22 pliki)

**Changelog 1.2.0 (2025-10-23):**
- Dodano **API_DOCUMENTATION.md** - kompletna dokumentacja API (~900 linii, 9 endpointów)
- Dodano **N8N_INTEGRATION.md** - integracja z N8N workflow automation
- Dodano **N8N_WORKFLOW_GUIDE.md** - przewodnik workflow v2.0
- Dodano **N8N_MEMORY_ONLY_GUIDE.md** - przewodnik memory-only workflow v3.0
- Dodano **test.local.http** - testy API dla localhost
- Dodano **test.prod.http** - testy API dla produkcji (217.182.76.146)
- Zaktualizowano **DEPLOYMENT.md** - sekcja "Konfiguracja Firewall"
- Zaktualizowano **test.http** - URL produkcyjne (port 80)
- Dodano sekcję "Chcę zintegrować z N8N" w ścieżkach nauki
- Rozszerzona tabela "Szukam informacji o..." (Nginx, Firewall, N8N, Diagnostyka)
- Zaktualizowana tabela statusu dokumentacji (21 plików)

**Changelog 1.1.0 (2025-10-22):**
- Dodano VSCODE_SETUP.md - kompletna konfiguracja Visual Studio Code
- Dodano test.http - testy API dla REST Client
- Dodano .vscode/ - settings, launch, tasks, extensions, snippets
- Dodano .editorconfig - uniwersalne ustawienia edytora
- Zaktualizowano .gitignore - współdzielenie konfiguracji VSCode
