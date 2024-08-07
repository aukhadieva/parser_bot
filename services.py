import requests
from lxml import html


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
