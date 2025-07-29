from fastapi.testclient import TestClient
from main import app
import os
import json

client = TestClient(app)

TEST_PRODUCT = {
    "product_id": "TEST123",
    "name": "Test Widget",
    "stock_quantity": 5,
    "min_threshold": 4,
    "restock_quantity": 60,
    "priority": "high"
}

LOW_PRIORITY_PRODUCT = {
    "product_id": "LOWP456",
    "name": "Low Priority Widget",
    "stock_quantity": 3,
    "min_threshold": 2,
    "restock_quantity": 30,
    "priority": "low"
}

def cleanup():
    """Reset storage.json before each test run."""
    if os.path.exists("storage.json"):
        with open("storage.json", "w") as f:
            json.dump({}, f)

def test_add_high_priority_product():
    cleanup()
    response = client.post("/products", json=TEST_PRODUCT)
    assert response.status_code == 200
    assert response.json()["product"]["priority"] == "high"
    assert response.json()["product"]["min_threshold"] == 10  # auto-enforced
    assert response.json()["product"]["category"] == "high_volume"

def test_add_low_priority_product():
    response = client.post("/products", json=LOW_PRIORITY_PRODUCT)
    assert response.status_code == 200
    assert response.json()["product"]["priority"] == "low"
    assert response.json()["product"]["min_threshold"] == 2  # no override
    assert response.json()["product"]["category"] == "low_volume"

def test_get_product_status_high_priority_auto_restock():
    response = client.get(f"/products/{TEST_PRODUCT['product_id']}/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["priority"] == "high"

def test_get_product_status_low_priority_no_auto_restock():
    response = client.get(f"/products/{LOW_PRIORITY_PRODUCT['product_id']}/status")
    assert response.status_code == 200
    data = response.json()
    # Still below threshold because low-priority isn't auto-restocked
    assert data["status"] in ["below_threshold", "ok", "out_of_stock"]
    assert data["priority"] == "low"

def test_purchase_product():
    response = client.post(
        f"/products/{TEST_PRODUCT['product_id']}/purchase",
        json={"quantity": 2}
    )
    assert response.status_code == 200
    assert "updated_stock" in response.json()

def test_manual_restock_low_priority():
    # Manually restock the low-priority product
    response = client.post(f"/products/{LOW_PRIORITY_PRODUCT['product_id']}/restock")
    assert response.status_code == 200
    assert "Manual restock successful" == response.json()["message"]


def test_list_all_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert TEST_PRODUCT["product_id"] in response.json()

def test_duplicate_product_id():
    # Attempt to add duplicate product
    response = client.post("/products", json=TEST_PRODUCT)
    assert response.status_code == 400
    assert response.json()["detail"] == "Product already exists"

def test_product_not_found_status():
    response = client.get("/products/INVALID123/status")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_product_not_found_purchase():
    response = client.post("/products/INVALID123/purchase", json={"quantity": 1})
    assert response.status_code == 404

def test_over_purchase_error():
    response = client.post(
        f"/products/{TEST_PRODUCT['product_id']}/purchase",
        json={"quantity": 999}
    )
    assert response.status_code == 400
    assert "Not enough stock" in response.json()["detail"]
