import re
from handlers import other
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from config import TOKEN, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, ADMIN_IDS
from sqlalchemy.orm import declarative_base

from handlers.other import show_main_menu

Base = declarative_base()


class Computer(Base):
    __tablename__ = 'computers'

    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    description = Column(String)


engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# Налаштування бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(other.send_welcome, commands=['start'])
dp.register_message_handler(other.send_help, commands=['help'])








class FSMContext:
    def __init__(self):
        self.image = None
        self.description = None
        self.can_add_computer = True
        self.expecting_description = False

    def reset(self):
        self.image = None
        self.description = None
        self.can_add_computer = True
        self.expecting_description = False


fsm = FSMContext()

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
async def show_pc_components(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        'Процесор', 'Відеокарта', 'Оперативна пам\'ять', 'SSD або HDD', 'Материнська плата', 'Повернутися'
    ]
    keyboard.add(*buttons)
    await bot.send_message(chat_id=message.chat.id, text='Виберіть компонент:', reply_markup=keyboard)

def create_confirm_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton('Підтвердити', callback_data='confirm'),
               types.InlineKeyboardButton('Скасувати', callback_data='cancel')]
    keyboard.add(*buttons)
    return keyboard


@dp.callback_query_handler(lambda c: c.data == 'confirm')
async def process_callback_confirm(callback_query: types.CallbackQuery):
    if fsm.image is None:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Помилка: Зображення не отримано")
    else:
        session = Session()
        computer = Computer(image_url=fsm.image.file_id, description=fsm.description)
        session.add(computer)
        session.commit()
        fsm.reset()  # Сбрасываем состояние после успешного добавления компьютера
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Комп'ютер успішно додано",
                               reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['add_computer'])
async def add_computer(message: types.Message):
    if fsm.can_add_computer:
        await bot.send_message(message.chat.id, "Будь ласка, відправте зображення")
    else:
        await bot.send_message(message.chat.id,
                               "Ви вже додали комп'ютер. Для додавання нового, використайте команду /add_computer ще раз")


@dp.callback_query_handler(lambda c: c.data == 'cancel')
async def process_callback_cancel(callback_query: types.CallbackQuery):
    fsm.reset()
    # fsm.can_add_computer = True  # Удалено
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Додавання комп'ютера скасовано",
                           reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(content_types=['photo'], is_chat_admin=True)
async def handle_docs_photo(message: types.Message):
    fsm.image = message.photo[-1]  # get the highest quality image
    fsm.expecting_description = True  # устанавливаем ожидание описания
    await bot.send_message(message.chat.id, "Будь ласка, введіть опис")


@dp.message_handler(is_chat_admin=True)
async def handle_description(message: types.Message):
    if fsm.expecting_description:
        description = re.sub(r'/', '', message.text)
        fsm.description = description
        fsm.expecting_description = False
        await bot.send_message(message.chat.id, "Ви впевнені, що хочете додати цей комп'ютер?",
                               reply_markup=create_confirm_keyboard())


if __name__ == '__main__':
    executor.start_polling(dp)
