"""
CLI dla konwersji PDF→DOCX.

Użycie:
    python -m pdf_converter.cli input.pdf output.docx
    python -m pdf_converter.cli --batch folder/ output_folder/
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import List

from .converter import PDFConverter, ConversionResult
from .config import PDFConverterConfig
from .post_processor import PostProcessor


# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_argparser() -> argparse.ArgumentParser:
    """Konfiguruje parser argumentów CLI."""
    parser = argparse.ArgumentParser(
        description='Konwersja PDF→DOCX dla dokumentów bankowych',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  # Konwersja pojedynczego pliku
  python -m pdf_converter.cli input.pdf output.docx

  # Konwersja z wymuszeniem metody
  python -m pdf_converter.cli input.pdf output.docx --method pdfplumber

  # Konwersja wsadowa
  python -m pdf_converter.cli --batch input_folder/ output_folder/

  # Konwersja z wyłączonym post-processing
  python -m pdf_converter.cli input.pdf output.docx --no-post-process

  # Konwersja z wyłączonym fallback
  python -m pdf_converter.cli input.pdf output.docx --no-fallback
        """
    )

    # Główne argumenty
    parser.add_argument(
        'input',
        type=str,
        help='Ścieżka do pliku PDF lub katalogu (z --batch)'
    )
    parser.add_argument(
        'output',
        type=str,
        help='Ścieżka do wyjściowego DOCX lub katalogu (z --batch)'
    )

    # Tryb wsadowy
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Tryb wsadowy - konwersja całego katalogu'
    )

    # Opcje konwersji
    parser.add_argument(
        '--method',
        choices=['pdf2docx', 'pdfplumber', 'auto'],
        default='auto',
        help='Metoda konwersji (domyślnie: auto z fallback)'
    )

    # Opcje konfiguracji
    parser.add_argument(
        '--no-fallback',
        action='store_true',
        help='Wyłącz automatyczny fallback do pdfplumber'
    )
    parser.add_argument(
        '--no-post-process',
        action='store_true',
        help='Wyłącz post-processing dla dokumentów prawnych'
    )
    parser.add_argument(
        '--min-quality',
        type=float,
        default=0.7,
        help='Minimalny wynik jakości (0.0-1.0) przed fallback (domyślnie: 0.7)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=60,
        help='Maksymalny czas konwersji w sekundach (domyślnie: 60)'
    )

    # Debugging
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Szczegółowe logowanie'
    )

    return parser


def convert_single_file(
    input_path: Path,
    output_path: Path,
    config: PDFConverterConfig,
    force_method: str,
    enable_post_process: bool
) -> ConversionResult:
    """
    Konwertuje pojedynczy plik.

    Args:
        input_path: Ścieżka do PDF
        output_path: Ścieżka do DOCX
        config: Konfiguracja konwertera
        force_method: Wymuszenie metody ('auto', 'pdf2docx', 'pdfplumber')
        enable_post_process: Czy włączyć post-processing

    Returns:
        ConversionResult
    """
    logger.info(f"Konwersja: {input_path} -> {output_path}")

    # Konwersja
    converter = PDFConverter(config)
    method = None if force_method == 'auto' else force_method
    result = converter.convert(input_path, output_path, force_method=method)

    # Post-processing
    if result.success and enable_post_process:
        logger.info("Post-processing...")
        processor = PostProcessor()
        processor.process(output_path)

    return result


def convert_batch(
    input_dir: Path,
    output_dir: Path,
    config: PDFConverterConfig,
    force_method: str,
    enable_post_process: bool
) -> List[ConversionResult]:
    """
    Konwertuje wsadowo wszystkie pliki PDF w katalogu.

    Args:
        input_dir: Katalog z plikami PDF
        output_dir: Katalog wyjściowy
        config: Konfiguracja konwertera
        force_method: Wymuszenie metody
        enable_post_process: Czy włączyć post-processing

    Returns:
        Lista ConversionResult
    """
    logger.info(f"Konwersja wsadowa: {input_dir} -> {output_dir}")

    # Znajdź wszystkie pliki PDF
    pdf_files = list(input_dir.glob('*.pdf'))
    logger.info(f"Znaleziono {len(pdf_files)} plików PDF")

    if not pdf_files:
        logger.warning("Brak plików PDF do konwersji")
        return []

    # Stwórz katalog wyjściowy
    output_dir.mkdir(parents=True, exist_ok=True)

    # Konwertuj każdy plik
    results = []
    for i, pdf_path in enumerate(pdf_files, 1):
        output_path = output_dir / f"{pdf_path.stem}.docx"
        logger.info(f"[{i}/{len(pdf_files)}] {pdf_path.name}")

        result = convert_single_file(
            pdf_path,
            output_path,
            config,
            force_method,
            enable_post_process
        )
        results.append(result)

        # Wyświetl wynik
        if result.success:
            logger.info(
                f"  ✓ Sukces (metoda: {result.method}, "
                f"jakość: {result.quality_score:.2f}, "
                f"czas: {result.conversion_time:.2f}s)"
            )
        else:
            logger.error(f"  ✗ Błąd: {result.error}")

    return results


