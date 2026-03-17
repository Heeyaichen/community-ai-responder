import pytest
from fastapi.testclient import TestClient
from app.main import app


def test_main():
    client = TestClient(app=app)
    
    def test_health_check():
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["version"] == "1.0.0"
