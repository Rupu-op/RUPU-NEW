
import traceback

from cache.admins import admins
from config import BOT_USERNAME, IMG_5

from driver.core import calls, me_user
from driver.design.thumbnail import thumb
from driver.design.chatname import CHAT_TITLE
from driver.queues import QUEUE, clear_queue
from driver.filters import command, other_filters
from driver.decorators import authorized_users_only, check_blacklist
from driver.utils import skip_current_song, skip_item, remove_if_exists
from driver.database.dbqueue import (
    is_music_playing,
    remove_active_chat,
    music_off,
    music_on,
)

from pyrogram import Client, filters
from program.utils.inline import stream_markup, close_mark
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
)


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
@check_blacklist()
async def update_admin(client, message: Message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ ʙᴏᴛ ʀᴇʟᴏᴀᴅᴇᴅ..**ᴀᴅᴍɪɴʟɪsᴛ ᴜᴘᴅᴀᴛᴇᴅ**"
    )


@Client.on_message(
    command(["stop", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "vstop"])
    & other_filters
)
@authorized_users_only
@check_blacklist()
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await calls.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
            clear_queue(chat_id)
            await m.reply_text("ᴍᴜsɪᴄ sᴛᴏᴘᴘᴇᴅ❗😇.")
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"⭕ **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply_text("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ**")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                return await m.reply_text("🥴ᴍᴜsɪᴄ ᴀʟʀᴇᴀᴅʏ ᴘᴀᴜsᴇᴅ")
            await calls.pause_stream(chat_id)
            await music_off(chat_id)
            await m.reply_text(
                "⏸ **ᴍᴜsɪᴄ ᴘᴀᴜsᴇᴅ**."
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"⭕ **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply_text("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ**")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                return await m.reply_text("👉 ᴍᴜsɪᴄ ᴀʟʀᴇᴀᴅʏ ʀᴇsᴜᴍᴇᴅ")
            await calls.resume_stream(chat_id)
            await music_on(chat_id)
            await m.reply_text(
                "**🎵 ᴍᴜsɪᴄ ʀᴇsᴜᴍᴇᴅ**."
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"⭕ **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply_text("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ**")


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
@check_blacklist()
async def skip(c: Client, m: Message):
    user_id = m.from_user.id
    chat_id = m.chat.id
    queue = await skip_current_song(chat_id)
    if queue == 0:
        await m.reply_text("❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ")
    elif queue == 1:
        await m.reply_text("» ɴᴏ ᴀɴʏ sᴏɴɢ ᴛᴏ sᴋɪᴘ ᴅᴇᴀʀ😙")
    elif queue == 2:
        await m.reply_text("🗑️ ᴄʟᴇᴀʀɪɴɢ ǫᴜᴇᴜᴇ...ᴀssɪsᴛᴀɴᴛ ʟᴇᴀᴠᴇ ᴠᴄ")
    else:
        buttons = stream_markup(user_id)
        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
        thumbnail = f"{IMG_5}"
        title = f"{queue[0]}"
        userid = m.from_user.id
        gcname = m.chat.title
        ctitle = await CHAT_TITLE(gcname)
        image = await thumb(thumbnail, title, userid, ctitle)
        await c.send_photo(
            chat_id,
            photo=image,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=f"⏭ **sᴋɪᴘᴘᴇᴅ** ᴛᴏ ɴᴇxᴛ sᴏɴɢ.\n\n🏷️ **ɴᴀᴍᴇ:** [{queue[0]}]({queue[1]})\n⏱️ **ᴅᴜʀᴀᴛɪᴏᴍ:** `{duration}`\n🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
        )
        remove_if_exists(image)


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                return await m.reply_text("😶ᴀssɪsᴛᴀɴᴛ ᴀʟʀᴇᴀᴅʏ ᴍᴜᴛᴇᴅ ..")
            await calls.mute_stream(chat_id)
            await music_off(chat_id)
            await m.reply_text(
                "🔇 **ᴀssɪsᴛᴀɴᴛ ᴜɴᴍᴜᴛᴇᴅ** !"
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"⭕ **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply_text("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ**")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                return await m.reply_text("🙏 ᴛʜᴇ sᴛʀᴇᴀᴍ ᴀʟʀᴇᴀᴅʏ ᴜɴᴍᴜᴛᴇᴅ.")
            await calls.unmute_stream(chat_id)
            await music_on(chat_id)
            await m.reply_text("🔊 **ᴀssɪsᴛᴀɴᴛ ᴜɴᴍᴜᴛᴇᴅ**."
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"⭕ **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply_text("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ**")


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def change_volume(c: Client, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("usage: `/volume` (`0-200`)")
    a = await c.get_chat_member(m.chat.id, me_user.id)
    if not a.can_manage_voice_chats:
        return await m.reply_text(
            "ᴍᴀᴋᴇ ᴀssɪsᴛᴀɴᴛ ᴀᴅᴍɪɴ ғɪʀsᴛ ᴛᴏ sᴇᴛ ᴠᴏʟᴜᴍᴇ!"
        )
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await calls.change_volume_call(chat_id, volume=int(range))
            await m.reply_text(
                f"✅ **ᴠᴏʟ sᴇᴛ ᴛᴏ** `{range}`%"
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"⭕ **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply_text("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ**")


@Client.on_callback_query(filters.regex("set_pause"))
@check_blacklist()
async def cbpause(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💫 ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴠᴄ ʀɪɢʜᴛ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await query.answer("🥴ᴍᴜsɪᴄ ᴀʟʀᴇᴀᴅʏ ᴘᴀᴜsᴇᴅ.", show_alert=True)
                return
            await calls.pause_stream(chat_id)
            await music_off(chat_id)
            await query.answer("⏸ ᴍᴜsɪᴄ ᴘᴀᴜsᴇᴅ !", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"⭕ **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("set_resume"))
@check_blacklist()
async def cbresume(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💫 ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴠᴄ ʀɪɢʜᴛ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await query.answer("👉 ᴍᴜsɪᴄ ᴀʟʀᴇᴀᴅʏ ʀᴇsᴜᴍᴇᴅ.", show_alert=True)
                return
            await calls.resume_stream(chat_id)
            await music_on(chat_id)
            await query.answer("🎵 ᴍᴜsɪᴄ ʀᴇsᴜᴍᴇᴅ !", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"⭕ **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("set_stop"))
@check_blacklist()
async def cbstop(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💫 ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴠᴄ ʀɪɢʜᴛ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await calls.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("ᴍᴜsɪᴄ sᴛᴏᴘᴘᴇᴅ❗😇.", reply_markup=close_mark)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"⭕ **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("set_mute"))
@check_blacklist()
async def cbmute(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💫 ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴠᴄ ʀɪɢʜᴛ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await query.answer("😶ᴀssɪsᴛᴀɴᴛ ᴀʟʀᴇᴀᴅʏ ᴍᴜᴛᴇᴅ ..", show_alert=True)
                return
            await calls.mute_stream(chat_id)
            await music_off(chat_id)
            await query.answer("🔇 ᴀssɪsᴛᴀɴᴛ ᴜɴᴍᴜᴛᴇᴅ !", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"⭕ **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("set_unmute"))
@check_blacklist()
async def cbunmute(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💫 ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴠᴄ ʀɪɢʜᴛ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await query.answer("🙏 ᴛʜᴇ sᴛʀᴇᴀᴍ ᴀʟʀᴇᴀᴅʏ ᴜɴᴍᴜᴛᴇᴅ.", show_alert=True)
                return
            await calls.unmute_stream(chat_id)
            await music_on(chat_id)
            await query.answer("🔊 **ᴀssɪsᴛᴀɴᴛ ᴜɴᴍᴜᴛᴇᴅ**!", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"⭕ **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("set_skip"))
@check_blacklist()
async def cbskip(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💫 ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴠᴄ ʀɪɢʜᴛ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ!", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    queue = await skip_current_song(chat_id)
    if queue == 0:
        await query.answer("❌ ɴᴏᴛʜɪɴʜ ɪs ᴘʟᴀʏɪɴɢ", show_alert=True)
    elif queue == 1:
        await query.answer("» ɴᴏ ᴀɴʏ sᴏɴɢ ᴛᴏ sᴋɪᴘ ᴅᴇᴀʀ😙.", show_alert=True)
    elif queue == 2:
        await query.answer("🗑️ ᴄʟᴇᴀʀɪɴɢ ǫᴜᴇᴜᴇ...ᴀssɪsᴛᴀɴᴛ ʟᴇᴀᴠᴇ ᴠᴄ.", show_alert=True)
    else:
        await query.answer("goes to the next track, proccessing...")
        await query.message.delete()
        buttons = stream_markup(user_id)
        requester = f"[{query.from_user.first_name}](tg://user?id={query.from_user.id})"
        thumbnail = f"{IMG_5}"
        title = f"{queue[0]}"
        userid = query.from_user.id
        gcname = query.message.chat.title
        ctitle = await CHAT_TITLE(gcname)
        image = await thumb(thumbnail, title, userid, ctitle)
        await _.send_photo(
            chat_id,
            photo=image,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=f"⏭ **sᴋɪᴘᴘᴇᴅ** ᴛᴏ ɴᴇxᴛ.sᴏɴɢ.\n\n🏷️ **ɴᴀᴍᴇ:** [{queue[0]}]({queue[1]})\n⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ᴜsᴇʀ ʙʏ:** {requester}",
        )
        remove_if_exists(image)
