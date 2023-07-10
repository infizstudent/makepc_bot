from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputMediaPhoto
from config import ADMIN_IDS
from loader import dp, bot
from kb.admin_kb import create_confirm_keyboard, admin_keyboard

from aiogram.dispatcher.filters.state import StatesGroup, State

from models import Computer, Session


class NewComputer(StatesGroup):
    Photo = State()
    Description = State()
    Confirm = State()


confirm_keyboard = create_confirm_keyboard()

# handlers/admin.py

from kb.admin_kb import admin_keyboard

@dp.message_handler(commands=['admin'])
async def handle_admin_command(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMIN_IDS:
        # Пользователь является администратором
        await bot.send_message(user_id, "Привет, администратор! Выберите действие:", reply_markup=admin_keyboard())
    else:
        # Пользователь не является администратором
        await message.answer("Извините, вы не являетесь администратором.")


@dp.message_handler(Command('add_computer'), is_chat_admin=True)
async def add_computer(message: types.Message):
    await message.answer("Please send me the photos of the computer.")
    await NewComputer.Photo.set()


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=NewComputer.Photo)
async def handle_docs_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    if 'computer_id' in data:  # Edit mode
        computer_id = data.get('computer_id')
        session = Session()
        computer = session.query(Computer).filter_by(id=computer_id).first()
        if computer:
            computer.image_url = photo_id
            session.commit()
            await message.answer("Now, send me a new description.")
        else:
            await message.answer("Computer not found.")
            await state.finish()
    else:  # Add mode
        await state.update_data(photo_id=photo_id)
        await message.answer("Now, send me a description of the computer.")
        await NewComputer.Description.set()



@dp.message_handler(state=NewComputer.Description)
async def handle_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    image_url = data.get("photo_id")
    description = message.text
    if 'computer_id' in data:  # Edit mode
        computer_id = data.get('computer_id')
        session = Session()
        computer = session.query(Computer).filter_by(id=computer_id).first()
        if computer:
            computer.description = description
            session.commit()
            session.close()
            await message.answer("Here is what you updated:\n\n"
                                 f"Image: {image_url}\n"
                                 f"Description: {description}\n\n"
                                 "Would you like to update this computer?",
                                 reply_markup=confirm_keyboard)
        else:
            await message.answer("Computer not found.")
            await state.finish()
    else:  # Add mode
        # Create a new computer instance
        new_computer = Computer(image_url=image_url, description=description)
        # Save it into the database
        session = Session()
        session.add(new_computer)
        session.commit()
        session.close()
        await message.answer("Here is what you sent:\n\n"
                             f"Image: {image_url}\n"
                             f"Description: {description}\n\n"
                             "Would you like to add this computer?",
                             reply_markup=confirm_keyboard)
    await NewComputer.Confirm.set()



@dp.callback_query_handler(text_contains='confirm', state=NewComputer.Confirm)
async def process_callback_confirm(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Computer added.')
    await state.finish()


@dp.callback_query_handler(text_contains='cancel', state=NewComputer.Confirm)
async def process_callback_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Operation canceled.')
    await state.finish()


@dp.callback_query_handler(text_contains='add_computer')
async def handle_add_computer(call: CallbackQuery):
    await call.answer()
    await call.message.answer("Пожалуйста, отправьте мне фотографии компьютера.")
    await NewComputer.Photo.set()


from aiogram import types

@dp.callback_query_handler(text='delete_computer')
async def show_computers(call: types.CallbackQuery):
    session = Session()
    computers = session.query(Computer).all()
    if not computers:
        await call.message.edit_text("No computers found.")
        return
    for comp in computers:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(f"Delete", callback_data=f"delete:{comp.id}"))
        await bot.send_photo(chat_id=call.message.chat.id, photo=comp.image_url, caption=comp.description, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('delete:'))
async def delete_computer(call: types.CallbackQuery):
    computer_id = int(call.data.split(':')[1])
    session = Session()
    computer = session.query(Computer).filter_by(id=computer_id).first()
    if computer:
        session.delete(computer)
        session.commit()
        await call.message.answer(f"Computer {computer_id} was deleted.")
    else:
        await call.message.edit_text(f"Computer with ID {computer_id} not found.")


