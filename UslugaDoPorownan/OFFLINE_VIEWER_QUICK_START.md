# 🚀 Quick Start: Offline Report Viewer

**Plik:** `report_viewer_offline.html`
**Czas setup:** 0 minut (gotowy do użycia!)

---

## 📋 Szybki Start

### Krok 1: Otwórz viewer w przeglądarce

**Windows:**
```bash
# W Eksploratorze:
Kliknij dwukrotnie na: report_viewer_offline.html

# Lub z terminala:
start report_viewer_offline.html
```

**Linux/Mac:**
```bash
# W terminalu:
open report_viewer_offline.html  # Mac
xdg-open report_viewer_offline.html  # Linux
```

### Krok 2: Załaduj plik JSON

**Opcja A: Drag & Drop (ZALECANE)**
1. Otwórz folder z plikiem JSON
2. Przeciągnij plik JSON na upload area
3. Upuść - raport się wyświetli natychmiast!

**Opcja B: File Picker**
1. Kliknij przycisk "Wybierz plik JSON"
2. Wybierz plik z dysku
3. Raport się wyświetli

### Krok 3: Przeglądaj raport

Gotowe! Możesz teraz:
- 📊 Zobaczyć **Summary Box** z gradientem
- 📈 Przejrzeć **statystyki** (wszystkie, zmodyfikowane, dodane, usunięte)
- 🔍 Użyć **filtrów** do sortowania paragrafów
- 📋 Zobaczyć **tabele** z highlightowanymi zmianami
- 🖨️ **Wydrukować** raport
- 🔄 **Załadować inny plik** JSON

---

## 🎨 Features

### Summary Box
Gradient box na górze z 4 głównymi metrykami:
- Łącznie zmian
- Zmodyfikowane
- Dodane
- Usunięte

### Interaktywne Filtry
```
[Wszystkie] [Zmodyfikowane] [Dodane] [Usunięte] [Niezmienione]
```
Kliknij żeby pokazać tylko wybrane paragrafy.

### Karty Statystyk
6 kart z hover effects:
- Wszystkie paragrafy
- Niezmienione
- Zmodyfikowane
- Dodane
- Usunięte
- Zmodyfikowane komórki

### Paragrafy
Każdy paragraf zawiera:
- Numer paragrafu
- Badge z typem (kolor bankowy)
- Treść paragrafu
- Szczegółowe zmiany (insert/delete)
- Stara treść (dla zmodyfikowanych)

### Tabele
- Nagłówki (duck blue background)
- Zmodyfikowane komórki (red background)
- Lista zmian pod każdą tabelą

---

## 💡 Przykłady Użycia

### Przykład 1: Przeglądanie lokalnego pliku
```bash
# Masz: comparison_result_abc123.json
# Chcesz: Szybko zobaczyć wyniki

1. Otwórz report_viewer_offline.html w Chrome/Firefox/Edge
2. Przeciągnij comparison_result_abc123.json na upload area
3. Przeglądaj raport z pełnymi bankowymi kolorami
```

### Przykład 2: Wydrukowanie raportu
```bash
1. Załaduj JSON do viewera
2. Kliknij przycisk "🖨️ Drukuj raport"
3. Wybierz drukarkę lub "Save as PDF"
4. Otrzymasz czytelny PDF z raportami (bez upload area i filtrów)
```

### Przykład 3: Porównanie kilku plików
```bash
1. Otwórz viewer, załaduj plik1.json
2. Przejrzyj wyniki
3. Kliknij "🔄 Załaduj inny plik"
4. Załaduj plik2.json
5. Porównaj różnice
```

---

## 🎨 Bankowe Kolory

Viewer używa oficjalnej palety Credit Agricole:

### Główne Kolory
- **Duck blue #009597** - Nagłówki H1, przyciski, linki
- **Zielony ciemny #70A300** - Nagłówki H2, dodane paragrafy
- **Zielony #81BC00** - Gradient (summary box)
- **Czerwony bankowy #ED1B2F** - Zmiany, usunięcia

### Kolory Pomocnicze
- **Jasny szary #F2F2F2** - Tło strony
- **Ciemny szary #595959** - Główna czcionka
- **Średni szary #A6A6A6** - Obramowania tabel
- **Szary bankowy ciemny #7E93A3** - Badge "niezmienione"
- **Szary bankowy jasny #BEC9D3** - Ramki, obramowania

---

## ❓ FAQ

### Q: Czy muszę być online?
**A:** NIE! Viewer działa w 100% offline. Nie wymaga internetu ani serwera.

### Q: Jakie przeglądarki są wspierane?
**A:** Wszystkie nowoczesne przeglądarki:
- ✅ Google Chrome / Chromium / Edge
- ✅ Mozilla Firefox
- ✅ Safari (Mac)
- ✅ Opera
- ⚠️ Internet Explorer (nie testowany)

