import json
from models import Product

DATA_FILE = "storage.json"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def determine_category(restock_quantity: int) -> str:
    return "high_volume" if restock_quantity > 50 else "low_volume"

def apply_business_rules(product: Product) -> dict:
    data = product.dict()

    # Rule: If high priority and min_threshold < 10, set to 10
    if data["priority"] == "high" and data["min_threshold"] < 10:
        data["min_threshold"] = 10

    # Always assign category at creation
    data["category"] = determine_category(data["restock_quantity"])

    return data

def check_and_restock(product: dict) -> dict:
    if (
        product["priority"] == "high" and
        product["stock_quantity"] < product["min_threshold"]
    ):
        product["stock_quantity"] += product["restock_quantity"]
    return product
