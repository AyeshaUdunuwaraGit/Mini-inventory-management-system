# 🧠 Mini Inventory Management System (FastAPI)

This is a smart and minimal Inventory Management System built with **FastAPI** and **pure Python** (no database). It handles product management, inventory tracking, automatic and manual restocking based on priority, and status classification.

---

## 📦 Features

- ✅ Add New Products
- 📦 Track Inventory Status
- 🛒 Purchase Products
- ♻️ Auto & Manual Restocking
- 🗃 View All Products
- 🧠 Smart Business Logic (Priority-based restocking)
- 📄 Persistent Storage (JSON)
- 🪵 Operation Logs

---

## 🧰 Tech Stack

- Python 3.9+
- FastAPI
- Uvicorn (ASGI server)

---

## ▶️ How to Run 🏃‍♀️

### 1. Activate your virtual environment

```
 python -m venv venv
venv\Scripts\activate   # On Windows
# Or:
source venv/bin/activate  # On macOS/Linux

```

### 2. 📦 Install dependencies (preferably in a virtual environment):

```bash

pip install fastapi uvicorn

```
### 3. 🏃‍♀️ Run the FastAPI server:

``` 
 uvicorn main:app --reload

```
### 4. 🌐 Open your browser and navigate to:

Swagger UI (interactive API): http://127.0.0.1:8000/docs
Redoc (alternate docs): http://127.0.0.1:8000/redoc

## 📂 Project Structure

mini_inventory_management_system/
│
├── main.py # FastAPI app and endpoints
├── models.py # Pydantic models
├── services.py # Business logic and operations
├── utils.py # Utility functions: logging, restock, storage
├── storage.json # Persistent product data
├── activity.log # Log file tracking operations
└── test_main.py # Unit tests using TestClient

---

## ⚙️ Business Logic

### 📌 Product Creation

- If `priority = "high"` and `min_threshold < 10` → force `min_threshold = 10`
- If `priority = "low"` and `min_threshold < 10` → accept as-is
- Category is auto-assigned based on `restock_quantity`:
  - `"high_volume"` if > 50
  - `"low_volume"` otherwise

---

### 🔁 Restocking Rules

- If `stock_quantity < min_threshold`:
  - `"high"` priority → Auto-restock immediately
  - `"low"` priority → Must be manually restocked via `/restock` endpoint

---

### 📊 Inventory Status

| Status           | Condition                              |
|------------------|-----------------------------------------|
| `ok`             | `stock_quantity >= min_threshold`       |
| `below_threshold`| `stock_quantity < min_threshold`        |
| `out_of_stock`   | `stock_quantity == 0`                   |

For `priority = "high"` products, system tries to avoid showing `"below_threshold"` or `"out_of_stock"` by restocking early.

---

## 🚀 API Endpoints

| Method | Endpoint                             | Description                         |
|--------|--------------------------------------|-------------------------------------|
| POST   | `/products`                          | Add new product                     |
| GET    | `/products`                          | List all products                   |
| GET    | `/products/{product_id}/status`      | Get product status (with logic)     |
| POST   | `/products/{product_id}/purchase`    | Purchase product                    |
| POST   | `/products/{product_id}/restock`     | **Manual restock** for low priority |

---

## 🔃 Sample Payloads

### ➕ Create Product

```json
POST /products

{
  "product_id": "P001",
  "name": "Smart Widget",
  "stock_quantity": 5,
  "min_threshold": 8,
  "restock_quantity": 60,
  "priority": "high"
}

```

### 🛒 Purchase Product

```json
POST /products/P1001/purchase

{
  "quantity": 5
}
```
---

## 📦 Storage & Logs

### 🔸 storage.json

Stores all product records in JSON format. Updated automatically on any change.

```json
[
  {
    "product_id": "P1001",
    "name": "Laptop",
    "stock_quantity": 15,
    "min_threshold": 5,
    "restock_quantity": 50,
    "priority": "high"
  }
]

```

### 🔸 activity.log

Log file containing all key operations with timestamps:

```vbnet

2025-07-29 21:45:13 - Added new product: Laptop
2025-07-29 21:46:00 - Purchased 5 of Laptop
2025-07-29 21:46:01 - Auto-restocked: 50 added to Laptop

```
---

## Run the Project


## 🧪 Testing

### 🛠 Requirements

Install the following packages before testing:

```bash

pip install pytest httpx

```

### ✅ Run Tests

```bash

pytest test_main.py

```

---

## ✅ What’s Covered?

| Test Description                    | File          |
|-----------------------------------|---------------|
| Add products (high & low priority) | test_main.py  |
| Inventory status check             | test_main.py  |
| Product purchasing & auto-restock  | test_main.py  |
| Manual restocking endpoint         | test_main.py  |
| Edge case & validation             | test_main.py  |


## 📬 API Endpoints Summary

| Method | Endpoint                          | Description                |
| ------ | --------------------------------  | -------------------------- |
| POST   | `/products`                       | Add new product            |
| GET    | `/products/{product_id}/status`   | Get inventory status       |
| GET    | `/products`                       | List all products          |
| POST   | `/products/{product_id}/purchase` | Purchase a product         |
| POST   | `/products/{product_id}/restock`  | Manually restock a product |


## 📌 Notes

No external DB required — uses JSON for storage.
Works offline and suitable for demos or assignments.
Cleanly separated into models, services, and utils.

## 📄 License

 **Note:** This project is intended for educational and demonstration purposes only. It is not designed for production use.