def print_summary(results: List[ConversionResult]) -> None:
    """
    Wyświetla podsumowanie konwersji wsadowej.

    Args:
        results: Lista wyników konwersji
    """
    total = len(results)
    successful = sum(1 for r in results if r.success)
    failed = total - successful

    # Średnie czasy i jakość
    if successful > 0:
        avg_time = sum(r.conversion_time for r in results if r.success) / successful
        avg_quality = sum(r.quality_score for r in results if r.success) / successful
    else:
        avg_time = 0
        avg_quality = 0

    # Metody użyte
    methods_count = {}
    for r in results:
        if r.success:
            methods_count[r.method] = methods_count.get(r.method, 0) + 1

    print("\n" + "=" * 60)
    print("PODSUMOWANIE KONWERSJI")
    print("=" * 60)
    print(f"Łącznie:           {total}")
    print(f"Sukces:            {successful} ({successful/total*100:.1f}%)")
    print(f"Błędy:             {failed} ({failed/total*100:.1f}%)")
    print(f"Średni czas:       {avg_time:.2f}s")
    print(f"Średnia jakość:    {avg_quality:.2f}")
    print(f"\nMetody użyte:")
    for method, count in methods_count.items():
        print(f"  - {method}: {count}")
    print("=" * 60)


def main() -> int:
    """
    Główna funkcja CLI.

    Returns:
        Kod wyjścia (0 = sukces, 1 = błąd)
    """
    parser = setup_argparser()
    args = parser.parse_args()

    # Konfiguracja logowania
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Parsuj ścieżki
    input_path = Path(args.input)
    output_path = Path(args.output)

    # Walidacja
    if not input_path.exists():
        logger.error(f"Plik/katalog nie istnieje: {input_path}")
        return 1

    # Konfiguracja konwertera
    config = PDFConverterConfig(
        enable_fallback=not args.no_fallback,
        enable_post_processing=not args.no_post_process,
        min_quality_score=args.min_quality,
        max_conversion_time=args.timeout,
        verbose=args.verbose
    )

    try:
        if args.batch:
            # Konwersja wsadowa
            if not input_path.is_dir():
                logger.error(f"--batch wymaga katalogu wejściowego: {input_path}")
                return 1

            results = convert_batch(
                input_path,
                output_path,
                config,
                args.method,
                not args.no_post_process
            )

            # Podsumowanie
            print_summary(results)

            # Kod wyjścia
            failed_count = sum(1 for r in results if not r.success)
            return 0 if failed_count == 0 else 1

        else:
            # Konwersja pojedynczego pliku
            if not input_path.is_file():
                logger.error(f"Plik nie istnieje: {input_path}")
                return 1

            result = convert_single_file(
                input_path,
                output_path,
                config,
                args.method,
                not args.no_post_process
            )

            # Wynik
            if result.success:
                print(f"\n✓ Konwersja zakończona sukcesem!")
                print(f"  Metoda:       {result.method}")
                print(f"  Jakość:       {result.quality_score:.2f}")
                print(f"  Czas:         {result.conversion_time:.2f}s")
                print(f"  Plik:         {result.output_path}")
                return 0
            else:
                print(f"\n✗ Konwersja nie powiodła się: {result.error}")
                return 1

    except KeyboardInterrupt:
        logger.warning("\nPrzerwano przez użytkownika")
        return 1
    except Exception as e:
        logger.exception(f"Nieoczekiwany błąd: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
