import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove

import config as cfg

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_command_handler(message: types.Message):
    await message.answer('Добро пожаловать в бот!')


@dp.message(Command('delmenu'))
async def del_main_menu(message: types.Message):
    await bot.delete_my_commands()
    await message.answer(text='Меню успешно удалено')


@dp.message(Command('delreplykb'))
async def del_reply_keyboard(message: types.Message):
    await message.answer(text='Клавиатура успешно удалена', reply_markup=ReplyKeyboardRemove())



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

