# Przykład Użycia Promptu LLM

## Scenariusz
Masz plik `full_result.json` i chcesz go przeanalizować przez AI.

---

## Krok 1: Przygotuj Prompty

### System Prompt (skopiuj z `prompt_system.txt`)
```
Jesteś ekspertem w analizie porównań dokumentów...
[cała zawartość z prompt_system.txt]
```

### User Prompt (skopiuj z `prompt_user.txt` i dostosuj)
```
Przeanalizuj załączony plik full_result.json...
[cała zawartość z prompt_user.txt]

Kontekst: Polityka Zarządzania Ryzykiem ICT - dokument bankowy, wymogi DORA

Plik JSON:
[WKLEJ TUTAJ full_result.json]
```

---

## Krok 2: Wybierz Platformę AI

### Opcja A: Claude (Anthropic)

**W Claude.ai:**
1. Otwórz https://claude.ai
2. Wklej System Prompt w pierwszej wiadomości z prefiksem "System:"
3. Wklej User Prompt + JSON
4. Wyślij

**Via API:**
```python
import anthropic
import json

client = anthropic.Anthropic(api_key="your-key")

with open('full_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('prompt_system.txt', 'r', encoding='utf-8') as f:
    system = f.read()

with open('prompt_user.txt', 'r', encoding='utf-8') as f:
    user = f.read()

# Wstaw JSON do promptu
user_final = user.replace('[WKLEJ TUTAJ ZAWARTOŚĆ full_result.json]',
                          json.dumps(data, ensure_ascii=False, indent=2))

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4000,
    system=system,
    messages=[{"role": "user", "content": user_final}]
)

print(response.content[0].text)
```

### Opcja B: ChatGPT (OpenAI)

**W ChatGPT:**
1. Otwórz https://chat.openai.com
2. Wklej System Prompt z etykietą "Instrukcja systemowa:"
3. Wklej User Prompt + JSON
4. Wyślij

**Via API:**
```python
import openai
import json

client = openai.OpenAI(api_key="your-key")

with open('full_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('prompt_system.txt', 'r', encoding='utf-8') as f:
    system = f.read()

with open('prompt_user.txt', 'r', encoding='utf-8') as f:
    user = f.read()

user_final = user.replace('[WKLEJ TUTAJ ZAWARTOŚĆ full_result.json]',
                          json.dumps(data, ensure_ascii=False, indent=2))

response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": user_final}
    ]
)

print(response.choices[0].message.content)
```

### Opcja C: Gemini (Google)

**W Google AI Studio:**
1. Otwórz https://aistudio.google.com
2. Wklej System Prompt
3. Wklej User Prompt + JSON
4. Wyślij

**Via API:**
```python
import google.generativeai as genai
import json

genai.configure(api_key="your-key")

with open('full_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('prompt_system.txt', 'r', encoding='utf-8') as f:
    system = f.read()

with open('prompt_user.txt', 'r', encoding='utf-8') as f:
    user = f.read()

user_final = user.replace('[WKLEJ TUTAJ ZAWARTOŚĆ full_result.json]',
                          json.dumps(data, ensure_ascii=False, indent=2))

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(
    f"{system}\n\n{user_final}"
)

print(response.text)
```

---

## Krok 3: Integracja z n8n

### Node Configuration:

**1. HTTP Request - Get Result**
```
Method: GET
URL: http://localhost:8001/api/result/{process_id}/full
```

**2. OpenAI / Anthropic Node**
```
Model: gpt-4-turbo / claude-3-5-sonnet
System Message: {{ $('Read System Prompt').item.json.content }}
User Message:
Przeanalizuj wyniki porównania:
{{ JSON.stringify($('Get Result').item.json, null, 2) }}

Kontekst: Polityka Zarządzania Ryzykiem ICT - dokument bankowy
```

**3. Send Email / Slack**
```
Subject: Raport Zmian w Dokumencie
Body: {{ $('OpenAI').item.json.choices[0].message.content }}
```

