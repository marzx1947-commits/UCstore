# main.py
# Fully configured entry point for the Telegram bot

import logging
import os

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import TOKEN
from database import load_database

# handlers
from handlers.start import start, set_language
from handlers.catalog import catalog_menu, catalog_uc, catalog_voucher, select_item
from handlers.cart import add_to_cart, show_cart, clear_cart
from handlers.payment import checkout, choose_payment, handle_game_id, receive_proof
from handlers.admin import admin_panel, admin_users, admin_orders
from handlers.free_uc import free_uc_menu, daily_uc, my_uc, invite_link


# ===================== LOGGING =====================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# ===================== ERROR HANDLER =====================

async def error_handler(update, context):
    logger.error(f"Update {update} caused error: {context.error}")


# ===================== MAIN =====================

def main():
    if not TOKEN:
        raise ValueError("⚠️ BOT TOKEN not found. Check your .env file!")

    # Load database before starting
    load_database()

    app = ApplicationBuilder().token(TOKEN).build()

    # -------- COMMANDS --------
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))

    # -------- CALLBACKS --------

    # language
    app.add_handler(CallbackQueryHandler(set_language, pattern="^lang_"))

    # catalog
    app.add_handler(CallbackQueryHandler(catalog_menu, pattern="^catalog$"))
    app.add_handler(CallbackQueryHandler(catalog_uc, pattern="^catalog_uc$"))
    app.add_handler(CallbackQueryHandler(catalog_voucher, pattern="^catalog_voucher$"))
    app.add_handler(CallbackQueryHandler(select_item, pattern="^select_"))

    # cart
    app.add_handler(CallbackQueryHandler(add_to_cart, pattern="^addcart_"))
    app.add_handler(CallbackQueryHandler(clear_cart, pattern="^clear_cart$"))
    app.add_handler(MessageHandler(filters.Regex("^🛒"), show_cart))

    # payment
    app.add_handler(CallbackQueryHandler(checkout, pattern="^checkout$"))
    app.add_handler(CallbackQueryHandler(choose_payment, pattern="^pay_"))

    # free uc
    app.add_handler(CallbackQueryHandler(free_uc_menu, pattern="^free_uc$"))
    app.add_handler(CallbackQueryHandler(daily_uc, pattern="^daily_uc$"))
    app.add_handler(CallbackQueryHandler(my_uc, pattern="^my_uc$"))
    app.add_handler(CallbackQueryHandler(invite_link, pattern="^invite_link$"))

    # admin
    app.add_handler(CallbackQueryHandler(admin_users, pattern="^admin_users$"))
    app.add_handler(CallbackQueryHandler(admin_orders, pattern="^admin_orders$"))

    # -------- MESSAGES --------
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_game_id))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, receive_proof))

    # error handler
    app.add_error_handler(error_handler)

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
