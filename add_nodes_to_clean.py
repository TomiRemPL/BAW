#!/usr/bin/env python3
"""
Dodaj nowe węzły do oczyszczonego workflow
BEZ ŻADNYCH options - wszystko ręcznie
"""

import json
import sys
from pathlib import Path
import uuid

def create_new_nodes_minimal():
    """Utwórz 15 nowych węzłów - MINIMALNA konfiguracja"""
    return [
        # 1. Create Summary - MINIMALNY
        {
            "parameters": {
                "method": "POST",
                "url": "http://217.182.76.146/api/summary",
                "sendBody": True,
                "contentType": "application/json",
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
        },

        # 2. Send Edit Link Email - MINIMALNY
        {
            "parameters": {
                "fromEmail": "ai_baw@credit-agricole.pl",
                "toEmail": "trembiasz@credit-agricole.pl",
                "subject": "Podsumowanie wymaga zatwierdzenia",
                "text": "Link: http://217.182.76.146/summary/{{ $json.summary_id }}"
            },
            "type": "n8n-nodes-base.emailSend",
            "typeVersion": 2.1,
            "position": [208, 592],
            "id": str(uuid.uuid4()),
            "name": "Send Edit Link Email",
            "credentials": {"smtp": {"id": "2joSLF2U4RnAaaXW", "name": "SMTP account 4"}}
        },

        # 3. Wait for User
        {
            "parameters": {"amount": 30, "unit": "seconds"},
            "type": "n8n-nodes-base.wait",
            "typeVersion": 1,
            "position": [432, 592],
            "id": str(uuid.uuid4()),
            "name": "Wait for User",
            "webhookId": str(uuid.uuid4())
        },

        # 4. Init Counter - UPROSZCZONY
        {
            "parameters": {
                "assignments": {
                    "assignments": [
                        {"id": str(uuid.uuid4()), "name": "iteration_count", "value": "0", "type": "number"},
                        {"id": str(uuid.uuid4()), "name": "summary_id", "value": "={{ $('Create Summary').item.json.summary_id }}", "type": "string"},
                        {"id": str(uuid.uuid4()), "name": "process_id", "value": "={{ $('Start Processing').item.json.process_id }}", "type": "string"}
                    ]
                }
            },
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.4,
            "position": [656, 592],
            "id": str(uuid.uuid4()),
            "name": "Init Counter"
        },

        # 5. Check Summary Status
        {
            "parameters": {
                "url": "=http://217.182.76.146/api/summary/{{ $json.summary_id }}/status"
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [880, 592],
            "id": str(uuid.uuid4()),
            "name": "Check Summary Status"
        },

        # 6. Increment Counter
        {
            "parameters": {
                "assignments": {
                    "assignments": [
                        {"id": str(uuid.uuid4()), "name": "iteration_count", "value": "={{ $('Init Counter').item.json.iteration_count + 1 }}", "type": "number"},
                        {"id": str(uuid.uuid4()), "name": "summary_id", "value": "={{ $('Init Counter').item.json.summary_id }}", "type": "string"},
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
        },

        # 7. Is Approved or Timeout? - NAJPROSTSZA wersja
        {
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
        },

        # 8. Wait 10 Seconds
        {
            "parameters": {"amount": 10, "unit": "seconds"},
            "type": "n8n-nodes-base.wait",
            "typeVersion": 1,
            "position": [1104, 816],
            "id": str(uuid.uuid4()),
            "name": "Wait 10 Seconds",
            "webhookId": str(uuid.uuid4())
        },

        # 9. Get Approved Summary
        {
            "parameters": {
                "url": "=http://217.182.76.146/api/summary/{{ $json.summary_id }}/approved"
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [1552, 368],
            "id": str(uuid.uuid4()),
            "name": "Get Approved Summary"
        },

        # 10. Merge Final Data
        {
            "parameters": {
                "mode": "combine",
                "combineBy": "combineByPosition"
            },
            "type": "n8n-nodes-base.merge",
            "typeVersion": 3,
            "position": [1776, 480],
            "id": str(uuid.uuid4()),
            "name": "Merge Final Data"
        },

        # 11. Format Final Email - PROSTY kod
        {
            "parameters": {
                "jsCode": "return [{ json: { html: '<p>Summary: ' + $input.first().json.summary_text + '</p>' } }];"
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [2000, 480],
            "id": str(uuid.uuid4()),
            "name": "Format Final Email"
        },

        # 12. Send Final Email
        {
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
        },

        # 13. Log Timeout Error - UPROSZCZONY
        {
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
        },

        # 14. Send Timeout Email
        {
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
        },

        # 15. Send Rejection Email
        {
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
        }
    ]

def update_connections_minimal(workflow):
    """Dodaj minimalne connections"""
    connections = workflow.get("connections", {})

    # Usuń stare połączenie AI Agent3 → Merge
    if "AI Agent3" in connections and "main" in connections["AI Agent3"]:
        # Znajdź i usuń połączenie do Merge
        new_main = []
        for conn_group in connections["AI Agent3"]["main"]:
            filtered = [c for c in conn_group if c.get("node") != "Merge"]
            if filtered or len(new_main) == 0:
                new_main.append(filtered if filtered else [])

        # Dodaj połączenie do Create Summary
        if new_main:
            new_main[0].append({"node": "Create Summary", "type": "main", "index": 0})
        else:
            new_main = [[{"node": "Create Summary", "type": "main", "index": 0}]]

        connections["AI Agent3"]["main"] = new_main

    # Dodaj nowe połączenia - PROSTE
    new_conn = {
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

    connections.update(new_conn)
    workflow["connections"] = connections
    return workflow

def main():
    input_file = Path("C:/Projects/BAW/API 04 Minimal Clean.json")
    output_file = Path("C:/Projects/BAW/API 04 Ultra Minimal.json")

    if not input_file.exists():
        print(f"Blad: Najpierw uruchom fix_workflow_minimal.py")
        sys.exit(1)

    print(f"Wczytuje czysty workflow...")
    with open(input_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    print(f"Dodaje 15 minimalnych wezlow...")
    new_nodes = create_new_nodes_minimal()
    workflow["nodes"].extend(new_nodes)

    print(f"Aktualizuje connections...")
    workflow = update_connections_minimal(workflow)

    print(f"Zapisuje...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"\nGotowe!")
    print(f"Wezlow: {len(workflow['nodes'])}")
    print(f"\nUWAGA: To jest ULTRA MINIMALNA wersja")
    print(f"- Bez retry")
    print(f"- Bez timeout")
    print(f"- Proste emaile (text zamiast HTML)")
    print(f"- IF zamiast Switch")
    print(f"- Wszystko dodasz recznie po imporcie")
    print(f"\nImport: {output_file}")

if __name__ == "__main__":
    main()
