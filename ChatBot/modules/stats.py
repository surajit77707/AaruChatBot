from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from ChatBot import app
from ChatBot.database import get_chats


@app.on_message(filters.command("statsggggggg"))
async def stats(client: app, message: Message):
    data = await get_chats()
    total_users = len(data["users"])
    total_chats = len(data["chats"])

    await message.reply_text(
        f"""📊 **ChatBot Stats - {(await client.get_me()).first_name}**\n\n
👥 **Total Users:** {total_users}
💬 **Total Chats:** {total_chats}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url="https://t.me/MissAaru_Robot?startgroup=true"),
                    InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/C0DE_SEARCH"),
                ]
            ]
        )
    )
