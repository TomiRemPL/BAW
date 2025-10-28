#!/usr/bin/env python3
"""
Fix N8N Workflow - MINIMALNA wersja
Usuwa WSZYSTKIE potencjalnie problematyczne parametry
"""

import json
import sys
from pathlib import Path

def minimal_fix(input_file, output_file):
    """Minimalna wersja - usuń wszystko co może powodować problemy"""
    print(f"Wczytuje workflow z: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    print(f"Czyszczenie wszystkich problematycznych opcji...")

    for node in workflow['nodes']:
        node_name = node.get('name', '')
        node_type = node.get('type', '')

        # USUŃ wszystkie 'options' które są puste lub problematyczne
        if 'parameters' in node:
            params = node['parameters']

            # Jeśli options istnieje i jest puste - usuń
            if 'options' in params:
                if not params['options'] or params['options'] == {}:
                    print(f"  Usuwam puste options z: {node_name}")
                    del params['options']
                else:
                    # Sprawdź co jest w options
                    options = params['options']

                    # Lista dozwolonych kluczy w options
                    allowed_keys = ['timeout', 'allowUnauthorizedCerts', 'redirect',
                                    'fallbackOutput', 'looseTypeValidation']

                    # Usuń wszystko co nie jest na liście
                    keys_to_remove = []
                    for key in options.keys():
                        if key not in allowed_keys:
                            keys_to_remove.append(key)

                    if keys_to_remove:
                        print(f"  Usuwam z options w {node_name}: {keys_to_remove}")
                        for key in keys_to_remove:
                            del options[key]

                    # Jeśli options jest teraz puste - usuń całość
                    if not options or options == {}:
                        del params['options']

        # Specjalna obsługa Switch node
        if node_type == 'n8n-nodes-base.switch' and node_name == 'Is Approved or Timeout?':
            print(f"  Szczegolna obsluga Switch: {node_name}")

            # Wymuszenie prostej struktury
            if 'parameters' in node:
                params = node['parameters']

                # Zachowaj tylko rules i options.fallbackOutput
                new_params = {}

                if 'rules' in params:
                    new_params['rules'] = params['rules']

                if 'options' in params and 'fallbackOutput' in params['options']:
                    new_params['options'] = {
                        'fallbackOutput': params['options']['fallbackOutput']
                    }

                node['parameters'] = new_params

                # Upewnij się że operator jest stringiem
                if 'rules' in new_params and 'rules' in new_params['rules']:
                    for rule in new_params['rules']['rules']:
                        if 'conditions' in rule and 'conditions' in rule['conditions']:
                            for cond in rule['conditions']['conditions']:
                                if 'operator' in cond and isinstance(cond['operator'], dict):
                                    # Zamień na string
                                    if cond['operator'].get('type') == 'number':
                                        cond['operator'] = cond['operator'].get('operation', 'gte')
                                    else:
                                        cond['operator'] = cond['operator'].get('operation', 'equals')

    print(f"Zapisuje minimalny workflow do: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"\nGotowe!")
    print(f"\nUsunięto wszystkie potencjalnie problematyczne 'options'")
    print(f"Import: {output_file}")

def main():
    input_file = Path("C:/Projects/BAW/API 04.json.backup")
    output_file = Path("C:/Projects/BAW/API 04 Minimal Clean.json")

    if not input_file.exists():
        print(f"Blad: Nie znaleziono pliku {input_file}")
        sys.exit(1)

    # Wczytaj ORYGINALNY workflow (backup)
    minimal_fix(str(input_file), str(output_file))

    print(f"\n=== UWAGA ===")
    print(f"To jest ORYGINALNY workflow bez nowych wezlow.")
    print(f"Sluzy do testowania czy podstawowy import dziala.")
    print(f"")
    print(f"Jesli ten import sie uda:")
    print(f"1. Bedziemy wiedziec ze podstawowy workflow jest OK")
    print(f"2. Problem jest w ktorym z 15 nowych wezlow")
    print(f"3. Dodamy nowe wezly pojedynczo w N8N UI")

if __name__ == "__main__":
    main()
