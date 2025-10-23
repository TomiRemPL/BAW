# 📊 Porównanie Wersji Report Viewer

**Data:** 2025-10-23
**Cel:** Wyjaśnienie różnic między trzema wersjami viewera raportów

---

## 📁 Dostępne Wersje

### 1. **`result_viewer.html`** - Wersja Oryginalna
**Status:** Bazowa wersja viewera
**Użycie:** Referencja, archiwum

**Funkcje:**
- ✅ Drag & drop + file picker dla JSON
- ✅ Offline viewer (brak połączenia z API)
- ✅ Podstawowe bankowe kolory
- ⚠️ Brak summary box z gradientem
- ⚠️ Brak hover effects
- ⚠️ Niepełna paleta bankowa

---

### 2. **`report_viewer_offline.html`** - Offline Viewer z Pełną Paletą Bankową ⭐
**Status:** ✅ ZALECANY do użytku offline
**Użycie:** Standalone viewer do otwierania plików JSON lokalnie

**Funkcje:**
- ✅ **Drag & drop + file picker** dla JSON
- ✅ **Pełna paleta bankowa** (10 kolorów)
- ✅ **Summary box z gradientem** (duck blue → green dark → green)
- ✅ **Hover effects** na kartach i przyciskach
- ✅ **Responsive design** (desktop + mobile)
- ✅ **Print-ready** styles
- ✅ **Interaktywne filtry** paragrafów
- ✅ **Offline** - działa bez internetu

**Zalety:**
- Najlepszy do lokalnego przeglądania plików JSON
- Nie wymaga serwera ani N8N
- Można otworzyć bezpośrednio w przeglądarce
- Pełna obsługa offline

**Użycie:**
```bash
# Otwórz plik w przeglądarce
start report_viewer_offline.html
# Lub przeciągnij plik JSON na otwarty viewer
```

---

### 3. **`generate_html_report_node.js`** - N8N Node (Embedded Data)
**Status:** ✅ Zaimplementowany w workflow N8N
**Użycie:** Node w workflow N8N (automatyczne generowanie raportów)

**Funkcje:**
- ✅ **Dane wstrzyknięte** (brak potrzeby uploadu JSON)
- ✅ **Pełna paleta bankowa** (10 kolorów)
- ✅ **Summary box z gradientem**
- ✅ **Hover effects**
- ✅ **Responsive design**
- ✅ **Print-ready** styles
- ✅ **Auto-display** - raport gotowy po otwarciu
- ⚠️ **NIE offline** - wymaga workflow N8N

**Zalety:**
- Automatyczne generowanie w N8N
- Dane już załadowane (nie trzeba uploadować)
- Idealny do workflow automation

**Użycie:**
- Wykorzystywany w node "Generate HTML Report" w N8N
- Output: `comparison_report_<process_id>.html`

---

## 🔍 Szczegółowe Porównanie

### Porównanie Funkcjonalności

| Funkcja | result_viewer.html | report_viewer_offline.html ⭐ | generate_html_report_node.js |
|---------|-------------------|-------------------------------|------------------------------|
| **Upload JSON** | ✅ Drag & Drop | ✅ Drag & Drop | ❌ (dane embedded) |
| **Offline** | ✅ | ✅ | ❌ (wymaga N8N) |
| **Pełna paleta bankowa** | ⚠️ Częściowa | ✅ 10 kolorów | ✅ 10 kolorów |
| **Summary box gradient** | ❌ | ✅ | ✅ |
| **Hover effects** | ⚠️ Podstawowe | ✅ Zaawansowane | ✅ Zaawansowane |
| **Responsive** | ✅ | ✅ | ✅ |
| **Print-ready** | ✅ | ✅ | ✅ |
| **Auto-display** | ❌ | ❌ (upload) | ✅ |
| **N8N integration** | ❌ | ❌ | ✅ |

---

## 🎨 Kolory Bankowe

### Pełna Paleta (używana w wersjach 2 i 3)

| Kolor | Hex | RGB | Użycie |
|-------|-----|-----|--------|
| Jasny szary | `#F2F2F2` | 242,242,242 | Tło strony |
| Duck blue | `#009597` | 0,149,151 | H1, przyciski, linki |
| Zielony ciemny | `#70A300` | 112,163,0 | H2, dodane paragrafy |
| Zielony | `#81BC00` | 129,188,0 | Gradient (summary box) |
| Zielony jasny | `#DAF60E` | 218,246,14 | Rezerwa |
| Szary bankowy ciemny | `#7E93A3` | 126,147,163 | Niezmienione (badge) |
| Szary bankowy jasny | `#BEC9D3` | 190,201,211 | Ramki, obramowania |
| Czerwony bankowy | `#ED1B2F` | 237,27,47 | Zmiany, usunięcia |
| Ciemny szary | `#595959` | 89,89,89 | Główna czcionka |
| Średni szary | `#A6A6A6` | 166,166,166 | Obramowania tabel |

