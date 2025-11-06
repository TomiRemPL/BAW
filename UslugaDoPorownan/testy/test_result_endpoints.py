

def test_get_modified_sentences(client, completed_process_id):
    """Testuje pobieranie tylko zmodyfikowanych zdań."""
    response = client.get(f"/api/result/{completed_process_id}/modified")
    assert response.status_code == 200
    data = response.json()
    assert "process_id" in data
    assert "modified_sentences" in data
    assert isinstance(data["modified_sentences"], list)


def test_get_added_sentences(client, completed_process_id):
    """Testuje pobieranie tylko dodanych zdań."""
    response = client.get(f"/api/result/{completed_process_id}/added")
    assert response.status_code == 200
    data = response.json()
    assert "process_id" in data
    assert "added_sentences" in data
    assert isinstance(data["added_sentences"], list)


def test_get_deleted_sentences(client, completed_process_id):
    """Testuje pobieranie tylko usuniętych zdań."""
    response = client.get(f"/api/result/{completed_process_id}/deleted")
    assert response.status_code == 200
    data = response.json()
    assert "process_id" in data
    assert "deleted_sentences" in data
    assert isinstance(data["deleted_sentences"], list)


def test_generate_html_report(client, completed_process_id):
    """Testuje generowanie raportu HTML."""
    response = client.get(f"/api/report/{completed_process_id}/generate")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "report_url" in data
    assert data["report_url"].endswith(".html")
