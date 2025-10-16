# Usługa do Porównywania Dokumentów

Niezależna usługa API do porównywania dokumentów DOCX z zachowaniem struktury i szczegółowymi znacznikami zmian.

## Opis

Usługa umożliwia:
- Załadowanie pary dokumentów (stary i nowy)
- Przetwarzanie i porównywanie dokumentów
- Pobranie wyników w formacie JSON z:
  - Pełną treścią nowego dokumentu ze znacznikami zmian
  - Tylko zmienionymi fragmentami
  - Tylko dodanymi fragmentami
  - Tylko usuniętymi fragmentami

## Struktura Projektu

```
UslugaDoPorownan/
├── main.py              # Główna aplikacja FastAPI
├── models.py            # Modele danych Pydantic
├── extractor.py         # Ekstrakcja treści z DOCX
├── comparator.py        # Algorytm porównywania
├── storage.py           # Przechowywanie w pamięci
├── pyproject.toml       # Konfiguracja i zależności
├── README.md            # Dokumentacja
└── uploads/             # Katalog na przesłane pliki
```

## Wymagania

- Python 3.10+
- uv (lub pip)

## Instalacja i Uruchomienie

### Metoda 1: Bezpośrednio przez Python (najprostsza)

```bash
cd UslugaDoPorownan
python -m uvicorn main:app --reload --port 8001
```

### Metoda 2: Używając środowiska wirtualnego

```bash
cd UslugaDoPorownan
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fastapi uvicorn[standard] python-multipart pydantic python-docx docx2python diff-match-patch
python -m uvicorn main:app --reload --port 8001
```

### Metoda 3: Używając uv

```bash
cd UslugaDoPorownan
uv pip install fastapi uvicorn[standard] python-multipart pydantic python-docx docx2python diff-match-patch
python -m uvicorn main:app --reload --port 8001
```

Usługa będzie dostępna pod adresem: `http://localhost:8001`

## API Endpoints

### 1. Health Check

**GET** `/health`

Sprawdzenie statusu usługi.

```bash
curl http://localhost:8001/health
```

Odpowiedź:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:00:00",
  "statistics": {
    "total_documents": 5,
    "total_processes": 10,
    "completed_processes": 8,
    "processing_count": 1,
    "error_count": 1,
    "cached_results": 8
  }
}
```

### 2. Załadowanie Dokumentów

**POST** `/api/documents/upload`

Załaduj parę dokumentów do porównania.

```bash
curl -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@stary_dokument.docx" \
  -F "new_document=@nowy_dokument.docx"
```

Odpowiedź:
```json
{
  "document_pair_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "uploaded",
  "message": "Dokumenty zostały załadowane: stary_dokument.docx, nowy_dokument.docx"
}
```

### 3. Uruchomienie Przetwarzania

**POST** `/api/process`

Rozpocznij porównywanie dokumentów.

```bash
curl -X POST http://localhost:8001/api/process \
  -H "Content-Type: application/json" \
  -d '{"document_pair_id": "550e8400-e29b-41d4-a716-446655440000"}'
```

Odpowiedź:
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "started",
  "message": "Przetwarzanie zostało rozpoczęte"
}
```

### 4. Sprawdzenie Statusu

**GET** `/api/status/{process_id}`

Sprawdź status przetwarzania.

```bash
curl http://localhost:8001/api/status/660e8400-e29b-41d4-a716-446655440001
```

