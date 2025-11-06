"""Test integracji API po wdrożeniu optymalizacji comparatora."""
import sys
import asyncio
from pathlib import Path

# Test importów
print("=" * 70)
print("🧪 TEST INTEGRACJI API - Po wdrożeniu optymalizacji")
print("=" * 70)

print("\n📦 KROK 1: Weryfikacja importów modułów...")

try:
    from models import (
        UploadResponse, ProcessRequest, ProcessResponse, ProcessingStatus,
        FullDocumentResult, ModifiedSentencesResult, AddedSentencesResult,
        DeletedSentencesResult
    )
    print("  ✅ models.py")
except Exception as e:
    print(f"  ❌ models.py - ERROR: {e}")
    sys.exit(1)

try:
    from extractor import DocumentExtractor
    print("  ✅ extractor.py")
except Exception as e:
    print(f"  ❌ extractor.py - ERROR: {e}")
    sys.exit(1)

try:
    from comparator import DocumentComparator
    print("  ✅ comparator.py (ZOPTYMALIZOWANA WERSJA)")
except Exception as e:
    print(f"  ❌ comparator.py - ERROR: {e}")
    sys.exit(1)

try:
    from storage import storage
    print("  ✅ storage.py")
except Exception as e:
    print(f"  ❌ storage.py - ERROR: {e}")
    sys.exit(1)

try:
    from main import app
    print("  ✅ main.py (FastAPI app)")
except Exception as e:
    print(f"  ❌ main.py - ERROR: {e}")
    sys.exit(1)

# Test funkcjonalności
print("\n📦 KROK 2: Weryfikacja funkcjonalności kluczowych klas...")

try:
    extractor = DocumentExtractor()
    print("  ✅ DocumentExtractor - instancja utworzona")
except Exception as e:
    print(f"  ❌ DocumentExtractor - ERROR: {e}")
    sys.exit(1)

try:
    comparator = DocumentComparator()
    print("  ✅ DocumentComparator - instancja utworzona")

    # Sprawdź optymalizacje
    has_cache = hasattr(comparator, '_diff_cache')
    has_whitespace = hasattr(comparator, '_normalize_whitespace')

    print(f"     • Cache enabled: {has_cache}")
    print(f"     • Whitespace normalization: {has_whitespace}")

    if not has_cache or not has_whitespace:
        print("  ⚠️  UWAGA: Brakuje optymalizacji!")
        sys.exit(1)

except Exception as e:
    print(f"  ❌ DocumentComparator - ERROR: {e}")
    sys.exit(1)

# Test storage
print("\n📦 KROK 3: Weryfikacja storage...")

try:
    stats = storage.get_statistics()
    print("  ✅ storage.get_statistics() działa")
    print(f"     • Total documents: {stats['total_documents']}")
    print(f"     • Total processes: {stats['total_processes']}")
    print(f"     • Completed: {stats['completed_processes']}")
    print(f"     • Processing: {stats['processing_count']}")
    print(f"     • Errors: {stats['error_count']}")
except Exception as e:
    print(f"  ❌ storage - ERROR: {e}")
    sys.exit(1)

# Test FastAPI app
print("\n📦 KROK 4: Weryfikacja FastAPI app...")

try:
    # Sprawdź dostępne endpointy
    routes = [route.path for route in app.routes]
    expected_routes = [
        "/",
        "/health",
        "/api/documents/upload",
        "/api/process",
        "/api/status/{process_id}",
        "/api/result/{process_id}/full",
        "/api/result/{process_id}/modified",
        "/api/result/{process_id}/added",
        "/api/result/{process_id}/deleted"
    ]

    print("  ✅ FastAPI app utworzona")
    print("     • Dostępne endpointy:")

    for route in expected_routes:
        if route in routes:
            print(f"       ✅ {route}")
        else:
            print(f"       ❌ {route} (BRAK!)")
            sys.exit(1)

except Exception as e:
    print(f"  ❌ FastAPI app - ERROR: {e}")
    sys.exit(1)

# Test kompatybilności comparatora
print("\n📦 KROK 5: Test kompatybilności comparatora z API...")

try:
    from extractor import ExtractedContent, TableStructure

    # Symulacja prostego porównania
    old_content = ExtractedContent(
        paragraphs=["Paragraf 1", "Paragraf 2"],
        tables=[],
        raw_text="Paragraf 1 Paragraf 2",
        metadata={}
    )

    new_content = ExtractedContent(
        paragraphs=["Paragraf 1", "Paragraf 2 zmodyfikowany"],
        tables=[],
        raw_text="Paragraf 1 Paragraf 2 zmodyfikowany",
        metadata={}
    )

    comparator = DocumentComparator()
    paragraphs, tables, statistics = comparator.compare_documents(old_content, new_content)

    print("  ✅ DocumentComparator.compare_documents() działa")
    print(f"     • Zwrócono paragrafów: {len(paragraphs)}")
    print(f"     • Zwrócono tabel: {len(tables)}")
    print(f"     • Statystyki:")
    print(f"       - Total paragraphs: {statistics.total_paragraphs}")
    print(f"       - Modified: {statistics.modified_paragraphs}")
    print(f"       - Total changes: {statistics.total_changes}")

    # Sprawdź typ zwracanego wyniku
    from models import ParagraphResult, TableResult, StatisticsResult

    if not all(isinstance(p, ParagraphResult) for p in paragraphs):
        print("  ❌ Błąd: paragraphs nie są typu ParagraphResult!")
        sys.exit(1)

    if not isinstance(statistics, StatisticsResult):
        print("  ❌ Błąd: statistics nie jest typu StatisticsResult!")
        sys.exit(1)

    print("  ✅ Typy zwracanych danych są poprawne")

except Exception as e:
    print(f"  ❌ Test kompatybilności - ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test normalizacji whitespace
print("\n📦 KROK 6: Test normalizacji whitespace...")

try:
    comparator = DocumentComparator()

    text1 = "To jest  tekst  z   wielokrotnymi    spacjami"
    text2 = "To jest tekst z wielokrotnymi spacjami"

    norm1 = comparator._normalize_whitespace(text1)
    norm2 = comparator._normalize_whitespace(text2)

    print(f"  • Tekst 1: '{text1}'")
    print(f"  • Tekst 2: '{text2}'")
    print(f"  • Znormalizowany 1: '{norm1}'")
    print(f"  • Znormalizowany 2: '{norm2}'")

    if norm1 == norm2:
        print("  ✅ Normalizacja działa poprawnie - teksty są identyczne")
    else:
        print("  ❌ Błąd: teksty różnią się po normalizacji!")
        sys.exit(1)

except Exception as e:
    print(f"  ❌ Test normalizacji - ERROR: {e}")
    sys.exit(1)

# Podsumowanie
print("\n" + "=" * 70)
print("✅ WSZYSTKIE TESTY INTEGRACJI PRZESZŁY POMYŚLNIE!")
print("=" * 70)
print("\n📊 Podsumowanie:")
print("  ✅ Wszystkie moduły importują się poprawnie")
print("  ✅ DocumentComparator z optymalizacjami działa")
print("  ✅ FastAPI app ma wszystkie wymagane endpointy")
print("  ✅ Storage działa poprawnie")
print("  ✅ Kompatybilność API zachowana (typy danych OK)")
print("  ✅ Normalizacja whitespace aktywna")
print("\n🚀 API gotowe do użycia w produkcji!")
print("=" * 70)
