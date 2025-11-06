
import pytest

def test_summary_workflow(client, completed_process_id):
    """Testuje cały przepływ pracy z podsumowaniem: od utworzenia po zatwierdzenie."""
    process_id = completed_process_id

    # --- Krok 1: Utworzenie podsumowania ---
    response = client.post(
        "/api/summary",
        json={
            "process_id": process_id,
            "summary_text": "Initial summary text.",
            "metadata": {"author": "test_suite"},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["process_id"] == process_id
    assert data["status"] == "pending_review"

    # --- Krok 2: Sprawdzenie statusu ---
    response = client.get(f"/api/summary/{process_id}/status")
    assert response.status_code == 200
    assert response.json()["status"] == "pending_review"

    # --- Krok 3: Sprawdzenie szczegółów ---
    response = client.get(f"/api/summary/{process_id}")
    assert response.status_code == 200
    assert response.json()["summary_text"] == "Initial summary text."

    # --- Krok 4: Próba pobrania przed zatwierdzeniem (oczekiwany błąd) ---
    response = client.get(f"/api/summary/{process_id}/approved")
    assert response.status_code == 400

    # --- Krok 5: Aktualizacja podsumowania ---
    response = client.put(
        f"/api/summary/{process_id}",
        json={
            "summary_text": "Updated summary text.",
            "metadata": {"author": "test_suite", "editor": "pytest"},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["summary_text"] == "Updated summary text."
    assert data["edited_by_user"] is True

    # --- Krok 6: Zatwierdzenie podsumowania ---
    response = client.post(f"/api/summary/{process_id}/approve", json={"approved": True})
    assert response.status_code == 200
    assert response.json()["status"] == "approved"

    # --- Krok 7: Pobranie zatwierdzonego podsumowania ---
    response = client.get(f"/api/summary/{process_id}/approved")
    assert response.status_code == 200
    data = response.json()
    assert data["summary_text"] == "Updated summary text."
