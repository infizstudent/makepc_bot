from aiogram import types, Dispatcher

from create_bot import dp
from main import bot, Session, Computer



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])

