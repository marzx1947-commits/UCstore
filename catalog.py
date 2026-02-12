# handlers/catalog.py
# Handles product catalog, wishlist and item selection

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ITEMS, VOUCHERS
from utils import get_item, item_label


# ===================== CATALOG MENU =====================

async def catalog_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main catalog categories."""

    if update.callback_query:
        q = update.callback_query
        await q.answer()
        message = q.message
    else:
        message = update.message

    kb = [
        [InlineKeyboardButton("🪙 UC", callback_data="catalog_uc")],
        [InlineKeyboardButton("🎫 Vouchers", callback_data="catalog_voucher")],
    ]

    await message.reply_text(
        "🛍 Маҳсулотро интихоб кунед:",
        reply_markup=InlineKeyboardMarkup(kb)
    )


# ===================== UC LIST =====================

async def catalog_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    rows = []
    row = []

    for item_id, item in ITEMS.items():
        row.append(
            InlineKeyboardButton(
                f"{item['name']} — {item['price']} TJS",
                callback_data=f"select_{item_id}"
            )
        )

        if len(row) == 2:
            rows.append(row)
            row = []

    if row:
        rows.append(row)

    rows.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data="catalog_back")])

    await q.message.edit_text(
        "🪙 Рӯйхати UC:",
        reply_markup=InlineKeyboardMarkup(rows)
    )


# ===================== VOUCHERS =====================

async def catalog_voucher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    rows = [
        [InlineKeyboardButton(
            f"{item['name']} — {item['price']} TJS",
            callback_data=f"select_{item_id}"
        )]
        for item_id, item in VOUCHERS.items()
    ]

    rows.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data="catalog_back")])

    await q.message.edit_text(
        "🎫 Рӯйхати Voucher:",
        reply_markup=InlineKeyboardMarkup(rows)
    )


# ===================== SELECT ITEM =====================

async def select_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    try:
        item_id = int(q.data.split("_")[1])
    except:
        await q.answer("⚠️ Error with item ID", show_alert=True)
        return

    item = get_item(item_id)

    if not item:
        await q.answer("⚠️ Item not found.", show_alert=True)
        return

    kb = [
        [
            InlineKeyboardButton("🛒 Ба сабад", callback_data=f"addcart_{item_id}"),
            InlineKeyboardButton("❤️ Ба дилхоҳҳо", callback_data=f"addwish_{item_id}")
        ],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="catalog_back")]
    ]

    await q.message.edit_text(
        f"{item_label(item_id)} • {item['name']} — {item['price']} TJS",
        reply_markup=InlineKeyboardMarkup(kb)
    )
