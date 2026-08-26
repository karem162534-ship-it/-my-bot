import os
import yt_dlp
from pyrogram import Client, filters

# قراءة التوكن من إعدادات رندر
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("خطأ: يرجى إضافة BOT_TOKEN في المنصة السحابية")
    exit(1)

# إعداد البوت
app = Client(
    "x_downloader_bot",
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "مرحباً بك! أنا بوت التحميل الخاص بك.\nأرسل لي رابط الفيديو من أي منصة وسأقوم بتحميله وإرساله لك."
    )

@app.on_message(filters.text & ~filters.command("start"))
async def download_video(client, message):
    url = message.text.strip()

    if not url.startswith("http"):
        await message.reply_text("الرجاء إرسال رابط صحيح يبدأ بـ http أو https")
        return

    status_message = await message.reply_text("...جاري التحميل")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await status_message.edit_text("...جاري رفع الفيديو إليك")
        await message.reply_video("video.mp4")
        await status_message.delete()

    except Exception as e:
        await status_message.edit_text(f"عذراً، حدث خطأ أثناء التحميل:\n{str(e)}")

    finally:
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

if __name__ == "__main__":
    print("...البوت يعمل الآن")
app.run()

