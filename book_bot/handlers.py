from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm import context
from aiogram import F

import database as db
from lexicon import lexicon
import filters


router = Router()


# @router.message()
# async def get_json(message: types.Message):
#     print(message.json(indent=4, exclude_none=True))


@router.message(Command('start'))
async def start_command_handler(message: types.Message):
    await message.answer(lexicon['/start'])


@router.message(Command('show_books'))
async def show_books(message: types.Message):
    await message.answer(*db.get_books())


