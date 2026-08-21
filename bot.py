import os
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(
        f"আসসালামু আলাইকুম {user.first_name}! 👋\n\n"
        "আমাদের বটে আপনাকে স্বাগতম।\n\n"
        "বটটি সফলভাবে চালু হয়েছে। ✅"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 সাহায্য\n\n"
        "/start — বট চালু করুন\n"
        "/help — সাহায্য দেখুন"
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling()


if __name__ == "__main__":
    main()
