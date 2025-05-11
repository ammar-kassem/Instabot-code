import logging
import os
import subprocess
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes

# إعداد السجل
logging.basicConfig(level=logging.INFO)

# توكن البوت
TOKEN = "7925984567:AAHd4bbHef7vhGmc_5i6ZnRiT0IPFnSApKc"

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل رابط إنستغرام (reel أو post) وسأرسله لك كفيديو.")

# معالجة الرابط
async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.message.chat_id

    if "instagram.com" not in url:
        await update.message.reply_text("رابط غير صالح.")
        return

    await update.message.reply_text("جاري التحميل...")

    try:
        filename = f"{chat_id}.mp4"
        subprocess.run(["yt-dlp", "-f", "best", "-o", filename, url], check=True)

        with open(filename, 'rb') as f:
            await context.bot.send_video(chat_id=chat_id, video=f)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"فشل التحميل: {e}")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))
    print("Bot is running...")
    app.run_polling()