---

## Przykładowa Odpowiedź AI

```markdown
# RAPORT ANALIZY ZMIAN W DOKUMENCIE

## EXECUTIVE SUMMARY
- Łącznie zmian: 12
- Charakterystyka: Głównie modyfikacje struktury organizacyjnej i nazewnictwa
- Ocena: Zmiany istotne, wymagające uwagi Zarządu

## ZMIANY KRYTYCZNE

### 1. Zmiana Właściciela Polityki
**Paragraf #11**
- Stare: "Właścicielem Polityki jest Chief Risk Officer (CRO)"
- Nowe: "Właścicielem Polityki jest Chief Operating Officer (COO)"
- Wpływ: KRYTYCZNY - zmiana odpowiedzialności za politykę ICT z CRO na COO.
  Wymaga aktualizacji matrycy odpowiedzialności i zgody Zarządu.

### 2. Restrukturyzacja Zespołu ICT
**Paragraf #20**
- Stare: "Zespół ds. Ryzyka ICT (ZRICT) w Departamencie Ryzyka"
- Nowe: "Biuro Odporności Cyfrowej (BOD) w Departamencie Operacji i IT"
- Wpływ: KRYTYCZNY - zmiana nazwy, lokalizacji organizacyjnej i raportowania.
  Wymaga aktualizacji organigramu i procedur.

### 3. Zmiana Nazwy Komitetu
**Paragraf #15**
- Stare: "Komitet Ryzyka ICT zbierający się co kwartał"
- Nowe: "Komitet Odporności Cyfrowej (KOC) zbierający się co miesiąc"
- Wpływ: ISTOTNY - zmiana częstotliwości posiedzeń z kwartalnej na miesięczną.
  Zwiększone wymagania czasowe dla członków.

## ZMIANY ISTOTNE

1. **Paragraf #12**: Zmiana odpowiedzialności 1LoD
2. **Paragraf #13**: Modyfikacja raportowania 2LoD
3. **Paragraf #18**: Aktualizacja definicji incydentu ICT

[... dalsze sekcje ...]

## REKOMENDACJE

### Działania Pilne:
1. Aktualizacja matrycy RACI (odpowiedzialności)
2. Komunikacja zmian do wszystkich interesariuszy
3. Aktualizacja dokumentów powiązanych (procedury, instrukcje)
4. Szkolenie dla zespołów dotyczących nowych struktur

### Weryfikacja:
1. Sprawdzić czy wszystkie odniesienia do CRO zostały zmienione na COO
2. Zweryfikować czy nowa struktura jest zgodna z wymogami DORA
3. Upewnić się że zmiana raportowania jest zatwierdzona

### Potencjalne Ryzyka:
1. WYSOKIE - Niespójność z innymi dokumentami referencyjnymi
2. ŚREDNIE - Brak jasności w nowej strukturze odpowiedzialności
3. NISKIE - Możliwe opóźnienia w implementacji zmian

## NASTĘPNE KROKI
1. Przedyskutować zmiany z Zarządem
2. Zatwierdzić nową strukturę organizacyjną
3. Zaktualizować powiązane dokumenty
4. Przeprowadzić komunikację i szkolenia
5. Monitorować implementację przez pierwsze 3 miesiące
```

---

## Krok 4: Zapisz Wynik

### Do Pliku:
```python
with open('ai_analysis_report.md', 'w', encoding='utf-8') as f:
    f.write(response.content[0].text)
```

### Do Email:
```python
import smtplib
from email.mime.text import MIMEText

msg = MIMEText(response.content[0].text)
msg['Subject'] = 'Raport Analizy Zmian w Dokumencie'
msg['From'] = 'system@example.com'
msg['To'] = 'management@example.com'

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
smtp.login('user', 'pass')
smtp.send_message(msg)
smtp.quit()
```

