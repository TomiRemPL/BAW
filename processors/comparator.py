"""Document comparison module using diff algorithms."""
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from diff_match_patch import diff_match_patch
from pydantic import BaseModel

from .extractor import ExtractedContent, TableStructure
from exceptions import ComparisonProcessError


logger = logging.getLogger(__name__)


class ModifiedParagraph(BaseModel):
    """Represents a modified paragraph with before/after state."""
    index: int
    old_text: str
    new_text: str
    changes: List[Tuple[int, str]]  # (operation, text) where operation: -1=delete, 0=equal, 1=insert


class MovedParagraph(BaseModel):
    """Represents a paragraph that was moved."""
    text: str
    old_index: int
    new_index: int


class DiffStatistics(BaseModel):
    """Statistics about the differences found."""
    added_count: int = 0
    removed_count: int = 0
    modified_count: int = 0
    moved_count: int = 0
    unchanged_count: int = 0
    total_changes: int = 0


class DiffResult(BaseModel):
    """Result of document comparison."""
    added_paragraphs: List[Tuple[int, str]]  # (index, text)
    removed_paragraphs: List[Tuple[int, str]]  # (index, text)
    modified_paragraphs: List[ModifiedParagraph]
    moved_paragraphs: List[MovedParagraph]
    statistics: DiffStatistics


class TableDiffResult(BaseModel):
    """Result of table comparison."""
    added_rows: List[Tuple[int, int, List[str]]]  # (table_idx, row_idx, cells)
    removed_rows: List[Tuple[int, int, List[str]]]  # (table_idx, row_idx, cells)
    modified_cells: List[Tuple[int, int, int, str, str]]  # (table_idx, row_idx, col_idx, old, new)
    statistics: Dict[str, int]


class MetadataDiff(BaseModel):
    """Differences in metadata."""
    author_changed: bool = False
    old_author: Optional[str] = None
    new_author: Optional[str] = None
    date_changed: bool = False
    old_date: Optional[str] = None
    new_date: Optional[str] = None
    structural_changes: Dict[str, Tuple[int, int]] = {}  # name: (old_count, new_count)


