from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_confirm_keyboard():
    confirm_keyboard = InlineKeyboardMarkup()
    confirm_button = InlineKeyboardButton(text="Confirm", callback_data="confirm")
    cancel_button = InlineKeyboardButton(text="Cancel", callback_data="cancel")
    confirm_keyboard.add(confirm_button, cancel_button)
    return confirm_keyboard


def admin_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton('Добавить информацию о ПК', callback_data='add_computer'),
        InlineKeyboardButton('Удалить информацию о ПК', callback_data='delete_computer')
    )
    return markup

