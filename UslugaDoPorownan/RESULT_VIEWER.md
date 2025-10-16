# 📊 Result Viewer - Instrukcja

## Opis

`result_viewer.html` to samodzielny HTML viewer do wizualizacji wyników porównania dokumentów z pliku `full_result.json`.

## Funkcje

✅ **Drag & Drop** - przeciągnij plik JSON na stronę
✅ **Kolorystyka** z głównego programu (banking colors)
✅ **Podsumowanie** - statystyki w przejrzystym widoku
✅ **Filtrowanie** - pokaż tylko wybrane typy paragrafów
✅ **Zmiany** - szczegółowe znaczniki (delete/insert/equal)
✅ **Tabele** - z wyróżnieniem zmienionych komórek
✅ **Bez instalacji** - działa bezpośrednio w przeglądarce

---

## Jak Używać

### Krok 1: Otwórz plik HTML

Kliknij dwukrotnie na:
```
result_viewer.html
```

Otworzy się w domyślnej przeglądarce.

### Krok 2: Załaduj plik JSON

**Opcja A: Drag & Drop**
- Przeciągnij plik `full_result.json` na stronę

**Opcja B: Przycisk**
- Kliknij w obszar uploadowania
- Wybierz plik `full_result.json`

### Krok 3: Przeglądaj Wyniki

Strona automatycznie wyświetli:
- 📊 Podsumowanie (łącznie zmian, zmodyfikowane, dodane, usunięte)
- ℹ️ Informacje (Process ID, Data wygenerowania)
- 📈 Statystyki (szczegółowe liczniki)
- 📝 Paragrafy (z filtrowaniem)
- 📋 Tabele (ze zmianami)

---

## Filtrowanie Paragrafów

Użyj przycisków filtrowania aby zobaczyć:
- **Wszystkie** - pełna lista
- **Zmodyfikowane** - tylko zmienione paragrafy
- **Dodane** - tylko nowe paragrafy
- **Usunięte** - tylko usunięte paragrafy
- **Niezmienione** - tylko identyczne paragrafy

---

## Kolorystyka

### Typy Paragrafów:

🔵 **Niezmieniony** - szary (ramka)
🔴 **Zmodyfikowany** - czerwony (#ED1B2F)
🟢 **Dodany** - zielony (#70A300)
🔴 **Usunięty** - czerwony (#ED1B2F, przezroczysty)

### Znaczniki Zmian:

⚪ **Equal** - normalny tekst
🔴 **Delete** - czerwone tło, przekreślenie
🟢 **Insert** - zielone tło, pogrubienie

---

## Przykład Użycia

```bash
# 1. Uruchom porównanie
cd UslugaDoPorownan
python test_simple.py stary.docx nowy.docx

# 2. Wygeneruje się: full_result.json

# 3. Otwórz viewer
start result_viewer.html

# 4. Przeciągnij full_result.json na stronę
```

---

## Lokalizacje Plików

### Viewer:
```
c:\Projects\BAW\result_viewer.html
c:\Projects\BAW\UslugaDoPorownan\result_viewer.html
```

### Wyniki (generowane przez test):
```
c:\Projects\BAW\full_result.json
c:\Projects\BAW\UslugaDoPorownan\full_result.json
```

---

## Przykłady Ekranów

### 1. Upload Screen
```
┌─────────────────────────────────────┐
│  📁                                  │
│  Przeciągnij plik full_result.json  │
│  tutaj                               │
│  lub kliknij aby wybrać plik         │
└─────────────────────────────────────┘
```

### 2. Summary View
```
┌─────────────────────────────────────┐
│  Podsumowanie Porównania            │
│                                     │
│   12          12          0     0   │
│  Łącznie   Zmodyfiko-  Dodane  Usu- │
│  Zmian     wane               nięte │
└─────────────────────────────────────┘
```

### 3. Paragraph View
```
┌─────────────────────────────────────┐
│ Paragraf #11           [Zmodyfikowany]│
│                                     │
│ Treść:                              │
│ Właścicielem Polityki jest Chief... │
│                                     │
│ Zmiany:                             │
│ Właścicielem Polityki jest Chief    │
│ [Risk] [Operating] Officer (C[R][O]O).│
└─────────────────────────────────────┘
```

---

## Techniczne Szczegóły

- **Technologia:** Pure HTML + CSS + JavaScript
- **Zależności:** Brak (self-contained)
- **Przeglądarki:** Chrome, Firefox, Edge, Safari
- **Rozmiar pliku:** ~24KB
- **Offline:** Działa bez internetu

---

## FAQ

### Czy potrzebuję serwera?
**Nie.** Viewer działa lokalnie w przeglądarce.

### Czy mogę otworzyć wiele plików?
**Tak.** Odśwież stronę i załaduj inny plik JSON.

### Czy dane są wysyłane gdziekolwiek?
**Nie.** Wszystko działa lokalnie, dane pozostają na Twoim komputerze.

### Czy mogę dostosować kolory?
**Tak.** Edytuj sekcję `<style>` w pliku HTML.

### Czy mogę wydrukować wyniki?
**Tak.** Użyj Ctrl+P w przeglądarce.

---

## Porównanie z Głównym Programem

| Funkcja | Główny Program | Result Viewer |
|---------|---------------|---------------|
| Porównanie | ✅ | ❌ |
| Raport HTML | ✅ | ❌ |
| Raport PDF | ✅ | ❌ |
| AI Analiza | ✅ | ❌ |
| **Wizualizacja JSON** | ❌ | **✅** |
| Diagnostyka | ❌ | **✅** |
| Drag & Drop | ❌ | **✅** |
| Filtrowanie | ❌ | **✅** |

---

## Troubleshooting

### Problem: Plik nie ładuje się

**Rozwiązanie:**
- Sprawdź czy to poprawny plik `full_result.json`
- Otwórz JSON w edytorze, sprawdź czy jest poprawny
- Sprawdź konsolę przeglądarki (F12)

### Problem: Brak stylów/kolorów

**Rozwiązanie:**
- Otwórz plik w nowoczesnej przeglądarce (Chrome/Firefox/Edge)
- Sprawdź czy plik HTML nie został uszkodzony

### Problem: Bardzo duży plik JSON

**Rozwiązanie:**
- Przeglądarka może spowolnić przy bardzo dużych plikach (>10MB)
- Użyj filtrowania aby zobaczyć tylko interesujące sekcje
- Rozważ użycie Chrome - lepsze performance

---

## Przykładowe Scenariusze

### Scenariusz 1: Szybka weryfikacja zmian
```
1. Uruchom porównanie → full_result.json
2. Otwórz result_viewer.html
3. Przeciągnij JSON
4. Kliknij "Zmodyfikowane"
5. Zobacz tylko zmiany
```

### Scenariusz 2: Analiza dodanych treści
```
1. Załaduj full_result.json
2. Kliknij "Dodane"
3. Zobacz wszystkie nowe paragrafy
```

### Scenariusz 3: Sprawdzenie tabel
```
1. Załaduj full_result.json
2. Przewiń do sekcji "Tabele"
3. Zobacz zmiany w komórkach (czerwone tło)
```

---

## Kluczowe Zalety

✅ **Szybki** - natychmiastowe ładowanie
✅ **Prosty** - intuicyjny interfejs
✅ **Diagnostyczny** - wszystkie szczegóły
✅ **Offline** - działa bez internetu
✅ **Portable** - jeden plik HTML

---

## Gotowe do Użycia! 🎉

Otwórz `result_viewer.html` w przeglądarce i przeciągnij plik JSON!
