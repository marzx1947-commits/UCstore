# handlers/admin.py
# Admin panel and basic admin tools

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils import is_admin
from database import users_data, orders


# ===================== ADMIN PANEL =====================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("🚫 Танҳо барои админ!")
        return

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Users", callback_data="admin_users")],
        [InlineKeyboardButton("📦 Orders", callback_data="admin_orders")],
    ])

    await update.message.reply_text(
        "👑 Панели админ:",
        reply_markup=kb
    )


# ===================== USERS LIST =====================

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if not is_admin(q.from_user.id):
        return

    if not users_data:
        await q.message.reply_text("Ҳоло корбарон нестанд.")
        return

    text = "👤 Users:\n\n"

    # show first 20 users
    for uid, user in list(users_data.items())[:20]:
        text += f"{user.get('name','NoName')} | ID: {uid}\n"

    await q.message.reply_text(text)


# ===================== ORDERS LIST =====================

async def admin_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if not is_admin(q.from_user.id):
        return

    if not orders:
        await q.message.reply_text("Ҳоло фармоишҳо нестанд.")
        return

    text = "📦 Last orders:\n\n"

    for order in orders[-10:]:
        text += (
            f"ID: {order['id']} | "
            f"User: {order['user_id']} | "
            f"💰 {order['total']} TJS | "
            f"Status: {order['status']}\n"
        )

    await q.message.reply_text(text)
