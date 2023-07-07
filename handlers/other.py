from aiogram import types, Dispatcher

async def show_main_menu(message: types.Message, is_edit=False):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Новий комп\'ютер', 'Готові комп\'ютери']
    keyboard.add(*buttons)

    if is_edit:
        await dp.bot.edit_message_text(
            'Виберіть опцію:', chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard
        )
    else:
        await message.answer('Виберіть опцію:', reply_markup=keyboard)

async def send_welcome(message: types.Message):
    await show_main_menu(message)

async def send_help(message: types.Message):
    await message.answer(
        'Використовуйте команду /start, щоб почати, а потім виберіть опцію на клавіатурі.'
    )
