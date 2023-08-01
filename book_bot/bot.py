import asyncio

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

import config as cfg
import handlers
from fsm import registartion, add_book, chose_book
import utils

storage = MemoryStorage()

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(storage=storage)


async def main():
    await bot.set_my_commands(commands=utils.menu)
    dp.include_routers(handlers.router, add_book.router, chose_book.router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())

