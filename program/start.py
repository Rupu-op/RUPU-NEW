import asyncio
from time import time
from datetime import datetime
from config import BOT_USERNAME
from config import GROUP_SUPPORT,ALIVE_IMG,START_PIC
from driver.filters import command
from driver.command import commandpro
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from driver.core import bot as Client

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)
    
   

@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{START_PIC}",
        caption=f"""✌️ɪᴍ ʟᴀᴢʏ ᴀʙᴏᴜᴛ ᴛʏᴘɪɴɢ ᴀɴʏᴛʜɪɴɢ ɪᴛs ᴀ ᴍᴜsɪᴄ ʙᴏᴛ ʜᴀᴠᴇ ᴍᴀɴʏ ғᴇᴀᴛᴜʀᴇs.

💫 **ᴍᴀɪɴ ғᴇᴀᴛᴜʀᴇs**
~  ᴀᴜᴅɪᴏ /ᴠɪᴅᴇᴏ ᴘʟᴀʏ
~ YouTube/Local/Live/m3u8 sᴜᴘᴘᴏʀᴛs
~ ᴅᴏᴡɴʟᴏᴀᴅ ᴀᴜᴅɪᴏ ᴠɪᴅᴇᴏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ

ᴄʀᴇᴀᴛᴇᴅ ʙʏ[s•4•sʜɪᴠ](t.me/shivamdemon)...
""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ ɢᴇᴛ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴘ ʙᴀʙʏ🤭", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❣️ ᴏᴡɴᴇʀ", url=f"https://t.me/itz_rupu"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🐬 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", url=f"https://telegra.ph/𝐒𝟒𝐒𝐇𝐈𝐕-𝐗𝐃ད-ℑ-𝐀𝔪-ᗪye𝐌𝕠ℕ-ཌ-05-01-2"
                    ),
                    InlineKeyboardButton(
                        "💫 ɢʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"
                    )
                ]
                
           ]
        ),
    )
    
    
@Client.on_message(commandpro(["/start", "/stats"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{ALIVE_IMG}",
        caption=f"""ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🔥♥️""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "°ᴏᴡɴᴇʀ° 💞", url=f"https://t.me/itz_rupu"),
                    InlineKeyboardButton(
                        "°sᴜᴘᴘᴏʀᴛᴇʀ° ✨", url=f"https://t.me/shivamdemon")
                ]
            ]
        ),
    )

