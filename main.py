from fastapi import FastAPI, HTTPException
from models import Product, PurchaseRequest
from services import (
    add_new_product,
    get_inventory_status,
    list_all_products,
    purchase_product,
    manual_restock_low_priority
)

app = FastAPI(title="Mini Inventory Management System")


@app.post("/products")
def create_product(product: Product):
    try:
        return add_new_product(product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/products/{product_id}/status")
def get_status(product_id: str):
    status = get_inventory_status(product_id)
    if not status:
        raise HTTPException(status_code=404, detail="Product not found.")
    return status


@app.get("/products")
def get_all_products():
    return list_all_products()


@app.post("/products/{product_id}/purchase")
def make_purchase(product_id: str, purchase: PurchaseRequest):
    try:
        return purchase_product(product_id, purchase)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/products/{product_id}/restock")
def manual_restock(product_id: str):
    try:
        return manual_restock_low_priority(product_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
