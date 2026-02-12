# handlers/free_uc.py
# Handles free UC features like daily bonus and invite link

import datetime as dt
import random

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import users_data, save_database
from config import FREE_UC_CHANNEL


# ===================== FREE UC MENU =====================

async def free_uc_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        q = update.callback_query
        await q.answer()
        chat = q.message.chat
    else:
        chat = update.effective_chat

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 UC рӯзона", callback_data="daily_uc")],
        [InlineKeyboardButton("📊 UC-и ман", callback_data="my_uc")],
        [InlineKeyboardButton("🔗 Даъвати дӯстон", callback_data="invite_link")],
    ])

    await chat.send_message(
        "🎁 Менюи UC ройгон:",
        reply_markup=kb
    )


# ===================== DAILY UC =====================

async def daily_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = str(q.from_user.id)
    user = users_data.get(uid)

    if not user:
        await q.answer("⚠️ Аввал /start кунед.", show_alert=True)
        return

    now = dt.datetime.now()
    last = user.get("last_daily_uc")

    if last:
        last_dt = dt.datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
        diff = now - last_dt

        if diff.total_seconds() < 86400:
            hours = int((86400 - diff.total_seconds()) // 3600)
            minutes = int(((86400 - diff.total_seconds()) % 3600) // 60)

            await q.message.reply_text(
                f"⏳ Шумо имрӯз бонус гирифтед.
Баъд аз {hours} соат {minutes} дақиқа биёед."
            )
            return

    bonus = random.randint(1, 5)

    user["balance"] = user.get("balance", 0) + bonus
    user["last_daily_uc"] = now.strftime("%Y-%m-%d %H:%M:%S")

    save_database()

    await q.message.reply_text(
        f"🎉 Шумо {bonus} UC гирифтед!"
    )


# ===================== MY UC =====================

async def my_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = str(q.from_user.id)
    user = users_data.get(uid)

    if not user:
        return

    balance = user.get("balance", 0)

    await q.message.reply_text(
        f"📊 Тавозуни шумо: {balance} UC"
    )


# ===================== INVITE LINK =====================

async def invite_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = str(q.from_user.id)

    bot_username = (await context.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start=invite_{uid}"

    await q.message.reply_text(
        f"🔗 Истиноди даъват:\n{link}\n\n"
        "Барои ҳар дӯсте, ки ҳамроҳ мешавад — бонус мегиред!"
    )
