# 📥 Jak Zaimportować Workflow do n8n - Szybki Przewodnik

## 🎯 METODA 1: Import z Pliku (2 minuty)

### Krok 1: Otwórz n8n
```
http://localhost:5678
```

### Krok 2: Kliknij "+" w górnym prawym rogu

Znajdziesz tam przycisk z napisem **"Add workflow"** lub **"+"**

### Krok 3: Wybierz "Import from File"

W rozwijanym menu znajdziesz opcję:
```
☰ Import from File...
```

### Krok 4: Wybierz plik

Wskaż plik:
```
c:\Projects\BAW\UslugaDoPorownan\n8n_workflow_example.json
```

### Krok 5: Gotowe!

Workflow zostanie automatycznie załadowany z wszystkimi node'ami.

---

## 🎯 METODA 2: Import przez Menu (alternatywa)

Jeśli nie widzisz opcji "Import from File":

### Krok 1: Kliknij Menu (☰) w górnym lewym rogu

### Krok 2: Wybierz "Import workflow"

### Krok 3: Wybierz:
- **"From File"** → wybierz `n8n_workflow_example.json`
- **LUB "From URL"** (jeśli plik jest online)

---

## 🎯 METODA 3: Kopiuj-Wklej (gdy import nie działa)

### Krok 1: Otwórz plik JSON

Otwórz w Notatniku lub VS Code:
```
c:\Projects\BAW\UslugaDoPorownan\n8n_workflow_example.json
```

### Krok 2: Zaznacz wszystko i skopiuj

```
Ctrl+A (zaznacz wszystko)
Ctrl+C (skopiuj)
```

### Krok 3: W n8n użyj skrótu

```
Ctrl+I (Windows/Linux)
Cmd+I (Mac)
```

To otworzy okno importu.

### Krok 4: Wklej JSON

```
Ctrl+V (wklej)
```

Kliknij **"Import"**

---

## ⚠️ Jeśli NIC NIE DZIAŁA

Zbuduj workflow ręcznie według instrukcji w:
```
N8N_MANUAL_SETUP.md
```

---

## ✅ Po Zaimportowaniu - WAŻNE!

### 1. Dostosuj Ścieżki do Plików

Znajdź node'y:
- **"Read Old Document"**
- **"Read New Document"**

Zmień ścieżki na swoje:
```
PRZED: C:\\documents\\old_document.docx
PO:    C:\\twoja\\sciezka\\stary.docx
```

### 2. Sprawdź URL API

We wszystkich node'ach HTTP Request sprawdź czy URL to:
```
http://localhost:8001
```

Jeśli usługa działa na innym porcie lub adresie, zmień na właściwy.

### 3. Zapisz Workflow

Kliknij **"Save"** w górnym prawym rogu.

### 4. Przetestuj

Kliknij **"Execute Workflow"** (przycisk ▶ Play)

---

## 🖼️ Gdzie Kliknąć - Wizualny Przewodnik

```
┌─────────────────────────────────────────────┐
│  n8n                     [?]  [👤]  [+ ▼]  │ ← TU KLIKNIJ "+"
├─────────────────────────────────────────────┤
│                                             │
│  ┌────────────┐                             │
│  │ Workflows  │                             │
│  │            │                             │
│  │ + New      │                             │
│  │            │                             │
│  └────────────┘                             │
│                                             │
└─────────────────────────────────────────────┘
```

Po kliknięciu "+" zobaczysz menu:
```
┌────────────────────────┐
│ + Add workflow         │
│ ☰ Import from File...  │ ← TU KLIKNIJ
│ 🔗 Import from URL...  │
└────────────────────────┘
```

---

## 🔧 Najczęstsze Problemy

### Problem 1: Nie widzę opcji "Import from File"

**Rozwiązanie:**
- Sprawdź wersję n8n (powinna być > 0.200)
- Użyj Menu (☰) → Import workflow
- Użyj skrótu: `Ctrl+I`

### Problem 2: Błąd przy imporcie JSON

**Rozwiązanie:**
- Upewnij się że plik JSON jest poprawny (otwórz w edytorze)
- Spróbuj metodę kopiuj-wklej
- W ostateczności: buduj ręcznie (N8N_MANUAL_SETUP.md)

### Problem 3: Workflow nie działa po imporcie

**Rozwiązanie:**
- Sprawdź czy usługa API działa: `curl http://localhost:8001/health`
- Zaktualizuj ścieżki do plików w node'ach
- Sprawdź URL API w każdym HTTP Request node

---

## 📞 Szybki Test po Imporcie

### 1. Sprawdź czy usługa działa:

Otwórz przeglądarkę:
```
http://localhost:8001/health
```

Powinieneś zobaczyć:
```json
{"status":"healthy", ...}
```

### 2. Uruchom workflow w n8n:

Kliknij **"Execute Workflow"** (▶)

### 3. Obserwuj wykonanie:

Każdy node powinien pokazać zielony checkmark ✓

---

## 📚 Dodatkowe Zasoby

- **Pełny przewodnik n8n:** `N8N_GUIDE.md`
- **Ręczna konfiguracja:** `N8N_MANUAL_SETUP.md`
- **API dokumentacja:** `README.md`
- **Szybki start:** `QUICKSTART.md`

---

## ✅ Checklist

- [ ] n8n otwarte i działa
- [ ] Plik JSON znaleziony: `n8n_workflow_example.json`
- [ ] Workflow zaimportowany (jedna z 3 metod)
- [ ] Ścieżki do plików zaktualizowane
- [ ] URL API sprawdzone (http://localhost:8001)
- [ ] Workflow zapisany
- [ ] Test wykonany pomyślnie ✓

---

## 🎉 Gotowe!

Teraz możesz używać workflow do automatycznego porównywania dokumentów!
