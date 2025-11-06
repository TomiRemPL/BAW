# -*- coding: utf-8 -*-
"""
Aktualizacja workflow - dodanie linku do edycji podsumowania w mailu
"""
import json
from pathlib import Path

def update_send_review_email(workflow_data):
    """Zaktualizuj node Send Review Email z linkiem do edycji"""

    # Znajdź node "Send Review Email"
    for node in workflow_data["nodes"]:
        if node["name"] == "Send Review Email":
            # Zaktualizuj HTML maila z linkiem
            node["parameters"]["html"] = """=<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px 10px 0 0;">
        <h1 style="color: white; margin: 0; font-size: 24px;">📝 Podsumowanie dokumentu - weryfikacja</h1>
    </div>

    <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
        <p style="font-size: 16px; color: #333; margin-bottom: 20px;">
            <strong>Witaj!</strong>
        </p>

        <p style="font-size: 14px; color: #666; line-height: 1.6; margin-bottom: 20px;">
            System AI wygenerował podsumowanie zmian w dokumencie. Prosimy o weryfikację i zatwierdzenie treści.
        </p>

        <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; margin-bottom: 25px;">
            <h3 style="margin-top: 0; color: #333; font-size: 14px;">📄 Wygenerowane podsumowanie:</h3>
            <pre style="white-space: pre-wrap; font-family: Arial, sans-serif; font-size: 13px; color: #555; line-height: 1.6;">{{ $('AI Agent4').item.json.output }}</pre>
        </div>

        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 25px;">
            <p style="margin: 0; font-size: 13px; color: #856404;">
                <strong>💡 Co dalej?</strong><br>
                1. Kliknij poniższy link aby otworzyć edytor<br>
                2. Przejrzyj podsumowanie i wprowadź ewentualne poprawki<br>
                3. Zatwierdź lub odrzuć podsumowanie<br>
                4. System automatycznie wyśle finalny raport
            </p>
        </div>

        <div style="text-align: center; margin: 30px 0;">
            <a href="http://217.182.76.146/summary/{{ $('Start Processing').item.json.process_id }}"
               style="display: inline-block; background: #28a745; color: white; padding: 15px 40px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);">
                🔗 Otwórz edytor podsumowania
            </a>
        </div>

        <div style="background: #e9ecef; padding: 15px; border-radius: 8px; margin-top: 25px;">
            <p style="margin: 0; font-size: 12px; color: #6c757d; text-align: center;">
                <strong>Process ID:</strong> <code style="background: white; padding: 2px 6px; border-radius: 3px; font-family: monospace;">{{ $('Start Processing').item.json.process_id }}</code>
            </p>
        </div>

        <p style="font-size: 11px; color: #999; text-align: center; margin-top: 30px; border-top: 1px solid #dee2e6; padding-top: 20px;">
            Wiadomość wygenerowana automatycznie przez system n8n<br>
            Nie odpowiadaj na tego maila
        </p>
    </div>
</div>"""

            print(f"Zaktualizowano node: {node['name']} (ID: {node['id']})")
            return True

    return False

def main():
    """Główna funkcja"""
    input_file = Path("C:/Projects/BAW/API 05 - with summary.json")
    output_file = Path("C:/Projects/BAW/API 06 - with edit link.json")

    print(f"Wczytywanie workflow z {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    print(f"Aktualizowanie node Send Review Email...")
    if update_send_review_email(workflow):
        print("[OK] Node zaktualizowany")
    else:
        print("[BŁĄD] Nie znaleziono node 'Send Review Email'")
        return

    # Zaktualizuj nazwę workflow
    workflow["name"] = "API 06 - with edit link"

    # Generuj nowe ID wersji
    import uuid
    workflow["versionId"] = str(uuid.uuid4())

    print(f"Zapisywanie do {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"[OK] Gotowe!")
    print(f"\nLink do edycji w mailu: http://217.182.76.146/summary/{{process_id}}")
    print(f"Plik zapisany: {output_file}")

if __name__ == "__main__":
    main()
