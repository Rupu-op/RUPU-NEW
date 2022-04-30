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


import re
import asyncio

from asyncio.exceptions import TimeoutError
from config import BOT_USERNAME, IMG_1, IMG_2, IMG_5

from program import LOGS
from program.utils.inline import stream_markup
from driver.design.thumbnail import thumb
from driver.design.chatname import CHAT_TITLE
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.core import calls, user, me_user
from driver.utils import remove_if_exists, from_tg_get_msg
from driver.decorators import require_admin, check_blacklist
from driver.database.dbqueue import add_active_chat, remove_active_chat, music_on

from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, Message

from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from pytgcalls.exceptions import (
    NoAudioSourceFound,
    NoVideoSourceFound,
    NoActiveGroupCall,
    GroupCallNotFound,
)
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = data["thumbnails"][0]["url"]
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0

async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "--geo-bypass",
        "-g",
        "-f",
        "[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()

def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


async def play_tg_file(c: Client, m: Message, replied: Message = None, link: str = None):
    chat_id = m.chat.id
    user_id = m.from_user.id
    if link:
        try:
            replied = await from_tg_get_msg(link)
        except Exception as e:
            LOGS.info(f"[ERROR]: {e}")
            return await m.reply_text(f"🚫 ᴇʀʀᴏʀ:\n\n» {e}")
    if not replied:
        return await m.reply(
            "» ɢɪᴠᴇ sᴏᴍᴇᴛʜɪɴɢ ᴛᴏ ᴘʟᴀʏ✌️"
        )
    if replied.video or replied.document:
        if not link:
            loser = await replied.reply("📥  ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...")
        else:
            loser = await m.reply("📥 sᴀᴠɪɴɢ...")
        dl = await replied.download()
        link = replied.link
        songname = "video"
        duration = "00:00"
        Q = 720
        pq = m.text.split(None, 1)
        if ("t.me" not in m.text) and len(pq) > 1:
            pq = pq[1]
            if pq == "720" or pq == "480" or pq == "360":
                Q = int(pq)
            else:
                await loser.edit(
                    "sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ɪɴ 720ᴘ ǫᴜᴀʟɪᴛʏ"
                )
        try:
            if replied.video:
                songname = replied.video.file_name[:80]
                duration = convert_seconds(replied.video.duration)
            elif replied.document:
                songname = replied.document.file_name[:80]
        except BaseException:
            songname = "video"

        if chat_id in QUEUE:
            await loser.edit("🔄 ᴀᴅᴅ ᴛᴏ ǫᴜᴇᴜᴇ...")
            gcname = m.chat.title
            ctitle = await CHAT_TITLE(gcname)
            title = songname
            userid = m.from_user.id
            thumbnail = f"{IMG_5}"
            image = await thumb(thumbnail, title, userid, ctitle)
            pos = add_to_queue(chat_id, songname, dl, link, "video", Q)
            await loser.delete()
            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
            buttons = stream_markup(user_id)
            await m.reply_photo(
                photo=image,
                reply_markup=InlineKeyboardMarkup(buttons),
                caption=f"💡 **sᴏɴɢ ᴀᴅᴅᴇᴅ ᴀᴛ »** `{pos}`\n\n"
                        f"🏷️ **ɴᴀᴍᴇ:** [{songname}]({link}) | `video`\n"
                        f"⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n"
                        f"🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
            )
            remove_if_exists(image)
        else:
            try:
                await loser.edit("✨ ᴡᴀɪᴛɪɴɢ ᴛᴏ ᴘʟᴀʏ...")
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                title = songname
                userid = m.from_user.id
                thumbnail = f"{IMG_5}"
                image = await thumb(thumbnail, title, userid, ctitle)
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await music_on(chat_id)
                await add_active_chat(chat_id)
                await calls.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=image,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"🏷️**ɴᴀᴍᴇ:** [{songname}]({link}) | `video`\n"
                            f"⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n"
                            f"🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
                )
                remove_if_exists(image)
            except (NoActiveGroupCall, GroupCallNotFound):
                await loser.delete()
                await remove_active_chat(chat_id)
                await m.reply_text("ᴛᴜʀɴ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ғɪʀsᴛ❗")
            except Exception as e:
                LOGS.info(f"[ERROR]: {e}")
    else:
        await m.reply_text(
            "» **ɢɪᴠᴇ ᴠɪᴅᴇᴏ ғɪʟᴇ ᴏʀ ᴛᴇxᴛ ᴛᴏ ᴘʟᴀʏ✌️**"
        )


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
@check_blacklist()
@require_admin(permissions=["can_manage_voice_chats", "can_delete_messages", "can_invite_users"], self=True)
async def video_stream(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text(
            "😶ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ\nᴛʀʏ ᴡɪᴛʜ ʏᴏᴜʀ ʀᴇᴀʟ ᴀᴄᴄᴏᴜɴᴛ"
        )
    try:
        ubot = me_user.id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "banned":
            try:
                await m.reply_text("❌ ᴀssɪsᴛᴀɴᴛ ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ...ᴜɴʙᴀɴ ɪᴛ ғɪʀsᴛ ᴛᴏ ᴊᴏɪɴ")
                await remove_active_chat(chat_id)
            except BaseException:
                pass
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
    except UserNotParticipant:
        try:
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            LOGS.info(f"[ERROR]: {e}")
            return await m.reply_text(
                f"❌ **ᴀssɪsᴛᴀɴᴛ ғᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ ...ᴀsᴋ @shivamdemon ғᴏʀ ʜᴇʟᴘ."
            )
    if replied:
        if replied.video or replied.document:
            await play_tg_file(c, m, replied)
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» **ɢɪᴠᴇ ᴠɪᴅᴇᴏ ғɪʟᴇ ᴏʀ ᴛᴇxᴛ ᴛᴏ ᴘʟᴀʏ✌️**"
                )
            else:
                Q = 720
                loser = await c.send_message(chat_id, "🔍 **ᴘʀᴏᴄᴇssɪɴɢ...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **ғᴏᴜɴᴅ ɴᴏᴛʜɪɴɢ ...sᴘᴇʟʟ ᴄᴏʀʀᴇᴄᴛʟʏ**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    ctitle = await CHAT_TITLE(gcname)
                    image = await thumb(thumbnail, title, userid, ctitle)
                    data, ytlink = await ytdl(url)
                    if data == 0:
                        await loser.edit(f"❌ ʏᴛ-ᴅʟ ɪssᴜᴇ ᴀsᴋ sᴜᴘᴘᴏʀᴛᴇʀ")
                    else:
                        if chat_id in QUEUE:
                            await loser.edit("🔄 ᴀᴅᴅ ᴛᴏ ǫᴜᴇᴜᴇ...")
                            pos = add_to_queue(chat_id, songname, ytlink, url, "video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"👉 **sᴏɴɢ ᴀᴅᴅᴇᴅ ᴀᴛ »** `{pos}`\n\n🏷️ **ɴᴀᴍᴇ:** [{songname}]({url}) | `video`\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
                            )
                            remove_if_exists(image)
                        else:
                            try:
                                await loser.edit("✨ ᴡᴀɪᴛɪɴɢ ᴛᴏ ᴘʟᴀʏ...")
                                await music_on(chat_id)
                                await add_active_chat(chat_id)
                                await calls.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                buttons = stream_markup(user_id)
                                await m.reply_photo(
                                    photo=image,
                                    reply_markup=InlineKeyboardMarkup(buttons),
                                    caption=f"🏷️**ɴᴀᴍᴇ:** [{songname}]({url}) | `video`\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
                                )
                                remove_if_exists(image)
                            except (NoActiveGroupCall, GroupCallNotFound):
                                await loser.delete()
                                await remove_active_chat(chat_id)
                                await m.reply_text("ᴛᴜʀɴ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ғɪʀsᴛ❗")
                            except NoVideoSourceFound:
                                await loser.delete()
                                await remove_active_chat(chat_id)
                                await m.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ʟᴏᴀᴅ ʏᴏᴜʀ sᴏɴɢ sᴏʀʀʏ🥺")
                            except NoAudioSourceFound:
                                await loser.delete()
                                await remove_active_chat(chat_id)
                                await m.reply_text("sᴏᴍᴇᴛʜɪɴɢ ɪs ᴍɪssɪɴɢ ɪɴ ʏᴏᴜʀ sᴏɴɢ⭕")

    else:
        if len(m.command) < 2:
            await m.reply_text("» **ɢɪᴠᴇ ᴠɪᴅᴇᴏ ғɪʟᴇ ᴏʀ ᴛᴇxᴛ ᴛᴏ ᴘʟᴀʏ✌️**")
        elif "t.me" in m.command[1]:
            for i in m.command[1:]:
                if "t.me" in i:
                    await play_tg_file(c, m, link=i)
                continue
        else:
            Q = 720
            loser = await c.send_message(chat_id, "🔍 **ᴘʀᴏᴄᴇssɪɴɢ...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **ғᴏᴜɴᴅ ɴᴏᴛʜɪɴɢ...sᴘᴇʟʟ ᴄᴏʀʀᴇᴄᴛʟʏ**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await thumb(thumbnail, title, userid, ctitle)
                data, ytlink = await ytdl(url)
                if data == 0:
                    await loser.edit(f"❌ ʏᴛ-ᴅʟ ɪssᴜᴇ ᴀsᴋ ᴛᴏ sᴜᴘᴘᴏʀᴛᴇʀ")
                else:
                    if chat_id in QUEUE:
                        await loser.edit("🔄 ᴀᴅᴅ ᴛᴏ ǫᴜᴇᴜᴇ...")
                        pos = add_to_queue(chat_id, songname, ytlink, url, "video", Q)
                        await loser.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        buttons = stream_markup(user_id)
                        await m.reply_photo(
                            photo=image,
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"👉 **sᴏɴɢ ᴀᴅᴅᴇᴅ ᴀᴛ »** `{pos}`\n\n🏷️**ɴᴀᴍᴇ:** [{songname}]({url}) | `video`\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
                        )
                        remove_if_exists(image)
                    else:
                        try:
                            await loser.edit("✨ ᴡᴀɪᴛɪɴɢ ᴛᴏ ᴘʟᴀʏ...")
                            await music_on(chat_id)
                            await add_active_chat(chat_id)
                            await calls.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"🏷️ **ɴᴀᴍᴇ:** [{songname}]({url}) | `video`\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
                            )
                            remove_if_exists(image)
                        except (NoActiveGroupCall, GroupCallNotFound):
                            await loser.delete()
                            await remove_active_chat(chat_id)
                            await m.reply_text("ᴛᴜʀɴ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ғɪʀsᴛ❗")
                        except NoVideoSourceFound:
                            await loser.delete()
                            await remove_active_chat(chat_id)
                            await m.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ʟᴏᴀᴅ ʏᴏᴜʀ sᴏɴɢ sᴏʀʀʏ🥺")
                        except NoAudioSourceFound:
                            await loser.delete()
                            await remove_active_chat(chat_id)
                            await m.reply_text("sᴏᴍᴇᴛʜɪɴɢ ɪs ᴍɪssɪɴɢ ɪɴ ʏᴏᴜʀ sᴏɴɢ⭕")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
@check_blacklist()
@require_admin(permissions=["can_manage_voice_chats", "can_delete_messages", "can_invite_users"], self=True)
async def live_video_stream(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text(
            "😶ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ\nᴛʀʏ ᴡɪᴛʜ ʏᴏᴜʀ ʀᴇᴀʟ ᴀᴄᴄᴏᴜɴᴛ."
        )
    try:
        ubot = me_user.id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "banned":
            try:
                await m.reply_text("❌ ᴀssɪsᴛᴀɴᴛ ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ...ᴜɴʙᴀɴ ɪᴛ ғɪʀsᴛ ᴛᴏ ᴊᴏɪɴ")
                await remove_active_chat(chat_id)
            except BaseException:
                pass
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
    except UserNotParticipant:
        try:
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            LOGS.info(f"[ERROR]: {e}")
            return await m.reply_text(
                f"❌ **ᴀssɪsᴛᴀɴᴛ ғᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ ...ᴀsᴋ @shivamdemon ғᴏʀ ʜᴇʟᴘ."
            )
    if len(m.command) < 2:
        await m.reply("» **ɢɪᴠᴇ ᴠɪᴅᴇᴏ ғɪʟᴇ ᴏʀ ᴛᴇxᴛ ᴛᴏ ᴘʟᴀʏ✌️**")
    else:
        if len(m.command) == 2:
            Q = 720
            url = m.text.split(None, 1)[1]
            search = ytsearch(url)
            loser = await c.send_message(chat_id, "🔍 **ᴘʀᴏᴄᴇssɪɴɢ...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            url = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            search = ytsearch(op)
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply_text(
                    "» sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ɪɴ 720ᴘ ǫᴜᴀʟɪᴛʏ"
                )
            loser = await c.send_message(chat_id, "🔍 **ᴘʀᴏᴄᴇssɪɴɢ...**")
        else:
            pass

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, url)
        if match:
            coda, livelink = await ytdl(url)
        else:
            livelink = url
            coda = 1
        if coda == 0:
            await loser.edit(f"❌ ʏᴛ-ᴅʟ ɪssᴜᴇ ᴀsᴋ ᴛᴏ sᴜᴘᴘᴏʀᴛᴇʀ.")

        else:
            if "m3u8" in url:
                if chat_id in QUEUE:
                    await loser.edit("🔄 ᴀᴅᴅ ᴛᴏ ǫᴜᴇᴜᴇ...")
                    pos = add_to_queue(chat_id, "m3u8 video", livelink, url, "video", Q)
                    await loser.delete()
                    requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    buttons = stream_markup(user_id)
                    await m.reply_photo(
                        photo=f"{IMG_1}",
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=f"👉 **sᴏɴɢ ᴀᴅᴅᴇᴅ ᴀᴛ »** `{pos}`\n\n🏷️ **ɴᴀᴍᴇ:** [m3u8 video stream]({url}) | `live`\n🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
                    )
                else:
                    if Q == 720:
                        amaze = HighQualityVideo()
                    elif Q == 480:
                        amaze = MediumQualityVideo()
                    elif Q == 360:
                        amaze = LowQualityVideo
                    try:
                        await loser.edit("✨ ᴡᴀɪᴛɪɴɢ ᴛᴏ ᴘʟᴀʏ...")
                        await music_on(chat_id)
                        await add_active_chat(chat_id)
                        await calls.join_group_call(
                            chat_id,
                            AudioVideoPiped(
                                livelink,
                                HighQualityAudio(),
                                amaze,
                            ),
                            stream_type=StreamType().live_stream,
                        )
                        add_to_queue(chat_id, "m3u8 video", livelink, url, "video", Q)
                        await loser.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        buttons = stream_markup(user_id)
                        await m.reply_photo(
                            photo=f"{IMG_2}",
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"🏷️ **ɴᴀᴍᴇ:** [m3u8 video stream]({url}) | `live`\n🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
                        )
                    except (NoActiveGroupCall, GroupCallNotFound):
                        await loser.delete()
                        await remove_active_chat(chat_id)
                        await m.reply_text(" ᴛᴜʀɴ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ғɪʀsᴛ❗")
                    except NoVideoSourceFound:
                        await loser.delete()
                        await remove_active_chat(chat_id)
                        await m.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ʟᴏᴀᴅ ʏᴏᴜʀ sᴏɴɢ sᴏʀʀʏ🥺")
                    except NoAudioSourceFound:
                        await loser.delete()
                        await remove_active_chat(chat_id)
                        await m.reply_text("sᴏᴍᴇᴛʜɪɴɢ ɪs ᴍɪssɪɴɢ ɪɴ ʏᴏᴜʀ sᴏɴɢ⭕")
            else:
                search = ytsearch(url)
                title = search[0]
                songname = search[0]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await thumb(thumbnail, title, userid, ctitle)
                if chat_id in QUEUE:
                    await loser.edit("🔄 ᴀᴅᴅ ᴛᴏ ǫᴜᴇᴜᴇ...")
                    pos = add_to_queue(chat_id, songname, livelink, url, "video", Q)
                    await loser.delete()
                    requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    buttons = stream_markup(user_id)
                    await m.reply_photo(
                        photo=image,
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=f"👉 **sᴏɴɢ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ »** `{pos}`\n\n🏷️ **ɴᴀᴍᴇ:** [{songname}]({url}) | `live`\n🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
                    )
                    remove_if_exists(image)
                else:
                    if Q == 720:
                        amaze = HighQualityVideo()
                    elif Q == 480:
                        amaze = MediumQualityVideo()
                    elif Q == 360:
                        amaze = LowQualityVideo()
                    try:
                        await loser.edit("✨ ᴡᴀɪᴛɪɴɢ ᴛᴏ ᴘʟᴀʏ...")
                        await music_on(chat_id)
                        await add_active_chat(chat_id)
                        await calls.join_group_call(
                            chat_id,
                            AudioVideoPiped(
                                livelink,
                                HighQualityAudio(),
                                amaze,
                            ),
                            stream_type=StreamType().live_stream,
                        )
                        add_to_queue(chat_id, songname, livelink, url, "video", Q)
                        await loser.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        buttons = stream_markup(user_id)
                        await m.reply_photo(
                            photo=image,
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"🏷️**ɴᴀᴍᴇ:** [{songname}]({url}) | `live`\n🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
                        )
                        remove_if_exists(image)
                    except (NoActiveGroupCall, GroupCallNotFound):
                        await loser.delete()
                        await remove_active_chat(chat_id)
                        await m.reply_text("ᴛᴜʀɴ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ғɪʀsᴛ❗")
                    except NoVideoSourceFound:
                        await loser.delete()
                        await remove_active_chat(chat_id)
                        await m.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ʟᴏᴀᴅ ʏᴏᴜʀ sᴏɴɢ sᴏʀʀʏ🥺")
                    except NoAudioSourceFound:
                        await loser.delete()
                        await remove_active_chat(chat_id)
                        await m.reply_text("sᴏᴍᴇᴛʜɪɴɢ ɪs ᴍɪssɪɴɢ ɪɴ ʏᴏᴜʀ sᴏɴɢ⭕")
                    except TimeoutError:
                        await loser.delete()
                        await remove_active_chat(chat_id)
                        await m.reply_text("ᴘʀᴏᴄᴇss ᴡᴀs ᴄᴀɴᴄᴇʟʟᴇᴅ, ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ ᴏʀ ᴜsᴇ `/stream` ᴛᴏ sᴛʀᴇᴀᴍ.")