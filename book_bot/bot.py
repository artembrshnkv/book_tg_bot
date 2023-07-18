import asyncio

from aiogram import Bot, Dispatcher

import config as cfg
import handlers

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(handlers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

