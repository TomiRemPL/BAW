# 🚀 Szybki Start - Usługa Porównywania Dokumentów

## Krok 1: Uruchom usługę

```bash
cd UslugaDoPorownan
python -m uvicorn main:app --reload --port 8001
```

Usługa będzie dostępna na: `http://localhost:8001`

## Krok 2: Sprawdź czy działa

```bash
curl http://localhost:8001/health
```

Powinieneś zobaczyć:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-15T...",
  "statistics": {...}
}
```

## Krok 3: Użyj skryptu testowego (ZALECANE)

Najprostrzy sposób - użyj gotowego skryptu Pythonowego:

```bash
python test_api.py stara_wersja/dokument.docx nowa_wersja/dokument.docx
```

Skrypt automatycznie:
- ✅ Załaduje dokumenty
- ✅ Uruchomi porównanie
- ✅ Będzie czekał na zakończenie
- ✅ Wyświetli statystyki
- ✅ Zapisze wyniki do plików JSON

### Przykład użycia:

```bash
# Z katalogu głównego projektu BAW
cd UslugaDoPorownan
python test_api.py ../stara_wersja/Polityka_Zarzadzania_Ryzykiem_ICT_DORA.docx ../nowa_wersja/Polityka_Zarzadzania_Ryzykiem_ICT_DORA.docx
```

### Wynik:

```
======================================================================
TEST USŁUGI PORÓWNYWANIA DOKUMENTÓW
======================================================================

📤 Ładowanie dokumentów...
   Stary: ../stara_wersja/Polityka_Zarzadzania_Ryzykiem_ICT_DORA.docx
   Nowy:  ../nowa_wersja/Polityka_Zarzadzania_Ryzykiem_ICT_DORA.docx
✅ Dokumenty załadowane: f6be031e-01ba-49ff-94f9-668ce4129529

⚙️  Rozpoczynam przetwarzanie...
✅ Przetwarzanie wystartowało: d2df1354-8bfd-42f8-9f88-292db04f2f93

⏳ Oczekiwanie na zakończenie...
   Status: processing (50%)
   Status: completed (100%)
✅ Przetwarzanie zakończone!

📊 Pobieranie wyników...

======================================================================
STATYSTYKI PORÓWNANIA
======================================================================
Wszystkich paragrafów:     64
  • Niezmienione:          52
  • Zmodyfikowane:         12
  • Dodane:                0
  • Usunięte:              0
Łącznie zmian:             12
Tabel:                     2
Zmodyfikowanych komórek:   4

======================================================================
ZMIENIONE PARAGRAFY (pierwsze 3)
======================================================================

1. Paragraf 11:
   STARY: Właścicielem Polityki jest Chief Risk Officer (CRO)....
   NOWY:  Właścicielem Polityki jest Chief Operating Officer (COO)....
   Operacje: {'equal': 3, 'delete': 2, 'insert': 2}

...

======================================================================
ZAPISYWANIE DO PLIKÓW
======================================================================
✅ full_result.json
✅ modified.json
✅ added.json
✅ deleted.json

======================================================================
✅ TEST ZAKOŃCZONY POMYŚLNIE!
======================================================================
```

## Krok 4 (Opcjonalny): Użyj API bezpośrednio

Jeśli wolisz używać curl lub własnych skryptów:

### 4a. Załaduj dokumenty

```bash
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@stary.docx" \
  -F "new_document=@nowy.docx"
```

Odpowiedź:
```json
{
  "document_pair_id": "uuid-tutaj",
  "status": "uploaded",
  "message": "Dokumenty zostały załadowane..."
}
```

### 4b. Rozpocznij przetwarzanie

```bash
curl -X POST http://localhost:8001/api/process \
  -H "Content-Type: application/json" \
  -d '{"document_pair_id": "uuid-tutaj"}'
