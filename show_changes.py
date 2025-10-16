import json

print("=== ZMIENIONE PARAGRAFY (modified.json) ===")
with open('modified.json', 'r', encoding='utf-8') as f:
    modified_data = json.load(f)

print(f"Liczba zmienionych: {modified_data['total_count']}")
if modified_data['modified_sentences']:
    print("\nPierwszy przykład:")
    s = modified_data['modified_sentences'][0]
    print(f"Index: {s['paragraph_index']}")
    print(f"Stary: {s['old_text'][:80]}...")
    print(f"Nowy: {s['new_text'][:80]}...")

print("\n=== DODANE PARAGRAFY (added.json) ===")
with open('added.json', 'r', encoding='utf-8') as f:
    added_data = json.load(f)

print(f"Liczba dodanych: {added_data['total_count']}")
if added_data['added_sentences']:
    for s in added_data['added_sentences']:
        print(f"  - Index {s['paragraph_index']}: {s['text'][:60]}...")

print("\n=== USUNIĘTE PARAGRAFY (deleted.json) ===")
with open('deleted.json', 'r', encoding='utf-8') as f:
    deleted_data = json.load(f)

print(f"Liczba usuniętych: {deleted_data['total_count']}")
if deleted_data['deleted_sentences']:
    for s in deleted_data['deleted_sentences']:
        print(f"  - Index {s['paragraph_index']}: {s['text'][:60]}...")

print("\n=== SZCZEGÓŁY WSZYSTKICH ZMIAN ===")
for i, sentence in enumerate(modified_data['modified_sentences'][:5], 1):
    print(f"\n{i}. Paragraf {sentence['paragraph_index']}:")
    print(f"   Stary: {sentence['old_text'][:70]}...")
    print(f"   Nowy:  {sentence['new_text'][:70]}...")

    # Pokaż operacje
    ops = {}
    for change in sentence['changes']:
        op = change['operation']
        ops[op] = ops.get(op, 0) + 1
    print(f"   Operacje: {ops}")
