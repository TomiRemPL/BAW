"""Skrypt do sprawdzenia zależności między modułami i wykrycia circular dependencies."""
import sys
import ast
from pathlib import Path
from collections import defaultdict


def extract_imports(file_path):
    """Wyciąga importy z pliku Python."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return imports
    except Exception as e:
        print(f"Warning: Cannot parse {file_path}: {e}")
        return []


def build_dependency_graph():
    """Buduje graf zależności między modułami."""
    modules = [
        'main.py',
        'models.py',
        'extractor.py',
        'comparator.py',
        'storage.py',
    ]

    graph = defaultdict(list)

    for module in modules:
        if not Path(module).exists():
            continue

        imports = extract_imports(module)

        # Filtruj tylko lokalne importy (bez zewnętrznych bibliotek)
        local_imports = []
        for imp in imports:
            # Sprawdź czy to import lokalnego modułu
            if imp in ['models', 'extractor', 'comparator', 'storage', 'main']:
                local_imports.append(imp)
            elif imp.startswith('pdf_converter'):
                local_imports.append('pdf_converter')

        graph[module.replace('.py', '')] = list(set(local_imports))

    return graph


def detect_cycles(graph):
    """Wykrywa cykle w grafie zależności (circular dependencies)."""
    visited = set()
    rec_stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, path.copy())
                elif neighbor in rec_stack:
                    # Znaleziono cykl
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)

        rec_stack.remove(node)

    for node in graph:
        if node not in visited:
            dfs(node, [])

    return cycles


def print_dependency_graph(graph):
    """Wyświetla graf zależności."""
    print("\n" + "=" * 70)
    print("📊 GRAF ZALEŻNOŚCI MODUŁÓW")
    print("=" * 70)

    for module, dependencies in sorted(graph.items()):
        if dependencies:
            print(f"\n📦 {module}.py")
            print("  └─ importuje:")
            for dep in sorted(dependencies):
                print(f"     ├─ {dep}")
        else:
            print(f"\n📦 {module}.py")
            print("  └─ (brak lokalnych importów)")


def main():
    print("=" * 70)
    print("🔍 ANALIZA ZALEŻNOŚCI MODUŁÓW - Projekt BAW")
    print("=" * 70)

    # Buduj graf
    graph = build_dependency_graph()

    # Wyświetl graf
    print_dependency_graph(graph)

    # Wykryj circular dependencies
    print("\n" + "=" * 70)
    print("🔄 SPRAWDZANIE CIRCULAR DEPENDENCIES")
    print("=" * 70)

    cycles = detect_cycles(graph)

    if cycles:
        print("\n❌ WYKRYTO CIRCULAR DEPENDENCIES!\n")
        for i, cycle in enumerate(cycles, 1):
            print(f"Cykl {i}: {' → '.join(cycle)}")
        print("\n⚠️  UWAGA: Circular dependencies mogą powodować problemy z importami!")
        sys.exit(1)
    else:
        print("\n✅ BRAK CIRCULAR DEPENDENCIES")
        print("   Graf zależności jest acykliczny (DAG)")

    # Hierarchia zależności
    print("\n" + "=" * 70)
    print("📋 HIERARCHIA ZALEŻNOŚCI (od podstawowych do złożonych)")
    print("=" * 70)

    # Topological sort (uproszczony)
    in_degree = defaultdict(int)
    for node in graph:
        if node not in in_degree:
            in_degree[node] = 0
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    levels = []
    current_level = [node for node in graph if in_degree[node] == 0]

    while current_level:
        levels.append(sorted(current_level))
        next_level = []

        for node in current_level:
            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0 and neighbor not in next_level:
                    next_level.append(neighbor)

        current_level = next_level

    for i, level in enumerate(levels):
        print(f"\nPoziom {i + 1} (podstawowe):")
        for module in level:
            deps = graph.get(module, [])
            if deps:
                print(f"  • {module}.py → zależy od: {', '.join(deps)}")
            else:
                print(f"  • {module}.py (brak zależności)")

    # Podsumowanie
    print("\n" + "=" * 70)
    print("✅ WERYFIKACJA ZAKOŃCZONA")
    print("=" * 70)
    print(f"  Zbadano modułów: {len(graph)}")
    print(f"  Circular dependencies: {'❌ NIE' if not cycles else '⚠️ TAK'}")
    print(f"  Poziomów hierarchii: {len(levels)}")
    print("=" * 70)


if __name__ == '__main__':
    main()
