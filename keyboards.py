# keyboards.py
# All reply and inline keyboards

from telegram import ReplyKeyboardMarkup

from utils import is_admin


# ===================== MAIN MENU =====================

async def show_main_menu(chat, user_id: str):
    """
    Sends the main menu keyboard.
    Automatically shows admin button if user is admin.
    """

    keyboard = [
        ["🛍 Маҳсулот", "❤️ Дилхоҳҳо"],
        ["🛒 Сабад", "🎁 UC ройгон"],
        ["🤖 AI", "ℹ️ Маълумот"],
        ["🌐 Забон"],
    ]

    # Add admin panel if admin
    if is_admin(int(user_id)):
        keyboard.append(["👑 Панели админ"])

    await chat.send_message(
        "🏠 Менюи асосӣ:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )
