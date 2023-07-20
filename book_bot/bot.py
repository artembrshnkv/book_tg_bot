import asyncio

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

import config as cfg
import handlers

storage = MemoryStorage()

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(storage=storage)


async def main():
    dp.include_routers(handlers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

