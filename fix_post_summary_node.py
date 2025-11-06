# -*- coding: utf-8 -*-
"""
Naprawa noda POST Summary to API - zmiana z bodyParameters na JSON body
"""
import json
from pathlib import Path

def fix_post_summary_node(workflow_data):
    """Napraw node POST Summary to API"""

    for node in workflow_data["nodes"]:
        if node["name"] == "POST Summary to API":
            print(f"Znaleziono node: {node['name']} (ID: {node['id']})")

            # Usuń stare parametry
            if "bodyParameters" in node["parameters"]:
                del node["parameters"]["bodyParameters"]

            # Dodaj poprawne parametry JSON
            node["parameters"]["sendBody"] = True
            node["parameters"]["specifyBody"] = "json"
            node["parameters"]["jsonBody"] = """={
  "process_id": {{ $('Start Processing').item.json.process_id.toJsonString() }},
  "summary_text": {{ $('AI Agent4').item.json.output.toJsonString() }},
  "metadata": {
    "przedmiot_regulacji": "Dokument",
    "data_aktu": "",
    "data_wejscia_w_zycie": ""
  }
}"""

            print("[OK] Node naprawiony - używa teraz JSON body")
            return True

    print("[BŁĄD] Nie znaleziono noda 'POST Summary to API'")
    return False

def main():
    """Główna funkcja"""
    input_file = Path("C:/Projects/BAW/API 06 - with edit link.json")
    output_file = Path("C:/Projects/BAW/API 07 - fixed POST.json")

    print(f"Wczytywanie workflow z {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    print(f"Naprawianie noda POST Summary to API...")
    if fix_post_summary_node(workflow):
        print("[OK] Node naprawiony")
    else:
        print("[BŁĄD] Nie udało się naprawić")
        return

    # Zaktualizuj nazwę workflow
    workflow["name"] = "API 07 - fixed POST"

    # Generuj nowe ID wersji
    import uuid
    workflow["versionId"] = str(uuid.uuid4())

    print(f"Zapisywanie do {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"[OK] Gotowe!")
    print(f"\nZmiany:")
    print("  PRZED: bodyParameters (form-data)")
    print("  PO:    JSON body (application/json)")
    print(f"\nPlik zapisany: {output_file}")

if __name__ == "__main__":
    main()
