from aiogram.dispatcher.filters.state import StatesGroup, State


class AccountState(StatesGroup):
    enter_full_name = State()
    enter_age = State()