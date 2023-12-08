from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineQuery

from db.models import User
from telegram.common.States import RegistrationState, ChangePasswordState
from telegram.common.crud import get_user_by_uuid, update_any_obj
from telegram.common.keyboards import main_keyboard
from telegram.handlers.change_pwd_handler import change_pwd_router
from telegram.handlers.search_handler import search_router

main_router = Router()
main_router.include_router(search_router)
main_router.include_router(change_pwd_router)



@main_router.message(F.text.contains('start'))
async def cmd_start(message: Message, state: FSMContext):
    data = await state.get_data()
    user: User = data.get('user')
    if user:
        await message.answer(f'Оберіть дію:', reply_markup=main_keyboard)
    else:
        await message.answer('Надішліть код активації')
        await state.set_state(RegistrationState.waiting_for_code)


@main_router.message(RegistrationState.waiting_for_code)
async def process_code(message: Message, state: FSMContext):
    user = await get_user_by_uuid(message.text)
    if user:
        await state.update_data({'user': user})
        user.tgid = message.from_user.id
        await update_any_obj(user)
        if user.password=='1111':
            await message.answer(f'Вам необхідно змінити пароль. Введіть новий пароль:')
            await state.set_state(ChangePasswordState.waiting_for_password)
        else:
            await message.answer(f'Привіт, {user.username}', reply_markup=main_keyboard)
    else:
        await message.answer('Невірний код')


@main_router.callback_query(F.data == 'main_menu')
async def process_main_menu_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=main_keyboard)
    await state.clear()
