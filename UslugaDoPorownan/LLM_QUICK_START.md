# 🤖 LLM Analysis - Quick Start

## Co Masz Teraz

✅ **Gotowe prompty** do analizy `full_result.json` przez AI
✅ **System prompt** - instrukcje dla modelu
✅ **User prompt** - szablon zapytania
✅ **Przykłady użycia** - Python, n8n, API
✅ **Przykładowa odpowiedź** - jak wygląda raport

---

## 📁 Pliki

| Plik | Opis | Użycie |
|------|------|--------|
| `LLM_PROMPT_FULL_RESULT.md` | Pełna dokumentacja promptów | Przeczytaj |
| `prompt_system.txt` | System prompt (gotowy) | Skopiuj |
| `prompt_user.txt` | User prompt (szablon) | Skopiuj + dostosuj |
| `EXAMPLE_LLM_USAGE.md` | Praktyczne przykłady | Implementuj |
| `LLM_QUICK_START.md` | Ten plik | Start |

---

## ⚡ Szybki Start (2 minuty)

### Krok 1: Otwórz Claude / ChatGPT / Gemini

### Krok 2: Skopiuj System Prompt

Otwórz: `prompt_system.txt`
Skopiuj całość
Wklej jako "System Prompt" lub "Instrukcja systemowa"

### Krok 3: Skopiuj User Prompt + JSON

Otwórz: `prompt_user.txt`
Skopiuj całość
Znajdź miejsce: `[WKLEJ TUTAJ ZAWARTOŚĆ full_result.json]`
Wklej zawartość swojego pliku JSON
Dostosuj kontekst w linii: `Kontekst: [...]`

### Krok 4: Wyślij i Otrzymaj Raport

AI wygeneruje szczegółowy raport zawierający:
- Executive Summary
- Zmiany Krytyczne
- Zmiany Istotne
- Zmiany Mniejsze
- Dodane/Usunięte Treści
- Rekomendacje

---

## 🎯 Użycie w n8n

### Workflow:

```
1. Get Full Result (HTTP Request)
    ↓
2. Read System Prompt (Read File: prompt_system.txt)
    ↓
3. AI Analysis (OpenAI/Anthropic Node)
    - System: {{ $('Read System Prompt').item.json }}
    - User: "Przeanalizuj: {{ JSON.stringify($('Get Full Result').item.json) }}"
    ↓
4. Send Report (Email/Slack/Save)
```

### Konfiguracja Node'a AI:

**OpenAI Node:**
```
Model: gpt-4-turbo-preview
System Message: [zawartość prompt_system.txt]
User Message: [zawartość prompt_user.txt + JSON]
Max Tokens: 4000
```

**Anthropic (Claude) Node:**
```
Model: claude-3-5-sonnet-20241022
System: [zawartość prompt_system.txt]
Prompt: [zawartość prompt_user.txt + JSON]
Max Tokens: 4000
```

---

## 💻 Użycie w Python

### Prosty Skrypt:

```python
import json
import anthropic  # lub openai

# 1. Wczytaj pliki
with open('prompt_system.txt', 'r', encoding='utf-8') as f:
    system_prompt = f.read()

with open('prompt_user.txt', 'r', encoding='utf-8') as f:
    user_prompt = f.read()

with open('full_result.json', 'r', encoding='utf-8') as f:
    result_data = json.load(f)

# 2. Wstaw JSON do promptu
json_str = json.dumps(result_data, ensure_ascii=False, indent=2)
user_final = user_prompt.replace(
    '[WKLEJ TUTAJ ZAWARTOŚĆ full_result.json]',
    json_str
)

# 3. Wywołaj AI
client = anthropic.Anthropic(api_key="your-key")
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4000,
    system=system_prompt,
    messages=[{"role": "user", "content": user_final}]
)

# 4. Wyświetl/Zapisz raport
print(response.content[0].text)

# Opcjonalnie: zapisz do pliku
with open('ai_report.md', 'w', encoding='utf-8') as f:
    f.write(response.content[0].text)
```

---

## 🔧 Dostosowania

### Zmień Kontekst Domenowy:

W `prompt_user.txt` znajdź linię:
```
Kontekst: [opisz domenę dokumentu]
```

Zmień na np.:
- `Kontekst: Polityka Zarządzania Ryzykiem ICT - dokument bankowy, wymogi DORA`
- `Kontekst: Umowa SLA - dokument techniczny, parametry wydajności`
- `Kontekst: Regulamin Pracy - dokument HR, przepisy prawa pracy`

### Dodaj Specyficzne Pytania:

Na końcu User Prompt dodaj:
```
Dodatkowo odpowiedz na pytania:
1. Czy zmiany są zgodne z RODO?
2. Czy wymaga to zgody Zarządu?
3. Jaki jest szacowany czas implementacji?
```

### Zmień Format Raportu:

W User Prompt zmień sekcję "FORMAT ODPOWIEDZI" na własny, np.:
```
FORMAT ODPOWIEDZI:
1. Streszczenie (max 3 zdania)
2. Top 5 najważniejszych zmian (bullet points)
3. Podsumowanie wpływu (high/medium/low)
4. Rekomendowane działania (checklist)
```

