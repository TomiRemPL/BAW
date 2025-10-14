"""HTML report generation using Jinja2."""
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel

from processors.extractor import ExtractedContent
from processors.comparator import DiffResult, TableDiffResult, MetadataDiff
from processors.analyzer import AIAnalysisResult


logger = logging.getLogger(__name__)


class DocumentPair(BaseModel):
    """Information about a document pair."""
    name: str
    old_path: str
    new_path: str
    old_size: int
    new_size: int
    old_modified: str
    new_modified: str
    status: str  # pending, processing, completed, error
    comparison_id: Optional[str] = None  # ID of the comparison if completed


class ComparisonReport(BaseModel):
    """Complete comparison report data."""
    comparison_id: str
    document_pair: DocumentPair
    old_content: ExtractedContent
    new_content: ExtractedContent
    diff_result: DiffResult
    table_diff: TableDiffResult
    metadata_diff: MetadataDiff
    ai_analysis: Optional[AIAnalysisResult]
    generated_at: datetime


class HTMLReportGenerator:
    """Generates HTML reports using Jinja2 templates."""

    def __init__(self, template_dir: str = "templates"):
        """
        Initialize the HTML report generator.

        Args:
            template_dir: Directory containing Jinja2 templates
        """
        self.template_dir = Path(template_dir)
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

        # Add custom filters
        self.env.filters['format_datetime'] = self._format_datetime
        self.env.filters['format_number'] = self._format_number

        logger.info(f"HTMLReportGenerator initialized with template dir: {template_dir}")

    def generate_dashboard(
        self,
        document_pairs: List[DocumentPair],
        comparisons: Dict[str, str]  # comparison_id -> status
    ) -> str:
        """
        Generate dashboard HTML.

        Args:
            document_pairs: List of document pairs
            comparisons: Current comparison statuses

        Returns:
            Rendered HTML
        """
        logger.info(f"Generating dashboard for {len(document_pairs)} document pairs")

        template = self.env.get_template('dashboard.html')

        return template.render(
            document_pairs=document_pairs,
            comparisons=comparisons,
            total_pairs=len(document_pairs),
            generated_at=datetime.now()
        )

    def generate_comparison_report(
        self,
        report_data: ComparisonReport
    ) -> str:
        """
        Generate comparison report HTML.

        Args:
            report_data: Complete comparison report data

        Returns:
            Rendered HTML
        """
        logger.info(f"Generating comparison report for: {report_data.comparison_id}")

        template = self.env.get_template('comparison_report.html')

        # Prepare data for template
        context = {
            'comparison_id': report_data.comparison_id,
            'document_pair': report_data.document_pair,
            'old_meta': report_data.old_content.metadata,
            'new_meta': report_data.new_content.metadata,
            'diff': report_data.diff_result,
            'table_diff': report_data.table_diff,
            'metadata_diff': report_data.metadata_diff,
            'ai_analysis': report_data.ai_analysis,
            'generated_at': report_data.generated_at,
            'has_ai': report_data.ai_analysis is not None and report_data.ai_analysis.ai_available
        }

        return template.render(**context)

    def generate_summary(
        self,
        reports: List[ComparisonReport]
    ) -> str:
        """
        Generate summary page HTML.

        Args:
            reports: List of all completed comparison reports

        Returns:
            Rendered HTML
        """
        logger.info(f"Generating summary for {len(reports)} reports")

        template = self.env.get_template('summary.html')

        # Aggregate statistics
        total_changes = sum(r.diff_result.statistics.total_changes for r in reports)
        total_major = 0
        total_moderate = 0
        total_minor = 0

        if reports and reports[0].ai_analysis:
            for report in reports:
                if report.ai_analysis and report.ai_analysis.ai_available:
                    for change in report.ai_analysis.change_analyses:
                        if change.severity.value == "MAJOR":
                            total_major += 1
                        elif change.severity.value == "MODERATE":
                            total_moderate += 1
                        else:
                            total_minor += 1

        # Prepare chart data
        chart_data = {
            'labels': [r.document_pair.name for r in reports],
            'changes': [r.diff_result.statistics.total_changes for r in reports]
        }

        context = {
            'reports': reports,
            'total_reports': len(reports),
            'total_changes': total_changes,
            'total_major': total_major,
            'total_moderate': total_moderate,
            'total_minor': total_minor,
            'chart_data': chart_data,
            'generated_at': datetime.now()
        }

        return template.render(**context)

    @staticmethod
    def _format_datetime(dt: datetime) -> str:
        """Format datetime for display."""
        if dt is None:
            return "N/A"
        if isinstance(dt, str):
            return dt
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _format_number(num: int) -> str:
        """Format number with thousand separators."""
        return f"{num:,}"
