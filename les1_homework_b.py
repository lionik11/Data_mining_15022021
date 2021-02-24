import time
import json
from pathlib import Path
import requests


class Parse5ka:
    categories_list = []
    category = {}
    params = {'store': None,
              'records_per_page': 12,
              'page': 1,
              'categories': None,
              'ordering': None,
              'price_promo__gte': None,
              'price_promo__lte': None,
              'search': None
              }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.41 YaBrowser/21.2.0.1097 Yowser/2.5 Safari/537.36'}

    def __init__(self, start_url: str, save_path: Path, categories_url: str):
        self.start_url = start_url
        self.save_path = save_path
        self.categories_url = categories_url

    def _get_categories_response(self):
        while True:
            response = requests.get(self.categories_url)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def _get_category(self):
        response = self._get_categories_response()
        data: list = response.json()
        for category in data:
            yield category

    def _set_params(self):
        for category in self._get_category():
            if category not in self.categories_list:
                self.params['categories'] = category['parent_group_code']
                self.categories_list.append(category)
                self.category = category
                return self.params

    def run(self):
        for product in self._parse(self.start_url):
            category = self.category
            product_path = self.save_path.joinpath(f"{category['parent_group_name']}.json")
            self._save(product, product_path)

    def _get_response(self, url):
        params = self._set_params()
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            return response
        time.sleep(0.5)

    def _parse(self, url: str):
        for i in self._get_category():
            while url:
                response = self._get_response(url)
                data: dict = response.json()
                url = data['next']
                yield data["results"]

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    url = 'https://5ka.ru/api/v2/special_offers/'
    url_cat = 'https://5ka.ru/api/v2/categories/'
    save_path = Path(__file__).parent.joinpath('categories_products')
    if not save_path.exists():
        save_path.mkdir()

    parser = Parse5ka(url, save_path, url_cat)
    parser.run()
