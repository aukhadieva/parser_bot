import sqlite3

import pandas as pd
import requests
from lxml import html

from utils import db_path


def fetch_price(url: str, xpath: str) -> str | None:
    """
    Извлекает цену товара с указанной веб-страницы по-заданному XPath.

    :param url: URL-адрес веб-страницы
    :param xpath: XPath для нахождения элемента на странице, содержащего цену
    :return: Строка с ценой, если элемент найден, иначе None
    """
    response = requests.get(url)
    tree = html.fromstring(response.content)
    price_elements = tree.xpath(xpath)
    if price_elements:
        return price_elements[0].text_content().strip()

    return None


def calculate_avg_price() -> float:
    """
    Вычисляет среднюю цену товаров.

    :return: Средняя цена в рублях
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM products", conn)
    prices = []

    for index, row in df.iterrows():
        price = fetch_price(row['url'], row['xpath'])
        if price:
            price = price.replace(' ', '').replace('₽', '').replace('₴', '')
            prices.append(float(price))

    avg_price = sum(prices) / len(prices) if prices else 0
    conn.close()
    return avg_price
