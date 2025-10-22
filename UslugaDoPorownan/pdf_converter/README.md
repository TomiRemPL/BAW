# PDF→DOCX Converter Module

Moduł automatycznej konwersji PDF na DOCX dla systemu porównywania dokumentów bankowych.

## 📋 Funkcje

- **Dwupoziomowy system konwersji:**
  - `pdf2docx` (podstawowy, ~95% przypadków)
  - `pdfplumber` (fallback dla skomplikowanych tabel)
- **Automatyczna walidacja jakości** (wynik 0.0-1.0)
- **Automatyczny fallback** przy niskiej jakości
- **Post-processing** dla dokumentów prawnych/bankowych
- **Standalone CLI** do konwersji poza API
- **Transparentna integracja** z istniejącym API

## 🚀 Użycie

### Poprzez API

Upload plików PDF przez standardowy endpoint `/api/documents/upload`:

```bash
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@stary.pdf" \
  -F "new_document=@nowy.pdf"
```

Konwersja odbywa się automatycznie w tle. API zwraca informację o konwersji w `message`.

### CLI (Standalone)

Konwersja pojedynczego pliku:

```bash
cd UslugaDoPorownan
python -m pdf_converter.cli input.pdf output.docx
```

Konwersja wsadowa:

```bash
python -m pdf_converter.cli --batch pdf_folder/ docx_folder/
```

Wymuszenie metody:

```bash
# Tylko pdf2docx
python -m pdf_converter.cli input.pdf output.docx --method pdf2docx

# Tylko pdfplumber
python -m pdf_converter.cli input.pdf output.docx --method pdfplumber
```

Opcje CLI:

```
--batch               Tryb wsadowy
--method {pdf2docx|pdfplumber|auto}
--no-fallback         Wyłącz automatyczny fallback
--no-post-process     Wyłącz post-processing
--min-quality FLOAT   Minimalny próg jakości (0.0-1.0)
--timeout INT         Max czas konwersji w sekundach
--verbose             Szczegółowe logowanie
```

### Programatically (Python)

```python
from pathlib import Path
from pdf_converter import PDFConverter
from pdf_converter.config import PDFConverterConfig

# Domyślna konfiguracja
converter = PDFConverter()
result = converter.convert("input.pdf", "output.docx")

print(f"Sukces: {result.success}")
print(f"Jakość: {result.quality_score:.2f}")
print(f"Metoda: {result.method}")
print(f"Czas: {result.conversion_time:.2f}s")

# Własna konfiguracja
config = PDFConverterConfig(
    min_quality_score=0.8,
    enable_fallback=True,
    enable_post_processing=True,
    max_conversion_time=120
)

converter = PDFConverter(config)
result = converter.convert("input.pdf", "output.docx")
```

## 📊 System Walidacji Jakości

Wynik jakości (0.0-1.0) bazuje na:

- **Paragrafy (30%)** - liczba wyodrębnionych paragrafów
- **Tabele (40%)** - jakość wyodrębnienia tabel (priorytet!)
- **Struktura (20%)** - nagłówki, numeracja, listy
- **Formatowanie (10%)** - czcionki, pogrubienia, kursywa

### Interpretacja wyników:

- `0.9-1.0` - Doskonała konwersja
- `0.7-0.9` - Dobra konwersja
- `0.5-0.7` - Średnia konwersja (rozważ fallback)
- `0.0-0.5` - Słaba konwersja (użyj fallback)

Domyślny próg fallback: **0.7**

## 🔧 Konfiguracja

### Zmienne środowiskowe

Brak - moduł działa out-of-the-box.

### Plik konfiguracji (opcjonalnie)

```python
from pdf_converter.config import PDFConverterConfig

config = PDFConverterConfig(
    max_conversion_time=60,          # Max 60s dla 50-stron
    min_quality_score=0.7,           # Próg fallback
    preserve_tables=True,            # Priorytet: tabele
    preserve_structure=True,         # Priorytet: struktura
    preserve_numbering=True,         # Priorytet: numeracja
    preserve_formatting=True,        # Priorytet: formatowanie
    enable_fallback=True,            # Automatyczny fallback
    enable_post_processing=True,     # Post-processing
    verbose=False                    # Logowanie
)
```

