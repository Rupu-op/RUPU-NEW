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


from driver.core import me_bot, me_user
from driver.queues import QUEUE
from driver.decorators import check_blacklist
from program.utils.inline import menu_markup, stream_markup

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_USERNAME,
    UPDATES_CHANNEL,
    SUDO_USERS,
    OWNER_ID,
)


@Client.on_callback_query(filters.regex("home_start"))
@check_blacklist()
async def start_set(_, query: CallbackQuery):
    await query.answer("home start")
    await query.edit_message_sticker("CAADBQAD-QQAAhCWOFRERrHKHtIUvgI") 
    await query.edit_message_text(
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

@Client.on_callback_query(filters.regex("quick_use"))
@check_blacklist()
async def quick_set(_, query: CallbackQuery):
    await query.answer("quick bot usage")
    await query.edit_message_text(
        f"""ℹ️ ǫᴜɪᴄᴋ ᴜsᴇ ɢᴜɪᴅᴇ!

👩🏻‍💼 » /play - Type this with give the song title or youtube link or audio file to play Music. (Remember to don't play YouTube live stream by using this command!, because it will cause unforeseen problems.)

👩🏻‍💼 » /vplay - Type this with give the song title or youtube link or video file to play Video. (Remember to don't play YouTube live video by using this command!, because it will cause unforeseen problems.)

👩🏻‍💼 » /vstream - Type this with give the YouTube live stream video link or m3u8 link to play live Video. (Remember to don't play local audio/video files or non-live YouTube video by using this command!, because it will cause unforeseen problems.)

❓ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ɴᴏᴡ ᴍsɢ [s•4•sʜɪᴠ](https://t.me/shivamdemon)""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="user_guide")]]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("command_list"))
@check_blacklist()
async def commands_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.answer("commands menu")
    await query.edit_message_text(
        f"""✨ **ʜᴇʏ ᴅᴇᴀʀ [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**

» ᴄʟɪᴄᴋ ʙᴜᴛᴛᴏɴs ғᴏʀ ᴋɴᴏᴡ ᴍᴏʀᴇ !

ᴜsᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅ ʙʏ(`! / .`) ʜᴀɴᴅʟᴇʀ""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🥴 ғᴏʀ ᴀᴅᴍɪɴs", callback_data="admin_command"),
                ],[
                    InlineKeyboardButton("👩🏻‍💼 ғᴏʀ ᴀʟʟ ᴜsᴇʀs", callback_data="user_command"),
                ],[
                    InlineKeyboardButton("🔥ғᴏʀ sᴜᴅᴏᴇʀs", callback_data="sudo_command"),
                    InlineKeyboardButton("❣️ғᴏʀ ᴏᴡɴᴇʀ", callback_data="owner_command"),
                ],[
                    InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="home_start")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("user_command"))
@check_blacklist()
async def user_set(_, query: CallbackQuery):
    await query.answer("basic commands")
    await query.edit_message_text(
        f"""🤗ᴄᴏᴍᴍᴀɴᴅ ғᴏʀ ᴇᴠᴇʀᴏɴᴇ...ᴋᴇᴇᴘ ᴇɴᴊᴏʏɪɴɢ.

» /play (song name/youtube link) - play the music from youtube
» /stream (m3u8/youtube live link) - play youtube/m3u8 live stream music
» /vplay (video name/youtube link) - play the video from youtube
» /vstream (m3u8/youtube live link) - play youtube/m3u8 live stream video
» /playlist - view the queue list of songs and current playing song
» /lyric (query) - search for song lyrics based on the name of the song
» /video (query) - download video from youtube
» /song (query) - download song from youtube
» /search (query) - search for the youtube video link
» /ping - show the bot ping status
» /uptime - show the bot uptime status
» /alive - show the bot alive info (in Group only)""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("admin_command"))
@check_blacklist()
async def admin_set(_, query: CallbackQuery):
    await query.answer("admin commands")
    await query.edit_message_text(
        f"""♥️😙ᴛʜɪs ɪs ғᴏʀ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴛᴏ sᴛʀᴇᴀᴍɪɴɢ.

» /pause - pause the current track being played
» /resume - play the previously paused track
» /skip - goes to the next track
» /stop - stop playback of the track and clears the queue
» /vmute - mute the streamer userbot on group call
» /vunmute - unmute the streamer userbot on group call
» /volume `1-200` - adjust the volume of music (userbot must be admin)
» /reload - reload bot and refresh the admin data
» /userbotjoin - invite the userbot to join group
» /userbotleave - order userbot to leave from group
» /startvc - start/restart the group call
» /stopvc - stop/discard the group call""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("sudo_command"))
@check_blacklist()
async def sudo_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in SUDO_USERS:
        await query.answer("⚠️ ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ\n\n» ᴛʜɪs ɪs ғᴏʀ sᴜᴅᴏᴇʀs.", show_alert=True)
        return
    await query.answer("sudo commands")
    await query.edit_message_text(
        f"""✌️ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ ᴏᴜʀ ʙᴏᴛ ᴘᴀʀᴛɴᴇʀs.

» /stats - get the bot current statistic
» /calls - show you the list of all active group call in database
» /block (`chat_id`) - use this to blacklist any group from using your bot
» /unblock (`chat_id`) - use this to whitelist any group from using your bot
» /blocklist - show you the list of all blacklisted chat
» /speedtest - run the bot server speedtest
» /sysinfo - show the system information
» /logs - generate the current bot logs
» /eval - run an code
» /sh - run an code""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("owner_command"))
@check_blacklist()
async def owner_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in OWNER_ID:
        await query.answer("⚠️ ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ\n\n» ᴛʜɪs ɪs ғᴏʀ ᴏᴡɴᴇʀ.", show_alert=True)
        return
    await query.answer("owner commands")
    await query.edit_message_text(
        f"""💫 ᴄᴏᴍᴍᴀɴᴅ ʟɪsᴛ ғᴏʀ ᴍʏ ʟᴏᴠᴇʟʏ ᴍᴀsᴛᴇʀ.

» /gban (`username` or `user_id`) - for global banned people, can be used only in group
» /ungban (`username` or `user_id`) - for un-global banned people, can be used only in group
» /update - update your bot to latest version
» /restart - restart your bot server
» /leaveall - order userbot to leave from all group
» /leavebot (`chat id`) - order bot to leave from the group you specify
» /broadcast (`message`) - send a broadcast message to all groups in bot database
» /broadcast_pin (`message`) - send a broadcast message to all groups in bot database with the chat pin""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("stream_menu_panel"))
@check_blacklist()
async def at_set_markup_menu(_, query: CallbackQuery):
    user_id = query.from_user.id
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴠᴄ ʀɪɢʜᴛ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ!", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.message.from_user.id
    buttons = menu_markup(user_id)
    if chat_id in QUEUE:
        await query.answer("control panel opened")
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("stream_home_panel"))
@check_blacklist()
async def is_set_home_menu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴠᴄ ʀɪɢʜᴛ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ!", show_alert=True)
    await query.answer("control panel closed")
    user_id = query.message.from_user.id
    buttons = stream_markup(user_id)
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex("set_close"))
@check_blacklist()
async def on_close_menu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴠᴄ ʀɪɢʜᴛ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ!", show_alert=True)
    await query.message.delete()


@Client.on_callback_query(filters.regex("close_panel"))
@check_blacklist()
async def in_close_panel(_, query: CallbackQuery):
    await query.message.delete()
