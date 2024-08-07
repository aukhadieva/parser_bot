import sqlite3

from utils import db_path


def setup_database() -> None:
    """
    Инициализирует базу данных SQLite и создает таблицу 'products', если она не существует.
    :return:
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (title TEXT, url TEXT, xpath TEXT)''')
    conn.commit()
    conn.close()
