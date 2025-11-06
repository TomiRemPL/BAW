
import time
from pathlib import Path
from fastapi.testclient import TestClient
import pytest
from UslugaDoPorownan.main import app

client = TestClient(app)

# Definicja ścieżek do plików testowych
# Zakładamy, że testy są uruchamiane z głównego katalogu projektu BAW
OLD_DOC_PATH = Path("stara_wersja/test_doc.docx")
NEW_DOC_PATH = Path("nowa_wersja/test_doc.docx")

@pytest.mark.slow  # Oznaczamy jako wolny test
def test_full_processing_workflow():
    """Testuje pełny przepływ przetwarzania: upload, process, status, result."""
    # Upewnij się, że pliki testowe istnieją
    assert OLD_DOC_PATH.exists(), f"Plik testowy nie istnieje: {OLD_DOC_PATH}"
    assert NEW_DOC_PATH.exists(), f"Plik testowy nie istnieje: {NEW_DOC_PATH}"

    # --- Krok 1: Upload dokumentów ---
    with open(OLD_DOC_PATH, "rb") as old_file, open(NEW_DOC_PATH, "rb") as new_file:
        files = {
            "old_document": (OLD_DOC_PATH.name, old_file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            "new_document": (NEW_DOC_PATH.name, new_file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        }
        response = client.post("/api/documents/upload", files=files)

    assert response.status_code == 200
    upload_data = response.json()
    assert "document_pair_id" in upload_data
    document_pair_id = upload_data["document_pair_id"]

    # --- Krok 2: Rozpoczęcie przetwarzania ---
    response = client.post("/api/process", json={"document_pair_id": document_pair_id})
    assert response.status_code == 200
    process_data = response.json()
    assert "process_id" in process_data
    process_id = process_data["process_id"]

    # --- Krok 3: Sprawdzanie statusu (Polling) ---
    timeout = 60  # sekundy
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = client.get(f"/api/status/{process_id}")
        assert response.status_code == 200
        status_data = response.json()
        if status_data["status"] == "completed":
            break
        assert status_data["status"] != "error", f"Błąd przetwarzania: {status_data.get('error')}"
        time.sleep(2)  # Czekaj 2 sekundy przed kolejnym sprawdzeniem
    else:
        pytest.fail(f"Przekroczono czas oczekiwania ({timeout}s) na zakończenie przetwarzania.")

    assert status_data["status"] == "completed"

    # --- Krok 4: Pobranie wyników ---
    response = client.get(f"/api/result/{process_id}/full")
    assert response.status_code == 200
    result_data = response.json()

    assert result_data["process_id"] == process_id
    assert "paragraphs" in result_data
    assert "statistics" in result_data
    assert len(result_data["paragraphs"]) > 0

    # Sprawdź, czy zmiany zostały wykryte
    paragraph_types = {p["type"] for p in result_data["paragraphs"]}
    assert "modified" in paragraph_types
    assert "unchanged" in paragraph_types

