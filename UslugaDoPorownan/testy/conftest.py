
import pytest
import time
from pathlib import Path
from fastapi.testclient import TestClient
from UslugaDoPorownan.main import app


@pytest.fixture(scope="module")
def client():
    """Fixture dostarczający klienta testowego FastAPI."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def completed_process_id(client):
    """Fixture, który wykonuje pełny proces porównania i zwraca process_id."""
    old_doc_path = Path("stara_wersja/test_doc.docx")
    new_doc_path = Path("nowa_wersja/test_doc.docx")

    assert old_doc_path.exists()
    assert new_doc_path.exists()

    # Krok 1: Upload
    with open(old_doc_path, "rb") as old_f, open(new_doc_path, "rb") as new_f:
        files = {
            "old_document": (old_doc_path.name, old_f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            "new_document": (new_doc_path.name, new_f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        }
        response = client.post("/api/documents/upload", files=files)
    
    assert response.status_code == 200
    document_pair_id = response.json()["document_pair_id"]

    # Krok 2: Process
    response = client.post("/api/process", json={"document_pair_id": document_pair_id})
    assert response.status_code == 200
    process_id = response.json()["process_id"]

    # Krok 3: Polling
    timeout = 60
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = client.get(f"/api/status/{process_id}")
        assert response.status_code == 200
        status_data = response.json()
        if status_data["status"] == "completed":
            return process_id  # Zwróć process_id i zakończ fixture
        time.sleep(2)
    
    pytest.fail("Przekroczono czas oczekiwania na przetworzenie dokumentu w fixturze.")
