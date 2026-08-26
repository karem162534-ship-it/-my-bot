import os
from pyrogram import Client, filters
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("خطأ: يرجى إضافة BOT_TOKEN في إعدادات المنصة السحابية.")
    exit(1)

app = Client(
    "x_downloader_bot",
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "مرحباً بك! أنا بوت التحميل الخاص بك.\n"
        "أرسل لي رابط مقطع الفيديو (من إكس أو أي منصة أخرى) وسأقوم بتحميله وإرساله لك."
    )

@app.on_message(filters.text & ~filters.command("start"))
async def download_video(client, message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        await message.reply_text("الرجاء إرسال رابط صحيح يبدأ بـ http أو https.")
        return

    status_message = await message.reply_text("جاري جلب الفيديو وتحميله، انتظر قليلاً...")

    output_template = "video.mp4"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template,
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await status_message.edit_text("جاري رفع الفيديو إليك...")
        await message.reply_video(output_template)
        await status_message.delete()

    except Exception as e:
        await status_message.edit_text(f"عذراً، حدث خطأ أثناء التحميل:\n{str(e)}")
    
    finally:
        if os.path.exists(output_template):
            os.remove(output_template)

print("البوت يعمل الآن...")
app.run()
