# Document Comparison POC

Aplikacja do porównywania dokumentów bankowych w formacie DOCX z wykorzystaniem FastAPI i analizy AI.

## Wymagania

- Python 3.11+
- UV package manager
- (Opcjonalnie) Klucz API Anthropic Claude lub Google Gemini dla zaawansowanej analizy

## Instalacja

1. Sklonuj repozytorium lub rozpakuj pliki projektu

2. Zainstaluj zależności używając UV:
```bash
uv sync
```

3. **Wymagane dla generowania PDF (WeasyPrint):**

WeasyPrint wymaga bibliotek GTK+ na Windows. Wybierz jedną z metod instalacji:

### Metoda 1: GTK for Windows Runtime (ZALECANE)

1. Pobierz instalator GTK3 Runtime:
   ```
   https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
   ```

2. Pobierz najnowszą wersję (np. `gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe`)

3. Uruchom instalator jako Administrator

4. **WAŻNE:** Zaznacz opcję "Add to PATH" podczas instalacji

5. Po instalacji zrestartuj terminal/PowerShell

6. Sprawdź instalację:
   ```bash
   # Powinna pokazać ścieżkę do GTK
   where libcairo-2.dll
   ```

### Metoda 2: MSYS2 (dla zaawansowanych użytkowników)

1. Zainstaluj MSYS2:
   ```
   https://www.msys2.org/
   ```

2. Otwórz MSYS2 terminal i zainstaluj pakiety:
   ```bash
   pacman -Syu
   pacman -S mingw-w64-x86_64-gtk3
   pacman -S mingw-w64-x86_64-cairo
   pacman -S mingw-w64-x86_64-pango
   pacman -S mingw-w64-x86_64-gdk-pixbuf2
   ```

3. Dodaj ścieżkę MSYS2 do PATH systemowego:
   ```
   C:\msys64\mingw64\bin
   ```

4. Zrestartuj terminal

### Weryfikacja instalacji GTK+

Po instalacji GTK+, sprawdź czy WeasyPrint działa:

```bash
cd c:/Projects/BAW
uv run python -c "from weasyprint import HTML; print('WeasyPrint działa!')"
```

Jeśli widzisz komunikat "WeasyPrint działa!" - instalacja przebiegła pomyślnie!

### Rozwiązywanie problemów z GTK+

Jeśli nadal występują błędy:

1. **Sprawdź PATH:**
   ```powershell
   $env:PATH
   ```
   Upewnij się, że zawiera ścieżkę do GTK (np. `C:\Program Files\GTK3-Runtime Win64\bin`)

2. **Sprawdź czy biblioteki są dostępne:**
   ```bash
   where libgobject-2.0-0.dll
   where libcairo-2.dll
   where libpango-1.0-0.dll
   ```

3. **Błąd "cannot load library":**
   - Upewnij się, że instalowałeś 64-bitową wersję GTK (jeśli masz 64-bit Python)
   - Sprawdź czy wszystkie DLL są w tej samej lokalizacji
   - Spróbuj zrestartować komputer

4. **Alternatywnie:** Jeśli problemy się utrzymują, możesz tymczasowo użyć starszej wersji generatora PDF (xhtml2pdf) - skontaktuj się z zespołem.

## Konfiguracja

### Klucze API (opcjonalne, tylko dla trybu advanced)

