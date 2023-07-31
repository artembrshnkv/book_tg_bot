from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm import context
from aiogram import F

import database as db
from lexicon import lexicon
import filters
import keyboards as kb


router = Router()


# @router.message()
# async def get_json(message: types.Message):
#     print(message.json(indent=4, exclude_none=True))


@router.message(Command('start'))
async def start_command_handler(message: types.Message):
    await message.answer(lexicon['/start'])
    if not db.user_is_registered(user_tg_id=message.from_user.id):
        data = {'first_name': message.from_user.first_name,
                'second_name': message.from_user.last_name,
                'wish_news': 'false',
                }
        db.add_user(data=data, user_tg_id=message.from_user.id)


@router.message(Command('show_books'))
async def show_books(message: types.Message):
    await message.answer(*db.get_books())


@router.message(Command('read'))
async def read(message: types.Message):
    await message.answer(db.get_actual_page_content(book_id=db.select_book(title='Над пропастью во ржи',
                                                                           get_book_id_by_title=True),
                                                    page_number=1))