### Q: Czy mogę modyfikować kolory?
**A:** TAK! Otwórz plik w edytorze tekstowym i edytuj wartości CSS w sekcji `<style>`.

### Q: Gdzie są moje pliki JSON?
**A:** Viewer nie zapisuje plików. Ładuje je tylko do pamięci przeglądarki. Twoje pliki JSON pozostają w oryginalnej lokalizacji.

### Q: Czy mogę użyć tego na serwerze?
**A:** TAK, ale nie musisz. Możesz:
- Otworzyć lokalnie (double-click)
- Wgrać na serwer (hosting statyczny)
- Wysłać mailem (jako attachment)

### Q: Jaka jest różnica między tym a N8N node?
**A:**

| Feature | Offline Viewer | N8N Node |
|---------|----------------|----------|
| Upload JSON | ✅ Tak | ❌ Nie (embedded) |
| Offline | ✅ Tak | ❌ Nie |
| Use case | Lokalny podgląd | Automatyzacja |

Używaj offline viewera do **ręcznego przeglądania** plików JSON.
Używaj N8N node do **automatycznego generowania** raportów HTML.

---

## 🔧 Troubleshooting

### Problem: Plik JSON nie ładuje się
**Rozwiązanie:**
1. Sprawdź czy plik ma rozszerzenie `.json`
2. Otwórz plik w edytorze tekstowym i sprawdź czy jest poprawny JSON
3. Użyj walidatora JSON online: https://jsonlint.com

### Problem: Kolory nie wyświetlają się
**Rozwiązanie:**
1. Upewnij się, że używasz nowoczesnej przeglądarki
2. Wyczyść cache przeglądarki (Ctrl+Shift+Delete)
3. Otwórz plik ponownie

### Problem: Drag & drop nie działa
**Rozwiązanie:**
1. Użyj przycisku "Wybierz plik JSON"
2. Sprawdź czy przeglądarka ma włączoną obsługę JavaScript
3. Spróbuj innej przeglądarki

### Problem: Raport jest pusty
**Rozwiązanie:**
1. Sprawdź czy plik JSON zawiera pole `paragraphs` i `statistics`
2. Otwórz console przeglądarki (F12) i sprawdź błędy
3. Upewnij się, że JSON ma poprawną strukturę (zgodną z API)

---

## 📚 Struktura JSON

Viewer oczekuje JSON w następującym formacie:

```json
{
  "process_id": "abc-123",
  "document_pair_id": "xyz-456",
  "generated_at": "2025-10-23T10:30:00Z",
  "statistics": {
    "total_paragraphs": 50,
    "unchanged_paragraphs": 30,
    "modified_paragraphs": 10,
    "added_paragraphs": 5,
    "deleted_paragraphs": 5,
    "total_changes": 20,
    "tables_count": 2,
    "modified_cells": 8
  },
  "paragraphs": [
    {
      "index": 1,
      "type": "unchanged",
      "text": "Treść paragrafu..."
    },
    {
      "index": 2,
      "type": "modified",
      "text": "Nowa treść...",
      "old_text": "Stara treść...",
      "changes": [
        {"operation": "equal", "text": "Niezmieniony tekst"},
        {"operation": "delete", "text": "Usunięty"},
        {"operation": "insert", "text": "Dodany"}
      ]
    }
  ],
  "tables": [
    {
      "index": 1,
      "rows": [
        ["Header1", "Header2"],
        ["Cell1", "Cell2"]
      ],
      "changes": [
        {
          "row_index": 1,
          "col_index": 1,
          "old_value": "Stara",
          "new_value": "Nowa"
        }
      ]
    }
  ]
}
```

---

## 🎯 Best Practices

### 1. Nazwnictwo plików JSON
```bash
# Dobre nazewnictwo:
comparison_2025-10-23_document1_vs_document2.json
result_abc123_20251023.json

# Złe nazewnictwo:
wynik.json
test.json
```

### 2. Organizacja plików
```
Documents/
├── reports/
│   ├── 2025-10-23/
│   │   ├── comparison1.json
│   │   ├── comparison2.json
│   │   └── comparison3.json
│   └── 2025-10-22/
│       └── comparison_old.json
└── viewers/
    └── report_viewer_offline.html
```

### 3. Backup
```bash
# Zawsze zachowaj kopię JSON
cp comparison_result.json backups/comparison_result_$(date +%Y%m%d).json
```

---

## 🔗 Linki

- **API Documentation:** `C:\Projects\BAW\UslugaDoPorownan\API_DOCUMENTATION.md`
- **Porównanie viewerów:** `C:\Projects\BAW\UslugaDoPorownan\VIEWER_COMPARISON.md`
- **N8N Integration:** `C:\Projects\BAW\UslugaDoPorownan\N8N_INTEGRATION.md`
- **Progress Log:** `C:\Projects\BAW\PROGRESS_LOG.md`

---

**Autor:** BAW Project
**Data:** 2025-10-23
**Wersja:** 1.0 (report_viewer_offline.html v3.0)