Odpowiedź:
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "completed",
  "progress": 100,
  "message": "Przetwarzanie zakończone pomyślnie",
  "started_at": "2025-01-15T10:00:00",
  "completed_at": "2025-01-15T10:00:30"
}
```

Status może być: `pending`, `processing`, `completed`, `error`

### 5. Pełny Dokument ze Znacznikami

**GET** `/api/result/{process_id}/full`

Pobierz pełny dokument z wszystkimi znacznikami zmian.

```bash
curl http://localhost:8001/api/result/660e8400-e29b-41d4-a716-446655440001/full
```

Odpowiedź:
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "document_pair_id": "550e8400-e29b-41d4-a716-446655440000",
  "paragraphs": [
    {
      "index": 0,
      "text": "To jest nowa wersja pierwszego paragrafu",
      "type": "modified",
      "old_text": "To jest stara wersja pierwszego paragrafu",
      "changes": [
        {"operation": "equal", "text": "To jest "},
        {"operation": "delete", "text": "stara"},
        {"operation": "insert", "text": "nowa"},
        {"operation": "equal", "text": " wersja pierwszego paragrafu"}
      ]
    },
    {
      "index": 1,
      "text": "Ten paragraf nie został zmieniony",
      "type": "unchanged",
      "old_text": null,
      "changes": null
    },
    {
      "index": 2,
      "text": "To jest nowy paragraf",
      "type": "added",
      "old_text": null,
      "changes": null
    }
  ],
  "tables": [...],
  "statistics": {
    "total_paragraphs": 15,
    "unchanged_paragraphs": 10,
    "modified_paragraphs": 3,
    "added_paragraphs": 2,
    "deleted_paragraphs": 1,
    "total_changes": 6,
    "tables_count": 2,
    "modified_cells": 5
  },
  "generated_at": "2025-01-15T10:00:30"
}
```

### 6. Tylko Zmienione Fragmenty

**GET** `/api/result/{process_id}/modified`

Pobierz tylko zmienione paragrafy.

```bash
curl http://localhost:8001/api/result/660e8400-e29b-41d4-a716-446655440001/modified
```

Odpowiedź:
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "document_pair_id": "550e8400-e29b-41d4-a716-446655440000",
  "modified_sentences": [
    {
      "paragraph_index": 0,
      "old_text": "To jest stara wersja pierwszego paragrafu",
      "new_text": "To jest nowa wersja pierwszego paragrafu",
      "changes": [
        {"operation": "equal", "text": "To jest "},
        {"operation": "delete", "text": "stara"},
        {"operation": "insert", "text": "nowa"},
        {"operation": "equal", "text": " wersja pierwszego paragrafu"}
      ]
    }
  ],
  "total_count": 1,
  "generated_at": "2025-01-15T10:00:30"
}
```

### 7. Tylko Dodane Fragmenty

**GET** `/api/result/{process_id}/added`

Pobierz tylko dodane paragrafy.

```bash
curl http://localhost:8001/api/result/660e8400-e29b-41d4-a716-446655440001/added
```

Odpowiedź:
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "document_pair_id": "550e8400-e29b-41d4-a716-446655440000",
  "added_sentences": [
    {
      "paragraph_index": 2,
      "text": "To jest nowy paragraf"
    }
  ],
  "total_count": 1,
  "generated_at": "2025-01-15T10:00:30"
}
```

### 8. Tylko Usunięte Fragmenty

**GET** `/api/result/{process_id}/deleted`

Pobierz tylko usunięte paragrafy.

```bash
curl http://localhost:8001/api/result/660e8400-e29b-41d4-a716-446655440001/deleted
```

Odpowiedź:
```json
{
  "process_id": "660e8400-e29b-41d4-a716-446655440001",
  "document_pair_id": "550e8400-e29b-41d4-a716-446655440000",
  "deleted_sentences": [
    {
      "paragraph_index": 5,
      "text": "Ten paragraf został usunięty"
    }
  ],
  "total_count": 1,
  "generated_at": "2025-01-15T10:00:30"
}
```

## Kompletny Przykład Użycia

