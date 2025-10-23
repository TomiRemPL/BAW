"""Skrypt do benchmarkingu oryginalnej vs zoptymalizowanej wersji comparatora.

Usage:
    python benchmark_comparison.py --old-doc stara_wersja/dokument.docx --new-doc nowa_wersja/dokument.docx
"""
import time
import argparse
import sys
from pathlib import Path

# Import obu wersji
from comparator import DocumentComparator as OriginalComparator
from comparator_optimized import DocumentComparator as OptimizedComparator
from extractor import DocumentExtractor


def benchmark_single(comparator, old_content, new_content, name: str) -> dict:
    """Benchmark pojedynczego comparatora."""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {name}")
    print(f"{'='*60}")

    start_time = time.time()

    paragraphs, tables, stats = comparator.compare_documents(old_content, new_content)

    elapsed = time.time() - start_time

    print(f"\n📊 Results:")
    print(f"  ├─ Total paragraphs: {stats.total_paragraphs}")
    print(f"  ├─ Unchanged: {stats.unchanged_paragraphs}")
    print(f"  ├─ Modified: {stats.modified_paragraphs}")
    print(f"  ├─ Added: {stats.added_paragraphs}")
    print(f"  ├─ Deleted: {stats.deleted_paragraphs}")
    print(f"  ├─ Total changes: {stats.total_changes}")
    print(f"  ├─ Tables: {stats.tables_count}")
    print(f"  └─ Modified cells: {stats.modified_cells}")

    print(f"\n⏱️  Time: {elapsed:.3f} seconds")

    # Cache stats dla optimized
    if hasattr(comparator, '_cache_hits'):
        total_calls = comparator._cache_hits + comparator._cache_misses
        hit_rate = (comparator._cache_hits / total_calls * 100) if total_calls > 0 else 0
        print(f"\n💾 Cache Stats:")
        print(f"  ├─ Hits: {comparator._cache_hits}")
        print(f"  ├─ Misses: {comparator._cache_misses}")
        print(f"  └─ Hit rate: {hit_rate:.1f}%")

    return {
        'name': name,
        'time': elapsed,
        'paragraphs': stats.total_paragraphs,
        'changes': stats.total_changes,
        'cache_hits': getattr(comparator, '_cache_hits', None),
        'cache_misses': getattr(comparator, '_cache_misses', None)
    }


def compare_implementations(old_file: str, new_file: str, runs: int = 3):
    """Porównaj obie implementacje."""
    print(f"\n{'#'*60}")
    print(f"# Document Comparison Benchmark")
    print(f"{'#'*60}")
    print(f"\nFiles:")
    print(f"  Old: {old_file}")
    print(f"  New: {new_file}")
    print(f"  Runs: {runs}")

    # Ekstrakcja raz (nie liczymy czasu ekstrakcji)
    print(f"\n📄 Extracting documents...")
    extractor = DocumentExtractor()

    extract_start = time.time()
    old_content = extractor.extract(old_file)
    new_content = extractor.extract(new_file)
    extract_time = time.time() - extract_start

    print(f"✓ Extraction completed in {extract_time:.3f}s")
    print(f"  ├─ Old doc paragraphs: {len(old_content.paragraphs)}")
    print(f"  ├─ New doc paragraphs: {len(new_content.paragraphs)}")
    print(f"  ├─ Old doc tables: {len(old_content.tables)}")
    print(f"  └─ New doc tables: {len(new_content.tables)}")

    # Warmup (oba comparatory)
    print(f"\n🔥 Warmup run...")
    OriginalComparator().compare_documents(old_content, new_content)
    OptimizedComparator().compare_documents(old_content, new_content)
    print(f"✓ Warmup completed")

    # Benchmark obu wersji
    original_times = []
    optimized_times = []

    for run in range(runs):
        print(f"\n{'─'*60}")
        print(f"Run {run + 1}/{runs}")
        print(f"{'─'*60}")

        # Original
        original = OriginalComparator()
        result_original = benchmark_single(original, old_content, new_content, "Original")
        original_times.append(result_original['time'])

        # Optimized
        optimized = OptimizedComparator()
        result_optimized = benchmark_single(optimized, old_content, new_content, "Optimized")
        optimized_times.append(result_optimized['time'])

        # Porównanie dla tego run
        speedup = ((result_original['time'] - result_optimized['time']) / result_original['time']) * 100
        print(f"\n🚀 Run {run + 1} Speedup: {speedup:.1f}%")

    # Podsumowanie
    print(f"\n{'='*60}")
    print(f"📈 FINAL RESULTS (average of {runs} runs)")
    print(f"{'='*60}")

    original_avg = sum(original_times) / len(original_times)
    optimized_avg = sum(optimized_times) / len(optimized_times)
    total_speedup = ((original_avg - optimized_avg) / original_avg) * 100

    print(f"\n⏱️  Original:   {original_avg:.3f}s average")
    print(f"⏱️  Optimized:  {optimized_avg:.3f}s average")
    print(f"\n🚀 Overall Speedup: {total_speedup:.1f}%")
    print(f"💡 Time saved: {original_avg - optimized_avg:.3f}s per comparison")

    # Detailed times
    print(f"\n📊 Detailed Times:")
    print(f"  Original:  {', '.join(f'{t:.3f}s' for t in original_times)}")
    print(f"  Optimized: {', '.join(f'{t:.3f}s' for t in optimized_times)}")

    # Extrapolation
    print(f"\n🔮 Extrapolation:")
    comparisons_per_day = 100
    time_saved_per_day = (original_avg - optimized_avg) * comparisons_per_day
    print(f"  If you process {comparisons_per_day} documents/day:")
    print(f"    Time saved: {time_saved_per_day:.1f}s = {time_saved_per_day/60:.1f} minutes/day")
    print(f"    Time saved per month: {time_saved_per_day * 30 / 3600:.1f} hours")

    return {
        'original_avg': original_avg,
        'optimized_avg': optimized_avg,
        'speedup': total_speedup,
        'extract_time': extract_time
    }


def main():
    parser = argparse.ArgumentParser(description='Benchmark document comparison')
    parser.add_argument('--old-doc', required=True, help='Path to old document')
    parser.add_argument('--new-doc', required=True, help='Path to new document')
    parser.add_argument('--runs', type=int, default=3, help='Number of benchmark runs (default: 3)')

    args = parser.parse_args()

    # Sprawdź czy pliki istnieją
    if not Path(args.old_doc).exists():
        print(f"❌ Error: File not found: {args.old_doc}")
        sys.exit(1)

    if not Path(args.new_doc).exists():
        print(f"❌ Error: File not found: {args.new_doc}")
        sys.exit(1)

    try:
        results = compare_implementations(args.old_doc, args.new_doc, args.runs)

        # Save results
        import json
        from datetime import datetime

        report = {
            'timestamp': datetime.now().isoformat(),
            'old_doc': args.old_doc,
            'new_doc': args.new_doc,
            'runs': args.runs,
            'results': results
        }

        report_file = f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n💾 Report saved to: {report_file}")

    except Exception as e:
        print(f"\n❌ Error during benchmark: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
