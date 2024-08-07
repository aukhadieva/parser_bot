import logging
import os

import pandas as pd
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters

from database import save_to_database, setup_database
from services import calculate_avg_price
from utils import xlsx_path

load_dotenv()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """

    :param update: Объект обновления, содержащий информацию о полученном сообщении.
    :param context: Контекст, содержащий дополнительные данные и методы для обработки обновления.
    :return:
    """
    button = KeyboardButton('Загрузить файл')
    keyboard = [[button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Привет! Прикрепи файл Excel с данными.', reply_markup=reply_markup)


async def handle_average_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает команду /average_price и выводит результат пользователю.

    :param update: Объект обновления, содержащий информацию о полученном сообщении.
    :param context: Контекст, содержащий дополнительные данные и методы для обработки обновления.
    :return:
    """
    avg_price_data = calculate_avg_price()
    for site, avg_price in avg_price_data.items():
        await update.message.reply_text(f'Средняя цена на сайте {site}: {avg_price} рублей')


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает загруженный документ от пользователя,
    сохраняет его и считывает содержимое файла Excel.
    Если файл успешно прочитан, сохраняет данные в базу данных.

    :param update: Объект обновления, содержащий информацию о полученном сообщении.
    :param context: Контекст, содержащий дополнительные данные и методы для обработки обновления.
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

    await handle_average_price(update, context)


def main() -> None:
    """
    Запускает бота.
    :return:
    """
    logging.info('Бот запущен')

    setup_database()

    app = ApplicationBuilder().token(os.getenv('TG_TOKEN')).build()
    app.add_handler(CommandHandler('start', handle_start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(CommandHandler('average_price', handle_average_price))

    app.run_polling()


if __name__ == '__main__':
    main()
