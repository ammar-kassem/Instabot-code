import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes

# إعداد السجل
logging.basicConfig(level=logging.INFO)

# توكن البوت
TOKEN = "7925984567:AAHd4bbHef7vhGmc_5i6ZnRiT0IPFnSApKc"

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل رابط إنستغرام (post أو reel) وسأرسل لك الفيديو.")

# التعامل مع روابط إنستغرام
async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    original_url = update.message.text.strip()
    chat_id = update.message.chat_id

    if "instagram.com" not in original_url:
        await update.message.reply_text("الرجاء إرسال رابط إنستغرام صحيح.")
        return

    await update.message.reply_text("جارٍ التحميل...")

    # تحويل الرابط لـ ddinstagram
    dd_url = original_url.replace("www.", "").replace("instagram.com", "ddinstagram.com")

    try:
        # جلب صفحة ddinstagram
        response = requests.get(dd_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            await update.message.reply_text("فشل الوصول لموقع ddinstagram.")
            return

        # استخراج رابط الفيديو من HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        video_tag = soup.find('video')

        if video_tag and video_tag.get('src'):
            video_url = video_tag['src']
            await context.bot.send_video(chat_id=chat_id, video=video_url)
        else:
            await update.message.reply_text("تعذر العثور على الفيديو.")

    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))
    print("Bot is running...")
    app.run_polling()
