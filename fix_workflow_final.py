#!/usr/bin/env python3
"""
Final Fix for N8N Workflow - N8N 1.111.0
Poprawki:
1. contentType: "json" (NIE "application/json")
2. Parametry zgodne z faktycznym API
3. Minimalna konfiguracja (bez options)
"""

import json
import sys
from pathlib import Path
import uuid

def fix_existing_nodes(workflow):
    """Popraw istniejące węzły - content type i parametry"""
    print("Poprawiam istniejące węzły HTTP Request...")

    for node in workflow['nodes']:
        if node.get('type') == 'n8n-nodes-base.httpRequest':
            params = node.get('parameters', {})

            # Popraw contentType
            if 'contentType' in params:
                if params['contentType'] == 'application/json':
                    print(f"  Poprawiam contentType w: {node.get('name')}")
                    params['contentType'] = 'json'

            # Usuń wszelkie options
            if 'options' in params:
                print(f"  Usuwam options z: {node.get('name')}")
                del params['options']

    return workflow

def create_minimal_summary_nodes():
    """15 nowych węzłów - MINIMALNE wersje z poprawnymi parametrami"""

    nodes = []

    # 1. Create Summary - poprawne parametry API
    nodes.append({
        "parameters": {
            "method": "POST",
            "url": "http://217.182.76.146:8001/api/summary",
            "sendBody": True,
            "contentType": "json",  # POPRAWIONE: json zamiast application/json
            "bodyParameters": {
                "parameters": [
                    {"name": "process_id", "value": "={{ $('Start Processing').item.json.process_id }}"},
                    {"name": "summary_text", "value": "={{ $json.output }}"},
                    {"name": "metadata", "value": "={{ {} }}"}
                ]
            }
        },
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [-16, 592],
        "id": str(uuid.uuid4()),
        "name": "Create Summary"
    })

    # 2. Send Edit Link Email
    nodes.append({
        "parameters": {
            "fromEmail": "ai_baw@credit-agricole.pl",
            "toEmail": "trembiasz@credit-agricole.pl",
            "subject": "Podsumowanie wymaga zatwierdzenia",
            "text": "Link: http://217.182.76.146:8000/summary/{{ $json.process_id }}"
        },
        "type": "n8n-nodes-base.emailSend",
        "typeVersion": 2.1,
        "position": [208, 592],
        "id": str(uuid.uuid4()),
        "name": "Send Edit Link Email",
        "credentials": {"smtp": {"id": "2joSLF2U4RnAaaXW", "name": "SMTP account 4"}}
    })

    # 3. Wait for User
    nodes.append({
        "parameters": {"amount": 30, "unit": "seconds"},
        "type": "n8n-nodes-base.wait",
        "typeVersion": 1,
        "position": [432, 592],
        "id": str(uuid.uuid4()),
        "name": "Wait for User",
        "webhookId": str(uuid.uuid4())
    })

    # 4. Init Counter
    nodes.append({
        "parameters": {
            "assignments": {
                "assignments": [
                    {"id": str(uuid.uuid4()), "name": "iteration_count", "value": "0", "type": "number"},
                    {"id": str(uuid.uuid4()), "name": "process_id", "value": "={{ $('Start Processing').item.json.process_id }}", "type": "string"}
                ]
            }
        },
        "type": "n8n-nodes-base.set",
        "typeVersion": 3.4,
        "position": [656, 592],
        "id": str(uuid.uuid4()),
        "name": "Init Counter"
    })

    # 5. Check Summary Status
    nodes.append({
        "parameters": {
            "url": "=http://217.182.76.146:8001/api/summary/{{ $json.process_id }}/status"
        },
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [880, 592],
        "id": str(uuid.uuid4()),
        "name": "Check Summary Status"
    })

    # 6. Increment Counter
    nodes.append({
        "parameters": {
            "assignments": {
                "assignments": [
                    {"id": str(uuid.uuid4()), "name": "iteration_count", "value": "={{ $('Init Counter').item.json.iteration_count + 1 }}", "type": "number"},
                    {"id": str(uuid.uuid4()), "name": "process_id", "value": "={{ $('Init Counter').item.json.process_id }}", "type": "string"},
                    {"id": str(uuid.uuid4()), "name": "status", "value": "={{ $json.status }}", "type": "string"}
                ]
            }
        },
        "type": "n8n-nodes-base.set",
        "typeVersion": 3.4,
        "position": [1104, 592],
        "id": str(uuid.uuid4()),
        "name": "Increment Counter"
    })

    # 7. Is Approved or Timeout? - IF node (prosty)
    nodes.append({
        "parameters": {
            "conditions": {
                "string": [
                    {"value1": "={{ $json.status }}", "value2": "approved"}
                ]
            }
        },
        "type": "n8n-nodes-base.if",
        "typeVersion": 1,
        "position": [1328, 592],
        "id": str(uuid.uuid4()),
        "name": "Is Approved or Timeout?"
    })

    # 8. Wait 10 Seconds (loop)
    nodes.append({
        "parameters": {"amount": 10, "unit": "seconds"},
        "type": "n8n-nodes-base.wait",
        "typeVersion": 1,
        "position": [1104, 816],
        "id": str(uuid.uuid4()),
        "name": "Wait 10 Seconds",
        "webhookId": str(uuid.uuid4())
    })

    # 9. Get Approved Summary
    nodes.append({
        "parameters": {
            "url": "=http://217.182.76.146:8001/api/summary/{{ $json.process_id }}/approved"
        },
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1552, 368],
        "id": str(uuid.uuid4()),
        "name": "Get Approved Summary"
    })

    # 10. Merge Final Data
    nodes.append({
        "parameters": {
            "mode": "combine",
            "combineBy": "combineByPosition"
        },
        "type": "n8n-nodes-base.merge",
        "typeVersion": 3,
        "position": [1776, 480],
        "id": str(uuid.uuid4()),
        "name": "Merge Final Data"
    })

    # 11. Format Final Email
    nodes.append({
        "parameters": {
            "jsCode": "return [{ json: { html: '<p>Summary: ' + $input.first().json.summary_text + '</p>' } }];"
        },
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [2000, 480],
        "id": str(uuid.uuid4()),
        "name": "Format Final Email"
    })

    # 12. Send Final Email
    nodes.append({
        "parameters": {
            "fromEmail": "ai_baw@credit-agricole.pl",
            "toEmail": "trembiasz@credit-agricole.pl",
            "subject": "ZATWIERDZONE podsumowanie",
            "html": "={{ $json.html }}"
        },
        "type": "n8n-nodes-base.emailSend",
        "typeVersion": 2.1,
        "position": [2224, 480],
        "id": str(uuid.uuid4()),
        "name": "Send Final Email",
        "credentials": {"smtp": {"id": "2joSLF2U4RnAaaXW", "name": "SMTP account 4"}}
    })

    # 13. Log Timeout Error
    nodes.append({
        "parameters": {
            "resource": "row",
            "operation": "create",
            "tableName": "errors",
            "fieldsToSend": "defineInNode",
            "fieldsUi": {
                "fieldValues": [
                    {"fieldId": "error_type", "fieldValue": "TIMEOUT"},
                    {"fieldId": "process_id", "fieldValue": "={{ $json.process_id }}"}
                ]
            }
        },
        "type": "n8n-nodes-base.seaTable",
        "typeVersion": 2,
        "position": [1552, 816],
        "id": str(uuid.uuid4()),
        "name": "Log Timeout Error",
        "credentials": {"seaTableApi": {"id": "308kg9y7cDXLbrvU", "name": "SeaTable account 3"}}
    })

    # 14. Send Timeout Email
    nodes.append({
        "parameters": {
            "fromEmail": "ai_baw@credit-agricole.pl",
            "toEmail": "trembiasz@credit-agricole.pl",
            "subject": "TIMEOUT - Brak zatwierdzenia",
            "text": "Timeout po 10 minutach"
        },
        "type": "n8n-nodes-base.emailSend",
        "typeVersion": 2.1,
        "position": [1776, 816],
        "id": str(uuid.uuid4()),
        "name": "Send Timeout Email",
        "credentials": {"smtp": {"id": "2joSLF2U4RnAaaXW", "name": "SMTP account 4"}}
    })

    # 15. Send Rejection Email
    nodes.append({
        "parameters": {
            "fromEmail": "ai_baw@credit-agricole.pl",
            "toEmail": "trembiasz@credit-agricole.pl",
            "subject": "Podsumowanie odrzucone",
            "text": "Uzytkownik odrzucil podsumowanie"
        },
        "type": "n8n-nodes-base.emailSend",
        "typeVersion": 2.1,
        "position": [1552, 592],
        "id": str(uuid.uuid4()),
        "name": "Send Rejection Email",
        "credentials": {"smtp": {"id": "2joSLF2U4RnAaaXW", "name": "SMTP account 4"}}
    })

    return nodes

