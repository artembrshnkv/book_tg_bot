from aiogram import Router, types
from aiogram.filters import Command
import database as db
from lexicon import lexicon

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
        db.add_user(data=data,
                    user_tg_id=message.from_user.id)
