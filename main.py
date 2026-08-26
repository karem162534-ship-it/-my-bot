import os
import asyncio
import yt_dlp
from pyrogram import Client, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("Error: BOT_TOKEN is missing")
    exit(1)

app = Client(
    "x_downloader_bot",
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "Hello! I am your downloader bot.\nSend me a video link from any platform and I will download it for you."
    )

@app.on_message(filters.text & ~filters.command("start"))
async def download_video(client, message):
    url = message.text.strip()

    if not url.startswith("http"):
        await message.reply_text("Please send a valid link starting with http or https")
        return

    status_message = await message.reply_text("Downloading...")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await status_message.edit_text("Uploading video...")
        await message.reply_video("video.mp4")
        await status_message.delete()

    except Exception as e:
        await status_message.edit_text(f"An error occurred:\n{str(e)}")

    finally:
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

if __name__ == "__main__":
    print("Bot is running now...")
    app.run()
