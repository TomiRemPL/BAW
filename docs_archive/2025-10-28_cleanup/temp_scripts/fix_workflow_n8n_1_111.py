#!/usr/bin/env python3
"""
Fix N8N Workflow dla wersji N8N 1.111.0
Kompatybilność z November 2024 release
"""

import json
import sys
from pathlib import Path

def fix_for_n8n_1_111(input_file, output_file):
    """Napraw workflow dla N8N 1.111.0"""
    print(f"Wczytuje workflow z: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    print(f"Dostosowuje do N8N 1.111.0...")

    for node in workflow['nodes']:
        node_name = node.get('name', '')
        node_type = node.get('type', '')

        # Fix 1: httpRequest nodes - N8N 1.111.0 używa typeVersion 4.2 ale inny format retry
        if node_type == 'n8n-nodes-base.httpRequest':
            if node_name in ['Create Summary', 'Check Summary Status', 'Get Approved Summary']:
                print(f"  Fix HTTP Request: {node_name}")

                # N8N 1.111.0 używa 'options.retry' ale z prostszą strukturą
                if 'parameters' in node and 'options' in node['parameters']:
                    options = node['parameters']['options']

                    # Usuń starą strukturę retry jeśli istnieje
                    if 'retry' in options:
                        del options['retry']

                    # Nie dodawaj retry w JSON - będzie dodany ręcznie w UI
                    # N8N 1.111.0 ma problemy z importowaniem retry configuration

        # Fix 2: Switch node - N8N 1.111.0 używa typeVersion 3
        elif node_type == 'n8n-nodes-base.switch':
            if node_name == 'Is Approved or Timeout?':
                print(f"  Fix Switch: {node_name}")

                # Upewnij się że typeVersion = 3
                node['typeVersion'] = 3

                if 'parameters' in node and 'rules' in node['parameters']:
                    rules = node['parameters']['rules']

                    # N8N 1.111.0 wymaga aby rules było obiektem z kluczem 'rules'
                    if not isinstance(rules, dict):
                        node['parameters']['rules'] = {'rules': rules}

                    for rule in node['parameters']['rules'].get('rules', []):
                        if 'conditions' in rule:
                            # Upewnij się że conditions jest obiektem z kluczem 'conditions'
                            if isinstance(rule['conditions'], list):
                                rule['conditions'] = {'conditions': rule['conditions']}

                            for condition in rule['conditions'].get('conditions', []):
                                # operator MUSI być stringiem
                                if 'operator' in condition:
                                    op = condition['operator']
                                    if isinstance(op, dict):
                                        # Wyciągnij operation ze struktury
                                        if op.get('type') == 'string':
                                            condition['operator'] = op.get('operation', 'equals')
                                        elif op.get('type') == 'number':
                                            condition['operator'] = op.get('operation', 'gte')
                                        else:
                                            condition['operator'] = 'equals'

                                # rightValue dla number comparison MUSI być stringiem w N8N 1.111.0
                                if condition.get('operator') in ['gte', 'gt', 'lte', 'lt']:
                                    if 'rightValue' in condition:
                                        condition['rightValue'] = str(condition['rightValue'])

        # Fix 3: emailSend nodes - N8N 1.111.0 używa typeVersion 2.1
        elif node_type == 'n8n-nodes-base.emailSend':
            if node_name in ['Send Edit Link Email', 'Send Final Email', 'Send Timeout Email', 'Send Rejection Email']:
                print(f"  Fix Email: {node_name}")

                # Upewnij się że typeVersion = 2.1
                node['typeVersion'] = 2.1

                # Usuń puste options
                if 'parameters' in node and 'options' in node['parameters']:
                    if not node['parameters']['options']:
                        del node['parameters']['options']

        # Fix 4: Set nodes - N8N 1.111.0 używa typeVersion 3.4
        elif node_type == 'n8n-nodes-base.set':
            if node_name in ['Init Counter', 'Increment Counter', 'Edit Fields', 'Edit Fields1']:
                print(f"  Fix Set: {node_name}")

                # Upewnij się że typeVersion = 3.4
                node['typeVersion'] = 3.4

                # N8N 1.111.0 używa 'assignments' zamiast 'values'
                if 'parameters' in node:
                    params = node['parameters']

                    # Jeśli jest stara struktura 'values', zamień na 'assignments'
                    if 'values' in params and 'assignments' not in params:
                        params['assignments'] = {
                            'assignments': params['values'].get('values', [])
                        }
                        del params['values']

                    # Upewnij się że assignments.assignments istnieje
                    if 'assignments' in params:
                        if not isinstance(params['assignments'], dict):
                            params['assignments'] = {'assignments': params['assignments']}

                        # Każdy assignment musi mieć: id, name, value, type
                        for idx, assignment in enumerate(params['assignments'].get('assignments', [])):
                            if 'id' not in assignment:
                                assignment['id'] = f"assignment-{idx}"
                            if 'type' not in assignment:
                                # Zgadnij typ na podstawie wartości
                                val = assignment.get('value', '')
                                if isinstance(val, str) and val.isdigit():
                                    assignment['type'] = 'number'
                                else:
                                    assignment['type'] = 'string'

                    # Usuń puste options
                    if 'options' in params and not params['options']:
                        del params['options']

        # Fix 5: Wait nodes - N8N 1.111.0 używa typeVersion 1.1
        elif node_type == 'n8n-nodes-base.wait':
            if node_name in ['Wait for User', 'Wait 10 Seconds', 'Wait 3 Seconds', 'Wait 2 Seconds', 'Wait']:
                print(f"  Fix Wait: {node_name}")

                # N8N 1.111.0 może używać typeVersion 1 lub 1.1
                if node.get('typeVersion') not in [1, 1.1]:
                    node['typeVersion'] = 1

                # Upewnij się że webhookId jest unikalny
                if 'webhookId' not in node or not node['webhookId']:
                    # Generuj unikalny webhookId
                    import uuid
                    node['webhookId'] = str(uuid.uuid4())

        # Fix 6: Merge nodes - N8N 1.111.0 używa typeVersion 3 lub 3.2
        elif node_type == 'n8n-nodes-base.merge':
            if node_name in ['Merge', 'Merge1', 'Merge2', 'Merge Final Data']:
                print(f"  Fix Merge: {node_name}")

                # Upewnij się że typeVersion = 3.2
                if 'typeVersion' not in node:
                    node['typeVersion'] = 3.2

        # Fix 7: Code nodes (JavaScript) - N8N 1.111.0 używa typeVersion 2
        elif node_type == 'n8n-nodes-base.code':
            if node_name in ['Final Summary', 'Code in JavaScript2', 'Code in JavaScript4', 'Format Final Email']:
                print(f"  Fix Code: {node_name}")

                # Upewnij się że typeVersion = 2
                node['typeVersion'] = 2

        # Fix 8: SeaTable - N8N 1.111.0 używa typeVersion 2
        elif node_type == 'n8n-nodes-base.seaTable':
            if node_name == 'Log Timeout Error':
                print(f"  Fix SeaTable: {node_name}")

                # Upewnij się że typeVersion = 2
                node['typeVersion'] = 2

    print(f"Zapisuje workflow dla N8N 1.111.0: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"\nGotowe!")
    print(f"\n=== WAZNE ===")
    print(f"Po imporcie dodaj RETRY recznie w 3 wezlach HTTP Request:")
    print(f"")
    print(f"1. Create Summary:")
    print(f"   Settings > Retry On Fail > ON")
    print(f"   Max Tries: 3, Wait: 2000ms")
    print(f"")
    print(f"2. Check Summary Status:")
    print(f"   Settings > Retry On Fail > ON")
    print(f"   Max Tries: 2, Wait: 1000ms")
    print(f"")
    print(f"3. Get Approved Summary:")
    print(f"   Settings > Retry On Fail > ON")
    print(f"   Max Tries: 3, Wait: 2000ms")
    print(f"")
    print(f"Import: {output_file}")

def main():
    input_file = Path("C:/Projects/BAW/API 04 Enhanced.json")
    output_file = Path("C:/Projects/BAW/API 04 Enhanced - N8N 1.111.0.json")

    if not input_file.exists():
        print(f"Blad: Nie znaleziono pliku {input_file}")
        sys.exit(1)

    fix_for_n8n_1_111(str(input_file), str(output_file))

if __name__ == "__main__":
    main()
