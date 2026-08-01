import pytest
from fastapi.testclient import TestClient
from src.main import app, storage


@pytest.fixture(autouse=True)
def reset_storage():
    storage.clear()
    yield
    storage.clear()


client = TestClient(app)

SAMPLE_EXPENSE = {
    "title": "Lunch",
    "amount": 15.50,
    "category": "Food",
    "date": "2025-01-15",
}


def test_create_expense():
    response = client.post("/expenses", json=SAMPLE_EXPENSE)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Lunch"
    assert data["amount"] == 15.50
    assert data["category"] == "Food"
    assert data["date"] == "2025-01-15"


def test_list_all_expenses():
    client.post("/expenses", json=SAMPLE_EXPENSE)
    client.post("/expenses", json={**SAMPLE_EXPENSE, "title": "Coffee", "amount": 5.00, "category": "Drinks"})

    response = client.get("/expenses")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_by_category():
    client.post("/expenses", json=SAMPLE_EXPENSE)
    client.post("/expenses", json={**SAMPLE_EXPENSE, "title": "Coffee", "amount": 5.00, "category": "Drinks"})

    response = client.get("/expenses?category=Food")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "Food"


def test_filter_by_category_case_insensitive():
    client.post("/expenses", json=SAMPLE_EXPENSE)

    response = client.get("/expenses?category=food")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_totals():
    client.post("/expenses", json=SAMPLE_EXPENSE)
    client.post("/expenses", json={**SAMPLE_EXPENSE, "title": "Dinner", "amount": 25.00})
    client.post("/expenses", json={**SAMPLE_EXPENSE, "title": "Bus", "amount": 3.00, "category": "Transport"})

    response = client.get("/expenses/total")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 43.50
    assert len(data["by_category"]) == 2
    food = next(c for c in data["by_category"] if c["category"] == "Food")
    assert food["total"] == 40.50


def test_delete_expense():
    client.post("/expenses", json=SAMPLE_EXPENSE)

    response = client.delete("/expenses/1")
    assert response.status_code == 200

    response = client.get("/expenses")
    assert len(response.json()) == 0


def test_delete_nonexistent():
    response = client.delete("/expenses/999")
    assert response.status_code == 404


def test_validation_negative_amount():
    bad = {**SAMPLE_EXPENSE, "amount": -10}
    response = client.post("/expenses", json=bad)
    assert response.status_code == 422


def test_validation_missing_title():
    bad = {"amount": 10, "category": "Food", "date": "2025-01-15"}
    response = client.post("/expenses", json=bad)
    assert response.status_code == 422


def test_id_survives_delete():
    client.post("/expenses", json=SAMPLE_EXPENSE)
    client.post("/expenses", json={**SAMPLE_EXPENSE, "title": "Coffee", "amount": 5.00})
    client.delete("/expenses/1")

    response = client.post("/expenses", json={**SAMPLE_EXPENSE, "title": "Tea", "amount": 3.00})
    data = response.json()
    assert data["id"] == 3
