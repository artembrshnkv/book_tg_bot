from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

import lexicon


class PageCallbackFactory(CallbackData, prefix='page'):
    book_id: int
    page_number: int


pagination_kb = InlineKeyboardBuilder()


def create_pagination_kb(*buttons):
    pagination_kb.row(*[lexicon.lexicon[button] for button in buttons if button in lexicon.lexicon])



