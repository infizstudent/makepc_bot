from aiogram import types

def create_main_menu_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text='Новий комп\'ютер', callback_data='new_computer'),
        types.InlineKeyboardButton(text='Готові комп\'ютери', callback_data='ready_computers')
    ]
    keyboard.add(*buttons)
    return keyboard

def create_pc_components_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text='Процесор', callback_data='processor'),
        types.InlineKeyboardButton(text='Відеокарта', callback_data='videocard'),
        types.InlineKeyboardButton(text='Оперативна пам\'ять', callback_data='ram'),
        types.InlineKeyboardButton(text='SSD або HDD', callback_data='ssd_hdd'),
        types.InlineKeyboardButton(text='Материнська плата', callback_data='motherboard'),
        types.InlineKeyboardButton(text='Повернутися', callback_data='back')
    ]
    keyboard.add(*buttons)
    return keyboard