from unittest.mock import AsyncMock, patch
import pytest
from fastapi import HTTPException

def test_health_returns_ok(client):
    response = client.get("/healthz/live")  # правильный путь

    assert response.status_code == 200

def test_antifraud_check_success(client):
    response = client.post(
        "/antifraud/check",
        json={
            "birth_date": "22.08.1977",
            "phone_number": "+79235648563",
            "loans_history": []
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert data["stop_factors"] == []

def test_antifraud_check_failed(client):
    response = client.post(
        "/antifraud/check",
        json={
            "birth_date": "22.08.2010",
            "phone_number": "+79235648563",
            "loans_history": []
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is False
    assert len(data["stop_factors"]) > 0


@pytest.mark.parametrize("phone_number, expected_result", [
        ("+79235648563", 200),
        ("89235648563", 200),
        ("7d7771235653", 422),
        ("79135556677", 422),
        ("822244532322", 422),
        ])
def test_phone_valid(client, phone_number, expected_result):
    response = client.post(
        "antifraud/check",
        json={
            "birth_date": "02.12.2000",
            "phone_number": phone_number,
            "loans_history": []
        }
    )
    assert response.status_code == expected_result