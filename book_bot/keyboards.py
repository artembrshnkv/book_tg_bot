from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

import database as db
import utils


class PageCallbackFactory(CallbackData, prefix='page'):
    book_id: int
    page_number: int


pagination_kb = InlineKeyboardBuilder()



def create_keyboard(book_id, page_number):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='<<',
                                 callback_data=PageCallbackFactory(book_id=book_id,
                                                                   page_number=page_number - 1).pack()),
            InlineKeyboardButton(text=f'{page_number}/{db.get_min_max_page_number(book_id=book_id, get_max_page=True)}',
                                 callback_data=f'{page_number}'),
            InlineKeyboardButton(text='>>',
                                 callback_data=PageCallbackFactory(book_id=book_id,
                                                                   page_number=page_number + 1).pack())
        ]]
                                    )
    return keyboard


def create_pagination_kb(book_id, page_number):
    # pagination_kb.export().clear()
    pagination_kb.row(InlineKeyboardButton(text='Назад', callback_data='backward'),
                      InlineKeyboardButton(text=f'{page_number}/{1000}', callback_data=f'{page_number}'),
                      InlineKeyboardButton(text='Вперед',
                                           callback_data=PageCallbackFactory(book_id=book_id,
                                                                             page_number=page_number + 1).pack())
                      )
    return pagination_kb.as_markup()


create_pagination_kb(book_id=10, page_number=4)

# if __name__ == '__main__':
#     print(pagination_kb.export())
#     # pagination_kb.export()
#     print(pagination_kb.export().clear())
#     print(pagination_kb.row(InlineKeyboardButton(text='text', callback_data='gbdvdc')).as_markup())
#     print(keyboard)
