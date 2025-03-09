import random
from datetime import datetime

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import IMG
from ChatBot import app


@app.on_message(filters.command("ping"))
async def ping(client, message: Message):
    start = datetime.now()
    response_msg = await message.reply_photo(
        photo=random.choice(IMG),
        caption="🪄",
    )

    ms = (datetime.now() - start).microseconds / 1000

    await response_msg.edit_text(
        text=f"❖ {app.name} ɪs ᴀʟɪᴠᴇ ♥︎.\n\n❖ ᴜᴘᴛɪᴍᴇ ➥ `{ms} ᴍs`",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{app.username}?startgroup"),
                InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇ", url="https://t.me/moviiieeeesss"),
            ]
        ]),
    )
