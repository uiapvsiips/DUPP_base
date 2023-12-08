import base64
from io import BytesIO

from PIL import Image
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from dateutil import parser

from config import bot
from db.models import Utb, User, Photo
from telegram.common.States import SearchState
from telegram.common.common_methods import get_search_results_keyboard
from telegram.common.crud import get_data_by_column_and_value, get_photos_by_utb_id, get_all_executors
from telegram.common.inline_pagination import Paginator
from telegram.common.keyboards import search_keyboard, generate_inline_keyboard

search_router = Router()


async def answer_to_search(user_id: int, state: FSMContext):
    await bot.send_message(chat_id=user_id, text='Пошук по:', reply_markup=search_keyboard)
    await state.set_state(SearchState.waiting_for_column)

@search_router.message(F.text.in_({'пошук', 'Пошук', '/search'}))
async def process_search_message(message: Message, state: FSMContext):
    await answer_to_search(message.from_user.id, state)


@search_router.callback_query(F.data == 'find_data')
async def search(query: CallbackQuery, state: FSMContext):
    await answer_to_search(query.from_user.id, state)
    await query.answer()


@search_router.callback_query(F.data.contains('search_by_'))
async def process_search(query: CallbackQuery, state: FSMContext):
    column_name = query.data.replace('search_by_', '')
    await state.update_data({'column_name': column_name})
    if column_name == 'executor':
        executors = await get_all_executors()
        executors_keyboard = []
        for i, executor in enumerate(executors):
            executors_keyboard.append([(executor, f'executor_{i}')])
        executors_keyboard = generate_inline_keyboard(executors_keyboard)
        await bot.send_message(chat_id=query.from_user.id, text='Оберіть виконавця:', reply_markup=executors_keyboard)
    else:
        await bot.send_message(chat_id=query.from_user.id, text='Введіть значення:')
    await state.set_state(SearchState.waiting_for_value)


async def get_search_result_by_value(value, state, chat_id):
    data = await state.get_data()
    column_name = data.get('column_name')
    results = await get_data_by_column_and_value(column_name, value)
    keyboard = await get_search_results_keyboard(results, state)
    text = await Paginator.get_current_text(keyboard, state)
    await bot.send_message(chat_id=chat_id, text=text if text else 'Оберіть дію:',
                           reply_markup=keyboard)
    await state.set_state(None)

@search_router.message(SearchState.waiting_for_value)
async def process_value(message: Message, state: FSMContext):
    data = await state.get_data()
    column_name = data.get('column_name')
    value = message.text
    if column_name == 'car_going_date':
        value = parser.parse(timestr=message.text)
    await get_search_result_by_value(value, state, message.from_user.id)

@search_router.callback_query(SearchState.waiting_for_value)
async def process_value(query: CallbackQuery, state: FSMContext):
    value = [g[0].text for g in query.message.reply_markup.inline_keyboard if g[0].callback_data == query.data][0]
    await get_search_result_by_value(value, state, query.from_user.id)


@search_router.callback_query(F.data.startswith('get_data_'))
async def get_utb_card_to_user(query: CallbackQuery, state: FSMContext):
    id = int(query.data.replace('get_data_', ''))
    data = await state.get_data()
    user = data.get('user')
    user: User
    utb_cards = data.get('utb_data')
    card = [card for card in utb_cards if card.id == id][0]
    card: Utb
    text = f'<b>Вх.№:</b> {card.in_number}\n' \
           f'<b>Дата проїзду:</b> {card.car_going_date}\n' \
           f'<b>Місце проїзду:</b> {card.car_going_place}\n' \
           f'<b>Інформація про авто:</b> {card.car_info}\n' \
           f'<b>Інформація про причеп:</b> {card.truck_info}\n' \
           f'<b>ДНЗ:</b> {card.license_plate}\n' \
           f'<b>Примітка:</b> {card.note}\n' \
           f'<b>Виконавець:</b> {card.executor}\n' \
           f'<b>ПІБ Власника/Назва компанії:</b> {card.owner}\n' \
           f'<b>Номер телефону:</b> {card.owner_phone}\n'
    if user.is_admin:
        text += f'<b>Вніс:</b> {card.add_by_user.last_name}\n' \
                f'<b>Дата внесення:</b> {card.dvv}\n' \
                f'<b>Редагував:</b> {card.kr_by_user.last_name}\n' \
                f'<b>Дата редагування:</b> {card.dkr}\n'
    await bot.send_message(chat_id=query.from_user.id, text=text)
    photos = await get_photos_by_utb_id(card.id)
    for photo in photos:
        photo: Photo
        with BytesIO() as buffer:
            image = Image.open(BytesIO(base64.b64decode(photo.photo)))
            image.save(buffer, format="JPEG")
            buffer.seek(0)
            file_to_send = BufferedInputFile(buffer.getvalue(), f"photo_{photo.id}.jpeg")
            await bot.send_photo(chat_id=query.from_user.id, photo=file_to_send)



