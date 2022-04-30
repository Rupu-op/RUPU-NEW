""" inline section button """


from pyrogram.types import (
  InlineKeyboardButton,
  InlineKeyboardMarkup,
)


def stream_markup(user_id):
  buttons = [
       [
            InlineKeyboardButton(text="**❣️ Oᴡɴᴇʀ**", url=f"https://t.me/itz_rupu"),
            InlineKeyboardButton(text="✨Gʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"),
       ],
     ]
  return buttons


def menu_markup(user_id):
  buttons = [
    [
      InlineKeyboardButton(text="⏹", callback_data=f'set_stop | {user_id}'),
      InlineKeyboardButton(text="⏸", callback_data=f'set_pause | {user_id}'),
      InlineKeyboardButton(text="▶️", callback_data=f'set_resume | {user_id}'),
      InlineKeyboardButton(text="⏭", callback_data=f'set_skip | {user_id}'),
    ],
    [
      InlineKeyboardButton(text="🔇", callback_data=f'set_mute | {user_id}'),
      InlineKeyboardButton(text="🔊", callback_data=f'set_unmute | {user_id}'),
    ],
    [
      InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data='stream_home_panel'),
    ]
  ]
  return buttons


close_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "🚫 ᴄʟᴏsᴇ", callback_data="set_close"
      )
    ]
  ]
)


back_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "🔙 ʙᴀᴄᴋ", callback_data="stream_menu_panel"
      )
    ]
  ]
)
