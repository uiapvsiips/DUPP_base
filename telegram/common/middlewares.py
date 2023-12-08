from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import bot
from telegram.common.States import RegistrationState
from telegram.common.crud import get_user_by_tg_id
from db.models import User


class ChekUserReg(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        tg_user = event.from_user
        user: User = await get_user_by_tg_id(tg_user)
        if not user and data['raw_state'] != 'RegistrationState:waiting_for_code':
            await bot.send_message(chat_id=tg_user.id, text='Надішліть код активації')
            await data['state'].set_state(RegistrationState.waiting_for_code)
            return
        state: FSMContext = data['state']
        await state.update_data({'user': user})
        # await check_and_delete_message(state, event.from_user.id)
        return await handler(event, data)
