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


import wget
import speedtest

from PIL import Image
from config import BOT_USERNAME as bname

from driver.filters import command
from driver.decorators import sudo_users_only
from driver.core import bot as app
from driver.utils import remove_if_exists

from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(command(["speedtest", f"speedtest@{bname}"]) & ~filters.edited)
@sudo_users_only
async def run_speedtest(_, message: Message):
    m = await message.reply_text("⚡️ ʀᴜɴɴɪɴɢ sᴇʀᴠᴇʀ sᴘᴇᴇᴅᴛᴇsᴛ...")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("⚡️ ʀᴜɴɴɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ sᴘᴇᴇᴅ ᴛᴇsᴛ...")
        test.download()
        m = await m.edit("⚡️ ʀᴜɴɴɪɴɢ ᴜᴘʟᴏᴀᴅ sᴘᴇᴇᴅ ᴛᴇsᴛ...")
        test.upload()
        test.results.share()
    except speedtest.ShareResultsConnectFailure:
        pass
    except Exception as e:
        await m.edit(e)
        return
    result = test.results.dict()
    m = await m.edit("⭐ sʜᴀʀɪɴɢ ʙᴏᴛ sᴘᴇᴇᴅ")
    if result["share"]:
        path = wget.download(result["share"])
        try:
            img = Image.open(path)
            c = img.crop((17, 11, 727, 389))
            c.save(path)
        except BaseException:
            pass

    output = f"""💤 **ʀᴇsᴜʟᴛs**
    
<u>**Client:**</u>
**ISP:** {result['client']['isp']}
**Country:** {result['client']['country']}
  
<u>**Server:**</u>
**Name:** {result['server']['name']}
**Country:** {result['server']['country']}, {result['server']['cc']}
**Sponsor:** {result['server']['sponsor']}
**Latency:** {result['server']['latency']}

⚡️ **ᴘɪɴɢ:** {result['ping']}"""
    if result["share"]:
        msg = await app.send_photo(
            chat_id=message.chat.id, photo=path, caption=output
        )
        remove_if_exists(path)
    else:
        msg = await app.send_message(
            chat_id=message.chat.id, text=output
        )
    await m.delete()
