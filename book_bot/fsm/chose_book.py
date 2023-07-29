from aiogram.fsm.state import State, default_state
from aiogram.filters import StateFilter, Command
from aiogram.fsm import context
from aiogram import Router, types

import book_bot.database as db

router = Router()

book_id = State()


@router.message(Command('chose_book'), StateFilter(default_state))
async def chose_book(message: types.Message,
                     state: context.FSMContext):
    await message.answer('Выберите книгу:')
    await state.set_state(book_id)
    await message.answer(*db.get_books())


@router.message(StateFilter(book_id))
async def show_book(message: types.Message):
    ...



