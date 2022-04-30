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


from config import BOT_USERNAME

from pyrogram import Client
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from driver.decorators import check_blacklist
from driver.queues import QUEUE, get_queue
from driver.filters import command, other_filters


keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🚫 ᴄʟᴏsᴇ", callback_data="set_close")]]
)


@Client.on_message(command(["playlist", f"playlist@{BOT_USERNAME}", "queue", f"queue@{BOT_USERNAME}"]) & other_filters)
@check_blacklist()
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.reply(
                f"🎵**ᴄᴜʀʀᴇɴᴛʟʏ sᴛʀᴇᴀᴍɪɴɢ**`:`\n\n"
                f"➣ [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                reply_markup=keyboard, disable_web_page_preview=True)
        else:
            QUE = f"🎧 **ᴄᴜʀʀᴇɴᴛʟʏ sᴛʀᴇᴀᴍɪɴɢ**`:`\n\n" \
                  f"➣ [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n" \
                  f"**🏷️ǫᴜᴇᴜᴇᴅ sᴏɴɢ ʟɪsᴛ**`:`\n"
            l = len(chat_queue)
            for x in range(1, l):
                han = chat_queue[x][0]
                hok = chat_queue[x][2]
                hap = chat_queue[x][3]
                QUE = QUE + "\n" + f"`#{x}` - [{han}]({hok}) | `{hap}`"
            await m.reply(QUE, reply_markup=keyboard, disable_web_page_preview=True)
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.**")
