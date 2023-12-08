from aiogram.fsm.context import FSMContext

from config import dp
from db.models import Utb
from telegram.common.inline_pagination import Paginator
from telegram.common.keyboards import generate_inline_keyboard


async def get_search_results_keyboard(results, state: FSMContext):
    keyboard = []
    if not results:
        keyboard = [
            [('За вашим запитом нічого не знайдено', 'None')],
            [('Повторити пошук', 'find_data')],
            [('Головне меню', 'main_menu')]
        ]
        keyboard = generate_inline_keyboard(keyboard)
    else:
        for i, res in enumerate(results):
            res: Utb
            keyboard.append(
                [(f'{i + 1}', f'get_data_{res.id}')]
            )
        if len(results) <= 5:
            keyboard.append([('Главное меню', 'main_menu')])
            keyboard = generate_inline_keyboard(keyboard)
        else:
            keyboard = generate_inline_keyboard(keyboard)
            paginator = Paginator(data=keyboard, dp=dp, size=5)
            keyboard = paginator()
        await state.update_data({'utb_data': results})
    return keyboard