---

## 📊 Przykładowa Odpowiedź

Po wysłaniu promptu otrzymasz raport podobny do:

```markdown
# RAPORT ANALIZY ZMIAN

## EXECUTIVE SUMMARY
Wykryto 12 zmian w dokumencie, w tym 3 krytyczne dotyczące
struktury organizacyjnej. Zmiany wymagają zatwierdzenia Zarządu
i aktualizacji procedur.

## ZMIANY KRYTYCZNE

### 1. Zmiana Właściciela Polityki (Paragraf #11)
- Stare: Chief Risk Officer (CRO)
- Nowe: Chief Operating Officer (COO)
- Wpływ: Zmiana odpowiedzialności wymaga aktualizacji RACI

[... dalsze szczegóły ...]

## REKOMENDACJE
1. Aktualizacja matrycy odpowiedzialności ⚠️
2. Komunikacja zmian do stakeholderów 📢
3. Weryfikacja zgodności z DORA ✓
```

---

## 🎓 Best Practices

### ✅ DO:
- Dodawaj kontekst domenowy
- Określ cel analizy (compliance/technical/business)
- Wskazuj na co zwrócić szczególną uwagę
- Proś o konkretny format odpowiedzi
- Testuj na małych plikach najpierw

### ❌ DON'T:
- Nie wysyłaj wrażliwych danych do publicznych API
- Nie używaj zbyt dużych plików (>100KB) bez filtrowania
- Nie ignoruj kontekstu biznesowego
- Nie polegaj tylko na AI - weryfikuj wyniki
- Nie używaj starych modeli (GPT-3.5, Claude-2)

---

## 💰 Szacunkowe Koszty

### Przykładowy plik (20KB JSON):

| Model | Tokeny Input | Tokeny Output | Koszt |
|-------|--------------|---------------|-------|
| GPT-4 Turbo | ~8000 | ~2000 | ~$0.12 |
| Claude Sonnet | ~8000 | ~2000 | ~$0.06 |
| Gemini Pro | ~8000 | ~2000 | ~$0.00 (darmowe do limitu) |

**Wskazówka:** Dla małych dokumentów (<50 paragrafów) koszty są minimalne.

---

## 🔐 Bezpieczeństwo

### Dane Publiczne:
✅ Możesz używać Claude.ai, ChatGPT, Gemini

### Dane Wrażliwe:
⚠️ Użyj:
- Azure OpenAI (danych nie używa do treningu)
- AWS Bedrock (własna infrastruktura)
- Lokalny model (Llama, Mistral via Ollama)

### Anonimizacja:
```python
def anonymize_json(data):
    """Zamień wrażliwe dane na placeholdery"""
    # Zamień nazwiska, numery, adresy itp.
    text = json.dumps(data)
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAZWA]', text)
    text = re.sub(r'\b\d{3}-\d{3}-\d{3}\b', '[NUMER]', text)
    return json.loads(text)
```

---

## 📚 Dalsze Materiały

- **Pełna dokumentacja:** `LLM_PROMPT_FULL_RESULT.md`
- **Przykłady kodu:** `EXAMPLE_LLM_USAGE.md`
- **API dokumentacja:** `README.md`
- **n8n integration:** `N8N_GUIDE.md`

---

## 🆘 Troubleshooting

### Problem: Token limit exceeded

**Rozwiązanie:**
- Filtruj tylko `type="modified"` przed wysłaniem
- Użyj modelu z większym limitem (GPT-4-32k, Claude-3-200k)
- Podziel dokument na części

### Problem: Niska jakość analizy

**Rozwiązanie:**
- Dodaj więcej kontekstu domenowego
- Użyj przykładów (few-shot learning)
- Zmień model na lepszy (GPT-4 zamiast 3.5)

### Problem: Zbyt ogólne odpowiedzi

**Rozwiązanie:**
- Zadaj konkretne pytania w prompcie
- Podaj template formatu odpowiedzi
- Poproś o przykłady dla każdej kategorii

---

## ✅ Checklist

Przed użyciem upewnij się:
- [ ] Masz plik `full_result.json`
- [ ] Skopiowałeś `prompt_system.txt`
- [ ] Skopiowałeś `prompt_user.txt`
- [ ] Wkleiłeś JSON do user prompt
- [ ] Dostosowałeś kontekst domenowy
- [ ] Wybrałeś platformę AI (Claude/ChatGPT/Gemini)
- [ ] Masz klucz API (jeśli używasz API)

---

## 🎉 Gotowe!

Masz wszystko co potrzebne do analizy wyników przez AI.

**Następny krok:**
1. Otwórz `prompt_system.txt` i `prompt_user.txt`
2. Skopiuj do swojego AI
3. Wklej JSON
4. Otrzymaj raport!

---

*Quick Start Guide v1.0*
*Działa z: Claude, GPT-4, Gemini, Llama*
