from ChatBot.database.total_user_chat_db import is_user_in_db, is_chat_in_db, save_chat, save_user
from functools import wraps
from pyrogram.types import Message, CallbackQuery
from typing import Callable
from pyrogram import Client
from ChatBot import app
import config
from pyrogram.enums import ChatType

def save(func: Callable):
    @wraps(func)
    async def wrapper(client: Client, update, *args, **kwargs):
        # Proceed to the original handler function first
        result = await func(client, update, *args, **kwargs)

        # Check if the update is a Message or CallbackQuery
        if isinstance(update, Message):
            # Handle saving user and chat for a Message
            if update.from_user:
                user_id = update.from_user.id
                first_name = update.from_user.first_name
                username = f"@{update.from_user.username}" or f"[User](tg://user?id={user_id})"
                if not await is_user_in_db(user_id):
                    await save_user(user_id, first_name, username)
                    # Log the new user
                    await app.send_message(
                        chat_id=config.LOG_GROUP_ID,
                        text=(
                            f"#NEWUSER\n"
                            f"👤 **Name**: {first_name}\n"
                            f"🆔 **User Id**: {user_id}\n"
                            f"📛 **Username**: {username}"
                        ),
                    )

            if update.chat and update.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                chat_id = update.chat.id
                chat_title = update.chat.title
                if not await is_chat_in_db(chat_id):
                    # Fetch chat details for logging
                    chat = await client.get_chat(chat_id)
                    member_count = chat.members_count or "Unknown"
                    await save_chat(chat_id, chat_title)
                    # Log the new chat
                    await app.send_message(
                        chat_id=config.LOG_GROUP_ID,
                        text=(
                            f"#NEWCHAT\n"
                            f"🏘️ **Name**: {chat_title}\n"
                            f"🆔 **Chat Id**: {chat_id}\n"
                            f"🧮 **Members Count**: {member_count}\n"
                        ),
                        disable_web_page_preview=True,
                    )

        elif isinstance(update, CallbackQuery):
            # Handle saving user and chat for a CallbackQuery
            if update.from_user:
                user_id = update.from_user.id
                first_name = update.from_user.first_name
                username = f"@{update.from_user.username}" or f"[User](tg://user?id={user_id})"
                if not await is_user_in_db(user_id):
                    await save_user(user_id, first_name, username)
                    # Log the new user
                    await app.send_message(
                        chat_id=config.LOG_GROUP_ID,
                        text=(
                            f"#NEWUSER\n"
                            f"👤 **Name**: {first_name}\n"
                            f"🆔 **User Id**: {user_id}\n"
                            f"📛 **Username**: {username}"
                        ),
                    )

            if update.message and update.message.chat and update.message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                chat_id = update.message.chat.id
                chat_title = update.message.chat.title
                if not await is_chat_in_db(chat_id):
                    # Fetch chat details for logging
                    chat = await client.get_chat(chat_id)
                    member_count = chat.members_count or "Unknown"
                    await save_chat(chat_id, chat_title)
                    # Log the new chat
                    await app.send_message(
                        chat_id=config.LOG_GROUP_ID,
                        text=(
                            f"#NEWCHAT\n"
                            f"🏘️ **Name**: {chat_title}\n"
                            f"🆔 **Chat Id**: {chat_id}\n"
                            f"🧮 **Members Count**: {member_count}\n"
                        ),
                        disable_web_page_preview=True,
                    )

        # Return the result of the original function
        return result

    return wrapper
