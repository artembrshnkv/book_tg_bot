from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters.state import StateFilter
from aiogram.filters import Command
from aiogram.fsm import context
from aiogram import Router, types, F

import book_bot.database as db
import book_bot.filters as filters

router = Router()
router.message.filter(filters.IsAdmin)


class FSMAddBook(StatesGroup):
    title = State()
    file = State()


@router.message(Command('add_book'), StateFilter(default_state))
async def fsm_fill_title(message: types.Message,
                         state: context.FSMContext):
    await message.answer('Enter book title')
    await state.set_state(FSMAddBook.title)


@router.message(StateFilter(FSMAddBook.title))
async def fsm_send_file(message: types.Message,
                        state: context.FSMContext):
    await state.update_data(title=message.text)
    await message.answer('Send .txt file ')
    await state.set_state(FSMAddBook.file)


@router.message(StateFilter(FSMAddBook.file), F.document.mime_type == 'text/plain')
async def fsm_end_adding(message: types.Message,
                         state: context.FSMContext):
    await state.update_data(file=message.document.file_id)
    await message.answer('Book added successfully')
    await state.clear()


@router.message(StateFilter(FSMAddBook.file), ~F.document.mime_type == 'text/plain')
async def warning_fsm_end_adding(message: types.Message):
    await message.answer('Отправьте .txt файл')
