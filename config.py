import configparser
import os
import sys

from aiogram import Bot, Dispatcher

is_exit = False
last_id = None
session = None
user: None = None  # Текущий пользователь программы
users = None  # Список всех пользователей из базы
data_for_complete_utb = None  # Данные для автозаполнения
show_mode = 'all'  # Режим отображения
last_qry = None  # Последний запрос
add_car_window = None  # Окно добавления авто
search_window = None  # Окно поиска

is_postgres = os.environ.get('TELEGRAM_BOT_TOKEN', None)

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '6379535978:AAGHlgXh2rWLj91ZWbd-OUEokO6xljX5Zjc')
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# __db_username = os.environ.get('DB_USERNAME', 'stas')
# __dp_password = os.environ.get('DB_PASSWORD', 'stas01')
# __db_name = os.environ.get('DB_NAME', 'uppdb')
# __db_host = os.environ.get('DB_HOST', '101.4.6.68')
# __db_port = os.environ.get('DB_PORT', '5432')


if not is_postgres:
    # abs_config_path = os.path.abspath(os.path.dirname(sys.executable))+'\\config.ini' # путь для компиляции EXE файла
    abs_config_path = os.path.dirname(os.path.abspath(__file__)) + '\\config.ini'
    config = configparser.ConfigParser()
    config.read(abs_config_path)

    sync_db_url = os.environ.get('DATABASE_URL', f"postgresql+psycopg2://{config.get('PG', 'db_url')}")
    async_db_url = os.environ.get('ASYNC_DATABASE_URL', f"postgresql+asyncpg://{config.get('PG', 'db_url')}")
else:
    async_db_url = os.environ.get('ASYNC_DATABASE_URL')