### Do Bazy Danych:
```python
import sqlite3

conn = sqlite3.connect('reports.db')
cursor = conn.cursor()

cursor.execute('''
INSERT INTO analysis_reports (process_id, report_text, created_at)
VALUES (?, ?, datetime('now'))
''', (process_id, response.content[0].text))

conn.commit()
conn.close()
```

---

## Zaawansowane Użycie

### 1. Automatyczna Klasyfikacja Severity

```python
def classify_severity(change):
    """Klasyfikuj zmianę jako CRITICAL/HIGH/MEDIUM/LOW"""
    critical_keywords = ['właściciel', 'odpowiedzialność', 'zarząd', 'compliance']
    high_keywords = ['komitet', 'departament', 'proces', 'procedura']

    text = f"{change.get('text', '')} {change.get('old_text', '')}".lower()

    if any(kw in text for kw in critical_keywords):
        return 'CRITICAL'
    elif any(kw in text for kw in high_keywords):
        return 'HIGH'
    elif change['type'] == 'deleted':
        return 'MEDIUM'
    else:
        return 'LOW'

# Użycie
with open('full_result.json') as f:
    data = json.load(f)

for para in data['paragraphs']:
    if para['type'] in ['modified', 'deleted']:
        severity = classify_severity(para)
        print(f"Paragraf #{para['index']}: {severity}")
```

### 2. Porównanie z Poprzednimi Wersjami

```python
# Zapisz historię analiz
analyses_history = []

current_analysis = {
    'date': datetime.now(),
    'process_id': process_id,
    'total_changes': data['statistics']['total_changes'],
    'ai_summary': response.content[0].text
}

analyses_history.append(current_analysis)

# Porównaj trendy
if len(analyses_history) > 1:
    prev = analyses_history[-2]
    curr = analyses_history[-1]

    change_delta = curr['total_changes'] - prev['total_changes']
    print(f"Zmiana w liczbie modyfikacji: {change_delta:+d}")
```

### 3. Multi-Agent Analysis

```python
# Różne AI do różnych zadań
compliance_agent = "Analizuj pod kątem compliance i regulacji"
technical_agent = "Analizuj pod kątem zmian technicznych"
business_agent = "Analizuj pod kątem wpływu biznesowego"

results = {}
for agent_name, agent_prompt in [
    ('compliance', compliance_agent),
    ('technical', technical_agent),
    ('business', business_agent)
]:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system=f"{system}\n\nSpecjalizacja: {agent_prompt}",
        messages=[{"role": "user", "content": user_final}]
    )
    results[agent_name] = response.content[0].text

# Agreguj wyniki
final_report = f"""
# COMPREHENSIVE ANALYSIS REPORT

## Compliance Perspective
{results['compliance']}

## Technical Perspective
{results['technical']}

## Business Perspective
{results['business']}
"""
```

---

## Wskazówki

### Optymalizacja Kosztów:
- Dla dużych dokumentów (>10000 tokenów) użyj modelu tańszego (gpt-3.5-turbo, claude-haiku)
- Filtruj tylko istotne zmiany przed wysłaniem do AI
- Używaj cache dla powtarzających się analiz

### Jakość Analizy:
- Dodaj kontekst domenowy (banking, legal, technical)
- Podaj przykłady podobnych zmian z przeszłości
- Użyj few-shot prompting dla lepszych wyników

### Bezpieczeństwo:
- Nie wysyłaj wrażliwych danych do publicznych AI
- Używaj Azure OpenAI / AWS Bedrock dla danych poufnych
- Anonimizuj dane przed wysłaniem (zamień nazwy na placeholdery)

---

## Gotowe Skrypty

### Pełny Skrypt Python:
```bash
# Zapisany jako: analyze_with_ai.py
python analyze_with_ai.py full_result.json
```

### n8n Workflow:
```bash
# Zaimportuj: n8n_ai_analysis_workflow.json
```

### CLI Tool:
```bash
# Interaktywne narzędzie
doc-compare-ai analyze full_result.json --output report.md
```

---

*Przykład przygotowany dla integracji z Claude, GPT-4, Gemini*
*Wersja: 1.0*
