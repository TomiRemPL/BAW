# Analiza Plików do Archiwizacji - Katalog Główny BAW

**Data:** 2025-10-28

## 📋 Kategorie Plików do Archiwizacji

### 1. ❌ Workflow JSON N8N (11 plików) - ARCHIWIZUJ
**Powód:** Tymczasowe pliki workflow, wersje robocze

- `API 04 Enhanced - N8N 1.111.0.json` (91K)
- `API 04 Enhanced Fixed.json` (92K)
- `API 04 Enhanced v2.json` (91K)
- `API 04 Enhanced.json` (92K)
- `API 04 FINAL - N8N 1.111.0.json` (73K) - finalna wersja, można zachować w n8n/
- `API 04 Minimal Clean.json` (58K)
- `API 04 Ultra Minimal.json` (69K)
- `API 04.json` (61K)
- `API 04.json.backup` (61K)

**Akcja:** Przenieś do `docs_archive/2025-10-28_cleanup/n8n_workflows/`

### 2. ❌ Skrypty Python do Fixowania Workflow (7 plików) - ARCHIWIZUJ
**Powód:** Jednorazowe skrypty naprawcze, już wykonane

- `add_nodes_to_clean.py` (13K)
- `enhance_workflow.py` (36K)
- `fix_workflow.py` (2.8K)
- `fix_workflow_final.py` (13K)
- `fix_workflow_minimal.py` (4.7K)
- `fix_workflow_n8n_1_111.py` (9.1K)
- `fix_workflow_v2.py` (5.8K)

**Akcja:** Przenieś do `docs_archive/2025-10-28_cleanup/temp_scripts/`

### 3. ❌ Pliki Import/Instrukcje (4 pliki) - ARCHIWIZUJ
**Powód:** Tymczasowe instrukcje importu, już wykonane

- `IMPORT_FIXED.txt` (5.1K)
- `IMPORT_INSTRUCTIONS.txt` (7.9K)
- `IMPORT_ULTRA_MINIMAL.txt` (6.4K)
- `IMPORT_V2.txt` (2.8K)

**Akcja:** Przenieś do `docs_archive/2025-10-28_cleanup/import_instructions/`

### 4. ❌ Pliki JSON Testowe (4 pliki) - ARCHIWIZUJ
**Powód:** Stare wyniki testów, przykładowe dane

- `added.json` (192B)
- `deleted.json` (194B)
- `modified.json` (8.7K)
- `full_result.json` (19K)

**Akcja:** Przenieś do `docs_archive/2025-10-28_cleanup/test_results/`

### 5. ❌ Stare Pliki Python (3 pliki) - ARCHIWIZUJ
**Powód:** Stare wersje, już nieużywane w głównym katalogu

- `main.py` (16K) - stary główny plik
- `config.py` (1.2K) - stara konfiguracja
- `exceptions.py` (1.2K) - stare wyjątki
- `check_imports.py` (6.9K) - skrypt diagnostyczny

**Akcja:** Przenieś do `docs_archive/2025-10-28_cleanup/old_python/`

### 6. ❌ Skrypty Windows (4 pliki) - ARCHIWIZUJ lub PRZENIEŚ
**Powód:** Duplikaty skryptów .sh lub nieużywane

- `check_services.bat` (2.7K)
- `check_services.ps1` (6.5K)
- `start_services.bat`
- `start_services.ps1`
- `stop_services.bat`
- `stop_services.ps1`

**Akcja:** Przenieś do `scripts/windows/` (lub archiwizuj jeśli nieużywane)

### 7. ❌ Plik Tymczasowy (1 plik) - USUŃ
**Powód:** Plik systemowy

- `nul` (3.7K) - tymczasowy plik systemowy Windows

**Akcja:** USUŃ

### 8. ❌ Stary Viewer HTML (1 plik) - ARCHIWIZUJ
**Powód:** Stara wersja viewera

- `result_viewer.html` - stary viewer (jeśli jest nowsza wersja)

**Akcja:** Sprawdź czy jest używany, jeśli nie - archiwizuj

---

## ✅ Pliki do ZACHOWANIA

### Konfiguracja Projektu
- `.editorconfig` ✅ KEEP
- `.gitignore` ✅ KEEP
- `pyproject.toml` ✅ KEEP
- `uv.lock` ✅ KEEP

### Skrypty Aktywne
- `check_api.sh` ✅ KEEP
- `fix_firewall.sh` ✅ KEEP

### Dokumenty Markdown
- Wszystkie `*.md` ✅ KEEP (już oczyszczone)

### Testy HTTP
- Wszystkie `*.http` ✅ KEEP

---

## 📊 Podsumowanie

| Kategoria | Liczba Plików | Akcja |
|-----------|---------------|-------|
| Workflow JSON N8N | 11 | Archiwizuj |
| Skrypty Python fix | 7 | Archiwizuj |
| Import instructions | 4 | Archiwizuj |
| Test JSON results | 4 | Archiwizuj |
| Stare Python files | 4 | Archiwizuj |
| Windows scripts | 6 | Przenieś/Archiwizuj |
| Temp files | 1 | Usuń |
| Stary viewer | 1 | Sprawdź/Archiwizuj |
| **RAZEM DO ARCHIWUM** | **38** | - |

---

## 🎯 Plan Akcji

1. Utwórz podfoldery w archiwum
2. Przenieś pliki według kategorii
3. Usuń `nul`
4. Opcjonalnie: utwórz `scripts/windows/` dla skryptów Windows
5. Zaktualizuj dokumentację
