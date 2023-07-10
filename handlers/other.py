from aiogram import types


async def send_help(message: types.Message):
    await message.answer(
        'Використовуйте команду /start, щоб почати, а потім виберіть опцію на клавіатурі.'
    )
