# Changelog - Ulepszenie Logowania

## Data: 2025-10-28

### Zmiany

Zaktualizowano format logowania w obu projektach, aby zawierał **precyzyjne timestampy z milisekundami**.

### Przed Zmianą

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Przykładowy output:**
```
2025-10-28 14:30:45 - __main__ - INFO - Uruchamianie usługi porównywania dokumentów
2025-10-28 14:30:45 - __main__ - INFO - Katalog uploads: C:\Projects\BAW\UslugaDoPorownan\uploads
2025-10-28 14:30:45 - __main__ - INFO - Usługa gotowa do działania
```

### Po Zmianie

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

**Przykładowy output:**
```
2025-10-28 14:30:45.123 - __main__ - INFO - Uruchamianie usługi porównywania dokumentów
2025-10-28 14:30:45.156 - __main__ - INFO - Katalog uploads: C:\Projects\BAW\UslugaDoPorownan\uploads
2025-10-28 14:30:45.189 - __main__ - INFO - Usługa gotowa do działania
```

### Korzyści

1. **Precyzja Czasowa** - Milisekundy pozwalają na dokładne śledzenie czasu wykonania operacji
2. **Debugging Wydajności** - Łatwiejsze identyfikowanie bottlenecków
3. **Analiza Sekwencji Zdarzeń** - Precyzyjne określanie kolejności operacji
4. **Standardowy Format** - Format ISO-like (`YYYY-MM-DD HH:MM:SS.mmm`)
5. **Kompatybilność** - Działa ze wszystkimi narzędziami do analizy logów

### Pliki Zmienione

#### UslugaDoPorownan
- `main.py` - linia 30-34

#### SecureDocCompare
- `main.py` - linia 22-26

### Przykłady Użycia

#### Pomiar Czasu Operacji

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Rozpoczęcie przetwarzania dokumentu")
# ... operacja ...
logger.info("Zakończenie przetwarzania dokumentu")
```

**Output:**
```
2025-10-28 14:30:45.123 - mymodule - INFO - Rozpoczęcie przetwarzania dokumentu
2025-10-28 14:30:47.456 - mymodule - INFO - Zakończenie przetwarzania dokumentu
```

Czas wykonania: **2.333 sekundy** (łatwo obliczyć z precyzją do milisekund)

#### Debugging Asynchronicznych Operacji

```python
logger.info(f"Upload started: {file_id}")
await process_upload(file_id)
logger.info(f"Upload completed: {file_id}")
```

**Output:**
```
2025-10-28 14:30:45.100 - api - INFO - Upload started: doc-123
2025-10-28 14:30:45.105 - api - INFO - Upload started: doc-456
2025-10-28 14:30:45.250 - api - INFO - Upload completed: doc-123
2025-10-28 14:30:45.301 - api - INFO - Upload completed: doc-456
```

Dzięki milisekundom widać dokładną kolejność i czasy wykonania.

### Kompatybilność

- ✅ Python 3.7+
- ✅ Wszystkie handlery logowania (console, file, syslog)
- ✅ Uvicorn
- ✅ FastAPI
- ✅ Narzędzia do analizy logów (ELK, Splunk, Grafana Loki)

### Notatki Techniczne

- `%(msecs)03d` - Milisekundy z padding do 3 cyfr (000-999)
- `datefmt='%Y-%m-%d %H:%M:%S'` - Format daty bez mikrosekund (dodajemy je ręcznie przez msecs)
- Format jest thread-safe i działa poprawnie w aplikacjach asynchronicznych

### Testy

Aby przetestować nowy format logowania:

```bash
# UslugaDoPorownan
cd C:\Projects\BAW\UslugaDoPorownan
uvicorn main:app --reload --port 8001

# SecureDocCompare
cd C:\Projects\BAW\SecureDocCompare
uvicorn main:app --reload --port 8000
```

Sprawdź output w konsoli - powinien zawierać milisekundy.

### Rollback

Jeśli z jakiegoś powodu potrzebujesz wrócić do starego formatu:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Rekomendacje

1. **Produkcja**: Użyj tego formatu wraz z rotacją logów
2. **Development**: Format idealny do debugowania wydajności
3. **Monitoring**: Łatwa integracja z systemami monitoring (Prometheus, Grafana)

### Zgodność z Innymi Modułami

Wszystkie moduły w projekcie korzystają z `logging.getLogger(__name__)`, więc automatycznie dziedziczą ten format z `main.py`:

- ✅ `extractor.py`
- ✅ `comparator.py`
- ✅ `storage.py`
- ✅ `pdf_converter/*.py`
- ✅ `auth.py` (SecureDocCompare)
- ✅ `middleware.py` (SecureDocCompare)

Nie ma potrzeby zmiany tych plików - dziedziczą konfigurację automatycznie.
