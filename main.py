import logging
import json
import time
import random

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions, Message, FSInputFile
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os

import config
from huggingFaceApi import ChatBot
from temp_html import create_temp_html_file

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

bot = Bot(token=config.API_KEY)
dp = Dispatcher()

chats = {}

async def getApiFromJson(user_id):
    user_id = str(user_id)
    with open('api_keys.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  
    if user_id in data:
        return data[user_id]
    else:
        return None
    
async def addApiKey(token, user_id):
    user_id = str(user_id)
    with open('api_keys.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  
    if user_id in data:
        del(data[user_id])
    data[user_id] = token
    with open('api_keys.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

@dp.message(Command('start'))    
async def start(msg: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Get api key", url="https://huggingface.co/settings/tokens"))
    builder.as_markup()
    await msg.reply("Before starting, you need to add the bot token using the command /add_token <token>. You can obtain the token by clicking the button below.", reply_markup=builder.as_markup())
 

async def proccesResponce(msg: Message):
    user_id = msg.from_user.id
    global chats
    if user_id not in chats:
        token = await getApiFromJson(user_id)
        if token != None:
            chats[user_id] = ChatBot(token)
        else:
            builder = InlineKeyboardBuilder()
            builder.add(InlineKeyboardButton(text="Get api key", url="https://huggingface.co/settings/tokens"))
            builder.as_markup()
            await msg.reply("You haven't added the token from Hugging Face. Please obtain the token by clicking the button below, and then enter /add_token <token> to add it.", reply_markup=builder.as_markup())
            return
    text = await chats[user_id].ask(msg.text)
    print(text)
    # text = text.split("Assistant:")[-1].strip()
    # print(text)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Clear the chat", callback_data=f"clear_dialogue_{str(user_id)}"))
    builder.as_markup()
    try:
        await msg.reply(text=text, reply_markup=builder.as_markup(), parse_mode="MarkDown")
    except Exception as e:
        file = await create_temp_html_file(text)
        print(file)
        document = FSInputFile(file)
        try:
            await bot.send_document(chat_id=user_id, document=document, reply_markup=builder.as_markup(), reply_to_message_id=msg.message_id)
        finally:
            # Удаляем временный файл после отправки
            if os.path.exists(file):
                os.remove(file)
        
        
@dp.message()
async def handleMessage(msg: Message):
    if msg.text.startswith("/add_token "):
        await addApiKey(msg.text[len("/add_token "):], msg.from_user.id)
        await msg.reply("Token added successfully.")
    else:
        await proccesResponce(msg)

@dp.callback_query(F.data.startswith("clear_dialogue_"))
async def clearChat(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split('_')[-1]
    user_who_pressed = callback_query.from_user.id
    if int(user_id) == user_who_pressed:
        if int(user_id) in chats:
            chats[int(user_id)].clear_history()
            await bot.send_message(chat_id=user_id, text="Chat history cleared")
        else:
            await callback_query.answer("So we never talked")
        
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())