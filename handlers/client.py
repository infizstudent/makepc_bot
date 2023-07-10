from aiogram import types, Dispatcher
from handlers.admin import Session, Computer
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters
from aiogram import types, Dispatcher
from handlers.admin import Session, Computer
from loader import dp, bot
from kb.client_kb import create_main_menu_keyboard, create_pc_components_keyboard


async def show_pc_components(message: types.Message):
    keyboard = create_pc_components_keyboard()
    await bot.send_message(chat_id=message.chat.id, text='Виберіть компонент:', reply_markup=keyboard)


async def show_main_menu(message: types.Message, is_edit=False):
    keyboard = create_main_menu_keyboard()

    if is_edit:
        await dp.bot.edit_message_text(
            'Виберіть опцію:', chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard
        )
    else:
        await message.answer('Виберіть опцію:', reply_markup=keyboard)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await show_main_menu(message)


# Handle 'Новий комп\'ютер' button press
@dp.message_handler(filters.Text(equals='Новий комп\'ютер'))
async def handle_new_computer(message: types.Message):
    await show_pc_components(message)


@dp.callback_query_handler(lambda c: c.data == 'ready_computers')
async def handle_ready_computers(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    session = Session()
    computers = session.query(Computer).all()

    if computers:
        for computer in computers:
            await bot.send_photo(
                chat_id=callback_query.from_user.id,
                photo=computer.image_url,
                caption=f"Опис: {computer.description}"
            )
    else:
        await bot.send_message(callback_query.from_user.id, text='Наразі немає готових комп\'ютерів.')

# handlers/client.py

@dp.callback_query_handler(lambda c: c.data == 'new_computer')
async def handle_new_computer(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await show_pc_components(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'ready_computers')
async def handle_ready_computers(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # ваш код здесь

@dp.callback_query_handler(lambda c: c.data == 'processor')
async def process_processor(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Вы выбрали 'Процесор'")

@dp.callback_query_handler(lambda c: c.data == 'videocard')
async def process_videocard(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Вы выбрали 'Відеокарта'")

@dp.callback_query_handler(lambda c: c.data == 'ram')
async def process_ram(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Вы выбрали 'Оперативна пам\'ять'")

@dp.callback_query_handler(lambda c: c.data == 'ssd_hdd')
async def process_ssd_hdd(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Вы выбрали 'SSD або HDD'")

@dp.callback_query_handler(lambda c: c.data == 'motherboard')
async def process_motherboard(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Вы выбрали 'Материнська плата'")

@dp.callback_query_handler(lambda c: c.data == 'back')
async def handle_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await show_main_menu(callback_query.message)

@dp.message_handler(filters.Text(equals='Повернутися'))
async def handle_back(message: types.Message):
    await show_main_menu(message)
