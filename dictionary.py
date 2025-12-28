import json
import os

DATA_FILE = "data.json"

# ---------- DEFAULT DATA ----------
products = {
    "Milk Tea": {"price": 120, "stock": 50},
    "Burger": {"price": 80, "stock": 30},
    "Fries": {"price": 50, "stock": 40}
}
total_sales = 0

# Users: username -> { "password": "...", "approved": True/False }
users = {}

# ---------- SAVE & LOAD DATA ----------
def save_data():
    data = {
        "products": products,
        "total_sales": total_sales,
        "users": users
    }
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

def load_data():
    global products, total_sales, users
    if not os.path.exists(DATA_FILE):
        save_data()
        return
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
        products = data.get("products", {})
        total_sales = data.get("total_sales", 0)
        users = data.get("users", {})

# ---------- PRODUCT LOGIC ----------
def add_product(name, price, stock):
    products[name] = {"price": price, "stock": stock}
    save_data()

def sell_product(name, quantity):
    global total_sales
    if name not in products:
        return "❌ Product not found"
    if products[name]["stock"] < quantity:
        return "❌ Not enough stock"
    products[name]["stock"] -= quantity
    sale_amount = products[name]["price"] * quantity
    total_sales += sale_amount
    save_data()
    return f"✅ Sale complete! Total: ₱{sale_amount}"

def low_stock(limit=5):
    return [name for name, info in products.items() if info["stock"] <= limit]

# ---------- USER AUTH ----------
def signup(username, password):
    """Sign up a new user (needs admin approval)"""
    if username in users:
        return "❌ Username already exists"
    users[username] = {"password": password, "approved": False}  # Not approved yet
    save_data()
    return "✅ Signup submitted! Wait for approval."

def login(username, password):
    """Login existing user (only approved)"""
    if username not in users:
        return "❌ Username not found"
    if users[username]["password"] != password:
        return "❌ Incorrect password"
    if not users[username]["approved"]:
        return "❌ Your account is not approved yet"
    return "✅ Login successful!"
