"""Moduł porównywania dokumentów używając algorytmów diff."""
import logging
from typing import List, Tuple, Set

from diff_match_patch import diff_match_patch

from extractor import ExtractedContent, TableStructure
from models import (
    ParagraphResult, ChangeMarker, TableResult, TableCellChange,
    StatisticsResult
)


logger = logging.getLogger(__name__)


class DocumentComparator:
    """Komparator dokumentów - identyfikuje różnice."""

    def __init__(self):
        """Inicjalizacja DocumentComparator."""
        self.dmp = diff_match_patch()
        self.dmp.Diff_Timeout = 2.0
        self.dmp.Diff_EditCost = 4

    def compare_documents(
        self,
        old_content: ExtractedContent,
        new_content: ExtractedContent
    ) -> Tuple[List[ParagraphResult], List[TableResult], StatisticsResult]:
        """
        Porównanie dwóch dokumentów.

        Args:
            old_content: Treść starego dokumentu
            new_content: Treść nowego dokumentu

        Returns:
            Tuple zawierająca (paragrafy, tabele, statystyki)
        """
        logger.info("Rozpoczęcie porównywania dokumentów")

        # Porównaj paragrafy
        paragraphs = self._compare_paragraphs(
            old_content.paragraphs,
            new_content.paragraphs
        )

        # Porównaj tabele
        tables = self._compare_tables(
            old_content.tables,
            new_content.tables
        )

        # Oblicz statystyki
        statistics = self._calculate_statistics(paragraphs, tables)

        logger.info(
            f"Porównanie zakończone: {statistics.total_changes} zmian "
            f"(dodane: {statistics.added_paragraphs}, usunięte: {statistics.deleted_paragraphs}, "
            f"zmodyfikowane: {statistics.modified_paragraphs})"
        )

        return paragraphs, tables, statistics

    def _compare_paragraphs(
        self,
        old_paragraphs: List[str],
        new_paragraphs: List[str]
    ) -> List[ParagraphResult]:
        """
        Porównanie paragrafów i utworzenie wynikowej struktury.

        Zwraca listę wszystkich paragrafów z nowego dokumentu wraz ze znacznikami zmian.
        """
        results = []

        # Śledź dopasowane paragrafy
        matched_old: Set[int] = set()
        matched_new: Set[int] = set()

        # Mapowanie: new_index -> old_index dla zmodyfikowanych
        modifications = {}

        # Krok 1: Znajdź dokładne dopasowania
        old_set = {p: i for i, p in enumerate(old_paragraphs)}
        new_set = {p: i for i, p in enumerate(new_paragraphs)}

        for para, old_idx in old_set.items():
            if para in new_set:
                new_idx = new_set[para]
                matched_old.add(old_idx)
                matched_new.add(new_idx)

        # Krok 2: Znajdź podobne paragrafy (modyfikacje)
        for old_idx, old_para in enumerate(old_paragraphs):
            if old_idx in matched_old:
                continue

            best_match_idx = None
            best_similarity = 0.0
            search_range = 5

            start = max(0, old_idx - search_range)
            end = min(len(new_paragraphs), old_idx + search_range + 1)

            for new_idx in range(start, end):
                if new_idx in matched_new:
                    continue

                new_para = new_paragraphs[new_idx]

                if self._are_similar(old_para, new_para, threshold=0.3):
                    diffs = self.dmp.diff_main(old_para, new_para)
                    levenshtein = self.dmp.diff_levenshtein(diffs)
                    max_len = max(len(old_para), len(new_para))
                    similarity = 1 - (levenshtein / max_len) if max_len > 0 else 0

                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match_idx = new_idx

            if best_match_idx is not None and best_similarity >= 0.3:
                matched_old.add(old_idx)
                matched_new.add(best_match_idx)
                modifications[best_match_idx] = old_idx

        # Krok 3: Utwórz wyniki dla NOWEGO dokumentu
        for new_idx, new_para in enumerate(new_paragraphs):
            if new_idx in modifications:
                # Paragraf zmodyfikowany
                old_idx = modifications[new_idx]
                old_para = old_paragraphs[old_idx]

                # Szczegółowe diff
                diffs = self.dmp.diff_main(old_para, new_para)
                self.dmp.diff_cleanupSemantic(diffs)

                changes = [
                    ChangeMarker(
                        operation="delete" if op == -1 else ("insert" if op == 1 else "equal"),
                        text=text
                    )
                    for op, text in diffs
                ]

                results.append(ParagraphResult(
                    index=new_idx,
                    text=new_para,
                    type="modified",
                    old_text=old_para,
                    changes=changes
                ))

            elif new_idx in matched_new:
                # Paragraf niezmieniony
                results.append(ParagraphResult(
                    index=new_idx,
                    text=new_para,
                    type="unchanged",
                    old_text=None,
                    changes=None
                ))

            else:
                # Paragraf dodany
                results.append(ParagraphResult(
                    index=new_idx,
                    text=new_para,
                    type="added",
                    old_text=None,
                    changes=None
                ))

        # Dodaj usunięte paragrafy (na końcu, z indeksami z starego dokumentu)
        for old_idx, old_para in enumerate(old_paragraphs):
            if old_idx not in matched_old:
                results.append(ParagraphResult(
                    index=old_idx,
                    text=old_para,
                    type="deleted",
                    old_text=old_para,
                    changes=None
                ))

        return results

    def _compare_tables(
        self,
        old_tables: List[TableStructure],
        new_tables: List[TableStructure]
    ) -> List[TableResult]:
        """Porównanie tabel."""
        results = []

        max_tables = max(len(old_tables), len(new_tables))

        for idx in range(max_tables):
            old_table = old_tables[idx] if idx < len(old_tables) else None
            new_table = new_tables[idx] if idx < len(new_tables) else None

            if new_table is None:
                # Tabela usunięta - pomijamy w wynikach (skupiamy się na nowym dokumencie)
                continue

            if old_table is None:
                # Tabela dodana
                results.append(TableResult(
                    index=idx,
                    rows=new_table.rows,
                    changes=None
                ))
            else:
                # Porównaj komórki
                changes = []

                max_rows = max(len(old_table.rows), len(new_table.rows))
                for row_idx in range(max_rows):
                    if row_idx >= len(old_table.rows) or row_idx >= len(new_table.rows):
                        continue

                    old_row = old_table.rows[row_idx]
                    new_row = new_table.rows[row_idx]
                    max_cols = max(len(old_row), len(new_row))

                    for col_idx in range(max_cols):
                        old_cell = old_row[col_idx] if col_idx < len(old_row) else ""
                        new_cell = new_row[col_idx] if col_idx < len(new_row) else ""

                        if old_cell != new_cell:
                            diffs = self.dmp.diff_main(old_cell, new_cell)
                            self.dmp.diff_cleanupSemantic(diffs)

                            cell_changes = [
                                ChangeMarker(
                                    operation="delete" if op == -1 else ("insert" if op == 1 else "equal"),
                                    text=text
                                )
                                for op, text in diffs
                            ]

                            changes.append(TableCellChange(
                                table_index=idx,
                                row_index=row_idx,
                                col_index=col_idx,
                                old_value=old_cell,
                                new_value=new_cell,
                                changes=cell_changes
                            ))

                results.append(TableResult(
                    index=idx,
                    rows=new_table.rows,
                    changes=changes if changes else None
                ))

        return results

    def _calculate_statistics(
        self,
        paragraphs: List[ParagraphResult],
        tables: List[TableResult]
    ) -> StatisticsResult:
        """Obliczenie statystyk porównania."""
        unchanged = sum(1 for p in paragraphs if p.type == "unchanged")
        modified = sum(1 for p in paragraphs if p.type == "modified")
        added = sum(1 for p in paragraphs if p.type == "added")
        deleted = sum(1 for p in paragraphs if p.type == "deleted")

        total_changes = modified + added + deleted

        modified_cells = sum(
            len(t.changes) if t.changes else 0
            for t in tables
        )

        return StatisticsResult(
            total_paragraphs=len(paragraphs),
            unchanged_paragraphs=unchanged,
            modified_paragraphs=modified,
            added_paragraphs=added,
            deleted_paragraphs=deleted,
            total_changes=total_changes,
            tables_count=len(tables),
            modified_cells=modified_cells
        )

    def _are_similar(self, text1: str, text2: str, threshold: float = 0.4) -> bool:
        """
        Sprawdzenie czy dwa teksty są wystarczająco podobne.

        Args:
            text1: Pierwszy tekst
            text2: Drugi tekst
            threshold: Próg podobieństwa (0-1)

        Returns:
            True jeśli teksty są podobne
        """
        if not text1 or not text2:
            return False

        diffs = self.dmp.diff_main(text1, text2)
        levenshtein = self.dmp.diff_levenshtein(diffs)
        max_len = max(len(text1), len(text2))

        if max_len == 0:
            return True

        similarity = 1 - (levenshtein / max_len)
        return similarity >= threshold
