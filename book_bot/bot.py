import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import config as cfg

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_command_handler(message: types.Message):
    await message.answer('Добро пожаловать в бот!')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

