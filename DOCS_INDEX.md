# 📚 Indeks Dokumentacji - Projekt BAW

**Wersja:** 2.0
**Ostatnia aktualizacja:** 2025-10-28
**Status:** ✅ Zaktualizowany i Uspójniony

---

## 🎯 Start Tutaj!

| Dokument | Opis | Czas |
|----------|------|------|
| **[README.md](README.md)** | Główny przegląd projektu, architektura, quick start | 10 min |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Wdrożenie produkcyjne (Debian, pyenv, nginx, systemd) | 30 min |
| **[TESTING_GUIDE.md](TESTING_GUIDE.md)** | Kompletny przewodnik testowania API | 15 min |

---

## 📖 Główna Dokumentacja

### Projekt BAW - Root Directory

| Dokument | Wersja | Opis | Dla Kogo |
|----------|--------|------|----------|
| [README.md](README.md) | aktualna | Główny opis projektu, komponenty, architektura | Wszyscy |
| [CLAUDE.md](CLAUDE.md) | 2025-10-28 | Instrukcje dla Claude Code AI | Deweloperzy |
| [DEPLOYMENT.md](DEPLOYMENT.md) | 2025-10-24 | Wdrożenie produkcyjne z nginx i systemd | DevOps, Admini |
| [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) | 2025-10-24 | Przewodnik po skryptach zarządzania (start/stop/status) | DevOps, Admin |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | 2025-10-28 | Kompletny przewodnik testowania API | QA, Deweloperzy |
| [VSCODE_SETUP.md](VSCODE_SETUP.md) | 2025-10-22 | Konfiguracja VS Code, debugowanie, tasks, snippets | Deweloperzy |
| [PROGRESS_LOG.md](PROGRESS_LOG.md) | v2.0 | Historia postępu prac i changelog projektu | Wszyscy |
| [PODSUMOWANIE_ZMIAN_2025-10-28.md](PODSUMOWANIE_ZMIAN_2025-10-28.md) | v1.0 | Podsumowanie zmian z dnia 2025-10-28 (API docs + logging) | Wszyscy |
| [PDF_CONVERSION_SUMMARY.md](PDF_CONVERSION_SUMMARY.md) | 2025-10-21 | Implementacja konwersji PDF→DOCX | Deweloperzy |
| [CHANGELOG.md](CHANGELOG.md) | **NOWY** | Historia zmian projektu (wersjonowanie) | Wszyscy |

---

## 🔌 API Documentation

### Kompletna Dokumentacja API

| Dokument | Wersja | Linie | Opis |
|----------|--------|-------|------|
| **[API_COMPLETE_REFERENCE.md](API_COMPLETE_REFERENCE.md)** | 2025-10-28 | ~1,000 | Pełna referencyjna dokumentacja wszystkich endpointów |
| **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** | 2025-10-28 | ~900 | Dokumentacja techniczna API z przykładami |

### Interaktywna Dokumentacja API

- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc
- **OpenAPI Schema:** http://localhost:8001/openapi.json

### Testy HTTP

| Plik | Środowisko | Opis |
|------|------------|------|
| [test.local.http](test.local.http) | Localhost | Testy dla środowiska lokalnego (port 8001) |
| [test.prod.http](test.prod.http) | Produkcja | Testy dla serwera produkcyjnego (217.182.76.146) |
| [test_summaries.http](test_summaries.http) | Localhost/Prod | Testy endpointów podsumowań (integracja n8n) |
| [test_complete_api.http](test_complete_api.http) | **NOWY** | Kompleksowe testy wszystkich endpointów |

---

## 🤖 Integracja n8n

### Główne Dokumenty

