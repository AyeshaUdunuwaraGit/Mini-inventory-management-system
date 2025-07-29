from pydantic import BaseModel

class Product(BaseModel):
    product_id: str
    name: str
    stock_quantity: int
    min_threshold: int
    restock_quantity: int
    priority: str  # "high" or "low"


class PurchaseRequest(BaseModel):
     quantity: int