```

Odpowiedź:
```json
{
  "process_id": "uuid-procesu",
  "status": "started",
  "message": "Przetwarzanie zostało rozpoczęte"
}
```

### 4c. Sprawdź status

```bash
curl http://localhost:8001/api/status/uuid-procesu
```

Odpowiedź:
```json
{
  "process_id": "uuid-procesu",
  "status": "completed",
  "progress": 100,
  "message": "Przetwarzanie zakończone pomyślnie"
}
```

### 4d. Pobierz wyniki

```bash
# Pełny dokument ze znacznikami
curl http://localhost:8001/api/result/uuid-procesu/full > full_result.json

# Tylko zmienione fragmenty
curl http://localhost:8001/api/result/uuid-procesu/modified > modified.json

# Tylko dodane fragmenty
curl http://localhost:8001/api/result/uuid-procesu/added > added.json

# Tylko usunięte fragmenty
curl http://localhost:8001/api/result/uuid-procesu/deleted > deleted.json
```

## Struktura Odpowiedzi JSON

### Full Result (`full_result.json`)

```json
{
  "process_id": "...",
  "document_pair_id": "...",
  "paragraphs": [
    {
      "index": 0,
      "text": "Treść nowego paragrafu",
      "type": "modified",
      "old_text": "Treść starego paragrafu",
      "changes": [
        {"operation": "equal", "text": "Treść "},
        {"operation": "delete", "text": "starego"},
        {"operation": "insert", "text": "nowego"},
        {"operation": "equal", "text": " paragrafu"}
      ]
    }
  ],
  "tables": [...],
  "statistics": {
    "total_paragraphs": 64,
    "unchanged_paragraphs": 52,
    "modified_paragraphs": 12,
    "added_paragraphs": 0,
    "deleted_paragraphs": 0,
    "total_changes": 12,
    "tables_count": 2,
    "modified_cells": 4
  },
  "generated_at": "2025-10-15T..."
}
```

### Modified Sentences (`modified.json`)

```json
{
  "process_id": "...",
  "document_pair_id": "...",
  "modified_sentences": [
    {
      "paragraph_index": 11,
      "old_text": "Właścicielem Polityki jest Chief Risk Officer (CRO).",
      "new_text": "Właścicielem Polityki jest Chief Operating Officer (COO).",
      "changes": [
        {"operation": "equal", "text": "Właścicielem Polityki jest Chief "},
        {"operation": "delete", "text": "Risk"},
        {"operation": "insert", "text": "Operating"},
        {"operation": "equal", "text": " Officer (C"},
        {"operation": "delete", "text": "R"},
        {"operation": "insert", "text": "O"},
        {"operation": "equal", "text": "O)."}
      ]
    }
  ],
  "total_count": 12,
  "generated_at": "2025-10-15T..."
}
```

## Typy Operacji w `changes`

- **`equal`** - fragment bez zmian (występuje zarówno w starym jak i nowym)
- **`delete`** - fragment usunięty (był w starym, nie ma w nowym)
- **`insert`** - fragment dodany (nie było w starym, jest w nowym)

## Typy Paragrafów w `type`

- **`unchanged`** - paragraf identyczny w obu dokumentach
- **`modified`** - paragraf z modyfikacjami (zawiera pole `changes`)
- **`added`** - paragraf dodany w nowym dokumencie
- **`deleted`** - paragraf usunięty (był w starym, nie ma w nowym)

## Rozwiązywanie Problemów

### Usługa nie odpowiada

```bash
# Sprawdź czy usługa działa
curl http://localhost:8001/health

# Jeśli nie, uruchom ją ponownie
cd UslugaDoPorownan
python -m uvicorn main:app --port 8001
```

### Port zajęty

```bash
# Użyj innego portu
python -m uvicorn main:app --port 8002

# Pamiętaj aby zmienić BASE_URL w test_api.py na:
# BASE_URL = "http://localhost:8002"
```

### Brak requests

```bash
pip install requests
```

## Więcej Informacji

Zobacz pełną dokumentację w `README.md`
