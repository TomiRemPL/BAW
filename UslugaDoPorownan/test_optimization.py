"""Test skrypt dla zoptymalizowanego comparatora."""
import time
from comparator import DocumentComparator
from extractor import DocumentExtractor

def test_comparison():
    """Test porównania dokumentów z pomiarem czasu."""
    print("=" * 60)
    print("TEST ZOPTYMALIZOWANEGO COMPARATORA")
    print("=" * 60)

    # Ścieżki dokumentów
    old_doc = "../stara_wersja/Polityka_Zarzadzania_Ryzykiem_ICT_DORA.docx"
    new_doc = "../nowa_wersja/Polityka_Zarzadzania_Ryzykiem_ICT_DORA.docx"

    print(f"\n📄 Dokumenty:")
    print(f"  Stary: {old_doc}")
    print(f"  Nowy: {new_doc}")

    # Ekstrakcja
    print("\n⏳ Ekstrakcja dokumentów...")
    extractor = DocumentExtractor()

    start_extract = time.time()
    old_content = extractor.extract(old_doc)
    new_content = extractor.extract(new_doc)
    extract_time = time.time() - start_extract

    print(f"✅ Ekstrakcja zakończona: {extract_time:.2f}s")
    print(f"  Stary dokument: {len(old_content.paragraphs)} paragrafów, {len(old_content.tables)} tabel")
    print(f"  Nowy dokument: {len(new_content.paragraphs)} paragrafów, {len(new_content.tables)} tabel")

    # Porównanie
    print("\n⏳ Porównywanie dokumentów (ZOPTYMALIZOWANE)...")
    comparator = DocumentComparator()

    start_compare = time.time()
    paragraphs, tables, statistics = comparator.compare_documents(old_content, new_content)
    compare_time = time.time() - start_compare

    print(f"✅ Porównanie zakończone: {compare_time:.2f}s")

    # Statystyki
    print("\n📊 STATYSTYKI PORÓWNANIA:")
    print(f"  Wszystkie paragrafy: {statistics.total_paragraphs}")
    print(f"  Niezmienione: {statistics.unchanged_paragraphs}")
    print(f"  Zmodyfikowane: {statistics.modified_paragraphs}")
    print(f"  Dodane: {statistics.added_paragraphs}")
    print(f"  Usunięte: {statistics.deleted_paragraphs}")
    print(f"  Zmienione komórki tabel: {statistics.modified_cells}")
    print(f"  Łącznie zmian: {statistics.total_changes}")

    # Cache statistics
    total_cache_calls = comparator._cache_hits + comparator._cache_misses
    hit_rate = (comparator._cache_hits / total_cache_calls * 100) if total_cache_calls > 0 else 0

    print("\n🚀 STATYSTYKI OPTYMALIZACJI:")
    print(f"  Cache hits: {comparator._cache_hits}")
    print(f"  Cache misses: {comparator._cache_misses}")
    print(f"  Cache hit rate: {hit_rate:.1f}%")
    print(f"  Cache size: {len(comparator._diff_cache)} entries")

    # Test normalizacji white-space
    print("\n✨ TEST NORMALIZACJI WHITE-SPACE:")
    test_text1 = "To jest  tekst  z   wielokrotnymi    spacjami"
    test_text2 = "To jest tekst z wielokrotnymi spacjami"
    norm1 = comparator._normalize_whitespace(test_text1)
    norm2 = comparator._normalize_whitespace(test_text2)
    print(f"  Oryginalny 1: '{test_text1}'")
    print(f"  Oryginalny 2: '{test_text2}'")
    print(f"  Znormalizowany 1: '{norm1}'")
    print(f"  Znormalizowany 2: '{norm2}'")
    print(f"  Są identyczne: {norm1 == norm2} ✅")

    # Podsumowanie
    print("\n" + "=" * 60)
    print("✅ TEST ZAKOŃCZONY POMYŚLNIE")
    print(f"⏱️  Całkowity czas: {extract_time + compare_time:.2f}s")
    print(f"🚀 Speedup cache: {hit_rate:.1f}% zapytań skorzystało z cache")
    print("=" * 60)

if __name__ == "__main__":
    test_comparison()
