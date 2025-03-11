import re
import requests
from pyrogram import Client, filters
from ChatBot import app

@app.on_message(filters.command("hug"))
async def send_hug(client, message):
    api_url = "https://myown.codesearchdev.workers.dev/hug"

    try:
        response = requests.get(api_url).json()
        hug_url = response.get("data")

        if hug_url:
            reply_id = message.reply_to_message.id if message.reply_to_message else message.id
            await client.send_animation(
                chat_id=message.chat.id,
                animation=hug_url,
                caption="pahadan ka ek special hug 🤗💕",
                reply_to_message_id=reply_id
            )
        else:
            await message.reply_text(" GIF abhi nahi mil rahi. 😔")

    except:
        await message.reply_text("Kuch gadbad hai, abhi hug nahi de sakti. 😞")

@app.on_message(filters.command("kiss"))
async def send_kiss(client, message):
    api_url = "https://myown.codesearchdev.workers.dev/kiss"

    try:
        response = requests.get(api_url).json()
        kiss_url = response.get("data")

        if kiss_url:
            reply_id = message.reply_to_message.id if message.reply_to_message else message.id
            await client.send_animation(
                chat_id=message.chat.id,
                animation=kiss_url,
                caption="Pahadan ka pyaara kiss 😘💕",
                reply_to_message_id=reply_id
            )
        else:
            await message.reply_text("Kiss GIF abhi nahi mil rahi. 😔")

    except:
        await message.reply_text("Kuch gadbad hai, abhi kiss nahi de sakti. 😞")
