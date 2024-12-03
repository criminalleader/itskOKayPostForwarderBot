import asyncio
from pyrogram import filters, Client
from config import *
from lazydeveloperr.database import db 
from asyncio.exceptions import TimeoutError

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from plugins.Data import Data
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
)
# user_forward_data = {}
St_Session = {}
handler = {}

def manager(id, value):
    global handler
    handler[id] = value
    return handler

def get_manager():
    global handler
    return handler


PHONE_NUMBER_TEXT = (
    "📞__ Now send your Phone number to Continue"
    " include Country code.__\n**Eg:** `+13124562345`\n\n"
    "Press /cancel to Cancel."
)

def set_session_in_config(id, session_string):
    from config import Lazy_session  # Import St_Session to modify it
    Lazy_session[id] = session_string

def set_api_id_in_config(id, lazy_api_id):
    from config import Lazy_api_id  # Import api id to modify it
    Lazy_api_id[id] = lazy_api_id

def set_api_hash_in_config(id, lazy_api_hash):
    from config import Lazy_api_hash  # Import api hash to modify it
    Lazy_api_hash[id] = lazy_api_hash

lazydeveloperrsession = {}

@Client.on_message(filters.private & filters.command("connect"))
async def connect_session(bot, msg):
    global lazydeveloperrsession
    user_id = msg.from_user.id
    if user_id in lazydeveloperrsession:
        return bot.send_message(chat_id=msg.chat.id, text=f"You are already logged in ✅.\n\nUse /rename and enjoy renaming 👍")
    
    # get users session string
    session_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `TELETHON SESSION STRING`", filters=filters.text
    )
    if await cancelled(session_msg):
        return
    lazydeveloper_string_session = session_msg.text
    
    #get user api id 
    api_id_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_ID`", filters=filters.text
        )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ API_ID (ᴡʜɪᴄʜ ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ). ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    
    # get user api hash
    api_hash_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_HASH`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text

    # 
    success = await bot.send_message(
        chat_id=msg.chat.id,
        text="Trying to login...\n\nPlease wait 🍟"
    )
    await asyncio.sleep(1)
    try:
        lazydeveloperrsession[user_id] = TelegramClient(StringSession(lazydeveloper_string_session), api_id, api_hash)
        await lazydeveloperrsession[user_id].start()
        # for any query msg me on telegram - @LazyDeveloperr 👍
        print(f"Session started successfully for user {user_id} ✅")
        
        await success.delete()
        
        await asyncio.sleep(1)
        
        await bot.send_message(
        chat_id=msg.chat.id,
        text="Logged in Successfully ✅. \n\nType /rename and enjoy renaming journey 👍"
             )
        try:
            set_session_in_config(msg.from_user.id, lazydeveloper_string_session)
            set_api_id_in_config(msg.from_user.id, api_id)
            set_api_hash_in_config(msg.from_user.id, api_hash)
        except Exception as lazydeveloper:
            print(f"Something went wrong : {lazydeveloper}")
            # for any query msg me on telegram - @LazyDeveloperr 👍
    except Exception as e:
        print(f"Error starting session for user {user_id}: {e}")
        await msg.reply("Failed to start session. Please re-check your provided credentials. 👍")
        return


