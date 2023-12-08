from itertools import islice
from typing import Iterable, Any, Iterator

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Utb
from telegram.common.ttext import Text


class Paginator:
    def __init__(
            self,
            data,
            state: State = None,
            callback_startswith: str = 'page_',
            size: int = 8,
            page_separator: str = '/',
            dp=None,
    ):
        """
        Example: paginator = Paginator(data=kb, size=5)

        :param data: An iterable object that stores an InlineKeyboardButton.
        :param callback_startswith: What should callback_data begin with in handler pagination. Default = 'page_'.
        :param size: Number of lines per page. Default = 8.
        :param state: Current state.
        :param page_separator: Separator for page numbers. Default = '/'.
        """
        self.dp = dp
        self.page_separator = page_separator
        self._state = state
        self._size = size
        self._startswith = callback_startswith
        if isinstance(data, types.InlineKeyboardMarkup):
            self._list_kb = list(
                self._chunk(
                    it=data.inline_keyboard,
                    size=self._size
                )
            )
        elif isinstance(data, Iterable):
            self._list_kb = list(
                self._chunk(
                    it=data,
                    size=self._size
                )
            )
        elif isinstance(data, InlineKeyboardBuilder):
            self._list_kb = list(
                self._chunk(
                    it=data.export(),
                    size=self._size
                )
            )
        else:
            raise ValueError(f'{data} is not valid data')

    """
    Class for pagination's in aiogram inline keyboards
    """

    def __call__(
            self,
            current_page=0,
            *args,
            **kwargs
    ) -> types.InlineKeyboardMarkup:
        """
        Example:

        await message.answer(
            text='Some menu',
            reply_markup=paginator()
        )

        :return: InlineKeyboardMarkup
        """
        _list_current_page = self._list_kb[current_page]

        paginations = self._get_paginator(
            counts=len(self._list_kb),
            page=current_page,
            page_separator=self.page_separator,
            startswith=self._startswith
        )
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[*_list_current_page, paginations])

        # keyboard.add(_list_current_page)
        # keyboard.row(paginations)
        # keyboard.adjust(3)

        main_menu_button = types.InlineKeyboardButton(
            text="Главное меню",
            callback_data="main_menu"  # Здесь укажите нужный вам callback_data
        )
        keyboard.inline_keyboard.append([main_menu_button])

        if self.dp:
            self.paginator_handler()

        return keyboard

    @staticmethod
    def _get_page(call: types.CallbackQuery) -> int:
        """
        :param call: CallbackQuery in paginator handler.
        :return: Current page.
        """
        return int(call.data[-1])

    @staticmethod
    def _chunk(it, size) -> Iterator[Iterator[Any]]:
        """
        :param it: Source iterable object.
        :param size: Chunk size.
        :return: Iterator chunks pages.
        """
        it = iter(it)
        return iter(lambda: tuple(islice(it, size)), ())

    @staticmethod
    def _get_paginator(
            counts: int,
            page: int,
            page_separator: str = '/',
            startswith: str = 'page_'
    ):
        """
        :param counts: Counts total buttons.
        :param page: Current page.
        :param page_separator: Separator for page numbers. Default = '/'.
        :return: Page control line buttons.
        """
        counts -= 1

        paginations = []

        if page > 0:
            paginations.append(
                types.InlineKeyboardButton(
                    text='⏮️️',
                    callback_data=f'{startswith}0'
                )
            )
            paginations.append(
                types.InlineKeyboardButton(
                    text='⬅️',
                    callback_data=f'{startswith}{page - 1}'
                ),
            )
        paginations.append(
            types.InlineKeyboardButton(
                text=f'{page + 1}{page_separator}{counts + 1}',
                callback_data='pass'
            ),
        )
        if counts > page:
            paginations.append(
                types.InlineKeyboardButton(
                    text='➡️',
                    callback_data=f'{startswith}{page + 1}'
                )
            )
            paginations.append(
                types.InlineKeyboardButton(
                    text='⏭️',
                    callback_data=f'{startswith}{counts}'
                )
            )
        return paginations

    @staticmethod
    async def get_current_text(kb: InlineKeyboardBuilder, state: FSMContext):
        if isinstance(kb, InlineKeyboardMarkup):
            kb = kb.inline_keyboard
        data = await state.get_data()
        if data.get('utb_data'):
            column_name = data.get('column_name')
            this_utb_cards = [utb_card for utb_card in data['utb_data'] if
                              utb_card.id in [int(k[0].callback_data.replace('get_data_', '')) for k in kb if
                                              k[0].callback_data.replace('get_data_', '').isdigit()]]
            nums = [k[0].text for k in kb]
            total_text = ''
            for i, card in enumerate(this_utb_cards):
                card: Utb
                text_set = {
                    'licence_plate': card.license_plate,
                    'note': card.note,
                    'owner': card.owner,
                    'owner_phone': card.owner_phone
                }
                text_set[f'{column_name}'] = card.__getattribute__(column_name)
                total_text += f'{nums[i]}. {text_set.get("licence_plate")}\n{text_set.get("note")}\n' \
                              f'{text_set.get("owner")}\n<b>{text_set.get("owner_phone")}</b>\n\n'
            return total_text

    def paginator_handler(self):
        """
        Example:

        args, kwargs = paginator.paginator_handler()

        dp.register_callback_query_handler(*args, **kwargs)

        :return: Data for register handler pagination.
        """

        async def _page(call: types.CallbackQuery, state: FSMContext):
            page = self._get_page(call)
            text = await self.get_current_text(self._list_kb[page], state)
            if text:
                await call.message.edit_text(text=text, reply_markup=self.__call__(
                    current_page=page
                ))
            else:
                await call.message.edit_reply_markup(
                    reply_markup=self.__call__(
                        current_page=page
                    )
                )

            await state.update_data({f'last_page_{self._startswith}': page})

        if not self.dp:
            return \
                (_page, Text(startswith=self._startswith))
        else:
            self.dp.callback_query.handlers.clear()
            self.dp.callback_query.register(
                _page,
                Text(startswith=self._startswith),
            )
            d = 1
