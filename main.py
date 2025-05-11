import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# توكن البوت الخاص بك
TOKEN = "7925984567:AAHd4bbHef7vhGmc_5i6ZnRiT0IPFnSApKc"

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل رابط Instagram Reels أو Post وسأقوم بتحميله لك!")

# معالجة الروابط
async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.message.chat_id
    filename = f"{chat_id}.mp4"

    if "instagram.com" not in url:
        await update.message.reply_text("الرجاء إرسال رابط إنستغرام صالح.")
        return

    await update.message.reply_text("جارٍ تحميل الفيديو... الرجاء الانتظار.")

    try:
        subprocess.run([
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "best",
            "-o", filename,
            url
        ], check=True)

        # إرسال الفيديو
        if os.path.exists(filename):
            with open(filename, 'rb') as video_file:
                await context.bot.send_video(chat_id=chat_id, video=video_file)
            os.remove(filename)
        else:
            await update.message.reply_text("لم يتم العثور على الفيديو بعد التنزيل.")

    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"فشل التحميل: {e}")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))
    print("Bot is running...")
    app.run_polling()