| Dokument | Wersja | Opis | Use Case |
|----------|--------|------|----------|
| **[N8N_WORKFLOW_QUICKSTART.md](N8N_WORKFLOW_QUICKSTART.md)** | 2025-10-28 | **START TUTAJ!** Quick start z n8n | Podstawowa integracja |
| **[N8N_INTEGRATION.md](N8N_INTEGRATION.md)** | 2025-10-23 | Szczegółowa dokumentacja integracji | Zaawansowana konfiguracja |
| **[N8N_SUMMARY_INTEGRATION.md](N8N_SUMMARY_INTEGRATION.md)** | 2025-10-27 | Integracja systemu podsumowań z LLM | Automatyczne podsumowania |
| **[N8N_HTML_REPORT_INTEGRATION.md](N8N_HTML_REPORT_INTEGRATION.md)** | 2025-10-24 | Generowanie raportów HTML przez n8n | Raporty w workflow |
| **[N8N_WORKFLOW_VERIFICATION.md](N8N_WORKFLOW_VERIFICATION.md)** | 2025-10-28 | Weryfikacja i testowanie workflow | Debugging, QA |

### Workflow Files

- Eksportowane workflow: `n8n/workflows/*.json`
- Credentials template: `n8n/credentials.example.json`

---

## 🏢 SecureDocCompare - Frontend

**Lokalizacja:** `SecureDocCompare/`
**Port:** 8000
**Opis:** Bezpieczny frontend z systemem logowania

| Dokument | Opis |
|----------|------|
| [SecureDocCompare/README.md](SecureDocCompare/README.md) | Główna dokumentacja frontendu - funkcje, konfiguracja, API |
| [SecureDocCompare/QUICK_START.md](SecureDocCompare/QUICK_START.md) | Szybki start - Windows i Linux, krok po kroku |
| [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) | Dokumentacja zabezpieczeń - 5 warstw ochrony, testy |

### Konfiguracja

- `.env.example` - Przykładowa konfiguracja środowiskowa
- `config.py` - Konfiguracja aplikacji
- `auth.py` - System autentykacji i sesji
- `middleware.py` - Middleware zabezpieczający

---

## ⚙️ UslugaDoPorownan - Backend API

**Lokalizacja:** `UslugaDoPorownan/`
**Port:** 8001
**Opis:** REST API do porównywania dokumentów DOCX/PDF

### Główna Dokumentacja

| Dokument | Linie | Opis | Dla Kogo |
|----------|-------|------|----------|
| **[UslugaDoPorownan/API_DOCUMENTATION.md](UslugaDoPorownan/API_DOCUMENTATION.md)** | ~1,500 | **NOWA!** Kompletna dokumentacja API | Wszyscy deweloperzy |
| **[UslugaDoPorownan/API_README.md](UslugaDoPorownan/API_README.md)** | ~550 | **NOWY!** Quick Start i przykłady (Python, JS, Bash) | Początkujący |
| **[UslugaDoPorownan/API_TESTS.http](UslugaDoPorownan/API_TESTS.http)** | ~450 | **NOWY!** Gotowe testy HTTP (30+ scenariuszy) | QA, Deweloperzy |
| [UslugaDoPorownan/README.md](UslugaDoPorownan/README.md) | - | Dokumentacja backendu - endpointy, architektura | Deweloperzy |
| [UslugaDoPorownan/QUICKSTART.md](UslugaDoPorownan/QUICKSTART.md) | - | Szybki start backendu API | Początkujący |

### Dokumentacja Techniczna

| Dokument | Data | Opis |
|----------|------|------|
| **[UslugaDoPorownan/LOGGING_CHANGELOG.md](UslugaDoPorownan/LOGGING_CHANGELOG.md)** | **NOWY** 2025-10-28 | Changelog zmian w loggingu (milisekundy) |
| [UslugaDoPorownan/PROMPTS_CHANGELOG.md](UslugaDoPorownan/PROMPTS_CHANGELOG.md) | 2025-10-25 | Changelog promptów LLM v2.0 (~755 linii) |
| [UslugaDoPorownan/PROJECT_SUMMARY.md](UslugaDoPorownan/PROJECT_SUMMARY.md) | - | Podsumowanie projektu backendu |

