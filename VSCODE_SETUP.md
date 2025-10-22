# Visual Studio Code - Konfiguracja Projektu BAW

## Spis Treści
- [Wymagania](#wymagania)
- [Pierwsze Uruchomienie](#pierwsze-uruchomienie)
- [Rekomendowane Rozszerzenia](#rekomendowane-rozszerzenia)
- [Debugowanie](#debugowanie)
- [Zadania (Tasks)](#zadania-tasks)
- [Skróty Klawiszowe](#skróty-klawiszowe)
- [Rozwiązywanie Problemów](#rozwiązywanie-problemów)

---

## Wymagania

### Oprogramowanie
- **Visual Studio Code** 1.80 lub nowszy
- **Python** 3.11.9 (dokładnie ta wersja - ze względu na zależności)
- **Git** (opcjonalne, ale zalecane)

### Środowisko Wirtualne
Projekt używa środowiska wirtualnego w katalogu `.venv`

---

## Pierwsze Uruchomienie

### 1. Otwórz Projekt w VSCode

**Opcja A: Z linii poleceń**
```bash
cd c:/Projects/BAW
code .
```

**Opcja B: Z VSCode**
- File → Open Folder...
- Wybierz katalog `C:\Projects\BAW`

### 2. Wybierz Interpreter Pythona

Po otwarciu projektu VSCode powinien automatycznie:
1. Wykryć środowisko `.venv`
2. Zaproponować jego użycie jako interpreter

Jeśli nie:
1. Naciśnij `Ctrl+Shift+P`
2. Wpisz: `Python: Select Interpreter`
3. Wybierz: `.venv` (Python 3.11.9)

### 3. Zainstaluj Rozszerzenia

VSCode zaproponuje instalację rekomendowanych rozszerzeń:
1. Kliknij **"Install All"** w powiadomieniu
2. Lub ręcznie: `Ctrl+Shift+P` → `Extensions: Show Recommended Extensions`

**Kluczowe rozszerzenia:**
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Black Formatter (ms-python.black-formatter)
- Flake8 (ms-python.flake8)

### 4. Zainstaluj Zależności Pythona

**Automatycznie (przez Task):**
1. `Ctrl+Shift+P`
2. Wpisz: `Tasks: Run Task`
3. Wybierz: `Install Dependencies`

**Ręcznie:**
```bash
# Aktywuj środowisko
.venv\Scripts\activate  # Windows
# lub
source .venv/bin/activate  # Linux/Mac

# Zainstaluj zależności produkcyjne
pip install -r requirements.txt

# OPCJONALNIE: Zainstaluj narzędzia deweloperskie (black, flake8, pytest, etc.)
pip install -r requirements-dev.txt
```

**Uwaga:** Instalacja `requirements-dev.txt` jest opcjonalna, ale zalecana dla pełnej funkcjonalności VSCode (formatowanie, linting, testy).

### 5. Skonfiguruj Environment Variables

Dla **SecureDocCompare**:
```bash
cd SecureDocCompare
cp .env.example .env
# Edytuj .env i ustaw hasło
```

---

## Rekomendowane Rozszerzenia

### Kluczowe (Wymagane)
| Rozszerzenie | ID | Opis |
|--------------|-----|------|
| Python | ms-python.python | Podstawowe wsparcie Python |
| Pylance | ms-python.vscode-pylance | IntelliSense dla Pythona |
| Black Formatter | ms-python.black-formatter | Formatowanie kodu |
| Flake8 | ms-python.flake8 | Linting |

### Dodatkowe (Zalecane)
| Rozszerzenie | ID | Opis |
|--------------|-----|------|
| GitLens | eamodio.gitlens | Rozszerzone funkcje Git |
| REST Client | humao.rest-client | Testowanie API |
| Markdown All in One | yzhang.markdown-all-in-one | Edycja Markdown |
| Todo Tree | gruntfuggly.todo-tree | Zarządzanie TODO |
| Polish Spell Checker | streetsidesoftware.code-spell-checker-polish | Sprawdzanie pisowni PL |

### Instalacja
Wszystkie rozszerzenia są zdefiniowane w `.vscode/extensions.json` i VSCode automatycznie zaproponuje ich instalację.

---

## Debugowanie

### Dostępne Konfiguracje

#### 1. Backend API (UslugaDoPorownan) - Debug
Uruchamia backend API z debuggerem na porcie 8001.

**Użycie:**
1. `F5` lub `Run → Start Debugging`
2. Wybierz: `Backend API (UslugaDoPorownan) - Debug`

**Breakpointy:**
- Kliknij na lewym marginesie obok numeru linii
- Czerwona kropka = breakpoint aktywny

#### 2. Frontend (SecureDocCompare) - Debug
Uruchamia frontend z debuggerem na porcie 8000.

**Użycie:**
1. `F5`
2. Wybierz: `Frontend (SecureDocCompare) - Debug`

#### 3. Full Stack (Backend + Frontend) - COMPOUND
Uruchamia oba serwisy jednocześnie z debuggerem.

**Użycie:**
1. `F5`
2. Wybierz: `Full Stack (Backend + Frontend)`
3. Obie aplikacje uruchomią się w osobnych terminalach

**Adresy:**
- Frontend: http://localhost:8000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

#### 4. PDF Converter CLI
Debuguje konwerter PDF z linii poleceń.

**Użycie:**
1. Dostosuj args w `.vscode/launch.json` (ścieżki do plików)
2. `F5`
3. Wybierz: `PDF Converter CLI`

#### 5. PDF Converter Tests
Uruchamia testy jednostkowe konwertera PDF.

#### 6. Python: Current File
Debuguje aktualnie otwarty plik Python.

### Skróty Debugowania
- `F5` - Start/Continue
- `F9` - Toggle Breakpoint
- `F10` - Step Over
- `F11` - Step Into
- `Shift+F11` - Step Out
- `Shift+F5` - Stop Debugging
- `Ctrl+Shift+F5` - Restart Debugging

---

## Zadania (Tasks)

Zadania dostępne przez `Ctrl+Shift+P` → `Tasks: Run Task`

### Uruchamianie Serwerów

| Task | Opis |
|------|------|
| **Run Backend (UslugaDoPorownan)** | Uruchamia backend na porcie 8001 |
| **Run Frontend (SecureDocCompare)** | Uruchamia frontend na porcie 8000 |
| **Run Both Servers** | Uruchamia oba serwisy równolegle |

### Development

| Task | Opis |
|------|------|
| **Install Dependencies** | Instaluje wszystkie zależności z requirements.txt |
| **Black - Format Code** | Formatuje kod całego projektu |
| **Flake8 - Lint Code** | Sprawdza kod (linting) |
| **Clean Python Cache** | Usuwa `__pycache__`, `*.pyc` |

### Testowanie

| Task | Opis |
|------|------|
| **PDF Converter - Run Tests** | Uruchamia testy konwertera PDF |
| **Run Pytest** | Uruchamia wszystkie testy pytest |

### Narzędzia

| Task | Opis |
|------|------|
| **Check Python Version** | Sprawdza wersję Pythona |
| **Activate Virtual Environment** | Aktywuje środowisko .venv |

---

## Skróty Klawiszowe

### Podstawowe
- `Ctrl+Shift+P` - Command Palette (wszystkie komendy)
- `Ctrl+P` - Quick Open (szybkie otwieranie plików)
- `Ctrl+Shift+F` - Search w całym projekcie
- `Ctrl+Shift+E` - Explorer (drzewo plików)
- `Ctrl+Shift+G` - Source Control (Git)
- `Ctrl+Shift+D` - Run and Debug
- `Ctrl+`` ` - Terminal

### Edycja
- `Ctrl+/` - Toggle Comment
- `Alt+Shift+F` - Format Document
- `Ctrl+Shift+I` - Format Selection
- `F2` - Rename Symbol
- `Ctrl+.` - Quick Fix

### Nawigacja
- `Ctrl+T` - Go to Symbol in Workspace
- `F12` - Go to Definition
- `Alt+F12` - Peek Definition
- `Shift+F12` - Find All References
- `Ctrl+G` - Go to Line

### Python Specific
- `Shift+Enter` - Run Selection in Terminal
- `Ctrl+Shift+P` → `Python: Select Interpreter`

---

## Rozwiązywanie Problemów

### VSCode nie wykrywa środowiska .venv

**Rozwiązanie:**
1. `Ctrl+Shift+P`
2. `Python: Select Interpreter`
3. Wybierz `.venv` ręcznie
4. Restartuj VSCode

### Import Errors / ModuleNotFoundError

**Rozwiązanie:**
1. Sprawdź czy aktywne środowisko to `.venv`:
   ```bash
   where python  # Windows
   which python  # Linux/Mac
   ```
2. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
3. Sprawdź `PYTHONPATH` w terminalu VSCode

### Formatowanie (Black) nie działa

**Rozwiązanie:**
1. Zainstaluj rozszerzenie: `ms-python.black-formatter`
2. Sprawdź ustawienia:
   - `Ctrl+Shift+P`
   - `Preferences: Open Workspace Settings (JSON)`
   - Sprawdź: `"python.formatting.provider": "black"`
3. Zainstaluj black w środowisku:
   ```bash
   pip install black
   ```

### Linting (Flake8) nie działa

**Rozwiązanie:**
1. Zainstaluj flake8:
   ```bash
   pip install flake8
   ```
2. Sprawdź ustawienia workspace
3. Reload Window: `Ctrl+Shift+P` → `Developer: Reload Window`

### Debugger nie zatrzymuje się na breakpointach

**Rozwiązanie:**
1. Sprawdź czy breakpoint jest w kodzie Pythona (nie w komentarzu)
2. Sprawdź konfigurację debugowania w `.vscode/launch.json`
3. Zmień `"justMyCode": false` na `true` (lub odwrotnie)

### Port już zajęty (8000 lub 8001)

**Rozwiązanie:**
1. Zatrzymaj inne instancje:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F

   # Linux/Mac
   lsof -i :8000
   kill -9 <PID>
   ```
2. Lub zmień port w konfiguracji debugowania

### UTF-8 Encoding Issues (polskie znaki)

**Rozwiązanie:**
1. Sprawdź kodowanie pliku: prawy dolny róg VSCode
2. Kliknij i wybierz "UTF-8"
3. Zapisz plik: `Ctrl+S`
4. Ustawienia globalne w `.editorconfig`:
   ```
   [*]
   charset = utf-8
   ```

---

## Porady i Wskazówki

### 1. Multi-root Workspace (Opcjonalnie)

Jeśli chcesz osobne foldery dla SecureDocCompare i UslugaDoPorownan:
1. File → Add Folder to Workspace...
2. Dodaj `SecureDocCompare` i `UslugaDoPorownan`
3. File → Save Workspace As...

### 2. REST Client - Testowanie API

Zainstaluj rozszerzenie `humao.rest-client` i utwórz plik `test.http`:

```http
### Health Check
GET http://localhost:8001/health

### Upload Documents
POST http://localhost:8001/api/documents/upload
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="old_document"; filename="old.docx"
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document

< ./stara_wersja/dokument.docx
------WebKitFormBoundary--
```

### 3. Snippets

VSCode wspiera snippety. Przykładowy `.vscode/python.code-snippets`:

```json
{
  "FastAPI Endpoint": {
    "prefix": "endpoint",
    "body": [
      "@app.${1:get}(\"/${2:path}\")",
      "async def ${3:function_name}():",
      "    \"\"\"${4:Description}\"\"\"",
      "    return {\"message\": \"${5:response}\"}",
      "$0"
    ]
  }
}
```

### 4. Git Integration

VSCode ma wbudowaną integrację Git:
- Source Control: `Ctrl+Shift+G`
- Stage changes: `+` obok pliku
- Commit: `Ctrl+Enter` w message box
- Push/Pull: Menu `...` w Source Control

### 5. Terminal Tips

- Nowy terminal: `Ctrl+Shift+`` `
- Split terminal: `Ctrl+Shift+5`
- Kill terminal: Ikona kosza
- Rename terminal: Prawy klawisz → Rename

---

## Pliki Konfiguracyjne

### `.vscode/settings.json`
Ustawienia workspace dla całego projektu. Współdzielone w repo.

### `.vscode/launch.json`
Konfiguracje debugowania. Współdzielone w repo.

### `.vscode/tasks.json`
Definicje zadań. Współdzielone w repo.

### `.vscode/extensions.json`
Rekomendowane rozszerzenia. Współdzielone w repo.

### `.editorconfig`
Uniwersalne ustawienia edytora (działa też poza VSCode).

### Lokalne ustawienia (NIE w repo)

Jeśli chcesz dodać osobiste ustawienia (tylko dla siebie):
- Utwórz `.vscode/settings.local.json` (w .gitignore)
- Lub użyj User Settings (`Ctrl+,`)

---

## Zasoby

### Dokumentacja
- [Visual Studio Code - Python](https://code.visualstudio.com/docs/languages/python)
- [VSCode Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [VSCode Tasks](https://code.visualstudio.com/docs/editor/tasks)

### Projekt BAW
- `README.md` - Główna dokumentacja
- `DOCS_INDEX.md` - Indeks wszystkich dokumentów
- `PROGRESS_LOG.md` - Historia zmian
- `SecureDocCompare/QUICK_START.md` - Szybki start frontend
- `UslugaDoPorownan/README.md` - Dokumentacja API

---

## Wsparcie

Jeśli masz problemy:
1. Sprawdź [Rozwiązywanie Problemów](#rozwiązywanie-problemów)
2. Przeczytaj dokumentację projektu
3. Sprawdź logi w Output panel (`Ctrl+Shift+U`)
4. Sprawdź Developer Tools (`Help → Toggle Developer Tools`)

---

**Data utworzenia:** 2025-10-22
**Wersja:** 1.0
**Ostatnia aktualizacja:** 2025-10-22
