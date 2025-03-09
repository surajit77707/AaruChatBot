import random
import requests
import time

from pyrogram import filters
from pyrogram.enums import PollType, ChatAction
from pyrogram import types
from ChatBot import app

last_command_time = {}

@app.on_message(filters.command(["quiz"]))
async def quiz(client, message):
    user_id = message.from_user.id
    current_time = time.time()

    # Throttle command usage to avoid spamming
    if user_id in last_command_time and current_time - last_command_time[user_id] < 5:
        await message.reply_text(
            "Pʟᴇᴀsᴇ ᴡᴀɪᴛ 𝟻 sᴇᴄᴏɴᴅs ʙᴇғᴏʀᴇ ᴜsɪɴɢ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀɢᴀɪɴ."
        )
        return

    last_command_time[user_id] = current_time

    categories = [9, 17, 18, 20, 21, 27]
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)

    # Fetch a random quiz question
    url = f"https://opentdb.com/api.php?amount=1&category={random.choice(categories)}&type=multiple"
    response = requests.get(url).json()

    question_data = response["results"][0]
    question = question_data["question"]
    correct_answer = question_data["correct_answer"]
    incorrect_answers = question_data["incorrect_answers"]

    # Combine the correct answer with the incorrect answers
    all_answers = incorrect_answers + [correct_answer]
    random.shuffle(all_answers)

    # Get the index of the correct answer
    correct_option_id = all_answers.index(correct_answer)

    # Create PollOption objects for the answers
    poll_options = [types.PollOption(text=answer) for answer in all_answers]

    # Send the poll with the correct answers
    await app.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=poll_options,  # Passing PollOption objects instead of strings
        is_anonymous=False,
        type=PollType.QUIZ,
        correct_option_id=correct_option_id,
    )

# Module metadata
__MODULE__ = "Qᴜɪᴢ"
__HELP__ = " /quiz - ᴛᴏ ɢᴇᴛ ᴀɴ ʀᴀɴᴅᴏᴍ ǫᴜɪᴢ"
