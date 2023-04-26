import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3

#получили из наших модулей данные
import keys as kb
from dialog_bot import query
from config import TOKEN

#логируем
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
    await message.reply("Hi!\nThis is an English learning bot!\nThe idea behind is to help you to create the"
                        "real one own Oxford dictionary. It collects <u>you personal definitions</u> for words you learn."
                        "Also you can chat to <b>AI</b> and train you communication skills.", reply_markup = kb.main_keyboard, parse_mode='HTML')


@dp.message_handler(commands=['help'])
async  def process_help_command(message: types.Message):
    await message.reply("How to use the bot?  It is very easy! You can use different commands:\n"
                        "/Main_menu to return to the start\n"
                        "/Pick_me_a_word to get a random word from your vocabluary\n"
                        "/Add_new_word to add more words to your dictionary\n"
                        "/Start_chat to speak to AI\n"
                        "/See_my_progress to see the usage and the size of vocabluary", reply_markup = kb.main_keyboard)


@dp.message_handler(commands = ['Main_menu'])
async def process_help_command(message: types.Message):
    await message.reply("How to use the bot? \n It is very easy! \nChoose Add new word if you want to add definition to"
                        "the bot \nChoose Pick me a word, if you want to read random word", reply_markup = kb.main_keyboard)




@dp.message_handler(commands = ['Add_new_word'])
async  def process_help_command(message: types.Message):
    await message.reply("How to use the bot? \n It is very easy! \nChoose Add new word if you want to add definition to"
                        "the bot \nChoose Pick me a word, if you want to read random word", reply_markup = kb.main_keyboard)


@dp.message_handler(commands = ['Start_chat'])
async  def process_help_command(message: types.Message):
    await message.reply("How to use the bot? \n It is very easy! \nChoose Add new word if you want to add definition to"
                        "the bot \nChoose Pick me a word, if you want to read random word", reply_markup = kb.main_keyboard)

@dp.message_handler(commands = ['See_my_progress'])
async  def process_help_command(message: types.Message):
    conn = sqlite3.connect('vocabluary.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM words')
    result = cur.fetchone()
    conn.close()
    await message.reply(f'The number of words in the Vocabluary is:<b>{result[0]}<b>', parse_mode='HTML', reply_markup = kb.main_keyboard)

@dp.message_handler(commands=['Pick_me_a_word'])
async def process_help_command(msg: types.Message):
    await msg.reply("Your word is !")
    try:
        conn = sqlite3.connect('vocabluary.db')
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM words ORDER BY RANDOM() LIMIT 1')
        conn.close()
    except Exception as e:
        print(e)
# Конец Раздел с командами

# Состояние добавления слова в словарь

@dp.message_handler(text="Add_new_word")
async def process_new_word_command(msg: types.Message, state: FSMContext):
    await msg.reply("Wow! Another new word! Please type the word!", reply_markup = kb.new_word_keyboard)
    await state.set_state(FSMAdmin.Add_new_word)

@dp.message_handler(state=FSMAdmin.Add_new_word)
async def process_new_word_definition_command(msg: types.Message, state: FSMContext):
    await msg.reply("Cool! We got it!", reply_markup=kb.new_word_keyboard)
    await state.update_data(word=msg.text)
    """try:
        conn = sqlite3.connect('vocabluary.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO words(user_id, word) VALUES("{msg.from_user.id}", "{msg.text}")')
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)"""
    await msg.reply("Now, please write your definition for this word.")
    await state.set_state(FSMAdmin.Add_new_definition)

@dp.message_handler(state = FSMAdmin.Add_new_definition)
async def process_new_word_definition_command(msg: types.Message, state: FSMContext):
    await msg.reply("Nice! Now we all set", reply_markup = kb.new_word_keyboard)
    await state.update_data(defini=msg.text)
    data = await state.get_data()
    try:
        conn = sqlite3.connect('vocabluary.db')
        cur = conn.cursor()
        cur.execute(f"INSERT INTO words(user_id, word, definition) VALUES('{msg.from_user.id}', '{data['word']}', '{data['defini']}')")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
    await state.finish()
    await msg.answer(f"The word you added is:\n"
                    f"<b>{data['word']}</b>\n"
                    f"def. <i>{data['defini']}</i>", parse_mode='HTML')
# Конец раздела добавления слова в словарь


# Раздел получения случайного слова из словаря
@dp.message_handler(text="Pick_me_a_word")
async def process_help_command(msg: types.Message):
    await msg.reply("One of the words from you dictionary!")
    try:
        conn = sqlite3.connect('vocabluary.db')
        cur = conn.cursor()
        word_from_dict = cur.execute(f'SELECT * FROM words ORDER BY RANDOM() LIMIT 1').fetchall()
        conn.close()
    except Exception as e:
        print(e)
    word_from_dict = str(word_from_dict).split(',')
    await bot.send_message(msg.from_user.id, text=f'<b>{word_from_dict[1]}</b>\n'
                    f'def. - <i>{word_from_dict[2]}</i>', parse_mode='HTML', reply_markup=kb.main_keyboard )

# Конец раздела получения случайного слова из словаря



# Раздел общения с чат ботом. Он перехватывает все сообщения, которые не отмечены командами.

@dp.message_handler()
async def chat_with_bot(msg: types.Message):
    await bot.send_message(msg.from_user.id, query({"inputs": {"text": msg.text},})['generated_text'], reply_markup=kb.chat_keyboard)


# Конец раздела общения с чат ботом. Он перехватывает все сообщения, которые не отмечены командами.



if __name__=='__main__':
    executor.start_polling(dp)