class DocumentComparator:
    """Compares two documents and identifies differences."""

    def __init__(self):
        """Initialize the DocumentComparator."""
        self.dmp = diff_match_patch()
        # Configure diff settings
        self.dmp.Diff_Timeout = 2.0  # seconds
        self.dmp.Diff_EditCost = 4

    def compare(
        self,
        old_content: ExtractedContent,
        new_content: ExtractedContent
    ) -> DiffResult:
        """
        Compare two documents at paragraph level.

        Args:
            old_content: Content from old document
            new_content: Content from new document

        Returns:
            DiffResult with all differences identified

        Raises:
            ComparisonProcessError: If comparison fails
        """
        logger.info("Starting document comparison")

        # Validate inputs
        if old_content is None or new_content is None:
            raise ComparisonProcessError("Zawartość dokumentu nie może być None")

        try:
            # Compare paragraphs
            added, removed, modified, moved = self._compare_paragraphs(
                old_content.paragraphs,
                new_content.paragraphs
            )

            # Calculate statistics
            statistics = DiffStatistics(
                added_count=len(added),
                removed_count=len(removed),
                modified_count=len(modified),
                moved_count=len(moved),
                unchanged_count=(
                    len(old_content.paragraphs) -
                    len(removed) -
                    len(modified) -
                    len(moved)
                ),
                total_changes=len(added) + len(removed) + len(modified)
            )

            logger.info(
                f"Comparison complete: {statistics.total_changes} total changes "
                f"(added: {statistics.added_count}, removed: {statistics.removed_count}, "
                f"modified: {statistics.modified_count}, moved: {statistics.moved_count})"
            )

            return DiffResult(
                added_paragraphs=added,
                removed_paragraphs=removed,
                modified_paragraphs=modified,
                moved_paragraphs=moved,
                statistics=statistics
            )

        except ComparisonProcessError:
            raise

        except Exception as e:
            logger.error(f"Error during document comparison: {e}", exc_info=True)
            raise ComparisonProcessError(f"Błąd podczas porównywania dokumentów: {str(e)}")

    def compare_tables(
        self,
        old_tables: List[TableStructure],
        new_tables: List[TableStructure]
    ) -> TableDiffResult:
        """
        Compare tables between documents.

        Args:
            old_tables: Tables from old document
            new_tables: Tables from new document

        Returns:
            TableDiffResult with table differences

        Raises:
            ComparisonProcessError: If table comparison fails
        """
        # Validate inputs - allow empty lists but not None
        if old_tables is None or new_tables is None:
            raise ComparisonProcessError("Listy tabel nie mogą być None")

        logger.info(f"Comparing {len(old_tables)} old tables with {len(new_tables)} new tables")

        try:
            added_rows = []
            removed_rows = []
            modified_cells = []

            # Compare each table pair
            max_tables = max(len(old_tables), len(new_tables))

            for idx in range(max_tables):
                old_table = old_tables[idx] if idx < len(old_tables) else None
                new_table = new_tables[idx] if idx < len(new_tables) else None

                if old_table is None and new_table is not None:
                    # Entire table added
                    for row_idx, row in enumerate(new_table.rows):
                        added_rows.append((idx, row_idx, row))

                elif old_table is not None and new_table is None:
                    # Entire table removed
                    for row_idx, row in enumerate(old_table.rows):
                        removed_rows.append((idx, row_idx, row))

                elif old_table is not None and new_table is not None:
                    # Compare rows
                    old_rows = old_table.rows
                    new_rows = new_table.rows

                    # Simple row-by-row comparison
                    max_rows = max(len(old_rows), len(new_rows))

                    for row_idx in range(max_rows):
                        if row_idx >= len(old_rows):
                            # Row added
                            added_rows.append((idx, row_idx, new_rows[row_idx]))
                        elif row_idx >= len(new_rows):
                            # Row removed
                            removed_rows.append((idx, row_idx, old_rows[row_idx]))
                        else:
                            # Compare cells
                            old_row = old_rows[row_idx]
                            new_row = new_rows[row_idx]
                            max_cols = max(len(old_row), len(new_row))

                            for col_idx in range(max_cols):
                                old_cell = old_row[col_idx] if col_idx < len(old_row) else ""
                                new_cell = new_row[col_idx] if col_idx < len(new_row) else ""

                                if old_cell != new_cell:
                                    modified_cells.append((idx, row_idx, col_idx, old_cell, new_cell))

            statistics = {
                "added_rows": len(added_rows),
                "removed_rows": len(removed_rows),
                "modified_cells": len(modified_cells)
            }

            logger.info(f"Table comparison complete: {statistics}")

            return TableDiffResult(
                added_rows=added_rows,
                removed_rows=removed_rows,
                modified_cells=modified_cells,
                statistics=statistics
            )

        except ComparisonProcessError:
            raise

        except Exception as e:
            logger.error(f"Error during table comparison: {e}", exc_info=True)
            raise ComparisonProcessError(f"Błąd podczas porównywania tabel: {str(e)}")

    def compare_metadata(
        self,
        old_content: ExtractedContent,
        new_content: ExtractedContent
    ) -> MetadataDiff:
        """
        Compare metadata between documents.

        Args:
            old_content: Content from old document
            new_content: Content from new document

        Returns:
            MetadataDiff with metadata differences
        """
        logger.info("Comparing metadata")

        old_meta = old_content.metadata
        new_meta = new_content.metadata

        author_changed = old_meta.author != new_meta.author
        date_changed = old_meta.last_modified != new_meta.last_modified

        structural_changes = {}
        if old_meta.paragraph_count != new_meta.paragraph_count:
            structural_changes["paragraphs"] = (
                old_meta.paragraph_count,
                new_meta.paragraph_count
            )
        if old_meta.table_count != new_meta.table_count:
            structural_changes["tables"] = (
                old_meta.table_count,
                new_meta.table_count
            )

        return MetadataDiff(
            author_changed=author_changed,
            old_author=old_meta.author,
            new_author=new_meta.author,
            date_changed=date_changed,
            old_date=str(old_meta.last_modified) if old_meta.last_modified else None,
            new_date=str(new_meta.last_modified) if new_meta.last_modified else None,
            structural_changes=structural_changes
        )

    def _compare_paragraphs(
        self,
        old_paragraphs: List[str],
        new_paragraphs: List[str]
    ) -> Tuple[List[Tuple[int, str]], List[Tuple[int, str]], List[ModifiedParagraph], List[MovedParagraph]]:
        """
        Compare paragraphs and identify added, removed, modified, and moved paragraphs.

        Returns:
            Tuple of (added, removed, modified, moved)
        """
        added = []
        removed = []
        modified = []
        moved = []

        # Track which paragraphs have been matched
        matched_old = set()
        matched_new = set()

        # Step 1: Find exact matches (unchanged and moved)
        old_set = {p: i for i, p in enumerate(old_paragraphs)}
        new_set = {p: i for i, p in enumerate(new_paragraphs)}

        for para, old_idx in old_set.items():
            if para in new_set:
                new_idx = new_set[para]
                matched_old.add(old_idx)
                matched_new.add(new_idx)

                # Check if moved
                if old_idx != new_idx:
                    moved.append(MovedParagraph(
                        text=para,
                        old_index=old_idx,
                        new_index=new_idx
                    ))

        # Step 2: Find similar paragraphs (modifications) using intelligent matching
        # Try to match similar paragraphs at similar positions first
        for old_idx, old_para in enumerate(old_paragraphs):
            if old_idx in matched_old:
                continue

            # Look for similar paragraph in nearby positions
            best_match_idx = None
            best_similarity = 0.0
            search_range = 5  # Look within 5 positions

            start = max(0, old_idx - search_range)
            end = min(len(new_paragraphs), old_idx + search_range + 1)

            for new_idx in range(start, end):
                if new_idx in matched_new:
                    continue

                new_para = new_paragraphs[new_idx]

                # Calculate similarity
                if self._are_similar(old_para, new_para, threshold=0.3):  # Lower threshold
                    # Calculate exact similarity score
                    diffs = self.dmp.diff_main(old_para, new_para)
                    levenshtein = self.dmp.diff_levenshtein(diffs)
                    max_len = max(len(old_para), len(new_para))
                    similarity = 1 - (levenshtein / max_len) if max_len > 0 else 0

                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match_idx = new_idx

            # If found a good match, mark as modified
            if best_match_idx is not None and best_similarity >= 0.3:
                new_para = new_paragraphs[best_match_idx]

                # Perform word-level diff
                diffs = self.dmp.diff_main(old_para, new_para)
                self.dmp.diff_cleanupSemantic(diffs)

                modified.append(ModifiedParagraph(
                    index=old_idx,
                    old_text=old_para,
                    new_text=new_para,
                    changes=diffs
                ))

                matched_old.add(old_idx)
                matched_new.add(best_match_idx)

        # Step 3: Mark remaining as added/removed
        for idx, para in enumerate(old_paragraphs):
            if idx not in matched_old:
                removed.append((idx, para))

        for idx, para in enumerate(new_paragraphs):
            if idx not in matched_new:
                added.append((idx, para))

        return added, removed, modified, moved

    def _are_similar(self, text1: str, text2: str, threshold: float = 0.4) -> bool:
        """
        Check if two texts are similar enough to be considered a modification.

        Args:
            text1: First text
            text2: Second text
            threshold: Similarity threshold (0-1)

        Returns:
            True if texts are similar
        """
        if not text1 or not text2:
            return False

        # Use Levenshtein distance
        diffs = self.dmp.diff_main(text1, text2)
        levenshtein = self.dmp.diff_levenshtein(diffs)
        max_len = max(len(text1), len(text2))

        if max_len == 0:
            return True

        similarity = 1 - (levenshtein / max_len)
        return similarity >= threshold