### Moduły Specjalizowane

| Dokument | Opis |
|----------|------|
| [UslugaDoPorownan/pdf_converter/README.md](UslugaDoPorownan/pdf_converter/README.md) | Dokumentacja modułu konwersji PDF→DOCX |

### Optimizacja i Performance

| Dokument | Opis |
|----------|------|
| [UslugaDoPorownan/OPTIMIZATION_GUIDE.md](UslugaDoPorownan/OPTIMIZATION_GUIDE.md) | Przewodnik optymalizacji wydajności |
| [UslugaDoPorownan/BENCHMARK_RESULTS.md](UslugaDoPorownan/BENCHMARK_RESULTS.md) | Wyniki benchmarków przed/po optymalizacji |

---

## 🔧 Narzędzia i Skrypty

### Skrypty Zarządzania Usługami

| Skrypt | Opis |
|--------|------|
| `start_services.sh` | Uruchomienie obu usług w screen sessions |
| `stop_services.sh` | Zatrzymanie usług |
| `status_services.sh` | Status i health check |
| `check_api.sh` | Diagnostyka API (firewall, porty, nginx) |

Dokumentacja: [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md)

### Narzędzia Diagnostyczne

| Skrypt | Opis |
|--------|------|
| `fix_firewall.sh` | Automatyczna naprawa firewalla |
| `setup_nginx_proxy.sh` | Instalacja i konfiguracja nginx |

---

## 📁 Struktura Projektu

```
BAW/
├── README.md                           # Główny README
├── DOCS_INDEX.md                       # ← TEN PLIK (v2.0)
├── CHANGELOG.md                        # Historia zmian (NOWY)
├── DEPLOYMENT.md                       # Wdrożenie produkcyjne
├── TESTING_GUIDE.md                    # Przewodnik testowania
│
├── API_COMPLETE_REFERENCE.md           # Pełna referencja API
├── API_DOCUMENTATION.md                # Dokumentacja API
│
├── N8N_WORKFLOW_QUICKSTART.md          # n8n Quick Start
├── N8N_INTEGRATION.md                  # n8n - szczegółowa integracja
├── N8N_SUMMARY_INTEGRATION.md          # n8n - podsumowania LLM
├── N8N_HTML_REPORT_INTEGRATION.md      # n8n - raporty HTML
├── N8N_WORKFLOW_VERIFICATION.md        # n8n - weryfikacja
│
├── SecureDocCompare/                   # Frontend (port 8000)
│   ├── README.md
│   ├── QUICK_START.md
│   └── SECURITY.md
│
├── UslugaDoPorownan/                   # Backend API (port 8001)
│   ├── README.md
│   ├── API_DOCUMENTATION.md            # NOWA (1,500 linii)
│   ├── API_README.md                   # NOWY (Quick Start)
│   ├── API_TESTS.http                  # NOWY (30+ testów)
│   ├── LOGGING_CHANGELOG.md            # NOWY
│   ├── PROMPTS_CHANGELOG.md
│   └── pdf_converter/README.md
│
├── docs_archive/                       # Archiwum starych dokumentów
│   └── 2025-10-28_cleanup/             # Cleanup z dnia 2025-10-28
│       └── README.md                   # Indeks zarchiwizowanych plików
│
├── test.local.http                     # Testy HTTP - localhost
├── test.prod.http                      # Testy HTTP - produkcja
├── test_summaries.http                 # Testy HTTP - podsumowania
│
└── *.sh                                # Skrypty zarządzania
```

---

## 🗂️ Archiwum Dokumentacji

Stare i zduplikowane dokumenty zostały przeniesione do:

**Lokalizacja:** `docs_archive/2025-10-28_cleanup/`

**Zawartość:** 19 plików (sesje, audyty, stare wersje N8N, duplikaty)

**Szczegóły:** Zobacz [docs_archive/2025-10-28_cleanup/README.md](docs_archive/2025-10-28_cleanup/README.md)