def update_connections_final(workflow):
    """Dodaj connections dla nowych węzłów"""
    print("Aktualizuje connections...")

    connections = workflow.get("connections", {})

    # Usuń stare połączenie AI Agent3 → Merge
    if "AI Agent3" in connections and "main" in connections["AI Agent3"]:
        new_main = []
        for conn_group in connections["AI Agent3"]["main"]:
            filtered = [c for c in conn_group if c.get("node") != "Merge"]
            if filtered or len(new_main) == 0:
                new_main.append(filtered if filtered else [])

        # Dodaj nowe połączenie AI Agent3 → Create Summary
        if new_main:
            new_main[0].append({"node": "Create Summary", "type": "main", "index": 0})
        else:
            new_main = [[{"node": "Create Summary", "type": "main", "index": 0}]]

        connections["AI Agent3"]["main"] = new_main

    # Nowe połączenia
    new_connections = {
        "Create Summary": {"main": [[{"node": "Send Edit Link Email", "type": "main", "index": 0}]]},
        "Send Edit Link Email": {"main": [[{"node": "Wait for User", "type": "main", "index": 0}]]},
        "Wait for User": {"main": [[{"node": "Init Counter", "type": "main", "index": 0}]]},
        "Init Counter": {"main": [[{"node": "Check Summary Status", "type": "main", "index": 0}]]},
        "Check Summary Status": {"main": [[{"node": "Increment Counter", "type": "main", "index": 0}]]},
        "Increment Counter": {"main": [[{"node": "Is Approved or Timeout?", "type": "main", "index": 0}]]},
        "Is Approved or Timeout?": {"main": [[{"node": "Get Approved Summary", "type": "main", "index": 0}], [{"node": "Wait 10 Seconds", "type": "main", "index": 0}]]},
        "Wait 10 Seconds": {"main": [[{"node": "Check Summary Status", "type": "main", "index": 0}]]},
        "Get Approved Summary": {"main": [[{"node": "Merge Final Data", "type": "main", "index": 0}]]},
        "HTTP Request": {"main": [[{"node": "Merge Final Data", "type": "main", "index": 1}]]},
        "Merge Final Data": {"main": [[{"node": "Format Final Email", "type": "main", "index": 0}]]},
        "Format Final Email": {"main": [[{"node": "Send Final Email", "type": "main", "index": 0}]]}
    }

    connections.update(new_connections)
    workflow["connections"] = connections
    return workflow

