# -*- coding: utf-8 -*-
"""
Skrypt rozszerzający workflow n8n o obsługę endpointów summary
"""
import json
import uuid
from pathlib import Path

def generate_uuid():
    """Generuje UUID zgodne z formatem n8n"""
    return str(uuid.uuid4())

def add_summary_nodes(workflow_data):
    """Dodaje nowe nody do obsługi summary"""

    # Pozycje dla nowych nodów (kontynuacja po istniejących)
    base_x = 1360  # Zaczynamy za Send email (1136)
    base_y = 756

    new_nodes = []

    # ========== NODE 1: POST Summary to API ==========
    node_post_summary = {
        "parameters": {
            "method": "POST",
            "url": "http://217.182.76.146/api/summary",
            "sendBody": True,
            "bodyParameters": {
                "parameters": [
                    {
                        "name": "process_id",
                        "value": "={{ $('Start Processing').item.json.process_id }}"
                    },
                    {
                        "name": "summary_text",
                        "value": "={{ $('AI Agent4').item.json.output }}"
                    },
                    {
                        "name": "metadata",
                        "value": "={{ { \"przedmiot_regulacji\": \"Dokument\", \"data_aktu\": \"\", \"data_wejscia_w_zycie\": \"\" } }}"
                    }
                ]
            },
            "options": {
                "timeout": 30000
            }
        },
        "id": generate_uuid(),
        "name": "POST Summary to API",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [base_x, base_y - 400]
    }
    new_nodes.append(node_post_summary)

    # ========== NODE 2: Send Review Email ==========
    node_send_review_email = {
        "parameters": {
            "fromEmail": "ai_baw@credit-agricole.pl",
            "toEmail": "trembiasz@credit-agricole.pl",
            "subject": "Podsumowanie dokumentu - wymaga zatwierdzenia",
            "html": "=<p><b>Podsumowanie zmian w dokumencie zostało wygenerowane i czeka na Twoją weryfikację.</b></p>\n<p>Podsumowanie:</p>\n<pre>{{ $('AI Agent4').item.json.output }}</pre>\n<p><b>Aby zatwierdzić:</b></p>\n<p>1. Przejdź do interfejsu edycji podsumowania</p>\n<p>2. Dokonaj ewentualnych poprawek</p>\n<p>3. Zatwierdź klikając przycisk \"Zatwierdź\"</p>\n<p><i>System automatycznie wykryje zatwierdzenie i wyśle ostateczny raport.</i></p>",
            "options": {}
        },
        "type": "n8n-nodes-base.emailSend",
        "typeVersion": 2.1,
        "position": [base_x + 224, base_y - 400],
        "id": generate_uuid(),
        "name": "Send Review Email",
        "webhookId": generate_uuid(),
        "credentials": {
            "smtp": {
                "id": "2joSLF2U4RnAaaXW",
                "name": "SMTP account 4"
            }
        }
    }
    new_nodes.append(node_send_review_email)

    # ========== NODE 3: Wait Before Polling ==========
    node_wait_before_poll = {
        "parameters": {
            "amount": 10,
            "unit": "seconds"
        },
        "id": generate_uuid(),
        "name": "Wait Before Polling",
        "type": "n8n-nodes-base.wait",
        "typeVersion": 1,
        "position": [base_x + 448, base_y - 400],
        "webhookId": generate_uuid()
    }
    new_nodes.append(node_wait_before_poll)

    # ========== NODE 4: Poll Summary Status ==========
    node_poll_status = {
        "parameters": {
            "url": "=http://217.182.76.146/api/summary/{{ $('Start Processing').item.json.process_id }}/status",
            "options": {}
        },
        "id": generate_uuid(),
        "name": "Poll Summary Status",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [base_x + 672, base_y - 400]
    }
    new_nodes.append(node_poll_status)

    # ========== NODE 5: Is Summary Approved? ==========
    node_is_approved = {
        "parameters": {
            "conditions": {
                "string": [
                    {
                        "value1": "={{ $json.status }}",
                        "value2": "approved"
                    }
                ]
            }
        },
        "id": generate_uuid(),
        "name": "Is Summary Approved?",
        "type": "n8n-nodes-base.if",
        "typeVersion": 1,
        "position": [base_x + 896, base_y - 472]
    }
    new_nodes.append(node_is_approved)

    # ========== NODE 6: Wait 5 Seconds ==========
    node_wait_5s = {
        "parameters": {
            "amount": 5,
            "unit": "seconds"
        },
        "id": generate_uuid(),
        "name": "Wait 5 Seconds",
        "type": "n8n-nodes-base.wait",
        "typeVersion": 1,
        "position": [base_x + 896, base_y - 200],
        "webhookId": generate_uuid()
    }
    new_nodes.append(node_wait_5s)

    # ========== NODE 7: Get Approved Summary ==========
    node_get_approved = {
        "parameters": {
            "url": "=http://217.182.76.146/api/summary/{{ $('Start Processing').item.json.process_id }}/approved",
            "options": {}
        },
        "id": generate_uuid(),
        "name": "Get Approved Summary",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [base_x + 1120, base_y - 472]
    }
    new_nodes.append(node_get_approved)

    # ========== NODE 8: Merge with HTTP Request (raport) ==========
    node_merge_approved = {
        "parameters": {
            "mode": "combine",
            "combineBy": "combineByPosition",
            "options": {}
        },
        "type": "n8n-nodes-base.merge",
        "typeVersion": 3.2,
        "position": [base_x + 1344, base_y - 328],
        "id": generate_uuid(),
        "name": "Merge Approved with Report"
    }
    new_nodes.append(node_merge_approved)

    # ========== NODE 9: Update Email Content ==========
    node_update_email = {
        "parameters": {
            "jsCode": """// Pobierz zatwierdzone podsumowanie z API
const approvedSummary = $('Get Approved Summary').item.json.summary_text;
const editedByUser = $('Get Approved Summary').item.json.edited_by_user;
const reportFilename = $('HTTP Request').item.json.report_filename;

// Formatuj podsumowanie (tak jak w Code in JavaScript4)
let content = approvedSummary.trim();

if (content.match(/^\\d+\\./m)) {
  content = content
    .split(/\\n*\\d+\\.\\s+/)
    .filter(line => line.trim() !== "")
    .map(line => `<li>${line.trim()}</li>`)
    .join("\\n");
} else if (content.includes('-')) {
  content = content
    .split(/\\s*-\\s+/)
    .filter(line => line.trim() !== "")
    .map(line => `<li>${line.trim()}</li>`)
    .join("\\n");
} else {
  content = content
    .split(/\\n+/)
    .filter(line => line.trim() !== "")
    .map(line => `<li>${line.trim()}</li>`)
    .join("\\n");
}

let formattedContent = `
<p><b>Podsumowanie kluczowych zmian:</b></p>
<ul style="color:#707173; font-size:11pt; padding-left:20px;">
${content}
</ul>
`;

// Dodaj informację czy zostało edytowane
if (editedByUser) {
  formattedContent += `<p style="color:#ED1B2F; font-size:9pt;"><i>⚠️ Podsumowanie zostało zweryfikowane i poprawione przez użytkownika</i></p>`;
}

// Wygeneruj pełny HTML maila (kopia z Code in JavaScript4)
let htmlTemplate = `
<table border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="width: 220px; text-align: center; vertical-align: middle;">
<div style="text-align: center; padding: 10px;">
<img src="data:image/png;base64,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"
     width="80"
     height="80"
     style="width: 80px !important; height: 80px !important; max-width: 80px !important; max-height: 80px !important; display: inline-block;">
</div>
</td>
<td>
<p><span style="color: #009795;font-size: 12pt;"><b>Dzień dobry, zapoznaj się z nowym aktem wewnętrznym/Check out the new internal act</b></span></p>
</td>
</tr>
<tr><td colspan="2" style="border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;"></td></tr>
<tr><td><span style="color: #707173;font-size: 11pt;">Typ aktu/Type of act</span></td><td style="padding-left: 15px;"><span style="color: #707173;font-size: 11pt;">Zarządzenie</span></td></tr>
<tr><td colspan="2" style="border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;"></td></tr>
<tr><td><span style="color: #707173;font-size: 11pt;">Numer aktu/Number of act</span></td><td style="padding-left: 15px;"><span style="color: #707173;font-size: 11pt;">676/2025</span></td></tr>
<tr><td colspan="2" style="border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;"></td></tr>
<tr><td><span style="color: #707173;font-size: 11pt;">Organ wydający/Issued by</span></td><td style="padding-left: 15px;"><span style="color: #707173;font-size: 11pt;">Wiceprezes Zarządu</span></td></tr>
<tr><td colspan="2" style="border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;"></td></tr>
<tr><td><span style="color: #707173;font-size: 11pt;">Przedmiot regulacji/concerning</span></td><td style="padding-left: 15px;"><span style="color: #707173;font-size: 11pt;">w sprawie: aktualizacji Ogłoszenia nr CA/TO/39 Zasady rozpatrywania reklamacji w Credit Agricole Bank Polska S.A. na tablicy ogłoszeń</span></td></tr>
<tr><td colspan="2" style="border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;"></td></tr>
<tr><td><span style="color: #707173;font-size: 11pt;">Dostępne/Available</span></td><td style="padding-left: 15px;"><span style="color: #707173;font-size: 11pt;"><a href="[Link do dokumentu]" target="_blank" style="color: #009795;">[Link do dokumentu]</a></span></td></tr>
<tr><td colspan="2" style="border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;"></td></tr>
<tr><td><span style="color: #707173;font-size: 11pt;">Data aktu/Release date</span></td><td style="padding-left: 15px;"><span style="color: #707173;font-size: 11pt;">26.10.2025</span></td></tr>
<tr><td colspan="2" style="border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;"></td></tr>
<tr><td><span style="color: #707173;font-size: 11pt;">Data wejścia w życie/Date of entry into force</span></td><td style="padding-left: 15px;"><span style="color: #707173;font-size: 11pt;">31.10.2025</span></td></tr>
<tr><td colspan="2" style="border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;"></td></tr>
<tr><td><span style="color: #707173;font-size: 11pt;">Opublikowane przez/Published by</span></td><td style="padding-left: 15px;"><span style="color: #707173;font-size: 11pt;">Tomasz</span></td></tr>
<tr><td colspan="2" style="border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;"></td></tr>

<tr><td colspan="2" style="height:15px;"></td></tr>

<tr>
<td><p><span style="color: #707173;font-size: 11pt;">Podsumowanie zmian/Summary of changes</span></p></td>
<td style="padding-left: 15px;"><p style="text-align: justify; white-space: normal;">${formattedContent}</p></td>
</tr>
<tr><td colspan="2" style="border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;"></td></tr>
<tr>
<td><p><span style="color: #707173;font-size: 11pt;">Szczegółowa analiza zmian</span></p></td>
<td style="padding-left: 15px;"><p><a href="http://217.182.76.146/reports/${reportFilename}" target="_blank" style="color: #009795;">Link do podsumowania zmian</a></p></td>
</tr>
<tr><td colspan="2" style="border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;"></td></tr>

</tbody>
</table>

<p><span style="color: #009795;font-size: 12pt;"><b>Wiadomość wygenerowana automatycznie, nie odpowiadaj na nią / Automatically generated message, please do not reply to it.</b></span></p>
<p><span style="color: #009795;font-size: 12pt;"><b>Więcej o nas / More about us:
<a href="http://bok.creditagricole/index.php" target="_blank" style="color: #009795;">http://bok.creditagricole/index.php</a></b></span></p>
`;

return [{ json: { html: htmlTemplate, approved_summary: approvedSummary, edited: editedByUser } }];"""
        },
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [base_x + 1568, base_y - 328],
        "id": generate_uuid(),
        "name": "Update Email Content"
    }
    new_nodes.append(node_update_email)

    # ========== NODE 10: Sticky Note - Summary Integration ==========
    node_sticky = {
        "parameters": {
            "content": "## INTEGRACJA SUMMARY\n\n1. POST Summary to API - wysłanie podsumowania\n2. Send Review Email - mail z prośbą o weryfikację\n3. Wait Before Polling - czekaj 10s\n4. Poll Summary Status - sprawdź status (polling)\n5. Is Summary Approved? - IF status == approved\n6. Wait 5 Seconds - czekaj jeśli nie approved\n7. Get Approved Summary - pobierz zatwierdzone\n8. Merge Approved with Report - połącz z raportem\n9. Update Email Content - aktualizuj mail\n10. Send email - wyślij finalny mail",
            "height": 656,
            "width": 1552
        },
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [base_x - 32, base_y - 656],
        "id": generate_uuid(),
        "name": "Sticky Note - Summary Integration"
    }
    new_nodes.append(node_sticky)

    return new_nodes