---

## 🎯 Przewodnik Szybki Start

### Dla Nowych Deweloperów

1. **Czytaj:** [README.md](README.md) (10 min)
2. **Instalacja:** [DEPLOYMENT.md](DEPLOYMENT.md) sekcja "Lokalne Środowisko" (15 min)
3. **API:** [UslugaDoPorownan/API_README.md](UslugaDoPorownan/API_README.md) (15 min)
4. **Testowanie:** [TESTING_GUIDE.md](TESTING_GUIDE.md) (10 min)
5. **VS Code:** [VSCODE_SETUP.md](VSCODE_SETUP.md) (10 min)

**Łączny czas:** ~60 minut

### Dla DevOps/Admin

1. **Wdrożenie:** [DEPLOYMENT.md](DEPLOYMENT.md) (30 min)
2. **Skrypty:** [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) (15 min)
3. **Bezpieczeństwo:** [SecureDocCompare/SECURITY.md](SecureDocCompare/SECURITY.md) (15 min)
4. **n8n:** [N8N_WORKFLOW_QUICKSTART.md](N8N_WORKFLOW_QUICKSTART.md) (20 min)

**Łączny czas:** ~80 minut

### Dla Integratorów API

1. **API Quick Start:** [UslugaDoPorownan/API_README.md](UslugaDoPorownan/API_README.md) (15 min)
2. **Pełna Dokumentacja:** [API_COMPLETE_REFERENCE.md](API_COMPLETE_REFERENCE.md) (30 min)
3. **Testy HTTP:** [UslugaDoPorownan/API_TESTS.http](UslugaDoPorownan/API_TESTS.http) (10 min)
4. **n8n Integration:** [N8N_SUMMARY_INTEGRATION.md](N8N_SUMMARY_INTEGRATION.md) (20 min)

**Łączny czas:** ~75 minut

---

## 📊 Statystyki Dokumentacji

| Kategoria | Liczba Plików | Łączne Linie |
|-----------|---------------|--------------|
| **Główne dokumenty** | 10 | ~2,500 |
| **API Documentation** | 5 | ~4,000 |
| **n8n Integration** | 5 | ~1,500 |
| **SecureDocCompare** | 3 | ~800 |
| **UslugaDoPorownan** | 8 | ~3,500 |
| **Testy HTTP** | 4 | ~1,000 |
| **RAZEM** | **35** | **~13,300** |

---

## 🔄 Historia Wersji

| Wersja | Data | Zmiany |
|--------|------|--------|
| **2.0** | 2025-10-28 | Cleanup dokumentacji, archiwizacja duplikatów, nowe API docs, uspójnienie wersji |
| 1.1.0 | 2025-10-25 | Dodano prompty LLM v2.0, optymalizacje |
| 1.0.0 | 2025-10-24 | Pierwsza stabilna wersja z pełną dokumentacją |

---

## 🆘 Wsparcie

### Pytania o Dokumentację

1. Sprawdź ten indeks (DOCS_INDEX.md)
2. Zobacz [README.md](README.md) - sekcja FAQ
3. Przejrzyj [CHANGELOG.md](CHANGELOG.md) - historia zmian

### Znalazłeś błąd w dokumentacji?

1. Sprawdź [PROGRESS_LOG.md](PROGRESS_LOG.md) - czy nie jest to znany issue
2. Utwórz issue lub zaktualizuj dokumentację
3. Prześlij PR z poprawką

### Brakuje dokumentacji?

1. Sprawdź `docs_archive/` - może dokument został zarchiwizowany
2. Zobacz [CHANGELOG.md](CHANGELOG.md) - historia usunięć
3. Utwórz issue z prośbą o dokumentację

---

**Wersja indeksu:** 2.0
**Ostatnia aktualizacja:** 2025-10-28
**Status:** ✅ Aktualny i Kompletny
**Następna rewizja:** Według potrzeby lub po znaczących zmianach w projekcie
