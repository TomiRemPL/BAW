#!/usr/bin/env python3
"""
Fix N8N Workflow - Naprawa błędu importu
"""

import json
import sys
from pathlib import Path

def fix_workflow(input_file, output_file):
    """Napraw workflow - usuń problematyczne struktury"""
    print(f"Wczytuje workflow z: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    print(f"Naprawiam wezly...")

    for node in workflow['nodes']:
        # Fix 1: Is Approved or Timeout? - operator powinien być stringiem
        if node['name'] == 'Is Approved or Timeout?':
            print(f"  Naprawiam: {node['name']}")

            if 'parameters' in node and 'rules' in node['parameters']:
                for rule in node['parameters']['rules'].get('rules', []):
                    if 'conditions' in rule:
                        for condition in rule['conditions'].get('conditions', []):
                            # Zamień operator object na string
                            if 'operator' in condition and isinstance(condition['operator'], dict):
                                # Dla string operator
                                if condition['operator'].get('type') == 'string':
                                    condition['operator'] = condition['operator'].get('operation', 'equals')
                                # Dla number operator
                                elif condition['operator'].get('type') == 'number':
                                    condition['operator'] = condition['operator'].get('operation', 'gte')

            # Upewnij się że jest typeVersion = 3
            if node.get('typeVersion') != 3:
                node['typeVersion'] = 3

        # Fix 2: Usuń nieobsługiwane options w retry
        if 'parameters' in node and 'options' in node['parameters']:
            options = node['parameters']['options']
            if 'retry' in options:
                retry = options['retry']
                # N8N 1.x używa: tries, waitBeforeTries
                if 'maxTries' in retry:
                    retry['tries'] = retry.pop('maxTries')
                if 'waitBetweenRetries' in retry:
                    retry['waitBeforeTries'] = retry.pop('waitBetweenRetries')

    print(f"Zapisuje naprawiony workflow do: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"Gotowe!")

def main():
    input_file = Path("C:/Projects/BAW/API 04 Enhanced.json")
    output_file = Path("C:/Projects/BAW/API 04 Enhanced Fixed.json")

    if not input_file.exists():
        print(f"Blad: Nie znaleziono pliku {input_file}")
        sys.exit(1)

    fix_workflow(str(input_file), str(output_file))
    print(f"\nImportuj plik: {output_file}")

if __name__ == "__main__":
    main()
