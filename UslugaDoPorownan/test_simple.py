# -*- coding: utf-8 -*-
"""
Prosty skrypt testowy dla Uslugi Porownywania Dokumentow (bez emoji)

Uzycie:
    python test_simple.py stary_dokument.docx nowy_dokument.docx
"""

import requests
import time
import json
import sys
from pathlib import Path


BASE_URL = "http://localhost:8001"


def upload_documents(old_path, new_path):
    """Zaladuj dokumenty i zwroc document_pair_id."""
    print("[>] Ladowanie dokumentow...")
    print(f"   Stary: {old_path}")
    print(f"   Nowy:  {new_path}")

    with open(old_path, 'rb') as old_file, open(new_path, 'rb') as new_file:
        files = {
            'old_document': old_file,
            'new_document': new_file
        }

        response = requests.post(f"{BASE_URL}/api/documents/upload", files=files)
        response.raise_for_status()

    result = response.json()
    document_pair_id = result['document_pair_id']
    print(f"[OK] Dokumenty zaladowane: {document_pair_id}\n")
    return document_pair_id


def start_processing(document_pair_id):
    """Rozpocznij przetwarzanie i zwroc process_id."""
    print("[>] Rozpoczynam przetwarzanie...")

    response = requests.post(
        f"{BASE_URL}/api/process",
        json={"document_pair_id": document_pair_id}
    )
    response.raise_for_status()

    result = response.json()
    process_id = result['process_id']
    print(f"[OK] Przetwarzanie wystartowalo: {process_id}\n")
    return process_id


def wait_for_completion(process_id):
    """Czekaj na zakonczenie przetwarzania."""
    print("[>] Oczekiwanie na zakonczenie...")

    while True:
        response = requests.get(f"{BASE_URL}/api/status/{process_id}")
        response.raise_for_status()

        status_data = response.json()
        status = status_data['status']
        progress = status_data.get('progress', 0)

        print(f"   Status: {status} ({progress}%)")

        if status == 'completed':
            print("[OK] Przetwarzanie zakonczone!\n")
            return status_data
        elif status == 'error':
            error = status_data.get('error', 'Unknown error')
            print(f"[ERROR] Blad: {error}")
            sys.exit(1)

        time.sleep(1)


def get_results(process_id):
    """Pobierz i wyswietl wyniki."""
    print("[>] Pobieranie wynikow...\n")

    # Pelny wynik
    response = requests.get(f"{BASE_URL}/api/result/{process_id}/full")
    response.raise_for_status()
    full_data = response.json()

    stats = full_data['statistics']

    print("=" * 70)
    print("STATYSTYKI POROWNANIA")
    print("=" * 70)
    print(f"Wszystkich paragrafow:     {stats['total_paragraphs']}")
    print(f"  - Niezmienione:          {stats['unchanged_paragraphs']}")
    print(f"  - Zmodyfikowane:         {stats['modified_paragraphs']}")
    print(f"  - Dodane:                {stats['added_paragraphs']}")
    print(f"  - Usuniete:              {stats['deleted_paragraphs']}")
    print(f"Lacznie zmian:             {stats['total_changes']}")
    print(f"Tabel:                     {stats['tables_count']}")
    print(f"Zmodyfikowanych komorek:   {stats['modified_cells']}")
    print()

    # Zmienione
    response = requests.get(f"{BASE_URL}/api/result/{process_id}/modified")
    modified_data = response.json()

    if modified_data['total_count'] > 0:
        print("=" * 70)
        print("ZMIENIONE PARAGRAFY (pierwsze 3)")
        print("=" * 70)

        for i, sentence in enumerate(modified_data['modified_sentences'][:3], 1):
            print(f"\n{i}. Paragraf {sentence['paragraph_index']}:")
            old_preview = sentence['old_text'][:80]
            new_preview = sentence['new_text'][:80]
            if len(sentence['old_text']) > 80:
                old_preview += "..."
            if len(sentence['new_text']) > 80:
                new_preview += "..."

            print(f"   STARY: {old_preview}")
            print(f"   NOWY:  {new_preview}")

            # Zlicz operacje
            ops = {}
            for change in sentence['changes']:
                op = change['operation']
                ops[op] = ops.get(op, 0) + 1

            print(f"   Operacje: {ops}")

    # Dodane
    response = requests.get(f"{BASE_URL}/api/result/{process_id}/added")
    added_data = response.json()

    if added_data['total_count'] > 0:
        print("\n" + "=" * 70)
        print("DODANE PARAGRAFY")
        print("=" * 70)
        for sentence in added_data['added_sentences']:
            text_preview = sentence['text'][:70]
            if len(sentence['text']) > 70:
                text_preview += "..."
            print(f"  - Index {sentence['paragraph_index']}: {text_preview}")

    # Usuniete
    response = requests.get(f"{BASE_URL}/api/result/{process_id}/deleted")
    deleted_data = response.json()

    if deleted_data['total_count'] > 0:
        print("\n" + "=" * 70)
        print("USUNIETE PARAGRAFY")
        print("=" * 70)
        for sentence in deleted_data['deleted_sentences']:
            text_preview = sentence['text'][:70]
            if len(sentence['text']) > 70:
                text_preview += "..."
            print(f"  - Index {sentence['paragraph_index']}: {text_preview}")

    # Zapisz do plikow
    print("\n" + "=" * 70)
    print("ZAPISYWANIE DO PLIKOW")
    print("=" * 70)

    with open('full_result.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    print("[OK] full_result.json")

    with open('modified.json', 'w', encoding='utf-8') as f:
        json.dump(modified_data, f, ensure_ascii=False, indent=2)
    print("[OK] modified.json")

    with open('added.json', 'w', encoding='utf-8') as f:
        json.dump(added_data, f, ensure_ascii=False, indent=2)
    print("[OK] added.json")

    with open('deleted.json', 'w', encoding='utf-8') as f:
        json.dump(deleted_data, f, ensure_ascii=False, indent=2)
    print("[OK] deleted.json")

    print()


def main():
    """Glowna funkcja."""
    if len(sys.argv) != 3:
        print("Uzycie: python test_simple.py stary_dokument.docx nowy_dokument.docx")
        sys.exit(1)

    old_path = sys.argv[1]
    new_path = sys.argv[2]

    # Sprawdz czy pliki istnieja
    if not Path(old_path).exists():
        print(f"[ERROR] Nie znaleziono pliku: {old_path}")
        sys.exit(1)

    if not Path(new_path).exists():
        print(f"[ERROR] Nie znaleziono pliku: {new_path}")
        sys.exit(1)

    print("=" * 70)
    print("TEST USLUGI POROWNYWANIA DOKUMENTOW")
    print("=" * 70)
    print()

    try:
        # 1. Zaladuj dokumenty
        document_pair_id = upload_documents(old_path, new_path)

        # 2. Rozpocznij przetwarzanie
        process_id = start_processing(document_pair_id)

        # 3. Czekaj na zakonczenie
        wait_for_completion(process_id)

        # 4. Pobierz wyniki
        get_results(process_id)

        print("=" * 70)
        print("[OK] TEST ZAKONCZONY POMYSLNIE!")
        print("=" * 70)

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Nie mozna polaczyc sie z usluga!")
        print("   Upewnij sie, ze usluga dziala na http://localhost:8001")
        print("   Uruchom: cd UslugaDoPorownan && python -m uvicorn main:app --port 8001")
        sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] Blad: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
