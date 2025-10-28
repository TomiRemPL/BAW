# Archiwum Dokumentacji i Plików - Cleanup 2025-10-28

## Powód Archiwizacji

Te pliki zostały przeniesione do archiwum podczas kompleksowego przeglądu i czyszczenia projektu BAW w dniu 2025-10-28.

**Łącznie zarchiwizowano:** ~57 plików

---

## 📁 Struktura Archiwum

```
docs_archive/2025-10-28_cleanup/
├── README.md (ten plik)
│
├── [19 plików] - Dokumenty Markdown
├── result_viewer.html
│
├── n8n_workflows/ (9 plików JSON)
├── temp_scripts/ (7 plików .py)
├── import_instructions/ (4 plików .txt)
├── test_results/ (4 plików .json)
├── old_python/ (4 pliki .py)
└── windows_scripts/ (6 plików .bat/.ps1)
```

---

## 📋 Kategorie Zarchiwizowanych Plików

### 1. Dokumenty Markdown (19 plików)

**Stare Dokumenty Sesji:**
- `SESSION_SUMMARY.md` - Zastąpiony przez PROGRESS_LOG.md
- `SESSION_SUMMARY_2025-10-27.md` - Zastąpiony przez PROGRESS_LOG.md
- `DOCUMENTATION_UPDATE_2025-10-28.md` - Skonsolidowany w PODSUMOWANIE_ZMIAN

**Tymczasowe Raporty Audytu:**
- `AUDIT_REPORT_2025-10-28.md` - Jednorazowy raport audytu
- `AUDIT_SUMMARY_2025-10-28.md` - Jednorazowe podsumowanie

**Diagnostyczne/Tymczasowe:**
- `DEPENDENCY_ANALYSIS_REPORT.md` - Jednorazowy raport zależności
- `REQUIREMENTS_VERIFICATION_REPORT.md` - Jednorazowy raport weryfikacji
- `FIX_UV_PRODUCTION.md` - Instrukcja naprawy (jednorazowa)
- `WINDOWS_SCRIPTS.md` - Duplikat SCRIPTS_GUIDE
- `WINDOWS_SCRIPTS_SUMMARY.md` - Duplikat SCRIPTS_GUIDE

**Stare Wersje N8N:**
- `N8N_WORKFLOW_GUIDE.md` - Zastąpiony przez N8N_WORKFLOW_QUICKSTART.md
- `N8N_WORKFLOW_ENHANCED.md` - Duplikat funkcjonalności
- `N8N_MEMORY_ONLY_GUIDE.md` - Stara wersja
- `IMPORT_N8N_1.111.0.md` - Tymczasowy import workflow
- `IMPORT_FINAL_N8N_1.111.0.md` - Tymczasowy import workflow
- `README_IMPORT.md` - Tymczasowy import instructions
- `WORKFLOW_VERSIONS.md` - Lista wersji (skonsolidowana)
- `WORKFLOW_MODIFICATION_SUMMARY.md` - Podsumowanie (skonsolidowane)

**Duplikaty:**
- `HTML_REPORT_ENDPOINT.md` - Informacje zawarte w API_DOCUMENTATION.md

---

### 2. N8N Workflow JSON (9 plików, ~600 KB)

**Katalog:** `n8n_workflows/`

Tymczasowe wersje robocze workflow N8N:
- `API 04 Enhanced - N8N 1.111.0.json` (91K)
- `API 04 Enhanced Fixed.json` (92K)
- `API 04 Enhanced v2.json` (91K)
- `API 04 Enhanced.json` (92K)
- `API 04 FINAL - N8N 1.111.0.json` (73K) - finalna wersja
- `API 04 Minimal Clean.json` (58K)
- `API 04 Ultra Minimal.json` (69K)
- `API 04.json` (61K)
- `API 04.json.backup` (61K)

**Powód:** Wiele wersji roboczych tego samego workflow. Finalna wersja powinna być w katalogu `n8n/workflows/` w głównym projekcie.

---

### 3. Skrypty Python Tymczasowe (7 plików, ~82 KB)

**Katalog:** `temp_scripts/`

Jednorazowe skrypty do naprawy i modyfikacji workflow N8N:
- `add_nodes_to_clean.py` (13K)
- `enhance_workflow.py` (36K)
- `fix_workflow.py` (2.8K)
- `fix_workflow_final.py` (13K)
- `fix_workflow_minimal.py` (4.7K)
- `fix_workflow_n8n_1_111.py` (9.1K)
- `fix_workflow_v2.py` (5.8K)

**Powód:** Skrypty naprawcze, już wykonane i nieużywane.

---

### 4. Instrukcje Importu (4 pliki, ~22 KB)

**Katalog:** `import_instructions/`

Tymczasowe instrukcje importu workflow do N8N:
- `IMPORT_FIXED.txt` (5.1K)
- `IMPORT_INSTRUCTIONS.txt` (7.9K)
- `IMPORT_ULTRA_MINIMAL.txt` (6.4K)
- `IMPORT_V2.txt` (2.8K)

**Powód:** Instrukcje już wykonane, workflow zaimportowane.

