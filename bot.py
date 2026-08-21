import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# =========================
# Logging
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# =========================
# Bot Token
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")


# =========================
# /start
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    keyboard = [
        [
            InlineKeyboardButton("🎮 Start Mining", callback_data="mining"),
            InlineKeyboardButton("💰 My Balance", callback_data="balance"),
        ],
        [
            InlineKeyboardButton("👥 Referral", callback_data="referral"),
            InlineKeyboardButton("📊 Token Information", callback_data="tokeninfo"),
        ],
        [
            InlineKeyboardButton("📈 Tokenomics", callback_data="tokenomics"),
            InlineKeyboardButton("🚀 Launch", callback_data="launch"),
        ],
        [
            InlineKeyboardButton("⏳ Countdown", callback_data="countdown"),
            InlineKeyboardButton("📢 Announcement", callback_data="announcement"),
        ],
        [
            InlineKeyboardButton("🛠 Support", callback_data="support"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🚀 Welcome to SHARM Mining, {user.first_name}!\n\n"
        "🌍 Welcome to the official SHARM Mining community!\n\n"
        "💎 Mine SHARM Points by tapping, completing daily "
        "tasks, and inviting your friends.\n\n"
        "✨ What you can do:\n"
        "🎮 Start Mining\n"
        "👥 Invite Friends & Earn Referral Rewards\n"
        "💰 Check Balance\n"
        "📊 View Token Information\n"
        "📈 Read Tokenomics\n"
        "🚀 View Launch Information\n"
        "📢 Get Latest Announcements\n"
        "🛠 Contact Support\n\n"
        "👇 Choose an option below:",
        reply_markup=reply_markup,
    )


# =========================
# /help
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📌 SHARM Mining Help\n\n"
        "/start — Open main menu\n"
        "/help — Show help\n"
        "/tokeninfo — Token information\n"
        "/tokenomics — Tokenomics\n"
        "/launch — Launch information\n"
        "/countdown — Launch countdown\n"
        "/referral — Referral information\n"
        "/announcement — Latest announcements\n"
        "/support — Contact support"
    )


# =========================
# Token Information
# =========================

async def tokeninfo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📊 SHARM Token Information\n\n"
        "🪙 Token Name: SHARM\n"
        "🔤 Symbol: SHARM\n"
        "⛓ Blockchain: To be announced\n"
        "💰 Target Price: Market dependent\n"
        "📅 Launch: To be announced\n\n"
        "⚠️ The final token details will be published "
        "before the official launch."
    )


# =========================
# Tokenomics
# =========================

async def tokenomics(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📈 SHARM Tokenomics\n\n"
        "🪙 Total Supply: To be announced\n"
        "🎮 Community Rewards: To be announced\n"
        "👥 Referral Rewards: To be announced\n"
        "💧 Liquidity: To be announced\n"
        "👨‍💻 Development: To be announced\n"
        "📢 Marketing: To be announced\n\n"
        "The final token allocation will be announced "
        "before launch."
    )


# =========================
# Launch
# =========================

async def launch(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🚀 SHARM Token Launch\n\n"
        "The official SHARM token has not been launched yet.\n\n"
        "📅 Launch Date: To be announced\n"
        "⛓ Blockchain: To be announced\n"
        "💰 Initial Price: To be announced\n\n"
        "Follow the official announcements for updates."
    )


# =========================
# Countdown
# =========================

async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "⏳ SHARM Launch Countdown\n\n"
        "🚀 Official launch date has not been announced yet.\n\n"
        "Stay tuned for the official announcement!"
    )


# =========================
# Referral
# =========================

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    bot_username = context.bot.username

    referral_link = (
        f"https://t.me/{bot_username}?start=ref_{user.id}"
    )

    await update.message.reply_text(
        "👥 SHARM Referral Program\n\n"
        "Invite your friends and earn SHARM Points "
        "through the referral program.\n\n"
        f"🔗 Your Referral Link:\n{referral_link}\n\n"
        "📌 Share your link with your friends!"
    )


# =========================
# Announcement
# =========================

async def announcement(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📢 SHARM Announcements\n\n"
        "No official announcements yet.\n\n"
        "Important project updates will be posted here."
    )


# =========================
# Support
# =========================

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🛠 SHARM Support\n\n"
        "Need help with SHARM Mining?\n\n"
        "Please contact the official support team "
        "through the support channel."
    )


# =========================
# Button Handler
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "mining":

        await query.message.reply_text(
            "🎮 Start Mining\n\n"
            "Mining system is currently being prepared.\n\n"
            "🚀 Coming soon!"
        )

    elif query.data == "balance":

        await query.message.reply_text(
            "💰 Your SHARM Balance\n\n"
            "SHARM Points: 0\n\n"
            "Start mining to earn points!"
        )

    elif query.data == "referral":

        user = update.effective_user
        bot_username = context.bot.username

        referral_link = (
            f"https://t.me/{bot_username}?start=ref_{user.id}"
        )

        await query.message.reply_text(
            "👥 Referral Program\n\n"
            f"🔗 Your Referral Link:\n{referral_link}\n\n"
            "Invite friends and earn rewards!"
        )

    elif query.data == "tokeninfo":

        await query.message.reply_text(
            "📊 SHARM Token Information\n\n"
            "🪙 Name: SHARM\n"
            "🔤 Symbol: SHARM\n"
            "⛓ Blockchain: To be announced\n"
            "💰 Price: Market dependent\n"
            "📅 Launch: To be announced"
        )

    elif query.data == "tokenomics":

        await query.message.reply_text(
            "📈 SHARM Tokenomics\n\n"
            "Total Supply: To be announced\n"
            "Community: To be announced\n"
            "Rewards: To be announced\n"
            "Liquidity: To be announced\n"
            "Development: To be announced"
        )

    elif query.data == "launch":

        await query.message.reply_text(
            "🚀 SHARM Launch\n\n"
            "Official launch details will be announced soon."
        )

    elif query.data == "countdown":

        await query.message.reply_text(
            "⏳ Countdown\n\n"
            "Launch date has not been announced yet."
        )

    elif query.data == "announcement":

        await query.message.reply_text(
            "📢 Announcements\n\n"
            "No official announcements yet."
        )

    elif query.data == "support":

        await query.message.reply_text(
            "🛠 Support\n\n"
            "Please contact the official SHARM support team."
        )


# =========================
# Main
# =========================

def main():

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN পাওয়া যায়নি। "
            "Environment Variables-এ BOT_TOKEN সেট করুন।"
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("tokeninfo", tokeninfo)
    )

    application.add_handler(
        CommandHandler("tokenomics", tokenomics)
    )

    application.add_handler(
        CommandHandler("launch", launch)
    )

    application.add_handler(
        CommandHandler("countdown", countdown)
    )

    application.add_handler(
        CommandHandler("referral", referral)
    )

    application.add_handler(
        CommandHandler("announcement", announcement)
    )

    application.add_handler(
        CommandHandler("support", support)
    )

    # Buttons
    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("SHARM Mining Bot is running...")

    application.run_polling()


# =========================
# Run
# =========================

if __name__ == "__main__":
    main()
