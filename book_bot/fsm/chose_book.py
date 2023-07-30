from aiogram.fsm.state import State, default_state
from aiogram.filters import StateFilter, Command, Text
from aiogram.fsm import context
from aiogram import Router, types
from aiogram import F
from aiogram.types import CallbackQuery

import book_bot.database as db
import book_bot.keyboards as kb

router = Router()

book_id = State()


@router.message(Command('chose_book'), StateFilter(default_state))
async def chose_book(message: types.Message,
                     state: context.FSMContext):
    await message.answer('Введите id книги:')
    await state.set_state(book_id)
    await message.answer(*db.get_books())


@router.message(StateFilter(book_id), F.text.isdigit())
async def show_book(message: types.Message,
                    state: context.FSMContext):
    actual_page_number = db.chose_books_page(user_tg_id=message.from_user.id, book_id=message.text)
    await message.answer(db.get_actual_page_content(book_id=message.text,
                                                    page_number=actual_page_number),
                         reply_markup=kb.create_keyboard(book_id=message.text,
                                                         page_number=actual_page_number))
    await state.clear()


@router.callback_query(kb.PageCallbackFactory.filter())
async def set_next_page(callback: CallbackQuery,
                        callback_data: kb.PageCallbackFactory):
    asked_page = callback_data.pack().split(':')[-1]
    asked_book_id = callback_data.pack().split(':')[-2]
    await callback.message.answer(db.get_actual_page_content(book_id=asked_book_id,
                                                             page_number=asked_page),
                                  reply_markup=kb.create_keyboard(book_id=int(asked_book_id),
                                                                  page_number=int(asked_page)))
    await callback.answer()
    # callback.message.reply_markup.inline_keyboard.clear()


