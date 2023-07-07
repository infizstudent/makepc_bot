from aiogram import types
from handlers.other import show_main_menu
from main import bot, fsm, Session, Computer, dp


async def show_pc_components(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        'Процесор', 'Відеокарта', 'Оперативна пам\'ять', 'SSD або HDD', 'Материнська плата', 'Повернутися'
    ]
    keyboard.add(*buttons)
    await bot.send_message(chat_id=message.chat.id, text='Виберіть компонент:', reply_markup=keyboard)

@dp.message_handler()
async def handle_message(message: types.Message):
    if message.text == 'Новий комп\'ютер':
        await show_pc_components(message)
    elif message.text == 'Готові комп\'ютери':
        session = Session()
        computers = session.query(Computer).all()
        if computers:
            for computer in computers:
                await bot.send_photo(
                    chat_id=message.chat.id, photo=computer.image_url, caption=f"Опис: {computer.description}"
                )
        else:
            await bot.send_message(chat_id=message.chat.id, text='Наразі немає готових комп\'ютерів.')
    elif message.text == 'Повернутися':
        await show_main_menu(message)
    else:
        await message.answer('Я не розумію вашу команду. Використовуйте /help для отримання довідки.')