def main():
    input_file = Path("C:/Projects/BAW/API 04.json.backup")
    output_file = Path("C:/Projects/BAW/API 04 FINAL - N8N 1.111.0.json")

    if not input_file.exists():
        print(f"Blad: Nie znaleziono {input_file}")
        sys.exit(1)

    print(f"Wczytuje oryginalny workflow...")
    with open(input_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    print(f"Poprawiam istniejace wezly...")
    workflow = fix_existing_nodes(workflow)

    print(f"Dodaje 15 nowych wezlow (minimalne)...")
    new_nodes = create_minimal_summary_nodes()
    workflow["nodes"].extend(new_nodes)

    print(f"Aktualizuje connections...")
    workflow = update_connections_final(workflow)

    print(f"Zapisuje...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"\nGotowe!")
    print(f"Wezlow: {len(workflow['nodes'])}")
    print(f"\nPLIK DO IMPORTU:")
    print(f"{output_file}")
    print(f"\nKLUCZOWE POPRAWKI:")
    print(f"1. contentType: 'json' (NIE 'application/json')")
    print(f"2. Parametry API zgodne z faktyczna implementacja")
    print(f"3. Usunieto wszystkie options")
    print(f"4. Minimalna konfiguracja - retry dodasz recznie")

if __name__ == "__main__":
    main()
