from aiogram import Router, types
from aiogram.filters import Command

from lexicon import lexicon

router = Router()


@router.message(Command('start'))
async def start_command_handler(message: types.Message):
    await message.answer(lexicon['/start'])
