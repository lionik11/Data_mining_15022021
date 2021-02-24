"""
HTTP
Header
Body

Методы запроса:
GET - получить данные
POST - опубликовать, для публикации чего-либо
PUT - для редактирования существующих материалов: редактирует полностью
PATCH - редактирует часть данныъ
DELETE - удалить данные


STATUS CODES - числовое разделение событий - унификация, меньше места:
1xx - INFO-коды
2xx - OK-коды
3xx - REDIRECT - документ сменил адрес
4xx - CLIENT ERROR - клиентом для сервером является программма, которая дает доступ (браузер); клиент совершил ошибку
5xx - SERVER ERROR - разработчики криворучки
"""

import time
import json
from pathlib import Path
import requests

# params = {'store': None,
#           'records_per_page': 12,
#           'page': 1,
#           'categories': None,
#           'ordering': None,
#           'price_promo__gte': None,
#           'price_promo__lte': None,
#           'search': None
#           }
# url = 'https://5ka.ru/api/v2/special_offers/'
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.41 YaBrowser/21.2.0.1097 Yowser/2.5 Safari/537.36'}

# # response = requests.get(url)
# response = requests.get(url, params=params, headers=headers)
#
# # result_html_file = Path(__file__).parent.joinpath('5ka.html')
# result_json_file = Path(__file__).parent.joinpath('5ka.json')
#
# # result_html_file.write_text(response.text, encoding='UTF-8') # то же самое, что строкой ниже
# # with open(result_html_file, encoding='UTF-8') as file:
# #     file.write(response.text)
# result_json_file.write_text(response.text, encoding='UTF-8')

print(1)


class Parse5ka:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.41 YaBrowser/21.2.0.1097 Yowser/2.5 Safari/537.36'}

    def __init__(self, start_url: str, save_path: Path):
        self.start_url = start_url
        self.save_path = save_path

    def _get_response(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for product in self._parse(self.start_url):
            product_path = self.save_path.joinpath(f"{product['id']}.json")
            self._save(product, product_path)

    def _parse(self, url: str):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data['next']
            for product in data["results"]:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    url = 'https://5ka.ru/api/v2/special_offers/'
    save_path = Path(__file__).parent.joinpath('products')
    if not save_path.exists():
        save_path.mkdir()

    parser = Parse5ka(url, save_path)
    parser.run()
