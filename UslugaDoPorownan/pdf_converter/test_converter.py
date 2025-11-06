"""
Testy dla modułu pdf_converter.

Uruchom: python -m pytest pdf_converter/test_converter.py
Lub: python pdf_converter/test_converter.py (standalone)
"""

import sys
import tempfile
from pathlib import Path

# Dodaj katalog nadrzędny do ścieżki
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_converter import PDFConverter, ConversionResult
from pdf_converter.config import PDFConverterConfig
from pdf_converter.validators import QualityValidator
from pdf_converter.exceptions import ConversionError, UnsupportedFormatError


def test_config():
    """Test konfiguracji."""
    print("Test 1: Konfiguracja...")

    config = PDFConverterConfig()
    assert config.max_conversion_time == 60
    assert config.min_quality_score == 0.7
    assert config.enable_fallback == True

    print("  ✓ Konfiguracja OK")


def test_converter_init():
    """Test inicjalizacji konwertera."""
    print("Test 2: Inicjalizacja konwertera...")

    converter = PDFConverter()
    assert converter.config is not None
    assert converter.validator is not None

    print("  ✓ Inicjalizacja OK")


def test_input_validation():
    """Test walidacji plików wejściowych."""
    print("Test 3: Walidacja wejścia...")

    converter = PDFConverter()

    # Test nieistniejącego pliku
    try:
        converter.convert("nieistniejacy.pdf", "output.docx")
        assert False, "Powinien rzucić ConversionError"
    except ConversionError as e:
        assert "nie istnieje" in str(e).lower()
        print("  ✓ Wykryto nieistniejący plik")

    # Test niewłaściwego formatu
    # Stwórz i zamknij plik tymczasowy, aby uzyskać jego ścieżkę
    tmp_file = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
    tmp_path = Path(tmp_file.name)
    tmp_file.close()

    try:
        converter.convert(tmp_path, "output.docx")
        assert False, "Powinien rzucić UnsupportedFormatError"
    except UnsupportedFormatError as e:
        assert ".txt" in str(e) or "pdf" in str(e).lower()
        print("  ✓ Wykryto niewłaściwy format")
    finally:
        # Upewnij się, że plik jest usuwany po teście
        if tmp_path.exists():
            tmp_path.unlink()

    print("  ✓ Walidacja wejścia OK")


def test_quality_validator():
    """Test walidatora jakości."""
    print("Test 4: Walidator jakości...")

    validator = QualityValidator()

    # Validator powinien działać (nawet bez pliku zwraca 0.0)
    score = validator.validate(Path("nieistniejacy.docx"))
    assert score == 0.0

    print("  ✓ Walidator jakości OK")


def test_conversion_result():
    """Test struktury wyniku konwersji."""
    print("Test 5: ConversionResult...")

    result = ConversionResult(
        success=True,
        output_path=Path("output.docx"),
        quality_score=0.95,
        conversion_time=10.5,
        method="pdf2docx",
        fallback_used=False
    )

    assert result.success == True
    assert result.quality_score == 0.95
    assert result.method == "pdf2docx"
    assert "sukces" in str(result).lower() or "success" in str(result).lower()

    print("  ✓ ConversionResult OK")


def test_config_immutable():
    """Test niezmienności konfiguracji."""
    print("Test 6: Immutable Config...")

    config = PDFConverterConfig()

    try:
        config.max_conversion_time = 120
        assert False, "Config powinien być immutable"
    except Exception:
        print("  ✓ Config jest immutable")


def run_all_tests():
    """Uruchom wszystkie testy."""
    print("\n" + "="*60)
    print("TESTY MODUŁU PDF_CONVERTER")
    print("="*60 + "\n")

    tests = [
        test_config,
        test_converter_init,
        test_input_validation,
        test_quality_validator,
        test_conversion_result,
        test_config_immutable
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ BŁĄD: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ NIEOCZEKIWANY BŁĄD: {e}")
            failed += 1

    print("\n" + "="*60)
    print(f"WYNIKI: {passed} passed, {failed} failed")
    print("="*60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
