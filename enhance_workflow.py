#!/usr/bin/env python3
"""
Enhanced N8N Workflow Generator
Dodaje 15 nowych węzłów do API 04.json zgodnie z v2.0.0
"""

import json
import sys
from pathlib import Path

def load_workflow(input_file):
    """Wczytaj workflow JSON"""
    with open(input_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_new_nodes():
    """Utwórz 15 nowych węzłów dla Enhanced Workflow"""
    return [
        # 1. Create Summary
        {
            "parameters": {
                "method": "POST",
                "url": "http://217.182.76.146/api/summary",
                "sendBody": True,
                "contentType": "application/json",
                "bodyParameters": {
                    "parameters": [
                        {
                            "name": "process_id",
                            "value": "={{ $('Start Processing').item.json.process_id }}"
                        },
                        {
                            "name": "summary_text",
                            "value": "={{ $json.output }}"
                        },
                        {
                            "name": "metadata",
                            "value": "={{ { \"source\": \"n8n\", \"ai_model\": \"azure-gpt-5\", \"created_at\": $now.toISO() } }}"
                        }
                    ]
                },
                "options": {
                    "timeout": 30000,
                    "retry": {
                        "maxTries": 3,
                        "waitBetweenRetries": 2000
                    }
                }
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [-16, 592],
            "id": "create-summary-node-001",
            "name": "Create Summary"
        },

        # 2. Send Edit Link Email
        {
            "parameters": {
                "fromEmail": "ai_baw@credit-agricole.pl",
                "toEmail": "trembiasz@credit-agricole.pl",
                "subject": "=⏳ Podsumowanie dokumentu wymaga zatwierdzenia - {{ $('Start Processing').item.json.process_id }}",
                "html": "=<html>\n<head>\n  <meta charset=\"UTF-8\">\n</head>\n<body style=\"font-family: Arial, sans-serif; color: #333;\">\n  <h2 style=\"color: #009795;\">📝 Podsumowanie wymaga zatwierdzenia</h2>\n  \n  <p>Dzień dobry,</p>\n  \n  <p>System BAW wygenerował automatyczne podsumowanie zmian w dokumencie:</p>\n  \n  <table style=\"border-collapse: collapse; width: 100%; max-width: 600px; margin: 20px 0;\">\n    <tr style=\"background-color: #f5f5f5;\">\n      <td style=\"padding: 10px; border: 1px solid #ddd; font-weight: bold;\">Process ID:</td>\n      <td style=\"padding: 10px; border: 1px solid #ddd;\">{{ $('Start Processing').item.json.process_id }}</td>\n    </tr>\n    <tr>\n      <td style=\"padding: 10px; border: 1px solid #ddd; font-weight: bold;\">Summary ID:</td>\n      <td style=\"padding: 10px; border: 1px solid #ddd;\">{{ $json.summary_id }}</td>\n    </tr>\n    <tr style=\"background-color: #f5f5f5;\">\n      <td style=\"padding: 10px; border: 1px solid #ddd; font-weight: bold;\">Status:</td>\n      <td style=\"padding: 10px; border: 1px solid #ddd;\">⏳ Oczekuje na zatwierdzenie</td>\n    </tr>\n  </table>\n  \n  <div style=\"background-color: #f0f9f9; border-left: 4px solid #009795; padding: 15px; margin: 20px 0;\">\n    <h3 style=\"margin-top: 0; color: #009795;\">Wygenerowane podsumowanie:</h3>\n    <div style=\"white-space: pre-wrap;\">{{ $('AI Agent3').item.json.output }}</div>\n  </div>\n  \n  <div style=\"margin: 30px 0;\">\n    <a href=\"http://217.182.76.146/summary/{{ $json.summary_id }}\" \n       style=\"display: inline-block; background-color: #009795; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;\">\n      📝 Edytuj i zatwierdź podsumowanie\n    </a>\n  </div>\n  \n  <p style=\"color: #666; font-size: 14px;\">\n    Po zatwierdzeniu, system automatycznie wyśle finalne podsumowanie do wszystkich zainteresowanych stron.\n  </p>\n  \n  <hr style=\"border: none; border-top: 1px solid #ddd; margin: 30px 0;\">\n  \n  <p style=\"color: #999; font-size: 12px;\">\n    <b>Wiadomość wygenerowana automatycznie przez system BAW AI.</b><br>\n    Nie odpowiadaj na tego maila.\n  </p>\n</body>\n</html>",
                "options": {}
            },
            "type": "n8n-nodes-base.emailSend",
            "typeVersion": 2.1,
            "position": [208, 592],
            "id": "send-edit-link-email-001",
            "name": "Send Edit Link Email",
            "credentials": {
                "smtp": {
                    "id": "2joSLF2U4RnAaaXW",
                    "name": "SMTP account 4"
                }
            }
        },

        # 3. Wait for User
        {
            "parameters": {
                "amount": 30,
                "unit": "seconds"
            },
            "type": "n8n-nodes-base.wait",
            "typeVersion": 1,
            "position": [432, 592],
            "id": "wait-for-user-001",
            "name": "Wait for User",
            "webhookId": "wait-for-user-webhook-001"
        },

        # 4. Init Counter
        {
            "parameters": {
                "assignments": {
                    "assignments": [
                        {
                            "id": "counter-init-001",
                            "name": "iteration_count",
                            "value": "0",
                            "type": "number"
                        },
                        {
                            "id": "summary-id-001",
                            "name": "summary_id",
                            "value": "={{ $('Create Summary').item.json.summary_id }}",
                            "type": "string"
                        },
                        {
                            "id": "process-id-001",
                            "name": "process_id",
                            "value": "={{ $('Start Processing').item.json.process_id }}",
                            "type": "string"
                        }
                    ]
                },
                "options": {}
            },
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.4,
            "position": [656, 592],
            "id": "init-counter-001",
            "name": "Init Counter"
        },

        # 5. Check Summary Status
        {
            "parameters": {
                "url": "=http://217.182.76.146/api/summary/{{ $json.summary_id }}/status",
                "options": {
                    "timeout": 10000,
                    "retry": {
                        "maxTries": 2,
                        "waitBetweenRetries": 1000
                    }
                }
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [880, 592],
            "id": "check-summary-status-001",
            "name": "Check Summary Status"
        },

        # 6. Increment Counter
        {
            "parameters": {
                "assignments": {
                    "assignments": [
                        {
                            "id": "counter-increment-001",
                            "name": "iteration_count",
                            "value": "={{ $('Init Counter').item.json.iteration_count + 1 }}",
                            "type": "number"
                        },
                        {
                            "id": "summary-id-keep-001",
                            "name": "summary_id",
                            "value": "={{ $('Init Counter').item.json.summary_id }}",
                            "type": "string"
                        },
                        {
                            "id": "process-id-keep-001",
                            "name": "process_id",
                            "value": "={{ $('Init Counter').item.json.process_id }}",
                            "type": "string"
                        },
                        {
                            "id": "status-keep-001",
                            "name": "status",
                            "value": "={{ $json.status }}",
                            "type": "string"
                        }
                    ]
                },
                "options": {}
            },
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.4,
            "position": [1104, 592],
            "id": "increment-counter-001",
            "name": "Increment Counter"
        },

        # 7. Is Approved or Timeout?
        {
            "parameters": {
                "rules": {
                    "rules": [
                        {
                            "id": "rule-approved-001",
                            "outputKey": "approved",
                            "conditions": {
                                "conditions": [
                                    {
                                        "id": "condition-approved-001",
                                        "leftValue": "={{ $json.status }}",
                                        "rightValue": "approved",
                                        "operator": {
                                            "type": "string",
                                            "operation": "equals"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "id": "rule-rejected-001",
                            "outputKey": "rejected",
                            "conditions": {
                                "conditions": [
                                    {
                                        "id": "condition-rejected-001",
                                        "leftValue": "={{ $json.status }}",
                                        "rightValue": "rejected",
                                        "operator": {
                                            "type": "string",
                                            "operation": "equals"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "id": "rule-timeout-001",
                            "outputKey": "timeout",
                            "conditions": {
                                "conditions": [
                                    {
                                        "id": "condition-timeout-001",
                                        "leftValue": "={{ $json.iteration_count }}",
                                        "rightValue": "60",
                                        "operator": {
                                            "type": "number",
                                            "operation": "gte"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                },
                "options": {
                    "fallbackOutput": "continue_polling"
                }
            },
            "type": "n8n-nodes-base.switch",
            "typeVersion": 3,
            "position": [1328, 592],
            "id": "is-approved-or-timeout-001",
            "name": "Is Approved or Timeout?"
        },

        # 8. Wait 10 Seconds
        {
            "parameters": {
                "amount": 10,
                "unit": "seconds"
            },
            "type": "n8n-nodes-base.wait",
            "typeVersion": 1,
            "position": [1104, 816],
            "id": "wait-10-seconds-001",
            "name": "Wait 10 Seconds",
            "webhookId": "wait-10-seconds-webhook-001"
        },

        # 9. Get Approved Summary
        {
            "parameters": {
                "url": "=http://217.182.76.146/api/summary/{{ $json.summary_id }}/approved",
                "options": {
                    "timeout": 10000,
                    "retry": {
                        "maxTries": 3,
                        "waitBetweenRetries": 2000
                    }
                }
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [1552, 368],
            "id": "get-approved-summary-001",
            "name": "Get Approved Summary"
        },

        # 10. Merge Final Data
        {
            "parameters": {
                "mode": "combine",
                "combineBy": "combineByPosition",
                "options": {}
            },
            "type": "n8n-nodes-base.merge",
            "typeVersion": 3.2,
            "position": [1776, 480],
            "id": "merge-final-data-001",
            "name": "Merge Final Data"
        },

        # 11. Format Final Email
        {
            "parameters": {
                "jsCode": "// Pobranie zatwierdzonego podsumowania\nconst summaryText = $input.first().json.summary_text || \"\";\nconst fileid = $input.last().json.report_filename || \"\";\nconst processId = $input.first().json.process_id || \"\";\nconst approvedBy = $input.first().json.metadata?.approved_by || \"Użytkownik\";\nconst approvedAt = $input.first().json.metadata?.approved_at || \"\";\n\n// Formatowanie podsumowania\nlet content = summaryText.trim();\n\n// Obsługa różnych formatów\nif (content.match(/^\\d+\\./m)) {\n  content = content\n    .split(/\\n*\\d+\\.\\s+/)\n    .filter(line => line.trim() !== \"\")\n    .map(line => `<li>${line.trim()}</li>`)\n    .join(\"\\n\");\n} else if (content.includes('-')) {\n  content = content\n    .split(/\\s*-\\s+/)\n    .filter(line => line.trim() !== \"\")\n    .map(line => `<li>${line.trim()}</li>`)\n    .join(\"\\n\");\n} else {\n  content = content\n    .split(/\\n+/)\n    .filter(line => line.trim() !== \"\")\n    .map(line => `<li>${line.trim()}</li>`)\n    .join(\"\\n\");\n}\n\nconst formattedContent = `\n<p><b>Podsumowanie kluczowych zmian:</b></p>\n<ul style=\"color:#707173; font-size:11pt; padding-left:20px;\">\n${content}\n</ul>\n\n<p style=\"color:#009795; font-size:9pt; margin-top:20px;\">\n  ✅ Zatwierdzone przez: <b>${approvedBy}</b><br>\n  📅 Data zatwierdzenia: <b>${new Date(approvedAt).toLocaleString('pl-PL')}</b>\n</p>\n`;\n\nconst htmlTemplate = `\n<table border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\n<tbody>\n<tr>\n<td style=\"width: 220px; text-align: center; vertical-align: middle;\">\n<div style=\"text-align: center; padding: 10px;\">\n<img src=\"data:image/png;base64,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\" \n     width=\"80\" \n     height=\"80\"\n     style=\"width: 80px !important; height: 80px !important; max-width: 80px !important; max-height: 80px !important; display: inline-block;\">\n</div>\n</td>\n<td>\n<p><span style=\"color: #009795;font-size: 12pt;\"><b>Zapoznaj się z nowym aktem wewnętrznym / Check out the new internal act</b></span></p>\n</td>\n</tr>\n<tr><td colspan=\"2\" style=\"border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;\"></td></tr>\n<tr><td><span style=\"color: #707173;font-size: 11pt;\">Process ID</span></td><td style=\"padding-left: 15px;\"><span style=\"color: #707173;font-size: 11pt;\">${processId}</span></td></tr>\n<tr><td colspan=\"2\" style=\"border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;\"></td></tr>\n<tr><td colspan=\"2\" style=\"height:15px;\"></td></tr>\n<tr>\n<td><p><span style=\"color: #707173;font-size: 11pt;\">Podsumowanie zmian/Summary of changes</span></p></td>\n<td style=\"padding-left: 15px;\"><p style=\"text-align: justify; white-space: normal;\">${formattedContent}</p></td>\n</tr>\n<tr><td colspan=\"2\" style=\"border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;\"></td></tr>\n<tr>\n<td><p><span style=\"color: #707173;font-size: 11pt;\">Szczegółowa analiza zmian</span></p></td>\n<td style=\"padding-left: 15px;\"><p><a href=\"http://217.182.76.146/reports/${fileid}\" target=\"_blank\" style=\"color: #009795;\">Link do podsumowania zmian</a></p></td>\n</tr>\n<tr><td colspan=\"2\" style=\"border-bottom: 1px solid rgb(0,150,150); height: 1px; padding: 0;\"></td></tr>\n</tbody>\n</table>\n\n<p><span style=\"color: #009795;font-size: 12pt;\"><b>Wiadomość wygenerowana automatycznie, nie odpowiadaj na nią / Automatically generated message, please do not reply to it.</b></span></p>\n`;\n\nreturn [{ json: { html: htmlTemplate } }];"
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [2000, 480],
            "id": "format-final-email-001",
            "name": "Format Final Email"
        },

        # 12. Send Final Email
        {
            "parameters": {
                "fromEmail": "ai_baw@credit-agricole.pl",
                "toEmail": "trembiasz@credit-agricole.pl",
                "subject": "✅ Nowy akt wewnętrzny - ZATWIERDZONE podsumowanie",
                "html": "={{ $json.html }}",
                "options": {}
            },
            "type": "n8n-nodes-base.emailSend",
            "typeVersion": 2.1,
            "position": [2224, 480],
            "id": "send-final-email-001",
            "name": "Send Final Email",
            "credentials": {
                "smtp": {
                    "id": "2joSLF2U4RnAaaXW",
                    "name": "SMTP account 4"
                }
            }
        },

        # 13. Log Timeout Error
        {
            "parameters": {
                "resource": "row",
                "operation": "create",
                "tableName": "errors",
                "fieldsToSend": "defineInNode",
                "fieldsUi": {
                    "fieldValues": [
                        {
                            "fieldId": "error_type",
                            "fieldValue": "TIMEOUT"
                        },
                        {
                            "fieldId": "error_message",
                            "fieldValue": "=Summary approval timeout after 60 iterations (10 minutes)"
                        },
                        {
                            "fieldId": "process_id",
                            "fieldValue": "={{ $json.process_id }}"
                        },
                        {
                            "fieldId": "summary_id",
                            "fieldValue": "={{ $json.summary_id }}"
                        },
                        {
                            "fieldId": "timestamp",
                            "fieldValue": "={{ $now.toISO() }}"
                        }
                    ]
                }
            },
            "type": "n8n-nodes-base.seaTable",
            "typeVersion": 2,
            "position": [1552, 816],
            "id": "log-timeout-error-001",
            "name": "Log Timeout Error",
            "credentials": {
                "seaTableApi": {
                    "id": "308kg9y7cDXLbrvU",
                    "name": "SeaTable account 3"
                }
            }
        },

        # 14. Send Timeout Email
        {
            "parameters": {
                "fromEmail": "ai_baw@credit-agricole.pl",
                "toEmail": "trembiasz@credit-agricole.pl",
                "subject": "⚠️ TIMEOUT - Brak zatwierdzenia podsumowania",
                "html": "=<html>\n<head>\n  <meta charset=\"UTF-8\">\n</head>\n<body style=\"font-family: Arial, sans-serif; color: #333;\">\n  <h2 style=\"color: #ED1B2F;\">⚠️ Przekroczono czas oczekiwania na zatwierdzenie</h2>\n  \n  <p>System BAW czekał 10 minut na zatwierdzenie podsumowania, ale nie otrzymał odpowiedzi.</p>\n  \n  <table style=\"border-collapse: collapse; width: 100%; max-width: 600px; margin: 20px 0;\">\n    <tr style=\"background-color: #f5f5f5;\">\n      <td style=\"padding: 10px; border: 1px solid #ddd; font-weight: bold;\">Process ID:</td>\n      <td style=\"padding: 10px; border: 1px solid #ddd;\">{{ $json.process_id }}</td>\n    </tr>\n    <tr>\n      <td style=\"padding: 10px; border: 1px solid #ddd; font-weight: bold;\">Summary ID:</td>\n      <td style=\"padding: 10px; border: 1px solid #ddd;\">{{ $json.summary_id }}</td>\n    </tr>\n    <tr style=\"background-color: #f5f5f5;\">\n      <td style=\"padding: 10px; border: 1px solid #ddd; font-weight: bold;\">Status:</td>\n      <td style=\"padding: 10px; border: 1px solid #ddd;\">❌ TIMEOUT (60 iteracji × 10s)</td>\n    </tr>\n  </table>\n  \n  <p>Możesz nadal zatwierdzić podsumowanie manualnie:</p>\n  <a href=\"http://217.182.76.146/summary/{{ $json.summary_id }}\" \n     style=\"display: inline-block; background-color: #009795; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;\">\n    Przejdź do podsumowania\n  </a>\n  \n  <hr style=\"border: none; border-top: 1px solid #ddd; margin: 30px 0;\">\n  <p style=\"color: #999; font-size: 12px;\">System BAW AI - Error Notification</p>\n</body>\n</html>",
                "options": {}
            },
            "type": "n8n-nodes-base.emailSend",
            "typeVersion": 2.1,
            "position": [1776, 816],
            "id": "send-timeout-email-001",
            "name": "Send Timeout Email",
            "credentials": {
                "smtp": {
                    "id": "2joSLF2U4RnAaaXW",
                    "name": "SMTP account 4"
                }
            }
        },

        # 15. Send Rejection Email
        {
            "parameters": {
                "fromEmail": "ai_baw@credit-agricole.pl",
                "toEmail": "trembiasz@credit-agricole.pl",
                "subject": "❌ Podsumowanie dokumentu zostało odrzucone",
                "html": "=<html>\n<head>\n  <meta charset=\"UTF-8\">\n</head>\n<body style=\"font-family: Arial, sans-serif; color: #333;\">\n  <h2 style=\"color: #ED1B2F;\">❌ Podsumowanie odrzucone</h2>\n  \n  <p>Użytkownik odrzucił automatycznie wygenerowane podsumowanie.</p>\n  \n  <table style=\"border-collapse: collapse; width: 100%; max-width: 600px; margin: 20px 0;\">\n    <tr style=\"background-color: #f5f5f5;\">\n      <td style=\"padding: 10px; border: 1px solid #ddd; font-weight: bold;\">Process ID:</td>\n      <td style=\"padding: 10px; border: 1px solid #ddd;\">{{ $json.process_id }}</td>\n    </tr>\n    <tr>\n      <td style=\"padding: 10px; border: 1px solid #ddd; font-weight: bold;\">Summary ID:</td>\n      <td style=\"padding: 10px; border: 1px solid #ddd;\">{{ $json.summary_id }}</td>\n    </tr>\n    <tr style=\"background-color: #f5f5f5;\">\n      <td style=\"padding: 10px; border: 1px solid #ddd; font-weight: bold;\">Status:</td>\n      <td style=\"padding: 10px; border: 1px solid #ddd;\">❌ REJECTED</td>\n    </tr>\n  </table>\n  \n  <p>Workflow został zakończony. Użytkownik może wygenerować nowe podsumowanie manualnie.</p>\n  \n  <hr style=\"border: none; border-top: 1px solid #ddd; margin: 30px 0;\">\n  <p style=\"color: #999; font-size: 12px;\">System BAW AI - Notification</p>\n</body>\n</html>",
                "options": {}
            },
            "type": "n8n-nodes-base.emailSend",
            "typeVersion": 2.1,
            "position": [1552, 592],
            "id": "send-rejection-email-001",
            "name": "Send Rejection Email",
            "credentials": {
                "smtp": {
                    "id": "2joSLF2U4RnAaaXW",
                    "name": "SMTP account 4"
                }
            }
        }
    ]

def update_connections(workflow, new_nodes):
    """Zaktualizuj connections - dodaj nowe połączenia"""

    connections = workflow.get("connections", {})

    # Usuń stare połączenie: AI Agent3 → Merge
    if "AI Agent3" in connections:
        # Zachowaj tylko inne połączenia jeśli istnieją
        ai_agent3_connections = connections["AI Agent3"].get("main", [[]])
        # Filtruj połączenia - usuń te do "Merge"
        filtered_connections = []
        for conn_group in ai_agent3_connections:
            filtered_group = [c for c in conn_group if c.get("node") != "Merge"]
            if filtered_group:
                filtered_connections.append(filtered_group)

        # Dodaj nowe połączenie do Create Summary
        if not filtered_connections:
            filtered_connections = [[]]
        filtered_connections[0].append({
            "node": "Create Summary",
            "type": "main",
            "index": 0
        })
        connections["AI Agent3"]["main"] = filtered_connections

    # Dodaj nowe połączenia
    new_connections = {
        "Create Summary": {
            "main": [[{
                "node": "Send Edit Link Email",
                "type": "main",
                "index": 0
            }]]
        },
        "Send Edit Link Email": {
            "main": [[{
                "node": "Wait for User",
                "type": "main",
                "index": 0
            }]]
        },
        "Wait for User": {
            "main": [[{
                "node": "Init Counter",
                "type": "main",
                "index": 0
            }]]
        },
        "Init Counter": {
            "main": [[{
                "node": "Check Summary Status",
                "type": "main",
                "index": 0
            }]]
        },
        "Check Summary Status": {
            "main": [[{
                "node": "Increment Counter",
                "type": "main",
                "index": 0
            }]]
        },
        "Increment Counter": {
            "main": [[{
                "node": "Is Approved or Timeout?",
                "type": "main",
                "index": 0
            }]]
        },
        "Is Approved or Timeout?": {
            "main": [
                [{
                    "node": "Get Approved Summary",
                    "type": "main",
                    "index": 0
                }],
                [{
                    "node": "Send Rejection Email",
                    "type": "main",
                    "index": 0
                }],
                [{
                    "node": "Log Timeout Error",
                    "type": "main",
                    "index": 0
                }],
                [{
                    "node": "Wait 10 Seconds",
                    "type": "main",
                    "index": 0
                }]
            ]
        },
        "Wait 10 Seconds": {
            "main": [[{
                "node": "Check Summary Status",
                "type": "main",
                "index": 0
            }]]
        },
        "Get Approved Summary": {
            "main": [[{
                "node": "Merge Final Data",
                "type": "main",
                "index": 0
            }]]
        },
        "HTTP Request": {
            "main": [[{
                "node": "Merge Final Data",
                "type": "main",
                "index": 1
            }]]
        },
        "Merge Final Data": {
            "main": [[{
                "node": "Format Final Email",
                "type": "main",
                "index": 0
            }]]
        },
        "Format Final Email": {
            "main": [[{
                "node": "Send Final Email",
                "type": "main",
                "index": 0
            }]]
        },
        "Log Timeout Error": {
            "main": [[{
                "node": "Send Timeout Email",
                "type": "main",
                "index": 0
            }]]
        }
    }

    # Merge nowych połączeń
    connections.update(new_connections)
    workflow["connections"] = connections

    return workflow

def enhance_workflow(input_file, output_file):
    """Główna funkcja - wczytaj, zmodyfikuj, zapisz"""
    print(f"Wczytuje workflow z: {input_file}")
    workflow = load_workflow(input_file)

    print(f"Tworze 15 nowych wezlow...")
    new_nodes = create_new_nodes()

    print(f"Dodaje wezly do workflow...")
    workflow["nodes"].extend(new_nodes)

    print(f"Aktualizuje connections...")
    workflow = update_connections(workflow, new_nodes)

    print(f"Zapisuje Enhanced Workflow do: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"Gotowe!")
    print(f"")
    print(f"Statystyki:")
    print(f"  - Wezlow w v1.0: {len(workflow['nodes']) - 15}")
    print(f"  - Wezlow v v2.0: {len(workflow['nodes'])}")
    print(f"  - Dodano: +15 wezlow")
    print(f"")
    print(f"Nastepne kroki:")
    print(f"  1. Import {output_file} do N8N")
    print(f"  2. Zweryfikuj credentials (SMTP, SeaTable)")
    print(f"  3. Test workflow: Execute Workflow")

def main():
    input_file = Path("C:/Projects/BAW/API 04.json")
    output_file = Path("C:/Projects/BAW/API 04 Enhanced.json")

    if not input_file.exists():
        print(f"Blad: Nie znaleziono pliku {input_file}")
        sys.exit(1)

    enhance_workflow(str(input_file), str(output_file))

if __name__ == "__main__":
    main()
