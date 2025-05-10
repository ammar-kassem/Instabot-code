import os
import logging
import instaloader
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes

# Logging for debug
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Telegram bot token (توكن بوتك)
TOKEN = "7925984567:AAHd4bbHef7vhGmc_5i6ZnRiT0IPFnSApKc"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any Instagram post/reel link and I'll download the video for you.")

# Handle Instagram links
async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.message.chat_id
    if "instagram.com" not in url:
        await update.message.reply_text("Please send a valid Instagram link.")
        return

    await update.message.reply_text("Downloading... Please wait.")

    loader = instaloader.Instaloader(dirname_pattern='downloads', save_metadata=False)
    try:
        shortcode = url.split("/p/")[1].split("/")[0] if "/p/" in url else url.split("/reel/")[1].split("/")[0]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=chat_id)
        for file in os.listdir(f"{chat_id}"):
            if file.endswith(".mp4"):
                with open(f"{chat_id}/{file}", 'rb') as video:
                    await context.bot.send_video(chat_id=chat_id, video=video)
        # Clean up
        for file in os.listdir(f"{chat_id}"):
            os.remove(f"{chat_id}/{file}")
        os.rmdir(f"{chat_id}")
    except Exception as e:
        await update.message.reply_text(f"Error downloading the video: {e}")

# Main
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))
    print("Bot is running...")
    app.run_polling()
