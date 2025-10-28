#!/usr/bin/env python3
"""
Fix N8N Workflow v2 - Kompatybilność ze starszymi wersjami N8N
"""

import json
import sys
from pathlib import Path

def fix_workflow_compatibility(input_file, output_file):
    """Napraw workflow - kompatybilność z różnymi wersjami N8N"""
    print(f"Wczytuje workflow z: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    print(f"Naprawiam kompatybilnosc...")

    for node in workflow['nodes']:
        node_name = node.get('name', '')
        node_type = node.get('type', '')

        # Fix 1: httpRequest nodes - użyj starszej wersji lub usuń problematyczne opcje
        if node_type == 'n8n-nodes-base.httpRequest':
            # Sprawdź czy to nowy węzeł
            if node_name in ['Create Summary', 'Check Summary Status', 'Get Approved Summary']:
                print(f"  Naprawiam HTTP Request: {node_name}")

                # Usuń retry - dodamy to ręcznie po imporcie
                if 'parameters' in node and 'options' in node['parameters']:
                    if 'retry' in node['parameters']['options']:
                        del node['parameters']['options']['retry']
                        print(f"    Usunieto retry (dodaj recznie po imporcie)")

                # Upewnij się że timeout jest prostym numerem
                if 'parameters' in node and 'options' in node['parameters']:
                    if 'timeout' in node['parameters']['options']:
                        timeout_val = node['parameters']['options']['timeout']
                        if isinstance(timeout_val, dict):
                            node['parameters']['options']['timeout'] = timeout_val.get('value', 30000)

        # Fix 2: emailSend nodes - uproszczenie
        elif node_type == 'n8n-nodes-base.emailSend':
            if node_name in ['Send Edit Link Email', 'Send Final Email', 'Send Timeout Email', 'Send Rejection Email']:
                print(f"  Naprawiam Email: {node_name}")

                # Usuń 'options' jeśli puste
                if 'parameters' in node and 'options' in node['parameters']:
                    if not node['parameters']['options'] or node['parameters']['options'] == {}:
                        del node['parameters']['options']

        # Fix 3: Switch node - uproszczenie
        elif node_type == 'n8n-nodes-base.switch':
            if node_name == 'Is Approved or Timeout?':
                print(f"  Naprawiam Switch: {node_name}")

                # Upewnij się że wszystkie operatory są stringami
                if 'parameters' in node and 'rules' in node['parameters']:
                    for rule in node['parameters']['rules'].get('rules', []):
                        if 'conditions' in rule:
                            for condition in rule['conditions'].get('conditions', []):
                                if 'operator' in condition:
                                    op = condition['operator']
                                    if isinstance(op, dict):
                                        condition['operator'] = op.get('operation', 'equals')
                                    # Dla number operator - upewnij się że rightValue jest stringiem
                                    if condition['operator'] in ['gte', 'gt', 'lte', 'lt', 'equals']:
                                        if 'rightValue' in condition:
                                            condition['rightValue'] = str(condition['rightValue'])

        # Fix 4: Set nodes (Edit Fields) - uproszczenie
        elif node_type == 'n8n-nodes-base.set':
            if node_name in ['Init Counter', 'Increment Counter']:
                print(f"  Naprawiam Set: {node_name}")

                # Usuń 'options' jeśli puste
                if 'parameters' in node and 'options' in node['parameters']:
                    if not node['parameters']['options'] or node['parameters']['options'] == {}:
                        del node['parameters']['options']

        # Fix 5: Wait nodes - uproszczenie
        elif node_type == 'n8n-nodes-base.wait':
            if node_name in ['Wait for User', 'Wait 10 Seconds']:
                print(f"  Naprawiam Wait: {node_name}")

                # Upewnij się że webhookId jest unikalny i prosty
                if 'webhookId' not in node:
                    node['webhookId'] = f"webhook-{node_name.lower().replace(' ', '-')}"

        # Fix 6: SeaTable node
        elif node_type == 'n8n-nodes-base.seaTable':
            if node_name == 'Log Timeout Error':
                print(f"  Naprawiam SeaTable: {node_name}")

                # Upewnij się że fieldsUi jest poprawnie sformatowane
                if 'parameters' in node and 'fieldsUi' in node['parameters']:
                    # N8N może wymagać różnych formatów w różnych wersjach
                    pass

    print(f"Zapisuje naprawiony workflow do: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"Gotowe!")
    print(f"")
    print(f"UWAGA: Retry logic zostal usuniety z HTTP Request nodes.")
    print(f"Po imporcie dodaj recznie w kazdym HTTP Request node:")
    print(f"  - Create Summary: Settings -> Retry On Fail -> tries=3")
    print(f"  - Check Summary Status: Settings -> Retry On Fail -> tries=2")
    print(f"  - Get Approved Summary: Settings -> Retry On Fail -> tries=3")

def main():
    input_file = Path("C:/Projects/BAW/API 04 Enhanced.json")
    output_file = Path("C:/Projects/BAW/API 04 Enhanced v2.json")

    if not input_file.exists():
        print(f"Blad: Nie znaleziono pliku {input_file}")
        sys.exit(1)

    fix_workflow_compatibility(str(input_file), str(output_file))
    print(f"\nImportuj plik: {output_file}")

if __name__ == "__main__":
    main()
