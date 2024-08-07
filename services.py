import sqlite3
from urllib.parse import urlparse

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


def calculate_avg_price() -> dict:
    """
    Вычисляет среднюю цену товаров.

    :return: Средняя цена в рублях
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM products", conn)
    site_prices = {}

    for index, row in df.iterrows():
        price = fetch_price(row['url'], row['xpath'])
        if price:
            price = price.replace(' ', '').replace('₽', '').replace('₴', '')
            price_value = float(price)
            hostname = urlparse(row['url']).netloc

            if hostname not in site_prices:
                site_prices[hostname] = {'total_price': 0, 'count': 0}

            site_prices[hostname]['total_price'] += price_value
            site_prices[hostname]['count'] += 1

    avg_prices = {site: round(data['total_price'] / data['count'], 2) for site, data in site_prices.items()
                  if data['count'] > 0}

    conn.close()
    return avg_prices
