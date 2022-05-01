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
import traceback

from pyrogram.types import Message
from pyrogram import Client, filters, __version__ as pyrover
from pytgcalls import (__version__ as pytgver)
from python import (__version__ as pyver)

from program import __version__ as ver

from driver.core import me_bot
from driver.filters import command
from driver.decorators import bot_creator, sudo_users_only
from driver.database.dbchat import get_served_chats
from driver.database.dbusers import get_served_users
from driver.database.dbpunish import get_gbans_count
from driver.database.dbqueue import get_active_chats

from config import BOT_USERNAME as uname


@Client.on_message(command(["broadcast", f"broadcast@{uname}"]) & ~filters.edited)
@bot_creator
async def broadcast_message_nopin(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"✅ 𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃𝙴𝙳 𝙸𝙽  {sent} 𝙶𝚁𝙾𝚄𝙿.")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**𝚄𝚂𝙰𝙶𝙴**:\n\n/broadcast (`message`) or (`reply to message`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"✅ 𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃𝙴𝙳 𝙸𝙽 {sent} 𝙶𝚁𝙾𝚄𝙿𝚂.")


@Client.on_message(command(["broadcast_pin", f"broadcast_pin@{uname}"]) & ~filters.edited)
@bot_creator
async def broadcast_message_pin(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"✅ 𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃𝙴𝙳 𝙸𝙽 {sent} 𝙶𝚁𝙾𝚄𝙿𝚂.\n📌 𝚂𝙴𝙽𝙳 𝚆𝙸𝚃𝙷 {pin} 𝙲𝙷𝙰𝚃 𝙿𝙸𝙽𝚂."
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**s**:\n\n/broadcast_pin (`message`) or (`reply to message`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"✅ 𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃𝙴𝙳 𝙸𝙽  {sent} 𝙶𝚁𝙾𝚄𝙿𝚂.\n📌 𝚂𝙴𝙽𝙳 𝚆𝙸𝚃𝙷 {pin} 𝙲𝙷𝙰𝚃 𝙿𝙸𝙽𝚂."
    )


@Client.on_message(command(["stats", f"stats@{uname}"]) & ~filters.edited)
@sudo_users_only
async def bot_statistic(c: Client, message: Message):
    name = me_bot.first_name
    chat_id = message.chat.id
    msg = await c.send_message(
        chat_id, "❖ 𝙲𝙾𝙻𝙻𝙴𝙲𝚃𝙸𝙽𝙶 𝚂𝚃𝙰𝚃𝚂..."
    )
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    gbans_usertl = await get_gbans_count()
    tgm = f"""
📊 𝙲𝚄𝚁𝚁𝙴𝙽𝚃 𝚂𝚃𝙰𝚃𝚂 𝙸𝚂 [{name}](https://t.me/{uname})`:`

➥ **𝙶𝚁𝙾𝚄𝙿 𝙲𝙷𝙰𝚃𝚂** : `{served_chats}`
➥ **𝚄𝚂𝙴𝚁𝚂** : `{served_users}`
➥ **𝙶𝙱𝙰𝙼𝙼𝙴𝙳 𝚄𝚂𝙴𝚁𝚂** : `{gbans_usertl}`

➛ **𝙿𝚈𝚃𝙷𝙾𝙽 𝚅𝙴𝚁** : `{pyver}`
➛ **𝙿𝙶𝚃𝚈𝙲𝙰𝙻𝙻𝚂 𝚅𝙴𝚁** : `{pytgver.__version__}`
➛ **𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚅𝙴𝚁** : `{pyrover}`

🤖 𝙱𝙾𝚃 𝚅𝙴𝚁𝚂𝙸𝙾𝙽: `{ver}`"""
    await msg.edit(tgm, disable_web_page_preview=True)


@Client.on_message(command(["calls", f"calls@{uname}"]) & ~filters.edited)
@sudo_users_only
async def active_group_calls(c: Client, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"🚫 ᴇʀʀᴏʀ: `{e}`")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await c.get_chat(x)).title
        except BaseException:
            title = "Private Group"
        if (await c.get_chat(x)).username:
            data = (await c.get_chat(x)).username
            text += (
                f"**{j + 1}.** [{title}](https://t.me/{data}) [`{x}`]\n"
            )
        else:
            text += f"**{j + 1}.** {title} [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("❌ 𝙽𝙾 𝙰𝙲𝚃𝙸𝚅𝙴 𝚅𝙾𝙸𝙲𝙴 𝙲𝙷𝙰𝚃𝚂")
    else:
        await message.reply_text(
            f"✏️ **𝚁𝚄𝙽𝙽𝙸𝙽𝙶 𝚅𝙲:**\n\n{text}\n❖ 𝚃𝙷𝙸𝚂 𝙸𝚂 𝙲𝚄𝚁𝚁𝙴𝙽𝚃𝙻𝚈 𝚁𝚄𝙽𝙽𝙸𝙽𝙶 𝚅𝙲𝚂 𝙸𝙽 𝙶𝚁𝙾𝚄𝙿𝚂",
            disable_web_page_preview=True,
        )