@Client.on_message(filters.private & filters.command("generate"))
async def generate_session(bot, msg):
    lazyid = msg.from_user.id
    global lazydeveloperrsession
    if not await verify_user(lazyid):
        return await msg.reply("⛔ You are not authorized to use this bot.")
    
    if lazyid in lazydeveloperrsession:
        return await msg.reply("Hello sweetheart!\nYour session is already in use. Type /rename and enjoy renaming. \n❤")

    await msg.reply(
        "sᴛᴀʀᴛɪɴG [ᴛᴇʟᴇᴛʜᴏɴ] sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛɪᴏɴ..."
    )
    user_id = msg.chat.id
    api_id_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_ID`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ API_ID (ᴡʜɪᴄʜ ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ). ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    api_hash_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_HASH`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(
        user_id,
        "ɴᴏᴡ ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ` ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ. \nᴇxᴀᴍᴘʟᴇ : `+19876543210`",
        filters=filters.text,
    )
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("sᴇɴᴅɪɴɢ ᴏᴛᴘ...")
    
    client = TelegramClient(StringSession(), api_id, api_hash)

    await client.connect()
    try:
        code = await client.send_code_request(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply(
            "`API_ID` ᴀɴᴅ `API_HASH` ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(
            "`PHONE_NUMBER` ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    try:
        phone_code_msg = await bot.ask(
            user_id,
            "ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ꜰᴏʀ ᴀɴ ᴏᴛᴘ ɪɴ ᴏꜰꜰɪᴄɪᴀʟ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ. ɪꜰ ʏᴏᴜ ɢᴏᴛ ɪᴛ, sᴇɴᴅ ᴏᴛᴘ ʜᴇʀᴇ ᴀꜰᴛᴇʀ ʀᴇᴀᴅɪɴɢ ᴛʜᴇ ʙᴇʟᴏᴡ ꜰᴏʀᴍᴀᴛ. \nɪꜰ ᴏᴛᴘ ɪs `12345`, **ᴘʟᴇᴀsᴇ sᴇɴᴅ ɪᴛ ᴀs** `1 2 3 4 5`.",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply(
            "ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 10 ᴍɪɴᴜᴛᴇs. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        await client.sign_in(phone_number, phone_code, password=None)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply(
            "ᴏᴛᴘ ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply(
            "ᴏᴛᴘ ɪs ᴇxᴘɪʀᴇᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(
                user_id,
                "ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ᴇɴᴀʙʟᴇᴅ ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴘᴀssᴡᴏʀᴅ.",
                filters=filters.text,
                timeout=300,
            )
        except TimeoutError:
            await msg.reply(
                "ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 5 ᴍɪɴᴜᴛᴇs. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        try:
            password = two_step_msg.text
            
            await client.sign_in(password=password)
            
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply(
                "ɪɴᴠᴀʟɪᴅ ᴘᴀssᴡᴏʀᴅ ᴘʀᴏᴠɪᴅᴇᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
                quote=True,
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return

    string_session = client.session.save()
    try:
        # St_Session[msg.from_user.id] = string_session
        set_session_in_config(msg.from_user.id, string_session)
        set_api_id_in_config(msg.from_user.id, api_id)
        set_api_hash_in_config(msg.from_user.id, api_hash)
        print(f"Credentials api id and hash saved to config successfully ✅")
    except Exception as LazyDeveloperr:
        print(LazyDeveloperr)

    text = f"**ᴛᴇʟᴇᴛʜᴏɴ sᴛʀɪɴɢ sᴇssɪᴏɴ** \n\n||`{string_session}`||"
       
    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    success = await phone_code_msg.reply(
        "Session generated ! Trying to login 👍"
    )
    # Save session to the dictionary
    await asyncio.sleep(1)
    try:
        lazydeveloperrsession[lazyid] = TelegramClient(StringSession(string_session), api_id, api_hash)
        await lazydeveloperrsession[lazyid].start()
        print(f"Session started successfully for user {user_id} ✅")
        await success.delete()
        await asyncio.sleep(1)
        await bot.send_message(
        chat_id=msg.chat.id,
        text="Logged in Successfully ✅. \n\nType /rename and enjoy renaming renaming journey 👍"
    )
    except Exception as e:
        print(f"Error starting session for user {user_id}: {e}")
        await msg.reply("Failed to start session. Please try again.")
        return


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇss!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    
    elif "/restart" in msg.text:
        await msg.reply(
            "ʙᴏᴛ ɪs ʀᴇsᴛᴀʀᴛᴇᴅ!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ ᴘʀᴏᴄᴇss!", quote=True)
        return True
    else:
        return False

lock = asyncio.Lock()

@Client.on_message(filters.command("post"))
async def rename(client, message):
    user_id = message.from_user.id

    # Check if the user is allowed to use the bot
    if not await verify_user(user_id):
        return await message.reply("⛔ You are not authorized to use this bot.")
    
    # verify session
    if user_id not in lazydeveloperrsession:
        return await message.reply("⚠️ No session found. Please generate a session first using /generate.")
    
    # check running task
    if lock.locked():
        print('Wait until previous process complete.')
        return await message.reply("⚠️ Another process is running. Please wait until previous process complete. ⏳")
    
    # setting up target chat id to take post from - BASE-CHANNEL
    chat_id = await client.ask(
        text="Send Target Channel Id, From Where You Want Posts To Be Forwarded: in `-100XXXX` Format ",
        chat_id=message.chat.id
    )

    target_chat_id = int(chat_id.text)
    print(f'✅Set target chat => {target_chat_id}' )
    
    # try:
    #     chat_info = await client.get_chat(target_chat_id)
    # except Exception as e:
    #     await client.send_message(message.chat.id, f"Something went wrong while accessing chat : {chat_info}")
    #     print(f"Error accessing chat: {e}")

    await db.set_lazy_target_chat_id(message.from_user.id, target_chat_id)

    print(f"Starting to forward files from channel {target_chat_id} to All-Channels.")

    lazy_userbot = lazydeveloperrsession[user_id]

    # Iterating through messages
    MAIN_POST_CHANNEL = target_chat_id  # Replace with your MAIN_POST_CHANNEL ID
    # CHANNELS = [
    #     -1001111111111, -1002222222222, -1003333333333,  # Replace with your channel IDs
    #     # Add up to 100 channel IDs here
    # ]
    DELAY_BETWEEN_POSTS = 60  # 15 minutes in seconds
    deleted = 0
    try:
        messages = []
        last_message_id = await db.get_skip_msg_id()  # Start fetching from the most recent message
        print(f"The last message id got => {last_message_id}")
        async with lock:
            # Fetch messages in reverse order
            async for msg in lazy_userbot.iter_messages(MAIN_POST_CHANNEL, offset_id=last_message_id):
                if msg:  # Collect valid messages
                    messages.append(msg)
                    last_message_id = msg.id  # Update the last processed message ID
                else:
                    break  # Exit the loop if no messages are left

            print(f"✅ Total messages collected: {len(messages)}")

            # Step 2: Sort messages in ascending order of message_id
            messages.sort(key=lambda m: m.id)

            # Step 3: Forward messages in ascending order
            for msg in messages:
                if message.empty:
                    deleted += 1
                    continue
                
                for channel_id in CHANNELS:
                    try:
                        await lazy_userbot.copy_message(chat_id=channel_id, from_chat_id=MAIN_POST_CHANNEL, message_id=msg.id)
                        print(f"✅ Forwarded message ID {msg.id} to channel {channel_id}")
                        await asyncio.sleep(1)  # Short delay between channels
                    except Exception as e:
                        print(f"❌ Failed to forward message ID {msg.id} to channel {channel_id}: {e}")

                # Delay before processing the next message
                await db.set_skip_msg_id(msg.id)
                print(f"⏳ Waiting {DELAY_BETWEEN_POSTS} minutes before processing the next post.")
                await asyncio.sleep(DELAY_BETWEEN_POSTS)

        await message.reply(f"✅ All messages from MAIN_POST_CHANNEL have been forwarded in ascending order.\nDeleted messages fetched : {deleted}")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        await message.reply("❌ Failed to process messages.")


async def verify_user(user_id: int):
    return user_id in ADMIN


