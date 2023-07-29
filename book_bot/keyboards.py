from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

import lexicon


class PageCallbackFactory(CallbackData, prefix='page'):
    book_id: int
    page_number: int


pagination_kb = InlineKeyboardBuilder()


def create_pagination_kb(book_id, page_number):
    pagination_kb.export().clear()
    pagination_kb.row(InlineKeyboardButton(text='Назад', callback_data='backward'),
                      InlineKeyboardButton(text=f'{page_number}/{1000}', callback_data=f'{page_number}'),
                      InlineKeyboardButton(text='Вперед',
                                           callback_data=PageCallbackFactory(book_id=book_id,
                                                                             page_number=page_number+1).pack())
                      )
    return pagination_kb.as_markup()


