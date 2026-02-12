# main.py
# Entry point for the Telegram bot

import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import TOKEN
from database import load_database
from handlers.start import start
from handlers.catalog import catalog_menu
from handlers.cart import show_cart
from handlers.payment import handle_game_id, receive_proof
from handlers.admin import admin_panel
from handlers.free_uc import free_uc_menu


# ===================== LOGGING =====================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# ===================== MAIN =====================

def main():
    # Load database before bot starts
    load_database()

    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Callback buttons
    app.add_handler(CallbackQueryHandler(catalog_menu, pattern="catalog"))
    app.add_handler(CallbackQueryHandler(free_uc_menu, pattern="free_uc"))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_game_id))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, receive_proof))

    # Admin
    app.add_handler(CommandHandler("admin", admin_panel))

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
