from aiogram.fsm.state import StatesGroup, State


class RegistrationState(StatesGroup):
    waiting_for_code = State()


class SearchState(StatesGroup):
    waiting_for_column = State()
    waiting_for_value = State()


class ChangePasswordState(StatesGroup):
    waiting_for_password = State()
