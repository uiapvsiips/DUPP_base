import os

from commonmethods import get_all_users, get_data_for_auto_complete_utb
from db.models.user import User

user: None | User = None  # Текущий пользователь программы
users: list = get_all_users()  # Список всех пользователей из базы
data_for_complete_utb = get_data_for_auto_complete_utb()  # Данные для автозаполнения
show_mode = 'all'  # Режим отображения
last_qry = None  # Последний запрос
add_car_window = None  # Окно добавления авто
search_window = None  # Окно поиска

__db_username = os.environ.get('DB_USERNAME', 'stas')
__dp_password = os.environ.get('DB_PASSWORD', 'stas01')
__db_name = os.environ.get('DB_NAME', 'dupp')
__db_host = os.environ.get('DB_HOST', 'localhost')
__db_port = os.environ.get('DB_PORT', '5432')

db_url = f"postgresql+psycopg2://{__db_username}:{__dp_password}@{__db_host}:{__db_port}/{__db_name}"
