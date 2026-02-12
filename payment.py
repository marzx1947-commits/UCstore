# handlers/payment.py
# Handles checkout, payment selection and receipt sending

import random

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import users_data, orders, save_database
from utils import get_item, now_str
from config import VISA_NUMBER, SBER_NUMBER


# ===================== CREATE ORDER =====================

def create_order(user_id: str, total: int, items: dict, game_id: str):
    order_id = random.randint(10000, 99999)

    order = {
        "id": order_id,
        "user_id": user_id,
        "items": items,
        "game_id": game_id,
        "total": total,
        "status": "choose_payment",
        "payment_method": None,
        "proof_file": None,
        "time": now_str(),
    }

    orders.append(order)
    save_database()

    return order


# ===================== CHECKOUT =====================

async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = str(q.from_user.id)
    cart = context.user_data.get("cart", {})

    if not cart:
        await q.message.reply_text("🛒 Сабад холист.")
        return

    context.user_data["awaiting_game_id"] = True
    await q.message.reply_text("🎮 ID-и бозиро ворид кунед:")


# ===================== HANDLE GAME ID =====================

async def handle_game_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_game_id"):
        return

    game_id = update.message.text.strip()

    if not game_id.isdigit() or not (8 <= len(game_id) <= 15):
        await update.message.reply_text("⚠️ ID хатост. Боз ворид кунед:")
        return

    uid = str(update.effective_user.id)
    cart = context.user_data.get("cart", {})

    total = 0
    for item_id, qty in cart.items():
        item = get_item(int(item_id))
        if item:
            total += item["price"] * qty

    order = create_order(uid, total, cart, game_id)
    context.user_data["cart"] = {}
    context.user_data["awaiting_game_id"] = False

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 VISA", callback_data=f"pay_visa_{order['id']}")],
        [InlineKeyboardButton("🏦 SberBank", callback_data=f"pay_sber_{order['id']}")],
    ])

    await update.message.reply_text(
        f"📦 Фармоиш №{order['id']}\n"
        f"🎮 ID: {game_id}\n"
        f"💰 Ҳамагӣ: {total} TJS\n\n"
        "Тарзи пардохтро интихоб кунед:",
        reply_markup=kb
    )


# ===================== FIND ORDER =====================

def find_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order
    return None


# ===================== PAYMENT METHOD =====================

async def choose_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    parts = q.data.split("_")
    method = parts[1]
    order_id = int(parts[2])

    order = find_order(order_id)

    if not order:
        await q.answer("⚠️ Фармоиш ёфт нашуд.", show_alert=True)
        return

    order["status"] = "awaiting_proof"
    order["payment_method"] = "VISA" if method == "visa" else "SberBank"

    card = VISA_NUMBER if method == "visa" else SBER_NUMBER
    context.user_data["awaiting_proof"] = order_id

    await q.message.edit_text(
        f"💳 Пардохт: {order['payment_method']}\n"
        f"📌 Рақами корт: `{card}`\n\n"
        "✅ Пас аз пардохт квитанцияро фиристед.",
        parse_mode="Markdown"
    )


# ===================== RECEIVE RECEIPT =====================

async def receive_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_id = context.user_data.get("awaiting_proof")

    if not order_id:
        return

    order = find_order(order_id)

    if not order:
        return

    file_id = None

    if update.message.photo:
        file_id = update.message.photo[-1].file_id
    elif update.message.document:
        file_id = update.message.document.file_id
    else:
        return

    order["proof_file"] = file_id
    order["status"] = "proof_sent"

    context.user_data.pop("awaiting_proof", None)
    save_database()

    await update.message.reply_text(
        "✅ Квитанция қабул шуд. Админ онро месанҷад."
    )
