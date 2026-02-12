# handlers/cart.py
# Handles shopping cart logic

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils import get_item


# ===================== ADD TO CART =====================

async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = str(q.from_user.id)

    try:
        item_id = int(q.data.split("_")[1])
    except:
        await q.answer("⚠️ Error adding item.", show_alert=True)
        return

    item = get_item(item_id)

    if not item:
        await q.answer("⚠️ Item not found.", show_alert=True)
        return

    # create cart if not exists
    context.user_data.setdefault("cart", {})
    cart = context.user_data["cart"]

    cart[item_id] = cart.get(item_id, 0) + 1

    await q.answer(f"✅ {item['name']} added to cart!")


# ===================== SHOW CART =====================

async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    cart = context.user_data.get("cart", {})

    if not cart:
        await update.message.reply_text("🛒 Сабад холист.")
        return

    total = 0
    text = "🛒 Сабади шумо:\n"

    for item_id, qty in cart.items():
        item = get_item(int(item_id))
        if not item:
            continue

        subtotal = item["price"] * qty
        total += subtotal

        text += f"- {item['name']} x{qty} = {subtotal} TJS\n"

    text += f"\n💰 Ҳамагӣ: {total} TJS"

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📦 Фармоиш", callback_data="checkout"),
            InlineKeyboardButton("🗑️ Пок", callback_data="clear_cart"),
        ]
    ])

    await update.message.reply_text(text, reply_markup=kb)


# ===================== CLEAR CART =====================

async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    context.user_data["cart"] = {}

    await q.message.edit_text(
        "🗑️ Сабад пок шуд.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Бозгашт", callback_data="catalog_back")]
        ])
    )
