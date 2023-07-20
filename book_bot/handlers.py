from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm import context

import database as db
from lexicon import lexicon
import filters


router = Router()


class FSMRegistration(StatesGroup):
    first_name = State()
    last_name = State()
    email = State()
    wish_news = State()


@router.message(Command('start'))
async def start_command_handler(message: types.Message):
    await message.answer(lexicon['/start'])


@router.message(Command('registration'), StateFilter(default_state))
async def fsm_fill_firstname(message: types.Message,
                             state: context.FSMContext):
    await message.answer('Please enter your name:')
    await state.set_state(FSMRegistration.first_name)


@router.message(StateFilter(FSMRegistration.first_name), filters.IsNameOrSurname)
async def fsm_fill_lastname(message: types.Message,
                            state: context.FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer('Please enter your lastname')
    await state.set_state(FSMRegistration.last_name)


@router.message(StateFilter(FSMRegistration.last_name), filters.IsNameOrSurname)
async def fsm_fill_email(message: types.Message,
                         state: context.FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer('Please enter your email')
    await state.set_state(FSMRegistration.email)


@router.message(StateFilter(FSMRegistration.email))
async def fsm_fill_wish_news(message: types.Message,
                             state: context.FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Do you want to get news?')
    await state.set_state(FSMRegistration.wish_news)


@router.message(StateFilter(FSMRegistration.wish_news))
async def fsm_end_registration(message: types.Message,
                               state: context.FSMContext):
    await state.update_data(wish_news=message.text)
    db.add_user(state=await state.get_data(), user_tg_id=message.from_user.id)
    await message.answer('Registration done successfully')
    await state.clear()
