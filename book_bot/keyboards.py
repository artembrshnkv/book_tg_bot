from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

import database as db
import utils


class PageCallbackFactory(CallbackData, prefix='page'):
    book_id: int
    page_number: int


class MenuCallbackFactory(CallbackData, prefix='menu'):
    book_id: int
    page_number: int


def create_pagination_kb(book_id, page_number):
    pagination_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='<<',
                                 callback_data=PageCallbackFactory(book_id=book_id,
                                                                   page_number=utils.get_correct_page_range(
                                                                       book_id=book_id,
                                                                       page_number=page_number - 1)).pack()),
            InlineKeyboardButton(text=f'{page_number}/{db.get_min_max_page_number(book_id=book_id, get_max_page=True)}',
                                 callback_data=MenuCallbackFactory(book_id=book_id,
                                                                   page_number=page_number).pack()),
            InlineKeyboardButton(text='>>',
                                 callback_data=PageCallbackFactory(book_id=book_id,
                                                                   page_number=utils.get_correct_page_range(
                                                                       book_id=book_id,
                                                                       page_number=page_number + 1)).pack())
        ]]
                                    )
    return pagination_keyboard



def create_menu_kb(book_id, page_number, buttons_per_side):
    menu_kb = InlineKeyboardBuilder()
    menu_kb.add(*[InlineKeyboardButton(text=f'{n}',
                                       callback_data=PageCallbackFactory(book_id=book_id,
                                                                         page_number=n).pack()) for n in utils.get_menu(
        book_id=book_id,
        page_number=page_number,
        buttons_per_side=buttons_per_side)])
    return menu_kb.as_markup()


def create_all_books_kb(user_tg_id):
    books_kb = InlineKeyboardBuilder()
    books_kb.add(*[InlineKeyboardButton(text=f'{key+1}',
                                        callback_data=PageCallbackFactory(
                                            book_id=value[0],
                                            page_number=db.chose_books_page(
                                                book_id=value[0],
                                                user_tg_id=user_tg_id)).pack()) for key, value in enumerate(db.get_books())])

    return books_kb.as_markup()
