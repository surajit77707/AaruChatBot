import re
import requests
from pyrogram import Client, filters
from ChatBot import app

# Function to fetch waifu image
def get_waifu(tag):
    api_url = f"https://waifu.codesearchdev.workers.dev/?tag={tag}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json().get("image_url")
    except requests.exceptions.RequestException:
        return None
    return None

# Command handler for custom tags
@app.on_message(filters.command("waifu"))
async def send_custom_waifu(client, message):
    if len(message.command) < 2:
        await message.reply_text("You need to provide a tag. Example: `/waifu maid`", reply_to_message_id=message.id)
        return

    tag = message.command[1].lower()
    valid_tags = [
        "maid", "waifu", "marin-kitagawa", "mori-calliope", 
        "raiden-shogun", "oppai", "selfies", "uniform", "kamisato-ayaka", 
        "ass", "hentai", "milf", "oral", "paizuri", "ecchi", "ero"
    ]

    if tag not in valid_tags:
        await message.reply_text("This tag isn't available. Try something from: " + ", ".join(valid_tags), reply_to_message_id=message.id)
        return

    image_url = get_waifu(tag)

    if image_url:
        reply_id = message.reply_to_message.id if message.reply_to_message else message.id
        await client.send_photo(
            chat_id=message.chat.id,
            photo=image_url,
            caption=f"Here's your {tag} waifu. 💕",
            reply_to_message_id=reply_id
        )
    else:
        await message.reply_text("Oops, couldn't find an image right now. 😞", reply_to_message_id=message.id)