---

### 5. Wyniki Testów JSON (4 pliki, ~28 KB)

**Katalog:** `test_results/`

Przykładowe wyniki testów API:
- `added.json` (192B) - Przykład dodanych paragrafów
- `deleted.json` (194B) - Przykład usuniętych paragrafów
- `modified.json` (8.7K) - Przykład zmodyfikowanych paragrafów
- `full_result.json` (19K) - Przykład pełnego wyniku

**Powód:** Stare wyniki testów, przykładowe dane. Aktualne testy w `test.http`.

---

### 6. Stare Pliki Python (4 pliki, ~25 KB)

**Katalog:** `old_python/`

Stare wersje plików Python z głównego katalogu:
- `main.py` (16K) - Stary główny plik (aktualny w `SecureDocCompare/main.py` i `UslugaDoPorownan/main.py`)
- `config.py` (1.2K) - Stara konfiguracja
- `exceptions.py` (1.2K) - Stare wyjątki
- `check_imports.py` (6.9K) - Skrypt diagnostyczny

**Powód:** Stare wersje, zastąpione przez nowsze implementacje w odpowiednich katalogach.

---

### 7. Skrypty Windows (6 plików, ~18 KB)

**Katalog:** `windows_scripts/`

Skrypty zarządzania usługami dla Windows:
- `check_services.bat` (2.7K)
- `check_services.ps1` (6.5K)
- `start_services.bat`
- `start_services.ps1`
- `stop_services.bat`
- `stop_services.ps1`

**Powód:** Duplikaty funkcjonalności skryptów `.sh` lub nieużywane w środowisku Linux produkcyjnym.

**Uwaga:** Jeśli potrzebujesz skryptów Windows, można je przywrócić lub stworzyć dedykowany katalog `scripts/windows/`.

---

### 8. Inne Pliki (1 plik)

**Katalog główny archiwum:**
- `result_viewer.html` - Stary viewer HTML (jeśli jest nowsza wersja w projekcie)

---

## 📊 Statystyki Archiwum

| Kategoria | Liczba Plików | Łączny Rozmiar |
|-----------|---------------|----------------|
| Dokumenty MD | 19 | ~500 KB |
| N8N Workflow JSON | 9 | ~600 KB |
| Skrypty Python | 7 | ~82 KB |
| Import instructions | 4 | ~22 KB |
| Test results JSON | 4 | ~28 KB |
| Stare Python files | 4 | ~25 KB |
| Windows scripts | 6 | ~18 KB |
| Inne | 1 | ~10 KB |
| **RAZEM** | **~54** | **~1.3 MB** |

---

## 🔄 Restore - Jak Przywrócić Pliki

### Przywrócenie pojedynczego pliku

```bash
# Przykład: przywrócenie workflow
cp docs_archive/2025-10-28_cleanup/n8n_workflows/"API 04 FINAL - N8N 1.111.0.json" n8n/workflows/

# Przykład: przywrócenie dokumentu
cp docs_archive/2025-10-28_cleanup/N8N_WORKFLOW_GUIDE.md .
```

### Przywrócenie całej kategorii

```bash
# Przykład: wszystkie workflow
cp docs_archive/2025-10-28_cleanup/n8n_workflows/*.json n8n/workflows/

# Przykład: wszystkie skrypty Windows
cp docs_archive/2025-10-28_cleanup/windows_scripts/* scripts/windows/
```

---

## 🗑️ Bezpieczne Usuwanie Archiwum

**Tylko jeśli masz 100% pewność, że pliki nie są potrzebne:**

```bash
# OSTROŻNIE - usuwa całe archiwum
rm -rf docs_archive/2025-10-28_cleanup/
```

**Zalecenie:** Zachowaj archiwum przez co najmniej 3 miesiące przed usunięciem.

---

## 📍 Gdzie Znaleźć Aktualne Wersje

### Dokumentacja

- **Indeks:** `DOCS_INDEX.md` (v2.0)
- **Changelog:** `CHANGELOG.md`
- **API Docs:** `API_COMPLETE_REFERENCE.md`, `API_DOCUMENTATION.md`
- **N8N:** `N8N_WORKFLOW_QUICKSTART.md`, `N8N_SUMMARY_INTEGRATION.md`

### Workflow N8N

- **Finalne workflow:** `n8n/workflows/` (jeśli katalog istnieje)
- **Instrukcje:** `N8N_WORKFLOW_QUICKSTART.md`

### Skrypty

- **Linux:** `*.sh` w głównym katalogu
- **Python:** W odpowiednich katalogach (`UslugaDoPorownan/`, `SecureDocCompare/`)

---

## 📝 Notatki

### Data archiwizacji
2025-10-28

### Wykonane przez
Claude Code - Comprehensive Documentation Cleanup v2.0

### Wersja projektu
2.0.0

### Następny przegląd
Zalecany za 3 miesiące (2026-01-28)

---

**Status:** ✅ Archiwum kompletne i udokumentowane
**Bezpieczeństwo:** Wszystkie pliki zachowane, możliwość restore w każdej chwili
