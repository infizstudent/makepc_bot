from aiogram import types
from keyboards import create_main_menu_keyboard, create_confirm_keyboard

class MessageHandler:
    def __init__(self, dp, fsm, Session, bot):
        self.dp = dp
        self.fsm = fsm
        self.Session = Session
        self.bot = bot

    def setup(self):
        self.dp.message_handler(commands=['start'])(self.send_welcome)
        self.dp.message_handler()(self.handle_message)

    async def send_welcome(self, message: types.Message):
        await self.show_main_menu(message, is_edit=False)

    async def show_main_menu(self, message: types.Message, is_edit=False):
        keyboard = create_main_menu_keyboard()
        # ... ваш код продолжается ...

    async def handle_message(self, message: types.Message):
        # ... ваш код продолжается ...
