from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

button_addword = KeyboardButton('Add new word')
button_pick_word = KeyboardButton('Pick me a word')
button_statistic = KeyboardButton('See my progress')
button_chat_bot= KeyboardButton('Start Chat')

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(button_addword, button_pick_word, button_statistic, button_chat_bot)


button_menu = KeyboardButton('Main menu')
button_next_word = KeyboardButton ('Next Word')

chat_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
chat_keyboard.add(button_menu)

new_word_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
new_word_keyboard.add(button_menu, button_next_word)

random_word_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
random_word_keyboard.add(button_menu, button_next_word)