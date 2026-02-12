# database.py
# Handles loading and saving bot data

import os
import json

from config import DB_FILE

# ===================== DATA (RAM) =====================

users_data = {}
orders = []


# ===================== LOAD =====================

def load_database():
    """Load users and orders from JSON file."""
    global users_data, orders

    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                users_data = data.get("users", {})
                orders = data.get("orders", [])
                print(f"✅ Database loaded: {len(users_data)} users.")
        except Exception as e:
            print(f"⚠️ Error reading database: {e}")
    else:
        print("ℹ️ Database file not found. A new one will be created.")


# ===================== SAVE =====================

def save_database():
    """Save users and orders to JSON file."""

    data = {
        "users": users_data,
        "orders": orders
    }

    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"⚠️ Error saving database: {e}")


# ===================== HELPERS =====================

def get_user(user_id: str):
    return users_data.get(str(user_id))


def add_user(user_id: str, user_data: dict):
    users_data[str(user_id)] = user_data
    save_database()


def add_order(order: dict):
    orders.append(order)
    save_database()


def find_order(order_id: int):
    for order in orders:
        if order.get("id") == order_id:
            return order
    return None
