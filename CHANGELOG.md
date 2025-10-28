# Changelog - Projekt BAW

Wszystkie znaczące zmiany w projekcie są dokumentowane w tym pliku.

Format bazuje na [Keep a Changelog](https://keepachangelog.com/pl/1.0.0/),
i ten projekt stosuje [Semantic Versioning](https://semver.org/lang/pl/).

---

## [Unreleased]

### Planowane
- Integracja z bazą danych PostgreSQL/Redis (persistencja danych)
- System notyfikacji email
- Dashboard z metrykami i wykresami
- Export wyników do Excel/CSV
- WebSocket dla real-time updates statusu

---

## [2.0.0] - 2025-10-28

### 🎉 Major Release - Cleanup & Documentation v2.0

### Added
- **Kompletna dokumentacja API** dla UslugaDoPorownan (~2,750 linii)
  - `UslugaDoPorownan/API_DOCUMENTATION.md` (~1,500 linii)
  - `UslugaDoPorownan/API_README.md` (~550 linii - Quick Start)
  - `UslugaDoPorownan/API_TESTS.http` (~450 linii - 30+ testów HTTP)
- **Logging z milisekundami** w obu projektach
  - `UslugaDoPorownan/LOGGING_CHANGELOG.md` - dokumentacja zmian
  - Format: `YYYY-MM-DD HH:MM:SS.mmm`
- **Archiwum dokumentacji** - `docs_archive/2025-10-28_cleanup/`
- **CHANGELOG.md** - ten plik (historia wersji projektu)
- **CLEANUP_ANALYSIS.md** - raport analizy dokumentacji
- **PODSUMOWANIE_ZMIAN_2025-10-28.md** - szczegółowe podsumowanie

### Changed
- **DOCS_INDEX.md** zaktualizowany do v2.0
  - Nowa struktura z kategoriami
  - Przewodniki Quick Start dla różnych ról
  - Statystyki dokumentacji
  - Historia wersji
- **Logging format** w `main.py` (obu projektach)
  - Dodano precyzyjne timestampy z milisekundami
  - Format: `%(asctime)s.%(msecs)03d`

### Removed (Archived)
- Przeniesiono 19 plików do `docs_archive/2025-10-28_cleanup/`:
  - Stare dokumenty sesji (3 pliki)
  - Tymczasowe raporty audytu (2 pliki)
  - Diagnostyczne/tymczasowe (5 plików)
  - Stare wersje N8N (8 plików)
  - Duplikaty (1 plik)

### Fixed
- Uporządkowano duplikaty dokumentacji N8N
- Usunięto nieaktualne dokumenty sesyjne
- Uspójniono wersje we wszystkich głównych dokumentach

### Documentation
- Redukcja z 65 do ~35 aktywnych plików dokumentacji (~62% redukcja)
- Łączna dokumentacja: ~13,300 linii w 35 plikach
- Wszystkie dokumenty zaktualizowane do wersji 2.0

---

## [1.1.0] - 2025-10-25

### Added
- **Prompty LLM v2.0** - eliminacja halucynacji, pełna analiza ryzyka
  - `prompt_system.txt` - zaktualizowany prompt systemowy
  - `prompt_user.txt` - zaktualizowany prompt użytkownika
  - `PROMPTS_CHANGELOG.md` - dokumentacja zmian (~755 linii)
- **Optymalizacje wydajności** - 86% redukcja czasu przetwarzania
  - Cache dla diff results
  - Fast similarity pre-screen
  - Dynamiczny search range
  - Normalizacja white-space

### Changed
- **PROGRESS_LOG.md** zaktualizowany do v1.1.0
- **DOCS_INDEX.md** zaktualizowany do v1.1.0
- Ulepszone prompty LLM dla lepszej analizy compliance

---

## [1.0.0] - 2025-10-24

### 🎉 First Stable Release - Production Ready

### Added
- **Skrypty zarządzania usługami**
  - `start_services.sh` - uruchomienie w screen sessions
  - `stop_services.sh` - zatrzymanie usług
  - `status_services.sh` - status i health check
  - `SCRIPTS_GUIDE.md` - dokumentacja skryptów
- **Deployment documentation**
  - `DEPLOYMENT.md` - kompletny przewodnik wdrożenia
  - Nginx reverse proxy setup
  - Systemd service configuration
  - Firewall rules (UFW)
- **N8N Integration - HTML Reports**
  - `N8N_HTML_REPORT_INTEGRATION.md`
  - Automatyczne generowanie raportów HTML w workflow

### Changed
- Nginx konfiguracja dla reverse proxy
- Systemd units dla automatycznego startu

---

## [0.9.0] - 2025-10-23

### Added
- **N8N Workflows v3.0** - Memory-only variant
  - `N8N_MEMORY_ONLY_GUIDE.md`
  - Workflow bez persystencji (szybszy, prostszy)
- **N8N Enhanced Workflow**
  - `N8N_WORKFLOW_ENHANCED.md`
  - Rozszerzone funkcjonalności i error handling
- **Diagnostic Tools**
  - `check_api.sh` - diagnostyka API (firewall, porty, nginx)
  - `fix_firewall.sh` - automatyczna naprawa firewalla
  - `setup_nginx_proxy.sh` - instalacja nginx
  - `DEPENDENCY_ANALYSIS_REPORT.md`
  - `REQUIREMENTS_VERIFICATION_REPORT.md`

### Changed
- **N8N Integration** - ulepszona dokumentacja
  - `N8N_INTEGRATION.md` zaktualizowany
  - `N8N_WORKFLOW_GUIDE.md` - nowa wersja

---

## [0.8.0] - 2025-10-22

### Added
- **VS Code Configuration** - pełna konfiguracja workspace
  - `.vscode/settings.json` - workspace settings
  - `.vscode/launch.json` - debug configurations (Full Stack F5)
  - `.vscode/tasks.json` - 11 tasków (Run, Test, Format, Lint, Clean)
  - `.vscode/extensions.json` - ~20 rekomendowanych rozszerzeń
  - `.vscode/python.code-snippets` - 15 snippetów FastAPI/Pydantic
  - `VSCODE_SETUP.md` - dokumentacja (~600+ linii)
- **Development Tools**
  - `requirements-dev.txt` - narzędzia deweloperskie (Black, Flake8, pytest)
  - `.editorconfig` - uniwersalna konfiguracja edytora
  - `test.http` - testy REST Client dla VS Code

### Changed
- Uspójniono formatowanie kodu (Black)
- Dodano linting (Flake8)

---

## [0.7.0] - 2025-10-21

### Added
- **PDF Conversion** - automatyczna konwersja PDF→DOCX
  - Dwupoziomowy system (pdf2docx + pdfplumber fallback)
  - `pdf_converter/` - moduł konwersji
  - `PDF_CONVERSION_SUMMARY.md` - dokumentacja
- Upload endpoint obsługuje teraz DOCX i PDF

### Changed
- `POST /api/documents/upload` - rozszerzone o obsługę PDF
- Automatyczna konwersja przy uploading

---

## [0.6.0] - 2025-10-20

### Added
- **N8N Integration** - pierwsza wersja
  - `N8N_INTEGRATION.md` - podstawowa integracja
  - Webhook triggers
  - Automated workflows
- **API Testing**
  - `test.local.http` - testy dla localhost
  - `test.prod.http` - testy dla produkcji
  - `test_summaries.http` - testy podsumowań

---

## [0.5.0] - 2025-10-15

### Added
- **SecureDocCompare** - bezpieczny frontend
  - System logowania (hasło + sesje)
  - 5 warstw zabezpieczeń
  - `SecureDocCompare/README.md`
  - `SecureDocCompare/QUICK_START.md`
  - `SecureDocCompare/SECURITY.md`
- **Middleware zabezpieczający**
  - SecurityHeadersMiddleware
  - RateLimitMiddleware
  - FileValidationMiddleware

### Security
- Implementacja autentykacji i sesji
- Rate limiting (max 100 req/min)
- Walidacja plików (typ, rozmiar, zawartość)
- Secure headers (CSP, HSTS, etc.)
- Path traversal protection

---

## [0.4.0] - 2025-10-10

### Added
- **UslugaDoPorownan** - Backend API
  - REST API dla porównywania dokumentów
  - 9 głównych endpointów
  - Asynchroniczne przetwarzanie
  - In-memory storage
- **Core modules**
  - `extractor.py` - ekstrakcja z DOCX
  - `comparator.py` - algorytm diff
  - `storage.py` - zarządzanie danymi
  - `models.py` - modele Pydantic

### Changed
- Architektura: monorepo → multi-service (Frontend + Backend)

---

## [0.3.0] - 2025-10-05

### Added
- **Comparison Algorithm** - diff na poziomie słów i znaków
  - Wykorzystanie `diff_match_patch`
  - Wykrywanie zmian: added, deleted, modified, unchanged
  - Porównywanie tabel
  - Statystyki zmian

---

## [0.2.0] - 2025-10-01

### Added
- **Document Extraction** - ekstrakcja z DOCX
  - Wykorzystanie `docx2python` i `python-docx`
  - Ekstrakcja paragrafów, tabel, metadanych
  - Strukturyzacja treści

---

## [0.1.0] - 2025-09-25

### Added
- **Projekt BAW** - inicjalizacja
  - Podstawowa struktura projektu
  - README.md z założeniami
  - Konfiguracja środowiska Python

---

## Typy Zmian

- `Added` - nowe funkcjonalności
- `Changed` - zmiany w istniejących funkcjonalnościach
- `Deprecated` - funkcjonalności wycofywane w przyszłości
- `Removed` - usunięte funkcjonalności
- `Fixed` - poprawki bugów
- `Security` - zmiany związane z bezpieczeństwem
- `Documentation` - zmiany w dokumentacji

---

## Wersjonowanie

Projekt stosuje [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0) - Zmiany niekompatybilne wstecz (breaking changes)
- **MINOR** (0.X.0) - Nowe funkcjonalności kompatybilne wstecz
- **PATCH** (0.0.X) - Poprawki bugów kompatybilne wstecz

---

## Linki

- [PROGRESS_LOG.md](PROGRESS_LOG.md) - Szczegółowa historia postępu
- [DOCS_INDEX.md](DOCS_INDEX.md) - Indeks dokumentacji
- [README.md](README.md) - Główny README projektu

---

**Ostatnia aktualizacja:** 2025-10-28
**Następna planowana wersja:** 2.1.0 (Q4 2025)