Ustaw zmienne środowiskowe:

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="twoj-klucz-api"
```

**Windows (CMD):**
```cmd
set ANTHROPIC_API_KEY=twoj-klucz-api
```

**Linux/Mac:**
```bash
export ANTHROPIC_API_KEY="twoj-klucz-api"
```

Alternatywnie możesz użyć Google Gemini:
```bash
export GOOGLE_API_KEY="twoj-klucz-api"
```

## Uruchomienie

1. Uruchom aplikację:
```bash
uv run uvicorn main:app --reload
```

2. Otwórz przeglądarkę i przejdź do:
```
http://localhost:8000
```

## Użycie

### Przygotowanie dokumentów

1. Umieść stare wersje dokumentów DOCX w katalogu `stara_wersja/`
2. Umieść nowe wersje dokumentów DOCX w katalogu `nowa_wersja/`
3. Upewnij się, że pliki mają takie same nazwy w obu katalogach

### Porównywanie dokumentów

1. Na dashboardzie zobaczysz wszystkie pary dokumentów
2. Kliknij "Porównaj (Basic)" dla podstawowego porównania (bez AI)
3. Kliknij "Porównaj (Advanced + AI)" dla zaawansowanej analizy z AI (wymaga klucza API)
4. Poczekaj na zakończenie przetwarzania
5. Kliknij "Zobacz Raport" aby zobaczyć wyniki
6. Kliknij "Pobierz PDF" aby pobrać raport w formacie PDF

### Tryby porównywania

**Basic Mode:**
- Porównanie na poziomie akapitów
- Wykrywanie dodanych, usuniętych, zmodyfikowanych i przesunięty akapitów
- Porównanie tabel
- Porównanie metadanych
- Działa bez kluczy API

**Advanced Mode:**
- Wszystko z Basic Mode
- Analiza AI każdej zmiany
- Klasyfikacja wagi zmian (MINOR/MODERATE/MAJOR)
- Analiza zgodności z regulacjami (DORA, KYC, AML)
- Rekomendacje i podsumowanie
- Wymaga ANTHROPIC_API_KEY lub GOOGLE_API_KEY

## Struktura projektu

```
document_comparison_poc/
├── main.py                 # FastAPI application
├── config.py              # Configuration
├── processors/            # Document processing
│   ├── extractor.py      # DOCX extraction
│   ├── comparator.py     # Diff algorithms
│   └── analyzer.py       # AI analysis
├── report_generator/      # Report generation
│   ├── html_generator.py # HTML reports
│   └── pdf_generator.py  # PDF reports
├── templates/             # Jinja2 templates
│   ├── base.html
│   ├── dashboard.html
│   ├── comparison_report.html
│   └── summary.html
├── static/                # Static assets
│   ├── styles.css
│   └── app.js
├── nowa_wersja/          # Input: new versions
├── stara_wersja/         # Input: old versions
└── output/               # Output: reports and logs
```

## API Endpoints

- `GET /` - Dashboard
- `GET /api/documents` - Lista par dokumentów
- `POST /api/compare` - Start porównania
- `GET /api/compare/{id}/status` - Status porównania
- `GET /report/{id}` - Zobacz raport HTML
- `GET /api/download/{id}` - Pobierz raport PDF
- `GET /api/summary` - Podsumowanie wszystkich porównań
- `GET /health` - Health check

## Rozwiązywanie problemów

### Brak dokumentów na dashboardzie
- Upewnij się, że pliki DOCX są w katalogach `stara_wersja/` i `nowa_wersja/`
- Sprawdź czy pliki mają rozszerzenie `.docx`
- Sprawdź czy nazwy plików są identyczne w obu katalogach

### Błąd podczas porównywania
- Sprawdź logi w konsoli
- Upewnij się, że pliki DOCX nie są uszkodzone
- Spróbuj ponownie otworzyć i zapisać plik w MS Word

### Tryb Advanced nie działa
- Sprawdź czy zmienna środowiskowa ANTHROPIC_API_KEY jest ustawiona
- Sprawdź czy klucz API jest prawidłowy
- Sprawdź połączenie z internetem

### Problemy z PDF
- Zobacz szczegółowe instrukcje instalacji GTK+ w sekcji "Instalacja" powyżej
- WeasyPrint wymaga bibliotek GTK+ (libgobject, libcairo, libpango)
- Jeśli widzisz błąd "cannot load library", upewnij się że GTK+ jest zainstalowany i dodany do PATH
- Zrestartuj terminal po instalacji GTK+

## Wydajność

Aplikacja została zaprojektowana do przetwarzania:
- 5 par dokumentów po 50 stron każdy
- W mniej niż 5 minut (tryb advanced)

Przetwarzanie jest sekwencyjne (jedna para na raz) dla stabilności POC.

## Uwagi

- To jest POC (Proof of Concept) - aplikacja do demonstracji i testów
- Działa lokalnie, nie wymaga zewnętrznych baz danych
- Wyniki porównań są przechowywane w pamięci (znikają po restarcie)
- Dla produkcji zaleca się dodać trwałe przechowywanie danych

## Licencja

POC dla celów demonstracyjnych.
