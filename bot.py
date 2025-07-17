from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 22983083
API_HASH = "4e763b2e2523db147ab4e4ed10b244ad"
BOT_TOKEN = "7453797940:AAF38wylyaC306oNSr-pdJ4_Rv4wlWbzfzo"
OWNER_ID = 7774213647
CHANNEL_USERNAME = "cinema_zone_channel"

app = Client("uploader-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# چک عضویت در کانال
async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# پیام خوش‌آمد
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "سلام دوست عزیز 🌟\nبرای استفاده از ربات، ابتدا عضو کانال ما شو.\nسپس منتظر فایل‌های جدید باش!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}")]
        ])
    )

# دریافت و آپلود فایل توسط مدیر
@app.on_message(filters.user(OWNER_ID) & (filters.video | filters.document))
async def upload_from_admin(client, message):
    file = await message.copy(chat_id=message.chat.id)
    await message.reply(
        "✅ فایل آپلود شد و آماده دانلود است.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 دانلود فایل", url=f"https://t.me/{file.chat.username or CHANNEL_USERNAME}/{file.message_id}")]
        ])
    )

# جلوگیری از آپلود کاربران عادی
@app.on_message((filters.video | filters.document) & ~filters.user(OWNER_ID))
async def block_users(client, message):
    await message.reply("⛔ فقط مدیر می‌تونه فایل آپلود کنه.")

app.run()
