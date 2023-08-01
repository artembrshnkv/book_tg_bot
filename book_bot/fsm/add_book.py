from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters.state import StateFilter
from aiogram.filters import Command
from aiogram.fsm import context
from aiogram import Router, types, F

import book_bot.database as db
import book_bot.filters as filters
from book_bot.bot import bot
import book_bot.utils as utils

books_path = r"C:\Users\leoba\PycharmProjects\book_tg_bot\book_bot\books"


router = Router()
router.message.filter(filters.IsAdmin)

PAGE_SIZE = 1100


class FSMAddBook(StatesGroup):
    title = State()
    file = State()


@router.message(Command('add_book'), StateFilter(default_state))
async def fsm_fill_title(message: types.Message,
                         state: context.FSMContext):
    await message.answer("Введите название книги:")
    await state.set_state(FSMAddBook.title)


@router.message(StateFilter(FSMAddBook.title))
async def fsm_send_file(message: types.Message,
                        state: context.FSMContext):
    if db.select_book(title=message.text, already_in_table=True):
        await message.answer('Книга с таким названием уже существует', )
    else:
        await state.update_data(title=message.text)
        await message.answer('Отправьте .txt файл')
        await state.set_state(FSMAddBook.file)


@router.message(StateFilter(FSMAddBook.file), F.document.mime_type == 'text/plain')
async def fsm_end_adding(message: types.Message,
                         state: context.FSMContext):
    data = await state.get_data()
    file_path = books_path + rf"\{data['title']}.txt"
    await bot.download(message.document, destination=file_path)
    db.add_book(title=data['title'])
    utils.get_pages(file=file_path, max_page_size=PAGE_SIZE, book_title=data['title'])
    await state.clear()


@router.message(StateFilter(FSMAddBook.file))
async def warning_fsm_end_adding(message: types.Message):
    await message.answer('Файл должен быть с расширением .txt')


@router.message(StateFilter(FSMAddBook))
async def cancel_book_adding_process(message: types.Message,
                                     state: context.FSMContext):
    await state.clear()
    await message.answer('Добавление книги прервано')
