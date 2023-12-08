from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def generate_inline_keyboard(buttons_data):
    """
    Генерирует Inline-клавиатуру на основе переданных данных.

    :param buttons_data: Список кортежей вида (название кнопки, callback_data)
    :return: Объект InlineKeyboardMarkup
    """
    keyboard = []
    for str in buttons_data:
        keyboard_str = []
        for button_label, callback_data in str:
            if 'http' in callback_data:
                button = InlineKeyboardButton(text=button_label, url=callback_data)
            else:
                button = InlineKeyboardButton(text=button_label, callback_data=callback_data)
            keyboard_str.append(button)
        keyboard.append(keyboard_str)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup


main_keyboard = generate_inline_keyboard([
         [('🔍Пошук🔍', 'find_data')],
    [('Змінити пароль','change_password')]
    ])

search_keyboard = generate_inline_keyboard([
    [('Вх.№', 'search_by_in_number')],
    [('Дата та час проїзду', 'search_by_car_going_date')],
    [('Місце проїзду', 'search_by_car_going_place')],
    [('Інформація про автомобіль', 'search_by_car_info')],
    [('Інформація про вантаж', 'search_by_truck_info')],
    [('Номерной знак', 'search_by_license_plate')],
    [('Нотатки', 'search_by_note')],
    [('Виконавець', 'search_by_executor')],
    [('Власник', 'search_by_owner')],
    [('Номер телефону', 'search_by_owner_phone')],
    [('Назад','main_menu')]
])