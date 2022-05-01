from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_USERNAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.core import user
from driver.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_sticker("CAADBQAD-QQAAhCWOFRERrHKHtIUvgI") 
    await message.reply_text(
        f"""ʜᴇʏ {message.from_user.mention()} 👋🏻\n
💫 ɪᴛs {me_bot.first_name}...I ᴀᴍ ʟᴀᴢʏ Aʙᴏᴜᴛ ᴛʏᴘɪɴɢ sᴏᴍᴇᴛʜɪɴɢ ɴᴇᴡ..ɪᴛᴢ ᴀ ʙᴏᴛ ᴍᴀᴅᴇ ғᴏʀ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ Vᴄ.😈❣️
⚙️ᴄʜᴇᴄᴋ ᴏᴜᴛ ɪᴛs ᴄᴏᴍᴍᴀɴᴅ ʙʏ ʙᴜᴛᴛᴏɴ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("💞**Oᴡɴᴇʀ**", url=f"https://t.me/itz_rupu")
                ],[
                    InlineKeyboardButton("⚙️ ᴄᴏᴍᴍᴀɴᴅs", callback_data="command_list"),
                ],[
                    InlineKeyboardButton("🐬 ɢʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton("💫 ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],[
                    InlineKeyboardButton(" ɢᴇᴛ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴅᴀʀʟɪɴɢ🤭", url=f"https://t.me/{me_bot.username}?startgroup=true")
                ],
            ]
        ),
        disable_web_page_preview=True
    )


@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✨ °ɢʀᴏᴜᴘ°", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "❣️°ᴏᴡɴᴇʀ°", url=f"https://t.me/itz_rupi"
                ),
            ]
        ]
    )

    alive = f"**ʜᴇʟʟᴏ {message.from_user.mention()}, ɪᴍ {me_bot.first_name}**\n\n✨ ʙᴏᴛ ʀᴜɴɴɪɴɢ ᴀғғɪᴄɪᴇɴᴛʟʏ\n❣️ ᴍʏ ᴅᴇᴀʀ ᴏᴡɴᴇʀ: [{ALIVE_NAME}](https://t.me/{OWNER_NAME})\n✨ ʙᴏᴛ ᴠᴇʀ: `v{__version__}`\n🍀 ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀ: `{pyrover}`\n✨ ᴘʏᴛʜᴏɴ ᴠᴇʀ: `{__python_version__}`\n🍀 ᴘʏᴛɢᴄᴀʟʟs ᴠᴇʀ: `{pytover.__version__}`\n✨ ᴜᴘᴛɪᴍᴇ: `{uptime}`\n\n**pᴛʜᴀɴᴋʏᴏᴜ** ❤"

    await message.reply_photo(
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("💫 `🇵 🇴 🇳 🇬 !!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 𝙱𝙾𝚃 𝚂𝚃𝙰𝚃𝚄𝚂:\n"
        f"• **𝚄𝙿𝚃𝙸𝙼𝙴:** `{uptime}`\n"
        f"• **𝚂𝚃𝙰𝚁𝚃 𝚃𝙸𝙼𝙴:** `{START_TIME_ISO}`"
    )


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    ass_uname = (await user.get_me()).username
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if member.id == bot_id:
            return await m.reply(
                " ❤️ ʜᴇʏ ɪᴍ{me_bot.first_name} ʜᴇʀᴇ ғᴏʀ ᴘʟᴀʏ sᴏɴɢs",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("❣️ᴏᴡɴᴇʀ", url=f"https://t.me/itz_rupu"),
                            InlineKeyboardButton("🔥 ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/shivamdemon")
                        ]
                    ]
                )
            )
