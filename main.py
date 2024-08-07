import logging

import pandas as pd
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from database import save_to_database
from utils import xlsx_path


# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает команду /start и инициирует взаимодействие с пользователем.
    :param update: Объект обновления, содержащий информацию о полученном сообщении.
    :param context: Контекст, содержащий информацию о состоянии бота и данные пользователя.
    :return:
    """
    button = KeyboardButton('Загрузить файл')
    keyboard = [[button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Привет! Прикрепи файл Excel с данными.', reply_markup=reply_markup)


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает загруженный документ от пользователя,
    сохраняет его на диске и считывает содержимое файла Excel.
    Если файл успешно прочитан, выводит его содержимое и сохраняет данные в базу данных.

    :param update: Объект обновления, содержащий информацию о полученном сообщении.
    :param context: Контекст, содержащий информацию о состоянии бота и данные пользователя.
    :return:
    """
    file = await update.message.document.get_file()

    await file.download_to_drive(xlsx_path)

    try:
        dataframe = pd.read_excel(xlsx_path)
    except Exception as error:
        await update.message.reply_text(f'Ошибка при чтении файла: {error}')
        return

    if dataframe.empty:
        await update.message.reply_text('Загруженный файл пуст.')
        return

    await update.message.reply_text('Файл успешно загружен.')

    save_to_database(dataframe)
