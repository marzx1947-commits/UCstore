# utils.py
# Helper functions used across the bot

import random
import string
import datetime as dt

from config import ADMIN_IDS, ITEMS, VOUCHERS


# ===================== ADMIN =====================

def is_admin(user_id: int) -> bool:
    """Check if a user is admin."""
    return user_id in ADMIN_IDS


# ===================== TIME =====================

def now_str() -> str:
    """Return current datetime as string."""
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ===================== CODE GENERATOR =====================

def gen_code(length: int = 6) -> str:
    """Generate random uppercase code."""
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


# ===================== ITEMS =====================

def get_item(item_id: int):
    """Return item from ITEMS or VOUCHERS."""
    return ITEMS.get(item_id) or VOUCHERS.get(item_id)


def item_label(item_id: int) -> str:
    """Return label depending on item type."""
    if item_id in ITEMS:
        return "🪙 UC"
    elif item_id in VOUCHERS:
        return "🎫 Voucher"
    return "Unknown"
