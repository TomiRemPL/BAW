"""Skrypt do sprawdzenia wszystkich importów zewnętrznych w projekcie."""
import ast
import sys
from pathlib import Path
from collections import defaultdict


def extract_imports_from_file(file_path):
    """Wyciąga importy z pliku Python."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())

        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Pobierz główny moduł (przed pierwszą kropką)
                    module_name = alias.name.split('.')[0]
                    imports.add(module_name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Pobierz główny moduł (przed pierwszą kropką)
                    module_name = node.module.split('.')[0]
                    imports.add(module_name)

        return imports
    except Exception as e:
        print(f"Warning: Cannot parse {file_path}: {e}")
        return set()


def is_stdlib_module(module_name):
    """Sprawdza czy moduł jest ze standardowej biblioteki Python."""
    stdlib_modules = {
        'os', 'sys', 'logging', 'pathlib', 'typing', 'datetime', 'uuid',
        'asyncio', 'json', 'time', 'argparse', 'collections', 'io',
        're', 'ast', 'importlib', 'traceback', 'warnings', 'copy',
        'dataclasses', 'functools', 'itertools', 'operator', 'string',
        'math', 'random', 'tempfile', 'shutil', 'subprocess', 'threading',
        'multiprocessing', 'queue', 'socket', 'email', 'http', 'urllib',
        'xml', 'html', 'hashlib', 'hmac', 'base64', 'binascii', 'struct',
        'pickle', 'csv', 'configparser', 'enum', 'abc', 'contextlib',
        'weakref', 'gc', 'inspect', 'dis', 'pdb', 'unittest', 'doctest'
    }
    return module_name in stdlib_modules


def scan_directory(directory, exclude_dirs=None):
    """Skanuje katalog w poszukiwaniu plików Python i wyciąga importy."""
    if exclude_dirs is None:
        exclude_dirs = {'.venv', '__pycache__', '.git', 'node_modules'}

    all_imports = defaultdict(set)  # moduł -> set plików które go importują

    for py_file in Path(directory).rglob('*.py'):
        # Sprawdź czy plik nie jest w wykluczonym katalogu
        if any(excluded in py_file.parts for excluded in exclude_dirs):
            continue

        imports = extract_imports_from_file(py_file)

        # Filtruj tylko zewnętrzne (nie stdlib, nie lokalne)
        for module in imports:
            if not is_stdlib_module(module):
                # Sprawdź czy to nie lokalny import
                relative_path = py_file.relative_to(directory)
                parent_modules = [p.stem for p in relative_path.parents if p.stem]

                # Jeśli moduł nie jest w tej samej ścieżce, to jest zewnętrzny
                if module not in parent_modules and module not in ['main', 'models', 'config', 'auth', 'middleware', 'extractor', 'comparator', 'storage']:
                    all_imports[module].add(str(relative_path))

    return all_imports


def main():
    print("=" * 70)
    print("🔍 ANALIZA IMPORTÓW ZEWNĘTRZNYCH - Projekt BAW")
    print("=" * 70)

    # Skanuj oba katalogi
    print("\n📦 Skanowanie UslugaDoPorownan...")
    backend_imports = scan_directory('UslugaDoPorownan')

    print("📦 Skanowanie SecureDocCompare...")
    frontend_imports = scan_directory('SecureDocCompare')

    # Połącz importy
    all_imports = defaultdict(set)
    for module, files in backend_imports.items():
        all_imports[module].update(files)
    for module, files in frontend_imports.items():
        all_imports[module].update(files)

    # Wyświetl wyniki
    print("\n" + "=" * 70)
    print("📋 ZNALEZIONE IMPORTY ZEWNĘTRZNE")
    print("=" * 70)

    if not all_imports:
        print("\n✅ Nie znaleziono importów zewnętrznych (wszystko stdlib)")
        return

    # Posortuj alfabetycznie
    for module in sorted(all_imports.keys()):
        files = all_imports[module]
        print(f"\n📦 {module}")
        print(f"   Używany w {len(files)} plikach:")
        for file in sorted(files):
            print(f"     • {file}")

    # Mapowanie modułów do pakietów PyPI
    print("\n" + "=" * 70)
    print("📦 WYMAGANE PAKIETY PyPI")
    print("=" * 70)

    # Mapowanie: moduł importowany -> pakiet PyPI
    module_to_package = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn[standard]',
        'pydantic': 'pydantic',
        'pydantic_settings': 'pydantic-settings',
        'dotenv': 'python-dotenv',
        'jinja2': 'jinja2',
        'httpx': 'httpx',
        'docx2python': 'docx2python',
        'docx': 'python-docx',
        'diff_match_patch': 'fast-diff-match-patch',
        'pdf2docx': 'pdf2docx',
        'pdfplumber': 'pdfplumber',
        'multipart': 'python-multipart',
        'starlette': '(included in fastapi)',
    }

    required_packages = set()
    for module in sorted(all_imports.keys()):
        if module in module_to_package:
            package = module_to_package[module]
            if package != '(included in fastapi)':
                required_packages.add(package)
            print(f"  • {module:<25} → {package}")
        else:
            print(f"  • {module:<25} → ⚠️  UNKNOWN (dodaj ręcznie)")

    # Porównaj z requirements.txt
    print("\n" + "=" * 70)
    print("✅ WERYFIKACJA Z requirements.txt")
    print("=" * 70)

    # Wczytaj requirements.txt
    requirements_file = Path('requirements.txt')
    if not requirements_file.exists():
        print("\n❌ Plik requirements.txt nie istnieje!")
        return

    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements_content = f.read()

    # Sprawdź czy wszystkie pakiety są w requirements
    missing_packages = []
    for package in sorted(required_packages):
        # Sprawdź czy pakiet jest w requirements (ignorując wersje)
        package_base = package.split('[')[0].split('>=')[0].split('==')[0]

        if package_base.lower() in requirements_content.lower():
            print(f"  ✅ {package}")
        else:
            print(f"  ❌ {package} (BRAKUJE!)")
            missing_packages.append(package)

    # Podsumowanie
    print("\n" + "=" * 70)
    print("📊 PODSUMOWANIE")
    print("=" * 70)
    print(f"  Znaleziono importów zewnętrznych: {len(all_imports)}")
    print(f"  Wymaganych pakietów: {len(required_packages)}")
    print(f"  Brakujących pakietów: {len(missing_packages)}")

    if missing_packages:
        print("\n⚠️  UWAGA: Brakujące pakiety w requirements.txt:")
        for package in missing_packages:
            print(f"     • {package}")
        print("\nDodaj je do requirements.txt!")
        sys.exit(1)
    else:
        print("\n✅ Wszystkie wymagane pakiety są w requirements.txt!")

    print("=" * 70)


if __name__ == '__main__':
    main()