---

## 🎯 Kiedy Użyć Której Wersji?

### Use Case 1: Lokalne przeglądanie JSON
**Użyj:** `report_viewer_offline.html` ⭐

```
Masz plik JSON z wynikami porównania i chcesz go
szybko otworzyć i przejrzeć na swoim komputerze.

1. Otwórz report_viewer_offline.html w przeglądarce
2. Przeciągnij plik JSON na upload area
3. Przeglądaj raport z pełnymi bankowymi kolorami
```

### Use Case 2: Automatyzacja w N8N
**Użyj:** `generate_html_report_node.js`

```
Workflow N8N automatycznie generuje raporty HTML
po każdym porównaniu dokumentów.

1. Workflow wykonuje porównanie
2. Node "Generate HTML Report" tworzy HTML
3. HTML zapisywany do Dropbox/Email/Download
4. Użytkownik otrzymuje gotowy raport (nie musi uploadować JSON)
```

### Use Case 3: Archiwum/Backup
**Użyj:** `result_viewer.html`

```
Zachowaj oryginalną wersję jako backup lub referencję.
Nie zalecane do aktywnego użycia.
```

---

## 📊 Przykładowe Workflow

### Workflow 1: Ręczne przeglądanie

```
1. N8N workflow generuje JSON → Zapisz do pliku
2. Pobierz plik JSON na komputer
3. Otwórz report_viewer_offline.html
4. Przeciągnij JSON → Zobacz raport
```

### Workflow 2: Automatyczne HTML (ZALECANE)

```
1. N8N workflow generuje JSON
2. Node "Generate HTML Report" tworzy HTML z embedded JSON
3. HTML zapisywany na Dropbox lub wysyłany mailem
4. Użytkownik otwiera HTML → Raport gotowy (zero kroków)
```

### Workflow 3: Hybrydowe

```
1. N8N workflow generuje:
   - JSON (do archiwizacji/API)
   - HTML (do szybkiego podglądu)
2. JSON może być później otwarty w report_viewer_offline.html
3. HTML gotowy do natychmiastowego przeglądu
```

---

## 🔧 Modyfikacje

### Jak zaktualizować kolory w istniejącym viewerze?

**Krok 1:** Otwórz plik HTML w edytorze

**Krok 2:** Znajdź deklaracje kolorów w `<style>`:
```css
/* Stare kolory */
background: #f9f9f9;
border: 1px solid #ccc;
```

**Krok 3:** Zastąp na bankowe:
```css
/* Nowe kolory */
background: #fafafa;
border: 1px solid #BEC9D3;
```

**Krok 4:** Dodaj gradient do summary box:
```css
.summary-box {
    background: linear-gradient(135deg, #009597 0%, #70A300 50%, #81BC00 100%);
    color: white;
    padding: 30px;
    border-radius: 8px;
    margin: 30px 0;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 149, 151, 0.3);
}
```

---

## 📝 Changelog

### v3.0 - report_viewer_offline.html (2025-10-23)
- ✅ Pełna paleta bankowa (10 kolorów)
- ✅ Summary box z gradientem
- ✅ Zaawansowane hover effects
- ✅ Poprawione kolory obramowań (#BEC9D3 zamiast #ccc)
- ✅ Szary bankowy dla niezmienione (#7E93A3)
- ✅ Lepsze style print
- ✅ Ulepszone responsive design

### v2.0 - generate_html_report_node.js (2025-10-23)
- ✅ Node dla N8N
- ✅ Embedded JSON data
- ✅ Pełna paleta bankowa
- ✅ Auto-display bez uploadu

### v1.0 - result_viewer.html (2025-10-21)
- ✅ Bazowa wersja viewera
- ✅ Drag & drop upload
- ⚠️ Częściowa paleta bankowa

---

## 🚀 Rekomendacje

### Dla użytkowników końcowych:
**Użyj:** `report_viewer_offline.html` ⭐
- Najlepsze doświadczenie offline
- Pełne bankowe kolory
- Hover effects i smooth animations

### Dla automatyzacji N8N:
**Użyj:** `generate_html_report_node.js` (node w workflow)
- Zero manual steps
- Auto-generated reports
- Ready to open (no upload needed)

### Dla developerów:
**Użyj:** Wszystkich trzech
- `result_viewer.html` - referencja
- `report_viewer_offline.html` - testing lokalnie
- `generate_html_report_node.js` - production N8N

---

**Autor:** BAW Project
**Data:** 2025-10-23
**Wersja dokumentu:** 1.0
