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


@router.message(Command('all_books'))
async def get_all_books(message: types.Message):
    await message.answer('Список всех книг:')
    all_books_list = [f'{key+1}. (id={value[0]}) {value[1]}' for key, value in enumerate(db.get_books())]
    await message.answer('\n'.join(all_books_list))


@router.message(Command('chose_book'), StateFilter(default_state))
async def chose_book(message: types.Message):
    await message.answer(text='Выберите номер книги:',
                         reply_markup=kb.create_all_books_kb(user_tg_id=message.from_user.id))

# @router.message(StateFilter(book_id), F.text.isdigit())
# async def show_book(message: types.Message,
#                     state: context.FSMContext):
#     actual_page_number = db.chose_books_page(user_tg_id=message.from_user.id, book_id=message.text)
#     await message.answer(db.get_actual_page_content(book_id=message.text,
#                                                     page_number=actual_page_number),
#                          reply_markup=kb.create_pagination_kb(book_id=message.text,
#                                                               page_number=actual_page_number))
#     await state.clear()


@router.callback_query(kb.PageCallbackFactory.filter())
async def set_next_page(callback: CallbackQuery,
                        callback_data: kb.PageCallbackFactory):
    asked_page_number = callback_data.pack().split(':')[-1]
    asked_book_id = callback_data.pack().split(':')[-2]
    db.update_actual_page_number(user_tg_id=callback.from_user.id,
                                 book_id=asked_book_id,
                                 page_number=asked_page_number)
    await callback.message.answer(db.get_actual_page_content(book_id=asked_book_id,
                                                             page_number=asked_page_number),
                                  reply_markup=kb.create_pagination_kb(book_id=int(asked_book_id),
                                                                       page_number=int(asked_page_number)))
    await callback.answer()


@router.callback_query(kb.MenuCallbackFactory.filter())
async def get_book_menu(callback: CallbackQuery,
                        callback_data: kb.MenuCallbackFactory):
    asked_page_number = callback_data.pack().split(':')[-1]
    asked_book_id = callback_data.pack().split(':')[-2]
    await callback.message.answer(text='Выберите страницу:',
                                  reply_markup=kb.create_menu_kb(book_id=int(asked_book_id),
                                                                 page_number=int(asked_page_number),
                                                                 buttons_per_side=96))
    await callback.answer()
