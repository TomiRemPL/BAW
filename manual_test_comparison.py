"""Test script to verify the comparison algorithm."""
import sys
sys.path.append('.')

from processors.extractor import DocumentExtractor
from processors.comparator import DocumentComparator

# Extract documents
print("Extracting documents...")
extractor = DocumentExtractor(verbose=True)
old_content = extractor.extract("stara_wersja/dokument.docx")
new_content = extractor.extract("nowa_wersja/dokument.docx")

print(f"\nOld document: {len(old_content.paragraphs)} paragraphs")
print(f"New document: {len(new_content.paragraphs)} paragraphs")

# Compare
print("\nComparing documents...")
comparator = DocumentComparator()
diff_result = comparator.compare(old_content, new_content)

# Print statistics
print("\n=== COMPARISON RESULTS ===")
print(f"Added: {diff_result.statistics.added_count}")
print(f"Removed: {diff_result.statistics.removed_count}")
print(f"Modified: {diff_result.statistics.modified_count}")
print(f"Moved: {diff_result.statistics.moved_count}")
print(f"Unchanged: {diff_result.statistics.unchanged_count}")
print(f"Total changes: {diff_result.statistics.total_changes}")

# Show first few modifications with details
if diff_result.modified_paragraphs:
    print(f"\n=== MODIFIED PARAGRAPHS ({len(diff_result.modified_paragraphs)}) ===")
    for i, mod in enumerate(diff_result.modified_paragraphs[:3]):
        print(f"\n--- Modification {i+1} at index {mod.index} ---")
        print(f"OLD: {mod.old_text[:100]}...")
        print(f"NEW: {mod.new_text[:100]}...")
        print(f"Changes: {len(mod.changes)} operations")

        # Show inline diff
        print("\nInline diff:")
        for operation, text in mod.changes:
            if operation == -1:
                print(f"[-{text[:50]}]", end="")
            elif operation == 1:
                print(f"[+{text[:50]}]", end="")
            else:
                print(text[:50], end="")
        print()

# Show some added/removed for comparison
if diff_result.added_paragraphs:
    print(f"\n=== ADDED PARAGRAPHS ({len(diff_result.added_paragraphs)}) ===")
    for idx, text in diff_result.added_paragraphs[:2]:
        print(f"Index {idx}: {text[:100]}...")

if diff_result.removed_paragraphs:
    print(f"\n=== REMOVED PARAGRAPHS ({len(diff_result.removed_paragraphs)}) ===")
    for idx, text in diff_result.removed_paragraphs[:2]:
        print(f"Index {idx}: {text[:100]}...")
