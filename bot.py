import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

application = (
    Application.builder()
    .token(BOT_TOKEN)
    .updater(None)
    .build()
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(
        f"👋 আসসালামু আলাইকুম {user.first_name}!\n\n"
        "SHARM TAP-এ আপনাকে স্বাগতম। 🎉\n\n"
        "আপনার অ্যাকাউন্ট সফলভাবে সংযুক্ত হয়েছে।"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 কমান্ডসমূহ\n\n"
        "/start - বট চালু করুন\n"
        "/help - সাহায্য দেখুন"
    )


application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
