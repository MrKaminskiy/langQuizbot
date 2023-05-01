#bot = Bot(token="5927342752:AAGvYv1LNg2lVNVQPUFTYLjfaxCDM81xkps")
from aiogram import Bot, types
from tabulate import tabulate
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random

TOKEN = 'your_bot_token_here'

bot = Bot(token="5927342752:AAGvYv1LNg2lVNVQPUFTYLjfaxCDM81xkps")
dp = Dispatcher(bot)

user_data = {}

# Create a reply keyboard markup with buttons
markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.row(KeyboardButton("Add new word"), KeyboardButton("Take a quiz"))
markup.row(KeyboardButton("Modify a word"), KeyboardButton("Delete a word"))
markup.row(KeyboardButton("List of all words"))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Welcome! Use the buttons to add new words or take a quiz.", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "Add new word")
async def add_new_word(message: types.Message):
    await message.answer("Please send the new word and its translation, separated by a comma (e.g., 'word,translation').")

    @dp.message_handler(lambda message: ',' in message.text, content_types=types.ContentTypes.TEXT)
    async def process_input(message: types.Message):
        user_id = str(message.from_user.id)
        word, translation = message.text.split(',')
        print(user_data)

        if user_id not in user_data:
            user_data[user_id] = []

        user_data[user_id].append((word.strip(), translation.strip()))
        await message.reply(f"Added the word '{word.strip()}' with translation '{translation.strip()}'.", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "Take a quiz")
async def quiz(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id not in user_data or len(user_data[user_id]) == 0:
        await message.reply("You need to add at least one word before taking the quiz.")
        return

    words = user_data[user_id]
    random.shuffle(words)
    correct_answers = 0

    for word, translation in words[:30]:
        await message.answer(f"What is the translation of '{word}'?")
        answer = await bot.wait_for('message', check=lambda message: message.from_user.id == message.from_user.id)
        if answer.text.strip().lower() == translation.lower():
            correct_answers += 1
            await message.reply("Correct!")
        else:
            await message.reply(f"Wrong! The correct translation of '{word}' is '{translation}.")

    await message.reply(f"You answered {correct_answers} out of {len(words[:30])} questions correctly!", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "Modify a word")
async def modify_word(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id not in user_data or len(user_data[user_id]) == 0:
        await message.reply("You have no words to modify.")
        return

    await message.reply("Please send the word you want to modify and its new translation, separated by a comma (e.g., 'word,new_translation').")

    @dp.message_handler(lambda message: ',' in message.text, content_types=types.ContentTypes.TEXT)
    async def process_modify_input(message: types.Message):
        word, new_translation = message.text.split(',')
        word, new_translation = word.strip(), new_translation.strip()

        for idx, (w, _) in enumerate(user_data[user_id]):
            if w == word:
                user_data[user_id][idx] = (word, new_translation)
                await message.reply(f"Modified the word '{word}' with the new translation '{new_translation}'.", reply_markup=markup)
                return

        await message.reply(f"The word '{word}' was not found in your list.", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "Delete a word")
async def delete_word(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id not in user_data or len(user_data[user_id]) == 0:
        await message.reply("You have no words to delete.")
        return

    await message.reply("Please send the word you want to delete.")

    @dp.message_handler(content_types=types.ContentTypes.TEXT)
    async def process_delete_input(message: types.Message):
        word_to_delete = message.text.strip()

        for idx, (word, _) in enumerate(user_data[user_id]):
            if word == word_to_delete:
                del user_data[user_id][idx]
                await message.reply(f"Deleted the word '{word_to_delete}'.", reply_markup=markup)
                return

        await message.reply(f"The word '{word_to_delete}' was not found in your list.", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "List of all words")
async def show_all_words(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(user_data)
    if user_id not in user_data:
        await message.answer("You haven't added any words yet.")
        return

    table = "Word\tTranslation\n"
    for idx, (word, translation) in enumerate(user_data[user_id]):
        table += f"{word}\t{translation}\n"

    await message.answer(f"<pre>{table}</pre>", parse_mode=types.ParseMode.HTML)

if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)

