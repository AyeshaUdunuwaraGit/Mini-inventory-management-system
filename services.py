import json
import os
import logging
from fastapi import HTTPException
from models import Product, PurchaseRequest
from utils import (
    load_data, save_data,
    apply_business_rules,
    check_and_restock
)

DATA_FILE = "storage.json"
LOG_FILE = "activity.log"

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize storage
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)


def add_new_product(product: Product):
    inventory = load_data()

    if product.product_id in inventory:
        raise HTTPException(status_code=400, detail="Product already exists")

    processed_product = apply_business_rules(product)
    inventory[product.product_id] = processed_product
    save_data(inventory)

    logging.info(f"Added product {product.product_id}")
    return {"message": "Product added", "product": processed_product}


def get_inventory_status(product_id: str):
    inventory = load_data()

    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")

    product = inventory[product_id]
    product = check_and_restock(product)
    inventory[product_id] = product
    save_data(inventory)

    stock = product["stock_quantity"]
    min_threshold = product["min_threshold"]
    priority = product["priority"]

    # High priority products never show "bad" status because they are auto-restocked
    if priority == "high":
        status = "ok"
    else:
        if stock == 0:
            status = "out_of_stock"
        elif stock < min_threshold:
            status = "below_threshold"
        else:
            status = "ok"

    logging.info(f"Checked status of product {product_id} - Status: {status}")

    return {
        "product_id": product_id,
        "stock_quantity": stock,
        "status": status,
        "priority": priority
    }


def list_all_products():
    return load_data()


def purchase_product(product_id: str, purchase: PurchaseRequest):
    inventory = load_data()

    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")

    product = inventory[product_id]

    if purchase.quantity > product["stock_quantity"]:
        raise HTTPException(status_code=400, detail="Not enough stock")

    product["stock_quantity"] -= purchase.quantity
    logging.info(f"Purchased {purchase.quantity} of product {product_id}")

    product = check_and_restock(product)
    inventory[product_id] = product
    save_data(inventory)

    return {"message": "Purchase successful", "updated_stock": product["stock_quantity"]}


def manual_restock_low_priority(product_id: str):
    inventory = load_data()

    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")

    product = inventory[product_id]

    if product["priority"] != "low":
        raise HTTPException(status_code=400, detail="Only low-priority products can be manually restocked.")

    product["stock_quantity"] += product["restock_quantity"]
    logging.info(f"Manually restocked {product['restock_quantity']} of product {product_id}")

    inventory[product_id] = product
    save_data(inventory)

    return {"message": "Manual restock successful", "updated_stock": product["stock_quantity"]}
