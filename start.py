# handlers/start.py
# Handles user start, registration flow, language and captcha

import random
import datetime as dt

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import users_data, save_database
from utils import now_str, gen_code
from keyboards import show_main_menu  # make sure you create keyboards.py later


# ===================== LANGUAGE =====================

LANGS = {
    "tj": "🇹🇯 Тоҷикӣ",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}


async def send_language_picker(chat, uid: str):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(v, callback_data=f"lang_{k}")]
        for k, v in LANGS.items()
    ])

    await chat.send_message("🌐 Забонро интихоб кунед:", reply_markup=kb)


# ===================== START =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)

    if uid not in users_data:
        users_data[uid] = {
            "id": user.id,
            "name": user.first_name or "",
            "username": user.username or "",
            "date": now_str(),
            "balance": 0,
            "lang": None,
            "code": gen_code(),
        }

        save_database()

        context.user_data["awaiting_lang"] = True
        await send_language_picker(update.effective_chat, uid)
        return

    # If language not selected yet
    if not users_data[uid].get("lang"):
        context.user_data["awaiting_lang"] = True
        await send_language_picker(update.effective_chat, uid)
        return

    await show_main_menu(update.effective_chat, uid)


# ===================== LANGUAGE CALLBACK =====================

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = str(q.from_user.id)
    lang = q.data.split("_")[1]

    if uid in users_data:
        users_data[uid]["lang"] = lang
        save_database()

    await q.message.edit_text("✅ Registration completed!")
    await show_main_menu(q.message.chat, uid)


# ===================== SIMPLE CAPTCHA =====================

async def start_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    a, b = random.randint(1, 10), random.randint(1, 10)
    context.user_data["captcha_answer"] = a + b

    await update.effective_chat.send_message(
        f"🔐 Санҷиш: {a} + {b} = ?"
    )


async def check_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "captcha_answer" not in context.user_data:
        return

    try:
        answer = int(update.message.text)
    except:
        await update.message.reply_text("❌ Фақат рақам нависед.")
        return

    if answer == context.user_data["captcha_answer"]:
        context.user_data.pop("captcha_answer")

        uid = str(update.effective_user.id)
        await update.message.reply_text("✅ Санҷиш гузашт!")

        await show_main_menu(update.effective_chat, uid)
    else:
        await update.message.reply_text("❌ Нодуруст. Боз кӯшиш кунед.")
