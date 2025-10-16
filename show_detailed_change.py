import json

with open('modified.json', 'r', encoding='utf-8') as f:
    modified_data = json.load(f)

print("=== SZCZEGÓŁOWA ANALIZA PIERWSZEJ ZMIANY ===\n")

first = modified_data['modified_sentences'][0]
print(f"Paragraf index: {first['paragraph_index']}")
print(f"\nTekst STARY:\n{first['old_text']}\n")
print(f"Tekst NOWY:\n{first['new_text']}\n")
print("=" * 70)
print("ZNACZNIKI ZMIAN (changes):\n")

for i, change in enumerate(first['changes'], 1):
    op = change['operation']
    text = change['text']

    symbol = {
        'delete': '[-]',
        'insert': '[+]',
        'equal': '[ ]'
    }[op]

    print(f"{i}. {symbol} {op.upper():8} | {repr(text)}")

print("\n" + "=" * 70)
print("\nREKONSTRUKCJA Z OZNACZENIAMI:")
print()

result = ""
for change in first['changes']:
    op = change['operation']
    text = change['text']

    if op == 'delete':
        result += f"[USUNIĘTE: {text}]"
    elif op == 'insert':
        result += f"[DODANE: {text}]"
    else:
        result += text

print(result)
