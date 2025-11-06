
from fastapi.testclient import TestClient
import pytest
from UslugaDoPorownan.main import app

client = TestClient(app)


def test_read_root():
    """Testuje główny endpoint '/'."""
    response = client.get("/")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["service"] == "Usługa Porównywania Dokumentów"
    assert "endpoints" in json_response
    assert "summary_endpoints" in json_response


def test_health_check():
    """Testuje endpoint '/health'."""
    response = client.get("/health")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "healthy"
    assert "timestamp" in json_response
    assert "statistics" in json_response

