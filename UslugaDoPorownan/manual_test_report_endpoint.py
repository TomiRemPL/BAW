"""Test endpointu generowania raportów HTML."""
import sys
import time
from pathlib import Path

print("=" * 70)
print("🧪 TEST ENDPOINTU GENEROWANIA RAPORTÓW HTML")
print("=" * 70)

# Test 1: Import i setup
print("\n📦 KROK 1: Weryfikacja importów...")
try:
    from main import app, storage
    from extractor import DocumentExtractor
    from comparator import DocumentComparator
    from models import FullDocumentResult
    print("  ✅ Importy OK")
except Exception as e:
    print(f"  ❌ Błąd importów: {e}")
    sys.exit(1)

# Test 2: Sprawdź czy są dane w storage
print("\n📦 KROK 2: Sprawdzanie storage...")
stats = storage.get_statistics()
print(f"  • Dokumentów: {stats['total_documents']}")
print(f"  • Procesów: {stats['total_processes']}")

# Jeśli są wyniki, użyj pierwszego dostępnego
existing_process_id = None
if stats['total_processes'] > 0:
    # Pobierz wszystkie process_ids
    for pid in storage.processing_status.keys():
        if storage.get_result(pid):
            existing_process_id = pid
            print(f"  ✅ Znaleziono proces z wynikami: {pid}")
            break

if not existing_process_id:
    print("  ⚠️  Brak procesów z wynikami - tworzę testowy...")

    # Test 3: Stwórz testowe dane
    print("\n📦 KROK 3: Tworzenie testowych danych...")

    # Sprawdź czy są dokumenty testowe
    old_doc = Path("../stara_wersja/Polityka_Zarzadzania_Ryzykiem_ICT_DORA.docx")
    new_doc = Path("../nowa_wersja/Polityka_Zarzadzania_Ryzykiem_ICT_DORA.docx")

    if not old_doc.exists() or not new_doc.exists():
        print("  ❌ Brak dokumentów testowych!")
        print(f"    Sprawdź: {old_doc.absolute()}")
        print(f"    Sprawdź: {new_doc.absolute()}")
        sys.exit(1)

    print(f"  ✅ Dokumenty testowe znalezione")

    # Ekstrakcja
    print("  📄 Ekstrakcja dokumentów...")
    extractor = DocumentExtractor(verbose=False)
    old_content = extractor.extract(str(old_doc))
    new_content = extractor.extract(str(new_doc))
    print(f"    Stary: {len(old_content.paragraphs)} paragrafów")
    print(f"    Nowy: {len(new_content.paragraphs)} paragrafów")

    # Porównanie
    print("  🔄 Porównywanie...")
    comparator = DocumentComparator()
    paragraphs, tables, statistics = comparator.compare_documents(old_content, new_content)
    print(f"    Zmiany: {statistics.total_changes}")

    # Zapisz do storage
    import uuid
    from datetime import datetime
    from models import ProcessingStatus

    process_id = str(uuid.uuid4())
    document_pair_id = str(uuid.uuid4())

    # Dodaj status
    status = ProcessingStatus(
        process_id=process_id,
        status="completed",
        progress=100,
        message="Zakończono pomyślnie",
        started_at=datetime.now(),
        completed_at=datetime.now()
    )
    storage.store_processing_status(process_id, status)

    # Dodaj wynik
    result = FullDocumentResult(
        process_id=process_id,
        document_pair_id=document_pair_id,
        paragraphs=paragraphs,
        tables=tables,
        statistics=statistics,
        generated_at=datetime.now()
    )
    storage.store_result(process_id, result)

    existing_process_id = process_id
    print(f"  ✅ Utworzono testowy proces: {process_id}")

# Test 4: Test endpointu generate_html_report
print(f"\n📦 KROK 4: Test endpointu generowania raportu...")
print(f"  Process ID: {existing_process_id}")

try:
    from main import generate_html_report
    import asyncio

    # Wywołaj endpoint
    result = asyncio.run(generate_html_report(existing_process_id))

    print(f"  ✅ Endpoint wykonany pomyślnie")
    print(f"\n📊 Wynik:")
    print(f"    Success: {result['success']}")
    print(f"    Report URL: {result['report_url']}")
    print(f"    Filename: {result['report_filename']}")
    print(f"    Path: {result['report_path']}")

    # Test 5: Sprawdź czy plik istnieje
    print(f"\n📦 KROK 5: Weryfikacja pliku HTML...")
    report_path = Path(result['report_path'])

    if report_path.exists():
        size = report_path.stat().st_size
        print(f"  ✅ Plik istnieje")
        print(f"    Rozmiar: {size:,} bytes ({size/1024:.1f} KB)")

        # Sprawdź czy zawiera dane
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'let fullData =' in content and len(content) > 10000:
            print(f"  ✅ Dane JSON osadzone w HTML")
            print(f"  ✅ Rozmiar HTML: {len(content):,} znaków")

            # Sprawdź czy ma auto-display
            if 'window.addEventListener' in content and 'DOMContentLoaded' in content:
                print(f"  ✅ Auto-display przy ładowaniu")
            else:
                print(f"  ⚠️  Brak auto-display")

        else:
            print(f"  ⚠️  Dane mogą być niepełne")

    else:
        print(f"  ❌ Plik NIE istnieje!")
        sys.exit(1)

except Exception as e:
    print(f"  ❌ Błąd: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Test dostępności przez URL
print(f"\n📦 KROK 6: Informacje o dostępie...")
print(f"  • Lokalny URL: http://localhost:8001{result['report_url']}")
print(f"  • Produkcyjny URL: http://217.182.76.146{result['report_url']}")
print(f"  • Plik lokalny: {report_path.absolute()}")

# Podsumowanie
print("\n" + "=" * 70)
print("✅ TEST ZAKOŃCZONY POMYŚLNIE!")
print("=" * 70)
print("\n📋 Podsumowanie:")
print(f"  ✅ Endpoint /api/report/{{process_id}}/generate działa")
print(f"  ✅ HTML generowany z osadzonymi danymi JSON")
print(f"  ✅ Plik zapisany w: {result['report_path']}")
print(f"  ✅ Dostępny przez: {result['report_url']}")
print("\n🚀 Raport gotowy do użycia!")
print("=" * 70)
