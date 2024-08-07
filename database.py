import logging
import sqlite3

import pandas as pd

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


def save_to_database(dataframe: pd.DataFrame) -> None:
    """
    Сохраняет данные из DataFrame в базу данных SQLite.
    :param dataframe: Pandas DataFrame, содержащий данные для сохранения.
    :return:
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for index, row in dataframe.iterrows():
            cursor.execute("INSERT INTO products (title, url, xpath) VALUES (?, ?, ?)",
                           (row['title'], row['url'], row['xpath']))

        conn.commit()

    except sqlite3.Error as error:
        logging.error(f'Ошибка при сохранении в БД: {error}')

    finally:
        if conn:
            conn.close()
