import os
import logging
import instaloader
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Bot token
TOKEN = "7925984567:AAHd4bbHef7vhGmc_5i6ZnRiT0IPFnSApKc"

# Instagram credentials
USERNAME = "pixel_value"
PASSWORD = "Asdf@#$123456789"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send an Instagram post or Reels link and I'll download the video for you.")

# Handle Instagram links
async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.message.chat_id

    if "instagram.com" not in url:
        await update.message.reply_text("Please send a valid Instagram link.")
        return

    await update.message.reply_text("Downloading... please wait.")

    loader = instaloader.Instaloader(dirname_pattern=str(chat_id), save_metadata=False)

    # Login to Instagram
    try:
        loader.login(USERNAME, PASSWORD)
    except Exception as e:
        await update.message.reply_text(f"Failed to log in to Instagram: {e}")
        return

    try:
        shortcode = ""
        if "/p/" in url:
            shortcode = url.split("/p/")[1].split("/")[0]
        elif "/reel/" in url:
            shortcode = url.split("/reel/")[1].split("/")[0]
        elif "/tv/" in url:
            shortcode = url.split("/tv/")[1].split("/")[0]
        else:
            await update.message.reply_text("Unsupported link. Only post or Reels links are allowed.")
            return

        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=str(chat_id))

        for file in os.listdir(str(chat_id)):
            if file.endswith(".mp4"):
                with open(f"{chat_id}/{file}", 'rb') as video:
                    await context.bot.send_video(chat_id=chat_id, video=video)

        # Cleanup
        for file in os.listdir(str(chat_id)):
            os.remove(f"{chat_id}/{file}")
        os.rmdir(str(chat_id))

    except Exception as e:
        await update.message.reply_text(f"An error occurred while downloading: {e}")

# Run bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))
    print("Bot is running...")
    app.run_polling()
