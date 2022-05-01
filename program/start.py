"""
Video + Music Stream Telegram Bot
Copyright (c) 2022-present levina=lab <https://github.com/levina-lab>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/licenses.html>
"""


import asyncio

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

from program import __version__, LOGS
from pytgcalls import (__version__ as pytover)

from driver.filters import command
from driver.core import bot, me_bot, me_user
from driver.database.dbusers import add_served_user
from driver.database.dbchat import add_served_chat, is_served_chat
from driver.database.dblockchat import blacklisted_chats
from driver.database.dbpunish import is_gbanned_user
from driver.decorators import check_blacklist

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest

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
@check_blacklist()
async def start_(c: Client, message: Message):
    user_id = message.from_user.id
    await add_served_user(user_id)
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
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@check_blacklist()
async def alive(c: Client, message: Message):
    chat_id = message.chat.id
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✨ ɢʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "🔥sᴜᴘᴘᴏʀᴛᴇʀ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )
    text = f"**ʜᴇʟᴏ {message.from_user.mention()}, ɪᴍ {me_bot.first_name}**\n\nᴍʏ ᴍᴀsᴛᴇʀ : [ɪᴛs•ʀᴜᴘᴜ](https://t.me/itz_rupu)\n👾 ʙᴏᴛ ᴠᴇʀsɪᴏɴ: `v{__version__}`\n🔥 ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀ: `{pyrover}`\n🐍 ᴘʏᴛʜᴏɴ: `{__python_version__}`\n✨ ᴘʏᴛɢᴄᴀʟʟs ᴠᴇʀ: `{pytover.__version__}`\n🆙 ᴜᴘᴛɪᴍᴇ: `{uptime}`\n\n❤ **ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ**"
    await c.send_photo(
        chat_id,
        photo=f"{ALIVE_IMG}",
        caption=text,
        reply_markup=buttons,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
@check_blacklist()
async def ping_pong(c: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 🇵 🇴 🇳 🇬  !\n" f"⏱ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@check_blacklist()
async def get_uptime(c: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"• ᴜᴘᴛɪᴍᴇ: `{uptime}`\n"
        f"• sᴛᴀʀᴛ ᴛɪᴍᴇ: `{START_TIME_ISO}`"
    )


@Client.on_chat_join_request()
async def approve_join_chat(c: Client, m: ChatJoinRequest):
    if not m.from_user:
        return
    try:
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)
    except FloodWait as e:
        await asyncio.sleep(e.x + 2)
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    chat_id = m.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    for member in m.new_chat_members:
        try:
            if member.id == me_bot.id:
                if chat_id in await blacklisted_chats():
                    await m.reply_text(
                        "❗️ ᴛʜɪs ɪs ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ ᴄᴏɴᴛᴀᴄᴛ @shivamdemon ᴏʀ ᴏᴛʜᴇʀ sᴜᴅᴏ ᴜsᴇʀs."
                    )
                    return await bot.leave_chat(chat_id)
            if member.id == me_bot.id:
                return await m.reply(
                    f"❤️ ʜᴇʏ ɪᴍ {me_bot.first_name} ʜᴇʀᴇ ғᴏʀ ᴘʟᴀʏ sᴏɴɢs",
                    )
            return
        except Exception:
            return


chat_watcher_group = 5

@Client.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message: Message):
    userid = message.from_user.id
    suspect = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.ban_member(userid)
        except ChatAdminRequired:
            LOGS.info(f"ᴄᴀɴᴛ ʀᴇᴍᴏᴠᴇ ɢʙᴀɴɴᴇᴅ ᴜsᴇʀ ғʀᴏᴍ ᴄʜᴀᴛ: {message.chat.id}")
            return
        await message.reply_text(
            f"👮🏼 (> {suspect} <)\n\n**ɢʙᴀɴɴᴇᴅ** ᴜsᴇʀ ғᴏᴜɴᴅ 😏.. ᴛʜɪs ᴜsᴇʀ ɪs ɢʙᴀɴɴᴇᴅ ᴛʜᴀᴛs ᴡʜʏ ɪᴛs ʙʟᴏᴄᴋ ғʀᴏᴍ ᴛʜɪs ᴄʜᴀᴛ!\n\n🚫 **ʀᴇᴀsᴏɴ:** ᴀʙᴜsᴇʀ,sᴘᴀᴍᴍᴇʀ,ᴅɪsʙᴜʀsᴇ ɢɪʀʟs."
        )
