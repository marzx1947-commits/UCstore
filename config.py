# config.py
# ⚠️ Keep this file secure and NEVER commit real tokens to public repos.

import os
from dotenv import load_dotenv

load_dotenv()

# ===================== TOKENS =====================

TOKEN = os.getenv("TOKEN", "PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "PUT_YOUR_GROQ_API_KEY_HERE")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# ===================== ADMINS =====================

ADMIN_IDS = [8508726295]

ADMIN_TELEGRAM = "https://t.me/MARZBON_TJ"
ADMIN_INSTAGRAM = "https://www.instagram.com/marzbon_media?igsh=MTB1bWRoZzIza2JqeA=="

# ===================== CHANNEL =====================

FREE_UC_CHANNEL = "@marzbon_media"

# ===================== PAYMENT =====================

VISA_NUMBER = "4439200020432471"
SBER_NUMBER = "2202208496090011"

# ===================== PRODUCTS =====================

ITEMS = {
    1: {"name": "60 UC", "price": 10},
    2: {"name": "325 UC", "price": 50},
    3: {"name": "660 UC", "price": 100},
    4: {"name": "1800 UC", "price": 250},
    5: {"name": "3850 UC", "price": 500},
    6: {"name": "8100 UC", "price": 1000},
}

VOUCHERS = {
    101: {"name": "Elite Pass", "price": 110},
    102: {"name": "Elite Pass Plus", "price": 260},
    103: {"name": "Bonus Pass", "price": 150},
}

# ===================== DATABASE =====================

DB_FILE = "database.json"
