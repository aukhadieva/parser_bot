import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
