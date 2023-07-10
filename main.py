from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from config import  DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, ADMIN_IDS
from sqlalchemy.orm import declarative_base
from aiogram.utils import executor
from loader import dp
from handlers.client import handle_new_computer, handle_ready_computers, process_processor, process_videocard, process_ram, process_ssd_hdd, process_motherboard, handle_back


from handlers import client, admin, other

dp.register_message_handler(client.send_welcome, commands=['start'])
dp.register_message_handler(other.send_help, commands=['help'])
dp.register_message_handler(admin.add_computer, commands=['add_computer'], is_chat_admin=True)
dp.register_message_handler(admin.handle_docs_photo, content_types=['photo'], is_chat_admin=True)
dp.register_message_handler(admin.handle_description, is_chat_admin=True)
dp.register_callback_query_handler(admin.process_callback_cancel, lambda c: c.data == 'cancel')
dp.register_callback_query_handler(handle_new_computer, lambda c: c.data == 'new_computer')
dp.register_callback_query_handler(handle_ready_computers, lambda c: c.data == 'ready_computers')
dp.register_callback_query_handler(process_processor, lambda c: c.data == 'processor')
dp.register_callback_query_handler(process_videocard, lambda c: c.data == 'videocard')
dp.register_callback_query_handler(process_ram, lambda c: c.data == 'ram')
dp.register_callback_query_handler(process_ssd_hdd, lambda c: c.data == 'ssd_hdd')
dp.register_callback_query_handler(process_motherboard, lambda c: c.data == 'motherboard')
dp.register_callback_query_handler(handle_back, lambda c: c.data == 'back')
dp.register_callback_query_handler(handle_ready_computers, lambda c: c.data == 'ready_computers')

if __name__ == '__main__':
    executor.start_polling(dp)
