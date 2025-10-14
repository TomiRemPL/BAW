"""PDF report generation using WeasyPrint."""
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader

from exceptions import ReportGenerationError


logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generates PDF reports from HTML using WeasyPrint."""

    def __init__(self, output_dir: str = "output", template_dir: str = "templates"):
        """
        Initialize the PDF generator.

        Args:
            output_dir: Directory for output PDFs
            template_dir: Directory containing Jinja2 templates
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.template_dir = Path(template_dir)
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=True
        )

        logger.info(f"PDFGenerator initialized with output dir: {output_dir}")

    def generate_pdf(
        self,
        report_data,
        comparison_id: str,
        doc1_name: str,
        doc2_name: str
    ) -> str:
        """
        Generate PDF from comparison report data.

        Args:
            report_data: ComparisonReport object with all data
            comparison_id: Unique comparison ID
            doc1_name: Name of first document
            doc2_name: Name of second document

        Returns:
            Path to generated PDF file

        Raises:
            ReportGenerationError: If PDF generation fails
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_comparison_{doc1_name}_vs_{doc2_name}.pdf"
        filename = self._sanitize_filename(filename)

        output_path = self.output_dir / filename

        logger.info(f"Generating PDF: {output_path}")

        try:
            # Render PDF-specific template
            template = self.env.get_template('pdf_report.html')

            html_content = template.render(
                comparison_id=report_data.comparison_id,
                document_pair=report_data.document_pair,
                old_meta=report_data.old_content.metadata,
                new_meta=report_data.new_content.metadata,
                diff=report_data.diff_result,
                table_diff=report_data.table_diff,
                metadata_diff=report_data.metadata_diff,
                ai_analysis=report_data.ai_analysis,
                generated_at=report_data.generated_at,
                has_ai=report_data.ai_analysis is not None and report_data.ai_analysis.ai_available
            )

            # Validate HTML content
            if not html_content or not html_content.strip():
                raise ReportGenerationError("Wygenerowana zawartość HTML jest pusta")

            # Generate PDF using WeasyPrint
            html_doc = HTML(string=html_content, base_url=str(self.template_dir))
            html_doc.write_pdf(
                output_path,
                presentational_hints=True,
                optimize_size=('fonts', 'images')
            )

            # Verify that PDF was created
            if not output_path.exists() or output_path.stat().st_size == 0:
                raise ReportGenerationError("PDF został wygenerowany, ale jest pusty")

            logger.info(f"PDF generated successfully: {output_path} ({output_path.stat().st_size} bytes)")
            return str(output_path)

        except ReportGenerationError:
            raise

        except Exception as e:
            logger.error(f"Error generating PDF: {e}", exc_info=True)
            raise ReportGenerationError(f"Nie udało się wygenerować PDF: {str(e)}")

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename for filesystem.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename
        """
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')

        # Limit length
        if len(filename) > 200:
            name, ext = filename.rsplit('.', 1)
            filename = name[:196] + '.' + ext

        return filename