def update_connections(workflow_data, new_nodes):
    """Aktualizuje połączenia między nodami"""

    connections = workflow_data["connections"]

    # Znajdź ID nodów
    ai_agent4_id = None
    http_request_id = None  # Node generujący raport
    send_email_id = None

    for node in workflow_data["nodes"]:
        if node["name"] == "AI Agent4":
            ai_agent4_id = node["id"]
        elif node["name"] == "HTTP Request" and "report" in node["parameters"].get("url", ""):
            http_request_id = node["id"]
        elif node["name"] == "Send email":
            send_email_id = node["id"]

    # Znajdź ID nowych nodów
    post_summary_id = next(n["id"] for n in new_nodes if n["name"] == "POST Summary to API")
    send_review_id = next(n["id"] for n in new_nodes if n["name"] == "Send Review Email")
    wait_before_id = next(n["id"] for n in new_nodes if n["name"] == "Wait Before Polling")
    poll_status_id = next(n["id"] for n in new_nodes if n["name"] == "Poll Summary Status")
    is_approved_id = next(n["id"] for n in new_nodes if n["name"] == "Is Summary Approved?")
    wait_5s_id = next(n["id"] for n in new_nodes if n["name"] == "Wait 5 Seconds")
    get_approved_id = next(n["id"] for n in new_nodes if n["name"] == "Get Approved Summary")
    merge_approved_id = next(n["id"] for n in new_nodes if n["name"] == "Merge Approved with Report")
    update_email_id = next(n["id"] for n in new_nodes if n["name"] == "Update Email Content")

    # MODYFIKACJA: AI Agent4 teraz łączy się z POST Summary
    # Usuń stare połączenie AI Agent4 -> Merge2
    if "AI Agent4" in connections:
        connections["AI Agent4"]["main"] = [
            [
                {
                    "node": "POST Summary to API",
                    "type": "main",
                    "index": 0
                }
            ]
        ]

    # NOWE POŁĄCZENIA:

    # POST Summary to API -> Send Review Email
    connections["POST Summary to API"] = {
        "main": [
            [
                {
                    "node": "Send Review Email",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }

    # Send Review Email -> Wait Before Polling
    connections["Send Review Email"] = {
        "main": [
            [
                {
                    "node": "Wait Before Polling",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }

    # Wait Before Polling -> Poll Summary Status
    connections["Wait Before Polling"] = {
        "main": [
            [
                {
                    "node": "Poll Summary Status",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }

    # Poll Summary Status -> Is Summary Approved?
    connections["Poll Summary Status"] = {
        "main": [
            [
                {
                    "node": "Is Summary Approved?",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }

    # Is Summary Approved? -> Get Approved Summary (TRUE) lub Wait 5 Seconds (FALSE)
    connections["Is Summary Approved?"] = {
        "main": [
            [
                {
                    "node": "Get Approved Summary",
                    "type": "main",
                    "index": 0
                }
            ],
            [
                {
                    "node": "Wait 5 Seconds",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }

    # Wait 5 Seconds -> Poll Summary Status (pętla)
    connections["Wait 5 Seconds"] = {
        "main": [
            [
                {
                    "node": "Poll Summary Status",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }

    # Get Approved Summary + HTTP Request -> Merge Approved with Report
    connections["Get Approved Summary"] = {
        "main": [
            [
                {
                    "node": "Merge Approved with Report",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }

    # HTTP Request już jest - musimy dodać drugie połączenie do Merge
    # Znajdź istniejące połączenie HTTP Request
    if "HTTP Request" in connections:
        # Dodaj połączenie do nowego Merge
        connections["HTTP Request"]["main"].append([
            {
                "node": "Merge Approved with Report",
                "type": "main",
                "index": 1
            }
        ])

    # Merge Approved with Report -> Update Email Content
    connections["Merge Approved with Report"] = {
        "main": [
            [
                {
                    "node": "Update Email Content",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }

    # Update Email Content -> Send email
    connections["Update Email Content"] = {
        "main": [
            [
                {
                    "node": "Send email",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }

    # USUŃ stare połączenie Code in JavaScript4 -> Send email
    # Send email otrzymuje teraz dane z Update Email Content
    if "Code in JavaScript4" in connections:
        # Nie usuwamy całego połączenia, ale możemy je pozostawić jako zapasową ścieżkę
        pass

    return connections

def main():
    """Główna funkcja"""
    input_file = Path("C:/Projects/BAW/API 04.json")
    output_file = Path("C:/Projects/BAW/API 05 - with summary.json")

    print(f"📖 Wczytywanie workflow z {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    print(f"✨ Dodawanie nowych nodów do obsługi summary...")
    new_nodes = add_summary_nodes(workflow)
    workflow["nodes"].extend(new_nodes)

    print(f"🔗 Aktualizowanie połączeń...")
    workflow["connections"] = update_connections(workflow, new_nodes)

    # Aktualizuj nazwę workflow
    workflow["name"] = "API 05 - with summary"

    # Generuj nowe ID wersji
    workflow["versionId"] = str(uuid.uuid4())

    print(f"💾 Zapisywanie do {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"✅ Gotowe! Dodano {len(new_nodes)} nowych nodów")
    print(f"📊 Łączna liczba nodów: {len(workflow['nodes'])}")
    print(f"📁 Plik zapisany: {output_file}")

    # Wyświetl listę nowych nodów
    print("\n📋 Dodane nody:")
    for i, node in enumerate(new_nodes, 1):
        print(f"  {i}. {node['name']} (ID: {node['id'][:8]}...)")

if __name__ == "__main__":
    main()
