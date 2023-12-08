from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import bot
from db.models import User
from telegram.common.States import ChangePasswordState
from telegram.common.crud import update_any_obj
from telegram.common.keyboards import main_keyboard

change_pwd_router = Router()

@change_pwd_router.callback_query(F.data == 'change_password')
async def change_password(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text('Введіть новий пароль:')
    await state.set_state(ChangePasswordState.waiting_for_password)

@change_pwd_router.message(ChangePasswordState.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    data = await state.get_data()
    user: User = data.get('user')
    user.password = message.text
    await update_any_obj(user)
    await state.clear()
    await message.answer('Пароль успішно змінено!')
    await bot.send_message(chat_id=user.tgid, text='Оберіть дію:', reply_markup=main_keyboard)
