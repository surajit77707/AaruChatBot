from functools import wraps
import asyncio
from pyrogram.errors import *
from pyrogram.types import Message, InlineQuery
import config 
from alicex import LOGGER , app

def error(func):
    @wraps(func)
    async def wrapper(client, update, *args, **kwargs):  # 'update' can be a Message or InlineQuery
        try:
            # Call the actual function
            return await func(client, update, *args, **kwargs)
        except FloodWait as e:
            log.warning(f"Flood wait for {e.value} seconds.")
            await asyncio.sleep(e.value)
            # Retry the function after the wait
            return await func(client, update, *args, **kwargs)
        except BadRequest as e:
            log.error(f"Bad request error: {e}")
            await log_error(client, f"Bad request error: {str(e)}", update)
        except Forbidden as e:
            log.error(f"Forbidden error: {e}")
            await log_error(client, f"Forbidden error: {str(e)}", update)
        except InternalServerError as e:
            log.error(f"Internal server error: {e}")
            await log_error(client, f"Internal server error: {str(e)}", update)
        except PeerIdInvalid as e:
            log.error(f"Peer ID invalid: {e}")
            await log_error(client, f"Peer ID invalid: {str(e)}", update)
        except MessageNotModified as e:
            log.error(f"Message not modified error: {e}")
            await log_error(client, f"Message not modified: {str(e)}", update)
        except ChatAdminRequired as e:
            log.error(f"Chat admin required: {e}")
            await log_error(client, f"Chat admin required error: {str(e)}", update)
        except ChannelInvalid as e:
            log.error(f"Channel invalid error: {e}")
            await log_error(client, f"Channel invalid: {str(e)}", update)
        except UserNotParticipant as e:
            log.error(f"User not a participant error: {e}")
            await log_error(client, f"User not a participant: {str(e)}", update)
        except RPCError as e:
            log.error(f"RPC error occurred: {e}")
            await log_error(client, f"RPC error occurred: {str(e)}", update)
        except asyncio.TimeoutError as e:
            log.error(f"Timeout error: {e}")
            await log_error(client, f"Timeout error: {str(e)}", update)
        except ValueError as e:
            log.error(f"Value error: {e}")
            await log_error(client, f"Value error: {str(e)}", update)
        except TypeError as e:
            log.error(f"Type error: {e}")
            await log_error(client, f"Type error: {str(e)}", update)
        except Exception as e:
            log.exception(f"An unexpected error occurred: {e}")
            await log_error(client, f"Unexpected error: {str(e)}", update)

    return wrapper

# Function to send error logs to the log channel
async def log_error(client, error_message, update):
    log_text = f"**Error Occurred**\n**Error:** `{error_message}`\n"

    if isinstance(update, Message):  # If it's a message object
        log_text += (
            f"**Chat:** {update.chat.title or 'Private Chat'} (`{update.chat.id}`)\n"
            f"**User:** {update.from_user.first_name} (`{update.from_user.id}`)\n"
            f"**Message:** {update.text or 'No text content'}\n"
        )
    elif isinstance(update, InlineQuery):  # If it's an inline query
        log_text += (
            f"**User:** {update.from_user.first_name} (`{update.from_user.id}`)\n"
            f"**Inline Query:** {update.query or 'No query content'}\n"
        )
    else:
        log_text += "**Unknown update type**"

    try:
        await app.send_message(chat_id=config.LOG_GROUP_ID, text=log_text)
    except Exception as log_exception:
        log.error(f"Failed to log error in the log channel: {log_exception}")
