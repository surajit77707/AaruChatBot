from alicex.utils.database import total_chats, total_users

# Save or update a user in the database
async def save_user(user_id: int, first_name: str, username: str = None):
    user_data = {
        "user_id": user_id,
        "first_name": first_name,
        "username": username,
    }
    await total_users.update_one(
        {"user_id": user_id},
        {"$set": user_data},
        upsert=True
    )

# Get all users from the database
async def get_all_users():
    return await total_users.find().to_list(None)

# Check if a user exists in the database
async def is_user_in_db(user_id: int):
    user = await total_users.find_one({"user_id": user_id})
    return user is not None

# Get the total count of users
async def get_total_users_count():
    return await total_users.count_documents({})

# Save or update a chat in the database
async def save_chat(chat_id: int, chat_title: str):
    chat_data = {
        "chat_id": chat_id,
        "chat_title": chat_title,
    }
    await total_chats.update_one(
        {"chat_id": chat_id},
        {"$set": chat_data},
        upsert=True
    )

# Get all chats from the database
async def get_all_chats():
    return await total_chats.find().to_list(None)

# Check if a chat exists in the database
async def is_chat_in_db(chat_id: int):
    chat = await total_chats.find_one({"chat_id": chat_id})
    return chat is not None

# Get the total count of chats
async def get_total_chats_count():
    return await total_chats.count_documents({})
