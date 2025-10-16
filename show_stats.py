import json

with open('full_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== STATYSTYKI PORÓWNANIA ===")
stats = data['statistics']
print(f"Wszystkich paragrafów: {stats['total_paragraphs']}")
print(f"Niezmienione: {stats['unchanged_paragraphs']}")
print(f"Zmodyfikowane: {stats['modified_paragraphs']}")
print(f"Dodane: {stats['added_paragraphs']}")
print(f"Usunięte: {stats['deleted_paragraphs']}")
print(f"Łącznie zmian: {stats['total_changes']}")
print(f"Tabel: {stats['tables_count']}")
print(f"Zmodyfikowanych komórek: {stats['modified_cells']}")

print("\n=== PRZYKŁAD ZMODYFIKOWANEGO PARAGRAFU ===")
modified_paras = [p for p in data['paragraphs'] if p['type'] == 'modified']
if modified_paras:
    para = modified_paras[0]
    print(f"Index: {para['index']}")
    print(f"\nStary tekst: {para['old_text'][:100]}...")
    print(f"\nNowy tekst: {para['text'][:100]}...")
    print(f"\nLiczba zmian: {len(para['changes'])}")
    print("\nPierwsze 3 zmiany:")
    for change in para['changes'][:3]:
        print(f"  - {change['operation']}: '{change['text'][:50]}'")