```bash
# 1. Załaduj dokumenty
UPLOAD_RESPONSE=$(curl -s -X POST http://localhost:8001/api/documents/upload \
  -F "old_document=@stary.docx" \
  -F "new_document=@nowy.docx")

DOCUMENT_PAIR_ID=$(echo $UPLOAD_RESPONSE | jq -r '.document_pair_id')
echo "Document Pair ID: $DOCUMENT_PAIR_ID"

# 2. Rozpocznij przetwarzanie
PROCESS_RESPONSE=$(curl -s -X POST http://localhost:8001/api/process \
  -H "Content-Type: application/json" \
  -d "{\"document_pair_id\": \"$DOCUMENT_PAIR_ID\"}")

PROCESS_ID=$(echo $PROCESS_RESPONSE | jq -r '.process_id')
echo "Process ID: $PROCESS_ID"

# 3. Sprawdzaj status (pętla)
while true; do
  STATUS=$(curl -s http://localhost:8001/api/status/$PROCESS_ID | jq -r '.status')
  echo "Status: $STATUS"

  if [ "$STATUS" = "completed" ]; then
    break
  elif [ "$STATUS" = "error" ]; then
    echo "Błąd podczas przetwarzania!"
    exit 1
  fi

  sleep 2
done

# 4. Pobierz wyniki
curl -s http://localhost:8001/api/result/$PROCESS_ID/full > full_result.json
curl -s http://localhost:8001/api/result/$PROCESS_ID/modified > modified.json
curl -s http://localhost:8001/api/result/$PROCESS_ID/added > added.json
curl -s http://localhost:8001/api/result/$PROCESS_ID/deleted > deleted.json

echo "Wyniki zapisane w plikach JSON"
```

## Algorytm Porównywania

Usługa wykorzystuje ten sam algorytm co główna aplikacja:

1. **Ekstrakcja** - używa `python-docx` i `docx2python` do wyodrębnienia:
   - Paragrafów (zachowując kolejność)
   - Tabel (ze strukturą)
   - Metadanych

2. **Porównywanie** - wykorzystuje `diff-match-patch` do:
   - Identyfikacji zmian na poziomie słów
   - Wykrywania dodanych/usuniętych/zmodyfikowanych paragrafów
   - Porównywania komórek tabel

3. **Struktura wynikowa** - zachowuje:
   - Kolejność wierszy z nowego dokumentu
   - Szczegółowe znaczniki zmian (delete/insert/equal)
   - Pełną treść przed i po zmianach

## Typy Zmian

- `unchanged` - paragraf bez zmian
- `modified` - paragraf zmodyfikowany (zawiera pole `changes` z detalami)
- `added` - paragraf dodany w nowym dokumencie
- `deleted` - paragraf usunięty (był w starym, nie ma w nowym)

## Znaczniki Operacji

W polu `changes` każdy fragment ma operację:
- `equal` - tekst bez zmian
- `delete` - tekst usunięty (był w starym)
- `insert` - tekst dodany (jest w nowym)

## Limity i Wydajność

- Przechowywanie w pamięci (brak bazy danych)
- Przetwarzanie sekwencyjne
- Pliki są automatycznie usuwane po 24h
- Brak limitu rozmiaru plików (zależny od pamięci RAM)

## Porównanie z Główną Aplikacją

| Funkcja | Główna Aplikacja | Usługa API |
|---------|-----------------|------------|
| Interface | Web UI | REST API |
| Raporty PDF | ✅ | ❌ |
| Raporty HTML | ✅ | ❌ |
| Raporty JSON | ❌ | ✅ |
| AI Analysis | ✅ | ❌ |
| Upload przez API | ❌ | ✅ |
| Filtrowanie wyników | ❌ | ✅ |

## Rozwiązywanie Problemów

### Port już zajęty

Jeśli port 8001 jest zajęty, użyj innego:

```bash
uvicorn main:app --reload --port 8002
```

### Błędy importu

Upewnij się, że wszystkie zależności są zainstalowane:

```bash
uv pip install -e .
```

### Błędy ekstrakcji DOCX

Sprawdź czy pliki są poprawnym formatem DOCX (nie DOC ani RTF).

## Licencja

Ten projekt jest częścią większego projektu POC do porównywania dokumentów bankowych.

## Autor

Wygenerowane przez Claude Code
