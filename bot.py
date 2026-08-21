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


async def post_init(application: Application):
    await application.initialize()
    await application.start()


async def post_shutdown(application: Application):
    await application.stop()
    await application.shutdown()


application = (
    Application.builder()
    .token(BOT_TOKEN)
    .updater(None)
    .post_init(post_init)
    .post_shutdown(post_shutdown)
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
