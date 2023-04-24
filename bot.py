import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3


import keys as kb
#from utils import States

from dialog_bot import query

from config import TOKEN

logging.basicConfig(format=u'%(filename)+13s [LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage = MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


# Состояние добавления слова в словарь
class FSMAdmin(StatesGroup):
    Add_new_word=State()
    Add_new_definition=State()




# Раздел с командами

@dp.message_handler(commands = ['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hi! \n This is an English learning bot! \n The idea behind is to help you to create the "
                        "real one own Oxford dictionatry. It contains you personal definitions for words you learn. "
                        "Also you can chat to AI and train you communication skills.", reply_markup = kb.main_keyboard)


@dp.message_handler(commands = ['help'])
async  def process_help_command(message: types.Message):
    await message.reply("How to use the bot?  It is very easy! You can use different commands:\n"
                        "/Main_menu to return to the start\n"
                        "/Pick_me_word to repeat the words you added to vocabluary\n"
                        "/Add_new_word to add more words you want to keep\n"
                        "/Chat to speak to AI\n"
                        "/Stats to see the usage and the size of vocabluary", reply_markup = kb.main_keyboard)


@dp.message_handler(commands = ['Main_menu'])
async  def process_help_command(message: types.Message):
    await message.reply("How to use the bot? \n It is very easy! \nChoose Add new word if you want to add definition to"
                        "the bot \nChoose Pick me a word, if you want to read random word", reply_markup = kb.main_keyboard)




@dp.message_handler(commands = ['Add new word'])
async  def process_help_command(message: types.Message):
    await message.reply("How to use the bot? \n It is very easy! \nChoose Add new word if you want to add definition to"
                        "the bot \nChoose Pick me a word, if you want to read random word", reply_markup = kb.main_keyboard)


@dp.message_handler(commands = ['Chat'])
async  def process_help_command(message: types.Message):
    await message.reply("How to use the bot? \n It is very easy! \nChoose Add new word if you want to add definition to"
                        "the bot \nChoose Pick me a word, if you want to read random word", reply_markup = kb.main_keyboard)

@dp.message_handler(commands = ['My_stats'])
async  def process_help_command(message: types.Message):
    conn = sqlite3.connect('vocabluary.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM words')
    result = cur.fetchone()
    await message.reply(f'The number of words in the Vocabluary is:{result[0]}', reply_markup = kb.main_keyboard)

# Конец Раздел с командами




# Состояние добавления слова в словарь

@dp.message_handler(text="Add new word")
async def process_new_word_command(msg: types.Message, state: FSMContext):
    await msg.reply("Wow! Another new word! Please type the word!", reply_markup = kb.new_word_keyboard)
    await state.set_state(FSMAdmin.Add_new_word)

@dp.message_handler(state=FSMAdmin.Add_new_word)
async def process_new_word_definition_command(msg: types.Message, state: FSMContext):
    await msg.reply("Cool! We got it!", reply_markup=kb.new_word_keyboard)
    try:
        conn = sqlite3.connect('vocabluary.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO words(user_id, word) VALUES("{msg.from_user.id}", "{msg.text}")')
        conn.commit()
    except Exception as e:
        print(e)
    await msg.reply("Now, please write your definition for this word.")
    await state.set_state(FSMAdmin.Add_new_definition)

@dp.message_handler(state=FSMAdmin.Add_new_definition)
async def process_new_word_definition_command(msg: types.Message):
    await msg.reply("Nice! Now we all set", reply_markup = kb.new_word_keyboard)
    try:
        conn = sqlite3.connect('vocabluary.db')
        cur = conn.cursor()
        cur.execute(f'UPDATE words SET definition = {msg.text} WHERE {msg.from_user.id})')
        conn.commit()
    except Exception as e:
        print(e)
    #await msg.reply("The word you added is", f'SELECT * from words WHERE {msg.text}')
    await state.finish()

# Конец раздела добавления слова в словарь

# Раздел получения случайного слова из словаря
@dp.message_handler(commands = ['Pick_me_word'])
async def process_help_command(message: types.Message):
    try:
        conn = sqlite3.connect('vocabluary.db')
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM words ORDER BY RANDOM() LIMIT 1')
        conn.commit()
    except Exception as e:
        print(e)
# Конец раздела получения случайного слова из словаря






@dp.message_handler(text="Main menu")
async def process_main_menu_command(msg: types.Message):
    await msg.reply("This is main menu. What would you like to do?", reply_markup = kb.main_keyboard)






@dp.message_handler()
async def chat_with_bot(msg: types.Message):
    await bot.send_message(msg.from_user.id, query({"inputs": {"text": msg.text},})['generated_text'], reply_markup=kb.chat_keyboard)



if __name__=='__main__':
    executor.start_polling(dp)