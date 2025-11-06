# -*- coding: utf-8 -*-
"""
Naprawa noda POST Summary to API - poprawna składnia n8n
"""
import json
from pathlib import Path

def fix_post_summary_node_v2(workflow_data):
    """Napraw node POST Summary to API - wersja 2"""

    for node in workflow_data["nodes"]:
        if node["name"] == "POST Summary to API":
            print(f"Znaleziono node: {node['name']} (ID: {node['id']})")

            # Usuń stare parametry
            node["parameters"] = {
                "method": "POST",
                "url": "http://217.182.76.146/api/summary",
                "authentication": "none",
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": """={{ JSON.stringify({
  process_id: $('Start Processing').item.json.process_id,
  summary_text: $('AI Agent4').item.json.output,
  metadata: {
    przedmiot_regulacji: "Dokument",
    data_aktu: "",
    data_wejscia_w_zycie: ""
  }
}) }}""",
                "options": {
                    "timeout": 30000
                }
            }

            print("[OK] Node naprawiony - poprawna składnia n8n")
            return True

    print("[BŁĄD] Nie znaleziono noda 'POST Summary to API'")
    return False

def main():
    """Główna funkcja"""
    input_file = Path("C:/Projects/BAW/API 06 - with edit link.json")
    output_file = Path("C:/Projects/BAW/API 08 - fixed POST v2.json")

    print(f"Wczytywanie workflow z {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    print(f"Naprawianie noda POST Summary to API (v2)...")
    if fix_post_summary_node_v2(workflow):
        print("[OK] Node naprawiony")
    else:
        print("[BŁĄD] Nie udało się naprawić")
        return

    # Zaktualizuj nazwę workflow
    workflow["name"] = "API 08 - fixed POST v2"

    # Generuj nowe ID wersji
    import uuid
    workflow["versionId"] = str(uuid.uuid4())

    print(f"Zapisywanie do {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"[OK] Gotowe!")
    print(f"\nZmiany:")
    print("  - Użyto JSON.stringify() dla n8n")
    print("  - Poprawne odwołania do danych z innych nodów")
    print("  - Content-Type: application/json")
    print(f"\nPlik zapisany: {output_file}")

if __name__ == "__main__":
    main()
