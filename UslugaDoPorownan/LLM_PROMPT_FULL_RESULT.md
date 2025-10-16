# Prompt dla LLM - Analiza full_result.json

## System Prompt

```
Jesteś ekspertem w analizie porównań dokumentów. Otrzymujesz plik JSON z wynikami porównania dwóch dokumentów DOCX. Twoim zadaniem jest przeanalizowanie tego pliku i dostarczenie szczegółowego raportu o zmianach.
```

---

## Main Prompt (do skopiowania)

```markdown
# INSTRUKCJA ANALIZY PLIKU full_result.json

## Twoje Zadanie
Przeanalizuj otrzymany plik JSON zawierający wyniki porównania dwóch dokumentów DOCX (stary vs nowy). Plik zawiera szczegółowe informacje o wszystkich zmianach, dodatkach i usunięciach.

## Struktura Pliku JSON

### 1. METADATA (na najwyższym poziomie)
```json
{
  "process_id": "uuid",           // Unikalny ID procesu porównania
  "document_pair_id": "uuid",     // ID pary dokumentów
  "generated_at": "timestamp",    // Kiedy wygenerowano wynik
  "statistics": {...},            // Ogólne statystyki (patrz niżej)
  "paragraphs": [...],            // Lista wszystkich paragrafów (patrz niżej)
  "tables": [...]                 // Lista tabel (patrz niżej)
}
```

### 2. STATISTICS (statistics)
Zawiera zagregowane statystyki porównania:
```json
{
  "total_paragraphs": number,      // Wszystkie paragrafy (włącznie z usuniętymi)
  "unchanged_paragraphs": number,  // Identyczne w obu dokumentach
  "modified_paragraphs": number,   // Zmodyfikowane (są w obu, ale różne)
  "added_paragraphs": number,      // Nowe (tylko w nowym dokumencie)
  "deleted_paragraphs": number,    // Usunięte (tylko w starym dokumencie)
  "total_changes": number,         // modified + added + deleted
  "tables_count": number,          // Liczba tabel w nowym dokumencie
  "modified_cells": number         // Zmodyfikowane komórki w tabelach
}
```

**INTERPRETACJA:**
- Jeśli `total_changes` > 10 → duże zmiany, wymaga szczególnej uwagi
- Jeśli `deleted_paragraphs` > 0 → treść została usunięta
- Jeśli `added_paragraphs` > 0 → dodano nową treść
- Jeśli `modified_paragraphs` > 0 → istniejąca treść została zmieniona

### 3. PARAGRAPHS (paragraphs)
Lista paragrafów z nowego dokumentu + usuniętych ze starego.

Każdy paragraf ma strukturę:
```json
{
  "index": number,           // Pozycja w dokumencie (0-based)
  "text": "string",          // Aktualna treść (z nowego dokumentu)
  "type": "string",          // Typ: "unchanged" | "modified" | "added" | "deleted"
  "old_text": "string|null", // Stara treść (tylko dla modified i deleted)
  "changes": [...]           // Lista zmian (tylko dla modified)
}
```

#### TYPY PARAGRAFÓW:

**a) "unchanged"** - Paragraf identyczny w obu dokumentach
```json
{
  "index": 5,
  "text": "Ten tekst jest taki sam",
  "type": "unchanged",
  "old_text": null,
  "changes": null
}
```
**CO TO ZNACZY:** Nic się nie zmieniło w tym paragrafie.

**b) "modified"** - Paragraf zmodyfikowany
```json
{
  "index": 11,
  "text": "Właścicielem Polityki jest Chief Operating Officer (COO).",
  "type": "modified",
  "old_text": "Właścicielem Polityki jest Chief Risk Officer (CRO).",
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
```
**CO TO ZNACZY:**
- Paragraf istniał w obu dokumentach, ale treść się zmieniła
- `text` = aktualna wersja (nowy dokument)
- `old_text` = poprzednia wersja (stary dokument)
- `changes` = dokładne zmiany słowo po słowie

**c) "added"** - Paragraf dodany (nowy)
```json
{
  "index": 25,
  "text": "To jest całkowicie nowy paragraf.",
  "type": "added",
  "old_text": null,
  "changes": null
}
```
**CO TO ZNACZY:** Ten paragraf nie istniał w starym dokumencie, został dodany.

**d) "deleted"** - Paragraf usunięty
```json
{
  "index": 30,
  "text": "Ten paragraf został usunięty.",
  "type": "deleted",
  "old_text": "Ten paragraf został usunięty.",
  "changes": null
}
```
**CO TO ZNACZY:** Ten paragraf był w starym dokumencie, ale został usunięty z nowego.

#### CHANGES ARRAY (dla type="modified"):
Każda zmiana ma strukturę:
```json
{
  "operation": "equal" | "delete" | "insert",
  "text": "fragment tekstu"
}
```

**OPERACJE:**
- **"equal"** → Fragment niezmieniony (występuje w obu wersjach)
- **"delete"** → Fragment usunięty (był w starym, nie ma w nowym)
- **"insert"** → Fragment dodany (nie było w starym, jest w nowym)

**PRZYKŁAD INTERPRETACJI:**
```json
[
  {"operation": "equal", "text": "Bank "},
  {"operation": "delete", "text": "XYZ"},
  {"operation": "insert", "text": "ABC"},
  {"operation": "equal", "text": " jest instytucją"}
]
```
**OZNACZA:**
"Bank XYZ jest instytucją" → "Bank ABC jest instytucją"
(Zmieniono nazwę banku z XYZ na ABC)

### 4. TABLES (tables)
Lista tabel z nowego dokumentu.

Każda tabela ma strukturę:
```json
{
  "index": number,              // Numer tabeli
  "rows": [[string]],           // Wiersze z komórkami
  "changes": [...]|null         // Zmiany w komórkach (jeśli są)
}
```

#### CHANGES w tabeli:
```json
{
  "table_index": number,    // Numer tabeli
  "row_index": number,      // Numer wiersza
  "col_index": number,      // Numer kolumny
  "old_value": "string",    // Stara wartość
  "new_value": "string",    // Nowa wartość
  "changes": [...]          // Szczegółowe zmiany (jak w paragrafach)
}
```

---

## TWOJE ZADANIA ANALITYCZNE

### 1. PODSUMOWANIE OGÓLNE
Przeanalizuj `statistics` i odpowiedz:
- Ile łącznie zmian wykryto?
- Jaki jest charakter zmian? (głównie modyfikacje/dodania/usunięcia)
- Czy zmiany są istotne? (>10 zmian = istotne)

### 2. ANALIZA MODYFIKACJI
Dla każdego paragrafu `type="modified"`:
- Zidentyfikuj CO DOKŁADNIE się zmieniło
- Oceń czy zmiana jest istotna (np. zmiana nazwy, liczby, definicji)
- Wskaż potencjalne konsekwencje

### 3. ANALIZA DODAŃ
Dla każdego paragrafu `type="added"`:
- Co zostało dodane?
- Czy to nowa funkcjonalność, wymaganie, definicja?
- Jaka jest lokalizacja w dokumencie?

### 4. ANALIZA USUNIĘĆ
Dla każdego paragrafu `type="deleted"`:
- Co zostało usunięte?
- Czy to może być istotne? (np. usunięcie wymagania)
- Czy może to wpłynąć na zgodność/compliance?

### 5. ANALIZA TABEL
Dla tabel z `changes`:
- Które komórki się zmieniły?
- Czy to dane liczbowe, definicje, czy nazwy?
- Jaki jest kontekst zmian?

### 6. KLASYFIKACJA WAŻNOŚCI
Oceń każdą zmianę jako:
- **KRYTYCZNA** - zmiana definicji, wymagań prawnych, liczb
- **ISTOTNA** - zmiana nazw, terminów, procedur
- **MNIEJSZA** - korekty stylistyczne, formatowanie

---

## FORMAT ODPOWIEDZI

Przygotuj raport w następującym formacie:

### EXECUTIVE SUMMARY
- Łącznie wykrytych zmian: [liczba]
- Charakterystyka: [głównie modyfikacje/dodania/usunięcia]
- Ocena ogólna: [istotne zmiany / drobne korekty]

### ZMIANY KRYTYCZNE
Lista zmian wymagających natychmiastowej uwagi:
1. [Paragraf #X]: [opis zmiany]
   - Stare: [tekst]
   - Nowe: [tekst]
   - Wpływ: [konsekwencje]

### ZMIANY ISTOTNE
Lista ważnych zmian:
1. [Paragraf #X]: [opis zmiany]

### ZMIANY MNIEJSZE
Lista mniejszych zmian:
1. [Paragraf #X]: [opis zmiany]

### DODANE TREŚCI
Lista nowych paragrafów:
1. [Paragraf #X]: [treść]

### USUNIĘTE TREŚCI
Lista usuniętych paragrafów:
1. [Paragraf #X]: [treść]

### ZMIANY W TABELACH
Lista zmian w tabelach:
1. Tabela #X, Wiersz Y, Kolumna Z: [stara wartość] → [nowa wartość]

### REKOMENDACJE
- [Lista działań do podjęcia]
- [Obszary wymagające weryfikacji]
- [Potencjalne ryzyka]

---

## PRZYKŁADOWE PYTANIA DO ANALIZY

1. Czy zmieniono jakieś kluczowe definicje?
2. Czy zmieniono jakieś liczby lub wartości liczbowe?
3. Czy dodano nowe wymagania?
4. Czy usunięto jakieś wymagania?
5. Czy zmieniono nazwy departamentów/ról/stanowisk?
6. Czy zmieniono procedury lub procesy?
7. Czy zmiany są spójne czy przypadkowe?
8. Czy wszystkie zmiany są celowe czy mogą być błędami?

---

## KONTEKST DOMENOWY (opcjonalnie dostosuj)

Jeśli analizujesz dokumenty w konkretnej domenie, uwzględnij:
- **Banking/Finanse:** Zwróć uwagę na zmiany w regulacjach, limitach, compliance
- **Prawne:** Skupić się na definicjach, zobowiązaniach, terminach
- **Techniczne:** Zwróć uwagę na zmiany w specyfikacjach, parametrach, interfejsach
- **HR/Procedury:** Sprawdź zmiany w rolach, odpowiedzialnościach, procesach

---

## UWAGI KOŃCOWE

- Traktuj `index` jako pozycję w dokumencie (0-based)
- Paragrafy `type="deleted"` są na końcu listy, ich `index` odnosi się do starego dokumentu
- `changes` może być null jeśli nie dotyczy (unchanged, added, deleted)
- Zawsze porównuj `text` vs `old_text` dla modyfikacji
- Zwróć uwagę na zmiany w liczbach, nazwach własnych, definicjach

---

Teraz przeanalizuj otrzymany plik JSON i przygotuj szczegółowy raport zgodnie z powyższymi wytycznymi.
```

---

## User Prompt (krótka wersja do szybkiego użycia)

```
Przeanalizuj załączony plik full_result.json z wynikami porównania dokumentów.

Przygotuj raport zawierający:
1. Executive Summary (liczba zmian, charakterystyka)
2. Lista zmian KRYTYCZNYCH (definicje, liczby, wymagania prawne)
3. Lista zmian ISTOTNYCH (nazwy, terminy, procedury)
4. Lista zmian MNIEJSZYCH (stylistyka, formatowanie)
5. Dodane treści (nowe paragrafy)
6. Usunięte treści (usunięte paragrafy)
7. Zmiany w tabelach
8. Rekomendacje i potencjalne ryzyka

Struktura JSON:
- statistics: ogólne statystyki
- paragraphs: lista paragrafów z type: unchanged/modified/added/deleted
- paragraphs[].changes: szczegółowe zmiany (operation: equal/delete/insert)
- tables: tabele ze zmianami w komórkach

Skup się na zmianach istotnych biznesowo. Wskaż potencjalne problemy compliance.
```

---

## Przykład Użycia w n8n

### Node: OpenAI / Anthropic / Gemini

**System Prompt:**
```
Jesteś ekspertem w analizie porównań dokumentów biznesowych, szczególnie w kontekście compliance, regulacji bankowych i zarządzania ryzykiem.
```

**User Prompt:**
```
Przeanalizuj wyniki porównania dokumentu "Polityka Zarządzania Ryzykiem ICT".

Plik JSON:
{{ $('Get Full Result').item.json }}

Zwróć szczególną uwagę na zmiany związane z:
- Rolami i odpowiedzialnościami (Chief Officers, departamenty)
- Wymogami DORA (Digital Operational Resilience Act)
- Procedurami raportowania
- Komitetami i ich kompetencjami

Przygotuj raport wykonawczy dla Zarządu.
```

---

## Przykład z kodem Python

```python
import json
import anthropic  # lub openai, google.generativeai

# Wczytaj plik
with open('full_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Przygotuj prompt
system_prompt = """
Jesteś ekspertem w analizie porównań dokumentów. Przeanalizuj plik JSON
z wynikami porównania i przygotuj szczegółowy raport o zmianach.
"""

user_prompt = f"""
Przeanalizuj wyniki porównania dokumentów:

{json.dumps(data, ensure_ascii=False, indent=2)}

Przygotuj raport zawierający executive summary, listę zmian krytycznych,
istotnych i mniejszych, oraz rekomendacje.
"""

# Wywołaj AI
client = anthropic.Anthropic(api_key="your-key")
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4000,
    system=system_prompt,
    messages=[{"role": "user", "content": user_prompt}]
)

print(response.content[0].text)
```

---

## Wskazówki

### Dla krótkich dokumentów (<100 paragrafów):
Wysyłaj cały JSON do AI.

### Dla długich dokumentów (>100 paragrafów):
1. Najpierw wyślij tylko `statistics`
2. Potem wyślij tylko `type="modified"` i `type="deleted"`
3. Na końcu zapytaj o konkretne paragrafy

### Dla analizy w czasie rzeczywistym:
Użyj streaming API i analizuj na bieżąco.

---

*Prompt przygotowany dla: Claude, GPT-4, Gemini, Llama*
*Wersja: 1.0*
*Data: 2025-10-15*