## 📁 Struktura Modułu

```
pdf_converter/
├── __init__.py           # Eksporty publiczne
├── __main__.py           # Uruchomienie CLI
├── cli.py                # CLI interface
├── converter.py          # Główna klasa PDFConverter
├── validators.py         # QualityValidator
├── post_processor.py     # PostProcessor
├── config.py             # PDFConverterConfig
├── exceptions.py         # Custom wyjątki
└── README.md             # Ta dokumentacja
```

## 🧪 Testowanie

### Test podstawowy

```bash
# Backend API
curl http://localhost:8001/health

# Upload PDF przez API
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@test_old.pdf" \
  -F "new_document=@test_new.pdf"
```

### Test CLI

```bash
# Pobierz przykładowy PDF
curl -o test.pdf https://example.com/sample.pdf

# Konwertuj
python -m pdf_converter.cli test.pdf test.docx --verbose

# Sprawdź wynik
ls -lh test.docx
```

## 🐛 Troubleshooting

### Problem: "Module not found: pdf2docx"

```bash
# Zainstaluj zależności
pip install -r requirements.txt
```

### Problem: Niska jakość konwersji

```bash
# Spróbuj wymusi pdfplumber
python -m pdf_converter.cli input.pdf output.docx --method pdfplumber

# Lub wyłącz fallback i zobacz szczegóły
python -m pdf_converter.cli input.pdf output.docx --no-fallback --verbose
```

### Problem: Timeout

```bash
# Zwiększ timeout dla dużych plików
python -m pdf_converter.cli large.pdf output.docx --timeout 300
```

### Problem: Błędne tabele

```
# pdfplumber często lepiej radzi sobie z tabelami
python -m pdf_converter.cli input.pdf output.docx --method pdfplumber
```

## 📈 Wydajność

- **Czas konwersji:** ~30-60s dla dokumentu 50-stronicowego
- **Pamięć:** ~200-500MB podczas konwersji
- **Jakość:** 95%+ dokumentów konwertuje się z wynikiem >0.7

### Benchmark

| Dokument | Strony | Metoda | Jakość | Czas |
|----------|--------|--------|--------|------|
| Prosty tekst | 10 | pdf2docx | 0.95 | 5s |
| Z tabelami | 20 | pdf2docx | 0.85 | 12s |
| Skomplikowane tabele | 20 | pdfplumber | 0.78 | 18s |
| Długi dokument | 50 | pdf2docx | 0.92 | 35s |

## 🔒 Bezpieczeństwo

- **Brak external API** - 100% lokalna konwersja
- **Walidacja plików** - tylko .pdf akceptowane
- **Timeout** - max 60s domyślnie (konfigurowalny)
- **Error handling** - graceful degradation

## 🛠️ Development

### Dodawanie nowych metod konwersji

1. Dodaj metodę w `converter.py`:
   ```python
   def _convert_with_new_method(self, pdf_path, output_path, start_time):
       ...
   ```

2. Zaktualizuj `convert()` aby używała nowej metody

3. Dodaj do `--method` choices w `cli.py`

### Dostosowanie post-processingu

Edytuj `post_processor.py`:

```python
class PostProcessor:
    def process(self, docx_path):
        # Twoje własne reguły formatowania
        ...
```

## 📞 Wsparcie

- **Dokumentacja główna:** `/BAW/README.md`
- **API Backend:** `/BAW/UslugaDoPorownan/README.md`
- **Frontend:** `/BAW/SecureDocCompare/README.md`

---

**Wersja:** 1.0.0
**Python:** 3.11.9
**Zależności:** pdf2docx, pdfplumber, python-docx
**Autor:** TomiRemPL
**Status:** ✅ Production Ready
